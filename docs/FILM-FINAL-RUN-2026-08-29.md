# Film final run · 2026-08-29 · GO (spine v2)

**Status:** preflight PASS · `--film` demo · hold deep links · clarity pass done.

**Hero record:** `H-a6151a95ac` · session `01Lzbh4XPYTAgCKg1dciFS3Q`  
**Live:** https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/?record=H-a6151a95ac

---

## Terminal capture (lock before rolling)

| Setting | Value |
|---------|--------|
| App | **Terminal.app** (macOS) · dark profile (Pro or Basic) |
| Font | **SF Mono Regular 14 pt** (fallback: Menlo 14 pt) |
| Window | **100×32** columns×rows minimum · hide tab bar · zoom **100%** (⌘0) |
| Shell | repo root `~/CODE/hack-fleet-ata` · `python3 -V` → **3.12.x** (not `/usr/bin/python3` 3.9) |
| Rehearsal | `PAUSE_SEC=8 ./film/capture.sh` then `./demo.sh --film` — same font/size as record |

Preflight note: record row is verified via public `GET /audit/export` (no token). Create
gitignored `.hold_api_token` before the live break-glass beat on camera.

---

## Film order (≤4:00 · matches voiceover + subtitles)

| Time | Beat | On camera |
|------|------|-----------|
| 0:00 | Board question | *If the regulator asks what you hand them…* |
| 0:10 | **Record first** | https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/?record=H-a6151a95ac |
| 0:28 | PR chain | PR #1 checks tab · verify-claims + witness-findings red |
| 0:52 | Stranger probe | `./demo.sh --film` (compact, readable) |
| 1:22 | Verdict map | UNVERIFIABLE → HOLD · gate never runs commands from report |
| 1:42 | Corpus (mid) | 78,618 · 41.7→8.1 · fixture in repo |
| 2:08 | Cloud proof | `/health` · `python3 contract/eligibility.py` — **3/3 ADC and 1/3 cold** |
| 2:32 | Close | *Run your agents. Check the math.* |

**Never say:** "required check" (branch protection off).

---

## Rehearsal

```bash
cd ~/CODE/hack-fleet-ata
./film/preflight.sh
PAUSE_SEC=8 ./film/capture.sh
./demo.sh --film
open "https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/?record=H-a6151a95ac"
```

---

## After record

1. `docs/SEALED-PREDICTION-2026-08-29.md` before Devpost button
2. Paste `SUBMISSION-PACK.md` §1 + `docs/architecture.png`
3. Share repo: `testing@devpost.com` + `cloudhackathons@google.com`

Checklist: `docs/DEVPOST-CHECKLIST.md`
