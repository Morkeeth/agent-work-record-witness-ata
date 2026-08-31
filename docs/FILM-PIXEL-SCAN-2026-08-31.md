# The film's pixels, looked at — 31 Aug 13:1x CEST

Every earlier privacy statement about this film was sourced from the transcript and the shot
list, never from the picture. This is the first pass that opened the frames.

**It does not replace a human watch.** It answers one question — is anything in frame unsafe to
publish — and it answers nothing about pace, level or whether the film is any good.

## Method

`ffmpeg` frame extraction from `demo/demo-final.mp4` (md5 `3147f34484886a83161f585d5084da44`,
207.6s), then the images were opened and read:

- Full-resolution single frames at 85s, 88s, 92s, 96s, 100s, 104s — the Google Cloud console segment.
- A 1-frame-per-second crop of the console's **top-right corner**, 80s to 110s, 30 frames tiled.
- Contact sheets at 1 frame / 12s over 0–140s and 1 frame / 8s over 140–207s.

## Result: the account is not in frame

**The signed-in Google account never appears.** The avatar menu is never opened. Across all 30
top-bar frames the corner holds only: the search box, the Gemini spark, the Cloud Shell icon, a
green notification count, the kebab, and a profile photo. **No email address, in any frame sampled.**

That was the one thing step 3 of the click list existed to check before flipping the video Public.

Also read and clean:
- The project chip reads `hack fleet`, and the service URL `fleet-wedge-568004190078.us-central1.run.app`.
  The project number is already public in the run.app hostname, so it discloses nothing new.
- The GitHub segments were captured **logged out** — the page shows Sign in / Sign up. No GitHub
  account state is on screen. The repo shows as `Morkeeth/agent-work-record-witness-ata · Public`,
  which is intended.
- No terminal frame sampled shows a home-directory path, a token, or a credential.

## The one judgement left, and it is yours

**Oscar's profile photo is on screen for the whole Cloud console segment**, roughly 1:26 to 1:45,
as the ~40px avatar in the top-right corner. It is his face, small, on a video that will be public
under his own name and next to his own byline. This is not a leak; it is a choice. Nothing here
can decide it.

## What this pass did NOT do

- It sampled frames. It did not inspect every one of the ~6,200. Small text at low resolution in
  an unsampled frame could have been missed.
- It read pictures, not audio. The two "append only" narration lines at 1:40 and 2:28 stand as
  already ruled: see `docs/RECORD-DELTA-2026-08-31.md`.
- **Nobody has still watched this film end to end with human eyes.** That remains open and only
  Oscar can close it.
