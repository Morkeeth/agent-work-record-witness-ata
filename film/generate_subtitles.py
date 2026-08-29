#!/usr/bin/env python3
"""Generate film/subtitles.srt from film/voiceover.txt — one cue per beat."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

FILM = Path(__file__).resolve().parent
VO = FILM / "voiceover.txt"
SRT = FILM / "subtitles.srt"
FIXED = FILM / "fixed.json"


def srt_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def load_beat_seconds() -> list[int]:
    data = json.loads(FIXED.read_text(encoding="utf-8"))
    return list(data["spine"]["beat_seconds"])


def generate() -> str:
    lines = [ln.strip() for ln in VO.read_text(encoding="utf-8").splitlines() if ln.strip()]
    beats = load_beat_seconds()
    if len(lines) != len(beats):
        raise SystemExit(f"voiceover has {len(lines)} lines, fixed.json has {len(beats)} beats")
    cues = []
    t = 0.0
    for i, (text, dur) in enumerate(zip(lines, beats), start=1):
        start = t
        end = t + dur
        cues.append(f"{i}\n{srt_time(start)} --> {srt_time(end)}\n{text}\n")
        t = end
    return "\n".join(cues) + "\n"


def check() -> bool:
    if not SRT.exists():
        print("subtitles.srt missing", file=sys.stderr)
        return False
    lines = [ln.strip() for ln in VO.read_text(encoding="utf-8").splitlines() if ln.strip()]
    srt_text = SRT.read_text(encoding="utf-8")
    # Extract subtitle text blocks (every third+ line in each cue)
    blocks = re.findall(r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n(.+?)(?:\n\n|\Z)", srt_text, re.DOTALL)
    blocks = [b.replace("\n", " ").strip() for b in blocks]
    if blocks != lines:
        print("voiceover.txt and subtitles.srt disagree line-for-line", file=sys.stderr)
        for i, (a, b) in enumerate(zip(lines, blocks), 1):
            if a != b:
                print(f"  line {i} vo: {a[:60]}…", file=sys.stderr)
                print(f"  line {i} srt: {b[:60]}…", file=sys.stderr)
        if len(blocks) != len(lines):
            print(f"  counts: vo={len(lines)} srt={len(blocks)}", file=sys.stderr)
        return False
    return True


def main() -> int:
    if "--check" in sys.argv:
        return 0 if check() else 1
    srt = generate()
    SRT.write_text(srt, encoding="utf-8")
    print(f"wrote {SRT}")
    return 0 if check() else 1


if __name__ == "__main__":
    raise SystemExit(main())
