# Film capture harness

Run before Oscar records the 3-minute Devpost video.

```bash
chmod +x film/preflight.sh film/capture.sh
./film/preflight.sh    # must exit 0
./film/capture.sh      # rehearsal with pauses (PAUSE_SEC=5 for faster)
```

**Needs locally (gitignored):** `.hold_api_token` for export probe and break-glass on camera. Preflight falls back to public `GET /audit` when the token is absent.

**Outputs:** `voiceover.txt` + `subtitles.srt` — same words, for Kokoro + burn-in.

Spine: `docs/SUBMISSION.md` §7.
