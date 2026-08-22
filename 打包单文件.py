#!/usr/bin/env python3
"""
把整个作品集打包成一个 .html 文件——双击就能开，完全不联网。

    python3 打包单文件.py                  # 原图质量，文件较大
    python3 打包单文件.py --px 1200 -q 76  # 压一档，文件小、打开快
    python3 打包单文件.py --out 轻量.html   # 指定输出文件名

产出 张政作品集-单文件.html。
所有图片、字体、JS 全部内联成 data URI，简历页用 srcdoc 塞进 iframe。
拷给别人 / 微信发送 / U盘拷贝都行，对方不需要装任何东西。
"""
import base64
import io
import mimetypes
import os
import re
import sys

from PIL import Image

Image.MAX_IMAGE_PIXELS = None

PX = 0        # 图片宽度上限，0 = 不缩
Q = 82        # 重压质量


def datauri(path, mime=None):
    """把文件读成 data URI。位图按 PX/Q 重新压一遍，其余原样内联。"""
    mime = mime or mimetypes.guess_type(path)[0] or "application/octet-stream"
    if PX and path.lower().endswith((".webp", ".jpg", ".jpeg", ".png")):
        im = Image.open(path)
        if im.width > PX:
            im = im.copy()
            im.thumbnail((PX, 10 ** 7), Image.LANCZOS)
        buf = io.BytesIO()
        if im.mode in ("RGBA", "LA", "P") and path.lower().endswith(".png"):
            im.convert("RGBA").save(buf, "WEBP", quality=Q, method=6)
        else:
            im.convert("RGB").save(buf, "WEBP", quality=Q, method=6)
        raw, mime = buf.getvalue(), "image/webp"
    else:
        raw = open(path, "rb").read()
    return "data:%s;base64,%s" % (mime, base64.b64encode(raw).decode())


# 内联后路径变成 data URI，works-data.js 里那句运行时字符串替换
# 就取不到缩略图了。让卡片直接复用原图那一份内联数据。
THUMB_FIX = ("w.thumb = w.cover.replace('assets/proj/', 'assets/thumb/');",
             "w.thumb = w.cover;  /* 单文件版：缩略图与原图共用一份内联数据 */")


def inline_imports(html, base="."):
    """<x-import from="./doc-page.js"> 是框架的运行时 fetch，不是 script 标签。
       file:// 下会被 CORS 拦掉，必须把地址换成 data: URL。"""
    def rep(m):
        pre, src, post = m.group(1), m.group(2), m.group(3)
        p = os.path.join(base, src.lstrip("./"))
        if not os.path.exists(p):
            return m.group(0)
        code = open(p, encoding="utf-8").read()
        code, _ = inline_assets(code, base)
        b64 = base64.b64encode(code.encode("utf-8")).decode()
        return '%sfrom="data:text/javascript;base64,%s"%s' % (pre, b64, post)
    return re.sub(r'(<x-import[^>]*?)from="(\.?/?[^"]+\.js)"([^>]*>)', rep, html)


def inline_scripts(html, base="."):
    """<script src="./x.js"> → 内容内联成 data: URL。"""
    def rep(m):
        src = m.group(1).lstrip("./")
        p = os.path.join(base, src)
        if not os.path.exists(p):
            return m.group(0)
        code = open(p, encoding="utf-8").read()
        code = code.replace(*THUMB_FIX)
        # 脚本里也有图片路径（works-data.js 就是一整张清单），
        # 必须先把资源换成 data URI，再整体 base64。
        code, _ = inline_assets(code, base)
        # 不能改成 <script>内容</script>：Design 的运行时靠脚本的
        # 外部性和兄弟关系定位模板，内联后会把 support.js 源码当成
        # 模板文本渲染出来。用 data: URL 保留「外部脚本」的语义。
        b64 = base64.b64encode(code.encode("utf-8")).decode()
        return '<script src="data:text/javascript;base64,%s"></script>' % b64
    return re.sub(r'<script[^>]*\bsrc="(\.?/?[^":]+\.js)"[^>]*></script>', rep, html)


def inline_assets(html, base="."):
    """把所有 assets/... 路径换成 data URI（同一个文件只编码一次）。"""
    cache = {}
    paths = sorted(set(re.findall(r'(?:\./)?((?:assets|vendor)/[A-Za-z0-9_./-]+'
                                  r'\.(?:webp|jpg|jpeg|png|svg|woff2|riv))', html)))
    for rel in paths:
        if rel.startswith("assets/thumb/"):
            continue                      # 单文件版用不到缩略图
        p = os.path.join(base, rel)
        if os.path.exists(p):
            cache[rel] = datauri(p)
    if cache:
        # 长路径先替换，避免前缀互相吃掉
        for rel in sorted(cache, key=len, reverse=True):
            html = html.replace("./" + rel, cache[rel]).replace(rel, cache[rel])
    return html, len(cache)


def build_resume():
    """把简历页做成自包含 HTML，用来塞进 iframe 的 srcdoc。"""
    h = open("resume.dc.html", encoding="utf-8").read()
    h = inline_imports(h)
    h = inline_scripts(h)
    h, n = inline_assets(h)
    print("  简历页内联了 %d 个资源" % n)
    return h


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    a = sys.argv
    global PX, Q
    if "--px" in a:
        PX = int(a[a.index("--px") + 1])
    for f in ("-q", "--quality"):
        if f in a:
            Q = int(a[a.index(f) + 1])

    print("读取 index.html …")
    h = open("index.html", encoding="utf-8").read()

    # Design 工具留下的构建元数据，运行时没用，但每个标签把路径写了两遍，
    # 内联时会让同一张图被编码三次（179 个标签 = 358 处重复）。
    n0 = h.count("ext-resource-dependency")
    h = re.sub(r'\s*<meta name="ext-resource-dependency"[^>]*>', "", h)
    print("  剔除 %d 个构建元数据标签" % n0)


    # 1) 简历 iframe → srcdoc（单文件里没法再去请求 resume.dc.html）
    print("打包简历页 …")
    r = build_resume()
    # 必须连 < > 一起转义。Design 框架把页面模板存在
    # <script type="text/x-dc"> 里，简历 HTML 里的 </script>
    # 会把那个块提前闭合，整页变成裸 JS 文本。
    esc = (r.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))
    # 用函数式替换：srcdoc 内容里含反斜杠，字符串模板会被当成正则转义
    h = re.sub(r'<iframe src="resume\.dc\.html\?embed=1"',
               lambda m: '<iframe srcdoc="%s"' % esc, h, count=1)

    # 2) 内联全部脚本
    print("内联脚本和运行时导入 …")
    h = inline_imports(h)
    h = inline_scripts(h)



    # 3) 内联全部图片和字体
    print("内联图片和字体（157 张作品图，慢一点）…")
    h, n = inline_assets(h)
    print("  主页面内联了 %d 个资源" % n)

    # 4) 提示：单文件下 IndexedDB 可能不可用，让它安静降级
    h = h.replace("</head>",
                  "<script>window.__ZZ_STANDALONE=1;</script>\n</head>", 1)

    out = a[a.index("--out") + 1] if "--out" in a else "张政作品集-单文件.html"
    open(out, "w", encoding="utf-8").write(h)
    mb = os.path.getsize(out) / 1048576
    left = h.count("assets/") + h.count("vendor/")
    print("\n✅ %s" % out)
    print("   %.1f MB · 双击即可打开 · 无需联网" % mb)
    if left:
        print("   ⚠️ 还有 %d 处没内联的路径，检查一下" % left)


if __name__ == "__main__":
    main()
