# Oscar film checklist · one page · Mon 31 Aug 17:00 PDT

**Product name on camera:** THE AGENT WORK RECORD WITNESS (full name, ≥2×).  
**Hero record:** `H-a6151a95ac` · session `01Lzbh4XPYTAgCKg1dciFS3Q`  
**Spine:** `docs/FILM-FINAL-RUN-2026-08-29.md` · voiceover `film/voiceover.txt` (8 beats)

---

## 1 · Preflight (do not roll until green)

```bash
cd ~/CODE/hack-fleet-ata
git pull
./film/preflight.sh
```

| Check | Expect |
|-------|--------|
| Numbers | 78,618 · 41.7 → 8.1 in voiceover + `docs/SUBMISSION.md` |
| Demo | `./demo.sh` exit 0 (cold, no network) |
| Live | `/health` → auth, firestore, demo_seed off |
| Record | `H-a6151a95ac` in `/audit/export` |
| PR #1 | OPEN · `verify-claims` conclusion **failure** (red by design) |

**Terminal lock:** SF Mono **14 pt** · window **100×32** · dark · zoom 100% — see FILM-FINAL-RUN.

**Local only:** gitignored `.hold_api_token` (same as Cloud Run `HOLD_API_TOKEN`) for break-glass on camera.

Rehearsal: `PAUSE_SEC=8 ./film/capture.sh` · `./demo.sh --film` · open hold URL with `?record=H-a6151a95ac`.

**Never say:** "required check" (branch protection off).

---

## 2 · Record (≤4:00 unedited)

| Time | Beat | On camera |
|------|------|-----------|
| 0:00 | Board question | *If the regulator asks what you hand them…* |
| 0:10 | **Record first** | `/hold/?record=H-a6151a95ac` · moat line at click |
| 0:28 | PR chain | PR #1 checks · verify-claims + witness-findings red |
| 0:52 | Stranger probe | `./demo.sh --film` |
| 1:22 | Verdict map | UNVERIFIABLE → HOLD · gate never runs commands from report |
| 1:42 | Corpus (mid) | 78,618 · 41.7→8.1 · fixture in repo |
| 2:08 | Cloud proof | `/health` · eligibility **3/3 with ADC** and **1/3 cold** |
| 2:32 | Close | *Run your agents. Check the math.* |

Voiceover MP3: `film/voiceover-vo.mp3` · subtitles: `film/subtitles.srt`.

---

## 3 · Upload

- [ ] Screen recording ≤4:00 · unedited · product name spoken in full
- [ ] Attach **`docs/architecture.png`** on Devpost
- [ ] Repo shared: `testing@devpost.com` + `cloudhackathons@google.com`

---

## 4 · Devpost fields (paste from `SUBMISSION-PACK.md` §1 only)

| Field | Value |
|-------|--------|
| Name | THE AGENT WORK RECORD WITNESS |
| Tagline | Run your agents. Check the math. |
| Track | Fortified Enterprise Fleet |
| Live URL | https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/ |
| Repo | https://github.com/Morkeeth/agent-work-record-witness-ata |
| Built with | Python · Google Cloud Run · Firestore · GitHub Actions · Vertex Gemini · ADK |

**What it does / How we built it:** copy §1 from `SUBMISSION-PACK.md` + partner block from
`docs/PARTNER-INTEGRATION-DEEP-DIVE-2026-08-29.md` §8.

**Before submit button:** complete `docs/SEALED-PREDICTION-2026-08-29.md`.

**Honest bullets (include ≥1):** PR #1 red · row `H-a6151a95ac` · `clear: 0` · zero non-author installs · cold eligibility 1/3.

Full field checklist: `docs/DEVPOST-CHECKLIST.md`.
