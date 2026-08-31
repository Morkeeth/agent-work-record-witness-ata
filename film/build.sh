#!/usr/bin/env bash
# Rebuild demo/demo-final.mp4 end to end.
#
#   ./film/build.sh              # picture + Kokoro voiceover
#   ./film/build.sh --silent     # picture only, for recording your own voice over it
#
# Nothing here is a mock-up. The terminal segment executes the real commands in a
# real shell; the browser segment drives the live Cloud Run service in a real
# Chromium. Both are continuous captures. The only cut is between the two.
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="$HOME/google-cloud-sdk/bin:$PATH"

SILENT=0
[ "${1:-}" = "--silent" ] && SILENT=1

echo "1/4 · slides + terminal segment"
( cd film/slides && for i in 1 2 3 4; do :; done )   # slides render via film/slides/render.sh
./film/slides/render.sh
vhs film/terminal.tape

echo "2/4 · console + browser segments (playwright) — the live service"
python3 film/console.py --record   # needs ~/.ata-film-profile: python3 film/console.py --login
python3 film/browser.py

# PROVENANCE, measured 2026-08-31 — this script does NOT reproduce demo/demo-final.mp4.
# The shipped 207.63s cut is five segments, not three:
#   seg-intro.mp4 25.00s + seg-terminal.mp4 62.32s + seg-console-trim.mp4 26.07s
#   + seg-browser.mp4 84.17s + seg-outro.mp4 10.00s  = 207.56s
# (25 + 62.32 = 87.32s, and lay_voice.py's cue 8 puts the Cloud Run console at 87.3s.)
# The join below drops the slides and uses the untrimmed console segment. Re-run it and you
# get a different, shorter film. Fix the join before trusting this script again.

echo "3/4 · joining"
ffmpeg -y -loglevel error -i demo/seg-terminal.mp4 \
  -vf "fps=30,scale=1920:1080:flags=lanczos,format=yuv420p" \
  -c:v libx264 -preset medium -crf 21 -an demo/.t30.mp4
ffmpeg -y -loglevel error -i demo/seg-console.mp4 \
  -vf "fps=30,scale=1920:1080:flags=lanczos,format=yuv420p" \
  -c:v libx264 -preset medium -crf 21 -an demo/.c30.mp4
ffmpeg -y -loglevel error -i demo/seg-browser.mp4 \
  -vf "fps=30,scale=1920:1080:flags=lanczos,format=yuv420p" \
  -c:v libx264 -preset medium -crf 21 -an demo/.b30.mp4
printf "file '.t30.mp4'\nfile '.c30.mp4'\nfile '.b30.mp4'\n" > demo/.seg30.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i demo/.seg30.txt -c copy demo/.picture.mp4

if [ "$SILENT" = "1" ]; then
  mv demo/.picture.mp4 demo/demo-silent.mp4
  rm -f demo/.t30.mp4 demo/.c30.mp4 demo/.b30.mp4 demo/.seg30.txt
  echo "4/4 · WROTE demo/demo-silent.mp4 ($(ffprobe -v error -show_entries format=duration -of csv=p=0 demo/demo-silent.mp4)s)"
  echo "     Record your voice against it, then mux:"
  echo "     ffmpeg -i demo/demo-silent.mp4 -i YOUR.m4a -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k demo/demo-final.mp4"
  exit 0
fi

echo "4/4 · voiceover (local Kokoro — no API, no key) + mux"
# One paragraph per beat, rendered separately, then laid onto the picture's own cue
# times. Rendering the script as one file and matching TOTAL length is not sync.
python3 film/split_voice.py
( cd ~/CODE/voice-generation && for f in ~/CODE/hack-fleet-ata/demo/.vo-parts/p*.txt; do \
    ./kvenv/bin/python vo.py "$f" -o "${f%.txt}.mp3" --preset demo --speed 1.42 >/dev/null; done )
python3 film/lay_voice.py
ffmpeg -y -loglevel error -i demo/.picture.mp4 -i demo/voiceover.mp3 \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k demo/demo-final.mp4
rm -f demo/.picture.mp4 demo/.t30.mp4 demo/.c30.mp4 demo/.b30.mp4 demo/.seg30.txt

echo
echo "WROTE demo/demo-final.mp4  $(ffprobe -v error -show_entries format=duration -of csv=p=0 demo/demo-final.mp4)s"
echo "Watch it end to end before you upload it. All of it."
