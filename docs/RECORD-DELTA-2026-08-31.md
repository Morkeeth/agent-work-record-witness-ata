# Fixing the film's two false lines — executable by someone who has never seen this repo

Written 31 Aug. **The headline finding: fixing the two wrong sentences does NOT need a re-cut.**
The picture is not wrong. Only the narration is. So you re-render two paragraphs of voice and
re-mux them onto the picture that already exists. Measured below: about 15 minutes, no re-capture,
no deploy, no Chromium, no Cloud Run.

The click list costed this at 90 minutes because it assumed a re-cut. That estimate was for a
different job.

---

## 🚨 Read this before you run anything

**`film/build.sh` does NOT reproduce `demo/demo-final.mp4`.** Its own comment says so, and it is
right. The shipped 207.63s cut is **five** segments:

    seg-intro 25.00s + seg-terminal 62.32s + seg-console-trim 26.07s
      + seg-browser 84.17s + seg-outro 10.00s  =  207.56s

The join inside `build.sh` uses **three**, drops the slides, and takes the *untrimmed* console
segment. Run it and you get a different, shorter film with the voice landing on the wrong picture.

**Do not run `film/build.sh` to fix a narration line.** Use the path below, which touches the
audio only and never rebuilds the picture.

---

## What is actually wrong: two sentences, both saying the record is append-only

It is not. The API never deletes, but closing a hold rewrites that clearance in place. Every text
surface now says the true thing; only the voice still says the false one.

| Cue | Time | Now says | Say instead |
|---|---|---|---|
| 33 | 00:01:40.494 | Firestore holds every clearance as an append only document. | Firestore holds every clearance as its own document. |
| 47 | 00:02:28.642 | And the record, exportable, append only. | And the record, exportable, every verdict kept. |

**Both replacements were rendered and measured on 31 Aug, so this is not a guess about whether
they fit.** `film/lay_voice.py` lays each paragraph at its own cue start, so what matters is
whether the paragraph still ends before the next cue begins:

| Paragraph | Cue window | Was | Corrected | Headroom |
|---|---|---|---|---|
| `p08` (carries cue 33) | 88.5s → 106.5s = **18.00s** | 16.93s | **16.53s** | 1.47s |
| `p12` (carries cue 47) | 142.8s → 160.0s = **17.20s** | 12.18s | **12.58s** | 4.62s |

`p08` gets shorter. `p12` grows by 0.40s into 5s of slack. Neither overruns.
`lay_voice.py` also warns on its own if a part runs past the next cue, so the tool checks this too.

---

## The path — audio only, about 15 minutes

The voice comes from `demo/voiceover.txt`. **That is the file you edit.** The `.srt` and the
`.vo-parts/*.txt` are both generated from it; editing either of those instead changes nothing you
can hear.

1 · Edit `demo/voiceover.txt`. Two replacements, exactly as in the table above:

    as an append only document      ->  as its own document
    exportable, append only         ->  exportable, every verdict kept

2 · Re-split into per-paragraph files:

    python3 film/split_voice.py

3 · Re-render **only the two changed paragraphs** with the local Kokoro voice. No API, no key:

    cd ~/CODE/voice-generation
    for f in ~/CODE/hack-fleet-ata/demo/.vo-parts/p08.txt ~/CODE/hack-fleet-ata/demo/.vo-parts/p12.txt; do
      ./kvenv/bin/python vo.py "$f" -o "${f%.txt}.mp3" --preset demo --speed 1.42
    done

   Re-rendering all of them also works and costs a few more minutes. It changes nothing else,
   because the preset and speed are pinned.

4 · Lay the paragraphs back onto their cue times:

    cd ~/CODE/hack-fleet-ata
    python3 film/lay_voice.py

   **Read its output.** If it prints a `WARN p12 ends … but p13 starts …` line, a paragraph
   overran and you must shorten the replacement wording. It did not on 31 Aug.

5 · Mux the new voice onto the **existing** picture. This is the step that avoids the re-cut:

    ffmpeg -y -i demo/demo-final.mp4 -i demo/voiceover.mp3 \
      -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k demo/demo-final-v2.mp4

   `-c:v copy` means the picture is not re-encoded and cannot change.

6 · Regenerate the subtitles from the new script:

    python3 film/make_srt.py

7 · Verify before you trust it:

    ffprobe -v error -show_entries format=duration -of csv=p=0 demo/demo-final-v2.mp4   # under 240
    grep -ci "append only" demo/demo-final-v2.srt                                        # must be 0
    grep -c ' --> ' demo/demo-final-v2.srt                                               # cue count

8 · Only when it plays correctly, replace the shipped file and re-copy it to Downloads:

    mv demo/demo-final-v2.mp4 demo/demo-final.mp4
    cp demo/demo-final.mp4 ~/Downloads/ATA-demo-final.mp4
    md5 -q demo/demo-final.mp4     # the old md5 3147f344… is now DEAD. Record the new one.

**The md5 changes.** `docs/OSCAR-CLICK-LIST-2026-08-31.md` step 0 and
`docs/SEALED-PREDICTION-2026-08-29.md` both cite `3147f34484886a83161f585d5084da44`. If you do
this, both are stale and must be updated, or the next reader verifies against a file that no
longer exists.

---

## Two further defects, picture not voice. These DO need a re-capture.

Both are cosmetic and neither is a false claim. They are here so a re-capture fixes the right
things and invents no fifth.

- **2:22 to 2:52** — the narration names the Google-stack tab, the queue and the audit while the
  picture stays on the record detail. Cause was the `?record=` console loop, since fixed. A
  re-capture now follows the words.
- **2:52** — the Policy panel reads `report-only` for about a second because the box had not
  finished loading, while the narrator says "Enforce mode" and live `/policy` returns `enforce`.

If you re-capture, do it against the **current** revision. `curl -s
https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/ | shasum -a 256` must print
`12e0db0982ed91c53c0c0c9ae9e492482bb536b83bfde2f68939f5c032e99eec` before you roll.

---

## The standing ruling, unchanged

**If you do nothing, ship as-is.** That was the recommendation and it is still defensible: a judge
who hears "append only" and then reads the console, which now says *"Keyed store, not an
append-only log"*, sees a product correcting itself in public, which is the thesis.

What this file changes is the price. The audio fix is 15 minutes and cannot alter a single pixel,
which is a different decision from a 90-minute re-cut that puts an unwatched revision in front of
judges. Only the picture defects carry that risk.

**Nobody has watched this film end to end with human eyes.** A frame scan was done and found no
account exposure (`docs/FILM-PIXEL-SCAN-2026-08-31.md`), but that is pixels, not pace, and it
sampled rather than exhausted. Watching it is still the open item and only Oscar closes it.
