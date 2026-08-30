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
    0: 0.8,    # slide 1 · title
    1: 5.0,    # slide 2 · the problem
    2: 16.0,   # slide 3 · the gap, deadbee in blue
    3: 25.8,   # terminal opens (25.0); BLOCK output ~29
    4: 36.0,   # the honest report, PASS
    5: 43.5,   # the claim it refuses to guess at, HOLD
    6: 55.0,   # gcloud table, then /health
    7: 68.5,   # eligibility typed; 3 OF 3 lands ~78
    8: 88.5,   # Cloud Run console, service details (87.3)
    9: 106.5,  # console logs
    10: 114.0, # the finding tab (113.3) — the corpus number
    11: 131.0, # the held record, resolving to its session (130.0)
    12: 142.8, # Google stack -> queue -> audit (142.8 / 151 / 155)
    13: 160.0, # Install (159.4)
    14: 172.5, # Policy (172.4)
    15: 181.0, # PR #1, verify-claims red (180.2)
    16: 188.5, # roadmap, carrying into the closing slide (197.6)
    17: 201.5, # close
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
