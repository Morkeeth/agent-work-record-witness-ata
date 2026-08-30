#!/usr/bin/env python3
"""Subtitles for the SHIPPED cut, built from the same two sources the film is.

Not transcribed by ear and not guessed: the text is demo/voiceover.txt (the script
Kokoro actually spoke) and the timing is film/lay_voice.py's CUES table plus the
measured duration of each rendered demo/.vo-parts/pNN.mp3. A paragraph is split into
sentences and each sentence gets a slice of its paragraph proportional to its length,
so a cue never runs past the paragraph that produced it.

    python3 film/make_srt.py            # -> demo/demo-final.srt

Checked 2026-08-31 against a local whisper.cpp transcript of demo/demo-final.mp4:
every sentence below is spoken, in this order.
"""
import pathlib, re, subprocess, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lay_voice import CUES                      # one cue table, never a second copy

PARTS = pathlib.Path("demo/.vo-parts")
OUT = pathlib.Path("demo/demo-final.srt")


def dur(p):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
         str(p)], capture_output=True, text=True).stdout.strip())


def stamp(t):
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}".replace(".", ",")


def main():
    parts = sorted(PARTS.glob("p*.mp3"))
    if len(parts) != len(CUES):
        sys.exit(f"{len(parts)} audio parts vs {len(CUES)} cues — rebuild the parts first")
    cues, n = [], 0
    for i, mp3 in enumerate(parts):
        body = (PARTS / f"p{i:02d}.txt").read_text()
        body = " ".join(l for l in body.splitlines() if l and not l.startswith("@")).strip()
        sents = [s.strip() for s in re.split(r"(?<=[.?!])\s+", body) if s.strip()]
        start, total = CUES[i], dur(mp3)
        chars = sum(len(s) for s in sents) or 1
        t = start
        for s in sents:
            span = total * len(s) / chars
            n += 1
            cues.append(f"{n}\n{stamp(t)} --> {stamp(t + span - 0.05)}\n{s}\n")
            t += span
    OUT.write_text("\n".join(cues))
    print(f"WROTE {OUT}  {n} cues, last ends {stamp(t)}")


if __name__ == "__main__":
    main()
