# Film final run · 2026-08-29 · GO (spine v2)

**Status:** record-first spine · `--film` demo · hold deep links · clarity pass done.

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

## Terminal capture (lock before rolling)

| Setting | Value |
|---------|--------|
| App | Terminal.app (macOS) |
| Font | **SF Mono Regular 14 pt** (Menlo 14 acceptable) |
| Window | **100 columns × 32 rows** minimum |
| Profile | Dark background · light text (match `/hold/` `#0f1419` if custom) |
| Zoom | Full-screen or 125% so gate `PASS`/`BLOCK`/`HOLD` lines are legible at 1080p |

Preflight verified 2026-08-29: `./demo.sh --film` compact output matches all 8 voiceover beats; record `H-a6151a95ac` present in live export; PR #1 `verify-claims` conclusion=failure.

---

## After record

1. `docs/SEALED-PREDICTION-2026-08-29.md` before Devpost button
2. Paste `SUBMISSION-PACK.md` §1 + `docs/architecture.png`
3. Share repo: `testing@devpost.com` + `cloudhackathons@google.com`

Checklist: `docs/OSCAR-FILM-CHECKLIST.md`
