# Film capture harness

Run before Oscar records the 3-minute Devpost video.

```bash
chmod +x film/preflight.sh film/capture.sh
./film/preflight.sh    # must exit 0
./film/capture.sh      # rehearsal with pauses (PAUSE_SEC=5 for faster)
```

**Token (optional for preflight):** `.hold_api_token` or `HOLD_API_TOKEN` for break-glass writes.
Record probe uses public `/audit/export` when no token is present.

**Checklist:** `docs/OSCAR-FILM-CHECKLIST.md` · spine: `docs/FILM-FINAL-RUN-2026-08-29.md`
