#!/usr/bin/env python3
"""
给作品卡片生成 4:3 缩略图，放到 assets/thumb/。

卡片在页面上只显示 341x256（4:3），2 倍屏需要 682x512，
但原来卡片直接下载原图（有的是 1600x9290 的长图、600 多 KB），
浪费极大。这个脚本按卡片实际的取景位置把封面裁成 700x525。

灯箱里的大图仍然用原图，不受影响。

加了新作品之后重跑一次即可：
    python3 生成缩略图.py
"""
from PIL import Image
import os, io, json, re, subprocess, sys

Image.MAX_IMAGE_PIXELS = None
TW, TH = 700, 525
OUT = 'assets/thumb'

def covers():
    """收集所有会出现在卡片上的封面图，以及各自的取景位置"""
    r = subprocess.run(['node', '-e',
        "global.window={};require('./works-data.js');"
        "console.log(JSON.stringify(window.__ZZ_PUBLISHED_SEED.map(w=>w.cover)))"],
        capture_output=True, text=True)
    if r.returncode:
        sys.exit("读 works-data.js 失败：" + r.stderr)
    # 作品卡 object-position 是 50% 0%（从顶部取景）
    out = [(c, 0.0) for c in json.loads(r.stdout)]
    # 节日海报硬编码在 html 里，默认 object-position 50% 30%
    html = open('portfolio.dc.html', encoding='utf-8').read()
    out += [(c, 0.30) for c in sorted(set(re.findall(r"assets/works/[a-z0-9-]+\.webp", html)))]
    return out

def make(src, focus_y):
    im = Image.open(src)
    if im.mode not in ('RGB', 'RGBA'):
        im = im.convert('RGB')
    w, h = im.size
    want = TW / TH
    if w / h > want:                       # 太宽 → 左右居中裁
        nw = int(h * want)
        im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:                                  # 太高 → 按取景位置上下裁
        nh = int(w / want)
        y = int((h - nh) * focus_y)
        im = im.crop((0, y, w, y + nh))
    return im.resize((TW, TH), Image.LANCZOS)

def main():
    os.makedirs(OUT, exist_ok=True)
    b_tot = a_tot = 0
    n = skip = 0
    for src, focus in covers():
        if not os.path.exists(src):
            print("  跳过（文件不存在）", src); skip += 1; continue
        dst = os.path.join(OUT, os.path.basename(src))
        b = os.path.getsize(src)
        buf = io.BytesIO()
        make(src, focus).save(buf, 'WEBP', quality=80, method=6)
        open(dst, 'wb').write(buf.getvalue())
        a = len(buf.getvalue())
        b_tot += b; a_tot += a; n += 1
        print("  %-28s %6.0fKB -> %5.0fKB" % (os.path.basename(src), b/1024, a/1024))
    print("\n生成 %d 张%s" % (n, ("，跳过 %d 张" % skip) if skip else ""))
    print("卡片下载量  %.2f MB -> %.2f MB   （省 %.0f%%）"
          % (b_tot/1048576, a_tot/1048576, 100*(1-a_tot/b_tot) if b_tot else 0))

if __name__ == '__main__':
    main()
