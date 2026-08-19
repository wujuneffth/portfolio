#!/usr/bin/env python3
"""
把作品集导成 16:9 横版 PDF（文字为矢量，可选中可搜索）。

    python3 生成PDF.py                # 全部 157 张 + 节日海报章
    python3 生成PDF.py --max 6        # 每个作品最多 6 张（精选版）
    python3 生成PDF.py --quality 72   # 调压缩，默认 80
    python3 生成PDF.py --px 1300      # 限制嵌入图片宽度，控体积

输出 张政-作品集.pdf。
超长图（比如 1600x9442 的长图）会被切成多片，两片一页并排放，
不会因为塞进横版页面而缩到看不清。
"""
import io
import json
import math
import os
import subprocess
import sys

import fitz
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
PX = 10 ** 7          # 嵌入图片的宽度上限，--px 可调
SLICE = True          # 长图是否切片。精选版关掉，整张一页，省体积

# ── 版面 ──────────────────────────────────────────────
W, H = 960.0, 540.0                     # 16:9，等同 13.33x7.5 英寸
M = 46.0                                # 页边距
CONTENT_W, CONTENT_H = W - 2 * M, H - 2 * M - 26   # 底部留出图注

# ── 配色（取自网站 :root）──────────────────────────────
PAPER = (0.980, 0.980, 0.969)           # #FAFAF7
INK = (0.102, 0.102, 0.094)             # #1A1A18
NIGHT = (0.106, 0.110, 0.200)           # #1B1C33
DEEP = (0.141, 0.204, 0.361)            # #24345C
HAZE = (0.561, 0.639, 0.769)            # #8FA3C4
SUN = (0.910, 0.847, 0.682)             # #E8D8AE
STAGE = (0.078, 0.078, 0.086)           # 图片页背景

FONT_SRC = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT = FONT_SRC          # 运行时会替换成子集字体


def subset_font(chars):
    """整套 Hiragino Sans GB 有 29352 个字形，嵌进 PDF 就是 9.6MB。
       这里只保留实际用到的字，通常几百个，体积降到 100KB 以内。"""
    import tempfile
    from fontTools import subset as fts
    from fontTools.ttLib import TTFont
    try:
        f = TTFont(FONT_SRC, fontNumber=0)
        opt = fts.Options()
        opt.drop_tables += ["DSIG"]
        opt.notdef_outline = True
        opt.recalc_bounds = True
        # 关键：保留原始字形编号。默认会重排 GID，PyMuPDF 按原编号
        # 引用字形，重排后整页会变成乱码。
        opt.retain_gids = True
        sub = fts.Subsetter(options=opt)
        sub.populate(text="".join(sorted(chars)))
        sub.subset(f)
        out = os.path.join(tempfile.gettempdir(), "zz-subset.ttf")
        f.save(out)
        return out
    except Exception as e:
        print("  字体子集化失败，用完整字体：", e)
        return FONT_SRC
CAT = {"poster": "海报", "book": "书籍装帧", "event": "活动视觉",
       "collateral": "项目物料", "ui": "网页UI"}

ME = {"name": "张政", "en": "Changzheng", "role": "视觉设计师",
      "mail": "wjdtnrdid319@gmail.com", "city": "现居苏州"}


def works():
    """从 works-data.js 读作品，保持和网站一致的顺序。"""
    r = subprocess.run(
        ["node", "-e",
         "global.window={};require('./works-data.js');"
         "console.log(JSON.stringify(window.__ZZ_PUBLISHED_SEED))"],
        capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
    if r.returncode:
        sys.exit("读 works-data.js 失败：" + r.stderr)
    return json.loads(r.stdout)


def festival():
    """节日海报硬编码在 index.html 里，把标题和文件对应起来。"""
    import re
    html = open("index.html", encoding="utf-8").read()
    out = []
    for m in re.finditer(r"title:\s*'([^']+)'[^}]*?year:\s*'(\d+)'[^}]*?"
                         r"img:\s*'(assets/works/[a-z0-9-]+\.webp)'", html):
        out.append({"title": m.group(1), "year": m.group(2), "img": m.group(3)})
    return out


def jpeg(im, quality):
    if im.mode != "RGB":
        im = im.convert("RGB")
    b = io.BytesIO()
    im.save(b, "JPEG", quality=quality, optimize=True, progressive=True)
    return b.getvalue()


def fit(iw, ih, bw, bh):
    """等比缩放到框内，返回居中矩形。"""
    s = min(bw / iw, bh / ih)
    w, h = iw * s, ih * s
    return w, h


_F_cache = {}


def wide(s, size):
    if FONT not in _F_cache:
        _F_cache[FONT] = fitz.Font(fontfile=FONT)
    return _F_cache[FONT].text_length(s, size)


def shrink(s, size, limit, floor=15):
    """标题过宽就自动降字号，降到底线为止。"""
    while size > floor and wide(s, size) > limit:
        size -= 1
    return size


def mid_trim(s, size, limit):
    """从中间截断，保住头尾——尾部往往才是区分度所在
       （比如「…日本站（第二站）」和「…日本站（第四站）」）。"""
    if wide(s, size) <= limit:
        return s
    lo, hi = 1, len(s) // 2
    best = s
    while lo <= hi:
        k = (lo + hi) // 2
        cand = s[:k] + "…" + s[-(k + 2):]
        if wide(cand, size) <= limit:
            best, lo = cand, k + 1
        else:
            hi = k - 1
    return best


def text(page, xy, s, size, color, font="F", align=0):
    page.insert_text(xy, s, fontname=font, fontsize=size, color=color)


def bg(page, color):
    page.draw_rect(fitz.Rect(0, 0, W, H), color=None, fill=color)


class Book:
    def __init__(self, quality):
        self.doc = fitz.open()
        self.q = quality
        self.marks = []          # (标题, 页码)

    def page(self, fill):
        p = self.doc.new_page(width=W, height=H)
        p.insert_font(fontname="F", fontfile=FONT)
        bg(p, fill)
        return p

    # ── 封面 ──────────────────────────────────────────
    def cover(self):
        p = self.page(NIGHT)
        # 上深下浅的竖向渐变，用横条模拟
        for i in range(120):
            t = i / 119.0
            c = tuple(NIGHT[k] + (DEEP[k] - NIGHT[k]) * t for k in range(3))
            p.draw_rect(fitz.Rect(0, H * t, W, H * (t + 1 / 119.0) + 1),
                        color=None, fill=c)
        text(p, (M, 190), ME["name"], 84, PAPER)
        text(p, (M, 232), ME["en"] + " · " + ME["role"], 19, HAZE)
        p.draw_line(fitz.Point(M, 262), fitz.Point(M + 130, 262),
                    color=SUN, width=1.6)
        text(p, (M, 300), "作品集", 30, SUN)
        text(p, (M, 328), "PORTFOLIO", 12, HAZE)
        text(p, (M, H - 78), ME["mail"], 12.5, PAPER)
        text(p, (M, H - 60), ME["city"] + " · 三年工作经验", 12.5, HAZE)
        text(p, (W - M - 74, H - 60), "2026", 12.5, HAZE)

    # ── 作品章节页 ────────────────────────────────────
    def chapter(self, idx, title, year, cat, n):
        p = self.page(NIGHT)
        text(p, (M, 150), "%02d" % idx, 56, DEEP)
        text(p, (M, 232), title, shrink(title, 30, CONTENT_W), PAPER)
        p.draw_line(fitz.Point(M, 262), fitz.Point(M + 90, 262),
                    color=SUN, width=1.4)
        text(p, (M, 296), "%s · %s · %d 张" % (CAT.get(cat, "作品"), year, n),
             13, HAZE)
        self.marks.append((title, self.doc.page_count))

    # ── 单图页 ────────────────────────────────────────
    def shot(self, path, caption):
        im = Image.open(path)
        iw, ih = im.size
        w, h = fit(iw, ih, CONTENT_W, CONTENT_H)
        # 只缩不放：按 2 倍屏密度重采样，但不超过原图
        tw = min(iw, int(w * 2), PX)
        if tw < iw:
            im = im.copy()
            im.thumbnail((tw, 10 ** 7), Image.LANCZOS)
        p = self.page(STAGE)
        x, y = (W - w) / 2, M + (CONTENT_H - h) / 2
        p.insert_image(fitz.Rect(x, y, x + w, y + h), stream=jpeg(im, self.q))
        text(p, (M, H - 24), caption, 8.5, (0.55, 0.55, 0.58))

    # ── 长图切片，两片一页 ────────────────────────────
    def longshot(self, path, caption):
        if not SLICE:
            # 精选版：整张放一页，看得出是长图、体积可控，
            # 细节留给完整版。
            self.shot(path, caption + "（长图）")
            return
        im = Image.open(path)
        iw, ih = im.size
        n = max(2, math.ceil(ih / (iw * 1.30)))
        step = ih / n
        ov = int(step * 0.015)                  # 切口留一点重叠
        slices = []
        for i in range(n):
            top = max(0, int(i * step) - (ov if i else 0))
            bot = min(ih, int((i + 1) * step) + (ov if i < n - 1 else 0))
            slices.append(im.crop((0, top, iw, bot)))
        per = 2
        gap = 26.0
        for i in range(0, len(slices), per):
            grp = slices[i:i + per]
            p = self.page(STAGE)
            cw = (CONTENT_W - gap * (per - 1)) / per
            boxes = []
            for s in grp:
                boxes.append(fit(s.width, s.height, cw, CONTENT_H))
            th = max(b[1] for b in boxes)
            total = sum(b[0] for b in boxes) + gap * (len(grp) - 1)
            x = (W - total) / 2
            for s, (bw_, bh_) in zip(grp, boxes):
                y = M + (CONTENT_H - bh_) / 2
                s2 = s
                tw = min(s.width, int(bw_ * 2), PX)
                if tw < s.width:
                    s2 = s.copy()
                    s2.thumbnail((tw, 10 ** 7), Image.LANCZOS)
                p.insert_image(fitz.Rect(x, y, x + bw_, y + bh_),
                               stream=jpeg(s2, self.q))
                x += bw_ + gap
            k = i // per + 1
            tot = math.ceil(len(slices) / per)
            text(p, (M, H - 24),
                 "%s（长图 %d / %d）" % (caption, k, tot), 8.5, (0.55, 0.55, 0.58))

    # ── 节日海报网格 ──────────────────────────────────
    def poster_grid(self, items):
        p0 = self.page(NIGHT)
        text(p0, (M, 232), "节日海报系列", 30, PAPER)
        p0.draw_line(fitz.Point(M, 262), fitz.Point(M + 90, 262),
                     color=SUN, width=1.4)
        text(p0, (M, 296), "2023 — 2026 · 共 %d 张" % len(items), 13, HAZE)
        self.marks.append(("节日海报系列", self.doc.page_count))

        per, gap = 4, 22.0
        cw = (CONTENT_W - gap * (per - 1)) / per
        ch = CONTENT_H - 20
        for i in range(0, len(items), per):
            grp = items[i:i + per]
            p = self.page(STAGE)
            boxes = [fit(*Image.open(g["img"]).size, cw, ch) for g in grp]
            total = sum(b[0] for b in boxes) + gap * (len(grp) - 1)
            x = (W - total) / 2
            for g, (bw_, bh_) in zip(grp, boxes):
                im = Image.open(g["img"])
                tw = min(im.width, int(bw_ * 2), PX)
                if tw < im.width:
                    im = im.copy()
                    im.thumbnail((tw, 10 ** 7), Image.LANCZOS)
                y = M + (ch - bh_) / 2
                p.insert_image(fitz.Rect(x, y, x + bw_, y + bh_),
                               stream=jpeg(im, self.q))
                text(p, (x, y + bh_ + 14), g["title"], 7.5, (0.62, 0.62, 0.65))
                text(p, (x, y + bh_ + 25), g["year"], 7.0, (0.45, 0.45, 0.48))
                x += bw_ + gap

    # ── 封底 ──────────────────────────────────────────
    def back(self):
        p = self.page(NIGHT)
        text(p, (M, 218), "谢谢观看", 34, PAPER)
        p.draw_line(fitz.Point(M, 248), fitz.Point(M + 90, 248),
                    color=SUN, width=1.4)
        text(p, (M, 292), ME["mail"], 14, HAZE)
        text(p, (M, 318), "在线作品集  wujuneffth.github.io/portfolio", 12, HAZE)

    # ── 目录（最后生成，插到封面后面）─────────────────
    def toc(self):
        p = self.doc.new_page(1, width=W, height=H)
        p.insert_font(fontname="F", fontfile=FONT)
        bg(p, PAPER)
        text(p, (M, 96), "目录", 26, INK)
        p.draw_line(fitz.Point(M, 116), fitz.Point(M + 60, 116),
                    color=DEEP, width=1.4)
        col_h = 22.0
        rows = self.marks
        half = math.ceil(len(rows) / 2)
        for c in range(2):
            cx = M + c * (CONTENT_W / 2 + 16)
            for r, (t, pg) in enumerate(rows[c * half:(c + 1) * half]):
                y = 158 + r * col_h
                num_x = cx + CONTENT_W / 2 - 58
                text(p, (cx, y), mid_trim(t, 10, num_x - cx - 14), 10, INK)
                text(p, (num_x, y), str(pg + 2), 10, DEEP)
        # 目录插在第 2 页，后面所有书签页码 +1
        self.doc.set_toc([[1, t, pg + 2] for t, pg in self.marks])

    def save(self, path):
        # 每页都 insert_font 会把整套中文字体（29352 字形）重复嵌进去，
        # 子集化后只保留实际用到的那几百个字，体积能降八成。
        try:
            self.doc.subset_fonts(verbose=False)
        except Exception as e:
            print("  字体子集化跳过：", e)
        self.doc.set_metadata({
            "title": "张政 · 视觉设计师作品集",
            "author": ME["name"],
            "subject": "作品集",
            "keywords": "视觉设计,活动全案,书籍装帧,网页UI",
        })
        self.doc.save(path, garbage=4, deflate=True, clean=True)


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    a = sys.argv
    cap = int(a[a.index("--max") + 1]) if "--max" in a else 0
    q = int(a[a.index("--quality") + 1]) if "--quality" in a else 80
    global PX, SLICE
    if "--px" in a:
        PX = int(a[a.index("--px") + 1])
    SLICE = not cap
    out = "张政-作品集%s.pdf" % ("-精选" if cap else "")

    ws, fs = works(), festival()

    # 收集 PDF 里会出现的每一个字符
    chars = set("0123456789/·—…（）&%,.:-—— ")
    chars |= set("".join(ME.values()) + "".join(CAT.values()))
    chars |= set("作品集目录节日海报系列谢谢观看在线张长图共页年经验现居三工")
    chars |= set("PORTFOLIO")
    chars |= set("wujuneffth.github.io/portfolio")
    for w in ws:
        chars |= set(w["title"]) | set(w["year"])
    for g in fs:
        chars |= set(g["title"]) | set(g["year"])

    global FONT
    FONT = subset_font(chars)

    b = Book(q)
    b.cover()

    done = 0
    total = sum(min(len(w["images"]), cap) if cap else len(w["images"]) for w in ws)
    for i, w in enumerate(ws, 1):
        imgs = w["images"][:cap] if cap else w["images"]
        b.chapter(i, w["title"], w["year"], w["cat"], len(imgs))
        for j, src in enumerate(imgs, 1):
            if not os.path.exists(src):
                print("  跳过（缺文件）", src); continue
            iw, ih = Image.open(src).size
            cap_txt = "%s · %02d/%02d" % (w["title"], j, len(imgs))
            if ih > iw * 2:
                b.longshot(src, cap_txt)
            else:
                b.shot(src, cap_txt)
            done += 1
            if done % 10 == 0 or done == total:
                print("  %d / %d" % (done, total), flush=True)

    if fs:
        b.poster_grid(fs)
    b.back()
    b.toc()
    b.save(out)
    mb = os.path.getsize(out) / 1048576
    print("\n✅ %s" % out)
    print("   %d 页 · %.1f MB · 16:9 横版 · 文字可选中" % (b.doc.page_count, mb))


if __name__ == "__main__":
    main()
