#!/usr/bin/env bash
# Render the four slides to PNG, then to the intro and outro segments.
# Palette rule (Oscar, 2026-08-30): cool white on true black, ONE cold blue per slide,
# used only on the thing that is gone — the commit that does not exist, the install
# count that is zero. If it is blue, it is missing.
set -euo pipefail
cd "$(dirname "$0")"
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
for i in 1 2 3 4; do
  "$CH" --headless=new --disable-gpu --hide-scrollbars --window-size=1920,1080 \
    --virtual-time-budget=4000 --screenshot="$PWD/s$i.png" \
    "data:text/html;charset=utf-8,$(python3 -c "
import urllib.parse,pathlib,re,sys
h=pathlib.Path('slides.html').read_text()
for j in ['1','2','3','4']:
    if j!='$i': h=re.sub(r'<section class=\"s\" id=\"s%s\">.*?</section>'%j,'',h,flags=re.S)
print(urllib.parse.quote(h,safe=''))")" >/dev/null 2>&1
done
ffmpeg -y -loglevel error -f concat -safe 0 -i intro.txt -t 25 \
  -vf "fps=30,scale=1920:1080,format=yuv420p" -c:v libx264 -preset medium -crf 21 ../../demo/seg-intro.mp4
ffmpeg -y -loglevel error -loop 1 -t 10 -i s4.png \
  -vf "fps=30,scale=1920:1080,format=yuv420p" -c:v libx264 -preset medium -crf 21 ../../demo/seg-outro.mp4
echo "slides -> demo/seg-intro.mp4 (25s) + demo/seg-outro.mp4 (10s)"
