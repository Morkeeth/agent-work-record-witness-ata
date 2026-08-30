"""Lay each narration paragraph onto the picture beat it describes.

Cue times are read off the picture itself (ffmpeg scene detection plus the tape's own
sleeps), not guessed. Building the two halves to the same TOTAL length is not sync:
the first cut matched on length and ran 9-15s ahead of the picture all through the
middle, narrating the corpus finding over a log viewer.
"""
import pathlib, subprocess, json

PARTS = pathlib.Path("demo/.vo-parts")
OUT = pathlib.Path("demo/voiceover.mp3")
SR = 24000

# paragraph index -> second at which it should START, taken from the beat map
CUES = {
    0: 1.0,    # title line, empty prompt
    1: 4.0,    # the problem
    2: 16.5,   # BLOCK on screen (output ~15.3)
    3: 26.8,   # still BLOCK
    4: 38.5,   # the honest report; PASS lands ~41
    5: 46.5,   # HOLD lands ~51
    6: 59.5,   # gcloud table ~62, /health ~68
    7: 74.5,   # eligibility typed ~75, 3 OF 3 lands ~85
    8: 92.0,   # Cloud Run console, service details (91.1)
    9: 114.5,  # console logs (117.3)
    10: 127.7, # the finding tab (127.2) — the corpus number
    11: 148.3, # the held record, resolving to its session (147.8)
    12: 162.5, # Google stack -> queue -> audit (164 / 171 / 176)
    13: 180.5, # Install (180.1)
    14: 195.5, # Policy (195.5)
    15: 205.5, # PR #1, verify-claims red (205.0)
    16: 213.2, # roadmap
    17: 228.2, # close
}


def dur(p):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


def main():
    parts = sorted(PARTS.glob("p*.mp3"))
    assert len(parts) == len(CUES), f"{len(parts)} parts vs {len(CUES)} cues"
    inputs, filters, labels = [], [], []
    for i, p in enumerate(parts):
        inputs += ["-i", str(p)]
        delay = int(CUES[i] * 1000)
        filters.append(f"[{i}:a]aresample={SR},adelay={delay}|{delay}[a{i}]")
        labels.append(f"[a{i}]")
    filters.append("".join(labels) + f"amix=inputs={len(parts)}:normalize=0,"
                   f"alimiter=level_in=1:level_out=0.95[out]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs,
                    "-filter_complex", ";".join(filters), "-map", "[out]",
                    "-c:a", "libmp3lame", "-b:a", "192k", str(OUT)], check=True)

    over = [(i, CUES[i] + dur(p)) for i, p in enumerate(parts)
            if i + 1 in CUES and CUES[i] + dur(p) > CUES[i + 1] + 0.15]
    for i, end in over:
        print(f"  WARN p{i:02d} ends {end:.1f} but p{i+1:02d} starts {CUES[i+1]:.1f}")
    print(f"WROTE {OUT}  {dur(OUT):.1f}s")


if __name__ == "__main__":
    main()
