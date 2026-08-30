# Record the demo fresh — screen and voice

Two paths. Pick one before you start, not halfway through.

- **A · Your own voice, live, one take.** Reads as a person. Costs takes.
- **B · Silent screen capture, local text-to-speech over it.** No talking, perfect sync,
  free, nothing leaves the laptop. This is how the current cut was made.

The hybrid at the bottom is the one to use if you are unsure: render the voice first, follow
it in headphones while you capture, then mux. It gives you A's picture with B's timing.

---

## Before you record — the setup that prevents a re-record

Do all of these. Each one has ended a take before.

1. **Do Not Disturb on.** One Slack toast in frame and the take is dead.
2. **Hide the Dock** — `⌥⌘D`.
3. **Hide the browser bookmarks bar** — `⌘⇧B`. Use a clean window with no personal tabs.
4. **Terminal font up** to about 18–20pt. Clear the scrollback.
5. **Display at 1920×1080.** Bigger resolutions make text unreadable after YouTube compresses it.
6. **Warm the service** — load `https://fleet-wedge-33kamss2jq-uc.a.run.app/health` once.
   A cold start hangs the first request, and it will hang on camera.
7. **Run `./film/preflight.sh`** — it re-probes every number in the script. If it fails, a
   number you are about to say out loud is stale.
8. **Open exactly three things:** the console at `/hold/?record=H-a6151a95ac`, the PR #1 checks
   page, and one terminal already in this repo. Nothing else.

---

## A · Your own voice, live

macOS records screen and microphone together. The microphone is **off by default** — this is
the single most common way to end up with four minutes of silent video.

1. Press `⌘⇧5`.
2. Choose **Record Entire Screen** (not a portion — a portion scales badly on YouTube).
3. Open **Options** and set:
   - **Microphone → your mic.** Confirm it does not say None.
   - **Save to → Desktop**
   - **Show Mouse Clicks → on**
   - **Timer → None**
4. Click **Record**. Speak from `demo/FILM-AND-SUBMIT.md`, which is the teleprompter.
5. Stop with the stop button in the menu bar, or `⌘⌃Esc`.

Say the full product name at least twice. Never say "required check" — branch protection is off.
Say the cold eligibility number, one of three, in the same breath as three of three.

You get a `.mov` on the Desktop. It will be large. Compress before uploading:

```sh
ffmpeg -i ~/Desktop/Screen\ Recording.mov -vf scale=1920:1080 \
  -c:v libx264 -preset medium -crf 22 -c:a aac -b:a 128k ~/CODE/hack-fleet-ata/demo/demo-final.mp4
```

---

## B · Local text-to-speech

The tool is `~/CODE/voice-generation` — Kokoro-82M, runs on CPU, no API key, no signup.
Do not reach for ElevenLabs; this is already installed and it is good enough.

**The script** is `demo/voiceover.txt`. One spoken line per line. Blank lines add a pause.
Edit the words there, not in the renderer.

**Render it:**

```sh
cd ~/CODE/voice-generation
./kvenv/bin/python vo.py ~/CODE/hack-fleet-ata/demo/voiceover.txt \
  -o ~/CODE/hack-fleet-ata/demo/voiceover.mp3 --preset demo
```

`--preset demo` is the right one: close, dry, and normalised to −16 LUFS so it sits under a
screen capture instead of fighting it. `trailer` is for film trailers and will sound absurd here.

**Directives** go at the top of the script file and apply downward:

```
@voice bm_george     # deep British. Others: bm_lewis, am_fenrir (US), af_heart
@lang b              # 'b' British, 'a' US — must match the voice prefix
@speed 1.0
@pause 400           # ms of silence after every line
```

Too slow overall? Do not edit thirty lines — scale them all at once:
`--speed 1.15 --pause 0.7`.

**Check the length before you build anything around it:**

```sh
ffprobe -v error -show_entries format=duration -of csv=p=0 ~/CODE/hack-fleet-ata/demo/voiceover.mp3
```

The cap is 4:00. The current script renders to about 2:27.

---

## The hybrid — recommended

Perfect sync, no talking, no timing anxiety.

1. Render the voiceover (B above) and check its duration.
2. Put on headphones and play it.
3. Press `⌘⇧5`, **Microphone → None**, and record the screen while you follow the audio and
   click along with it.
4. Mux the voice onto the silent capture:

```sh
ffmpeg -i ~/Desktop/Screen\ Recording.mov -i ~/CODE/hack-fleet-ata/demo/voiceover.mp3 \
  -map 0:v -map 1:a -vf scale=1920:1080 \
  -c:v libx264 -preset medium -crf 22 -c:a aac -b:a 128k -shortest \
  ~/CODE/hack-fleet-ata/demo/demo-final.mp4
```

`-shortest` ends the video with the voice, so a few stray seconds of clicking at the end
disappear on their own.

---

## Before you upload

- **Watch it end to end.** All of it. This is the step that always gets skipped, and it is the
  one that catches the defect the person who built it cannot see.
- Confirm it is under 4:00: `ffprobe -v error -show_entries format=duration -of csv=p=0 <file>`
- Nothing on screen that is banned: the Seed button, `/healthz`, the words "required check",
  the names Witness / Claims Inbox / hack-fleet-ata, the CLI presented as the product.
- Upload to YouTube, set **Public**, then open the link in an incognito window and watch it
  start. A private or still-processing video is an entry with no video.
