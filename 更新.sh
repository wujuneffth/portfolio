#!/bin/sh
# 加完作品之后跑这一个命令，网站 + 单文件 + PDF 一起更新。
#
#   sh 更新.sh              只重新生成，不推送
#   sh 更新.sh push         生成完顺便推到线上
#
# 加作品的步骤（跑这个脚本之前先做）：
#   1. 图片放进 assets/proj/，命名 p17-01.webp、p17-02.webp …
#      编号往后顺延，别和已有的重复
#   2. 打开 works-data.js，照着里面任意一段复制一条，填好
#      title / year / cat / images
#   3. 把 __ZZ_SEED_VER 的数字 +1
#      不改这个，老访客浏览器里的缓存会盖掉新内容

set -e
cd "$(dirname "$0")"

echo "── 1/3 生成卡片缩略图 ──"
python3 生成缩略图.py | tail -3

echo
echo "── 2/3 打包单文件 ──"
python3 打包单文件.py --px 1200 -q 76 --out "张政作品集-单文件.html" | tail -2
python3 打包单文件.py --px 900  -q 70 --out "张政作品集-单文件-轻量.html" | tail -2

echo
echo "── 3/3 生成 PDF ──"
python3 生成PDF.py | tail -2

if [ "$1" = "push" ]; then
  echo
  echo "── 推送到线上 ──"
  git add -A
  git commit -q -m "更新作品：$(date '+%Y-%m-%d %H:%M')" || echo "  没有改动可提交"
  git push origin main
  echo "  已推送，GitHub Pages 一两分钟后生效"
else
  echo
  echo "（没推送。要更新线上网站，跑：sh 更新.sh push）"
fi

echo
echo "✅ 全部完成"
ls -lh 张政作品集-单文件*.html 张政-作品集*.pdf 2>/dev/null \
  | awk '{printf "   %-32s %s\n", $9, $5}'
