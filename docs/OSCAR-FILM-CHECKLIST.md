# Oscar film checklist · one take · Mon 31 Aug 17:00 PDT

**Hero record:** `H-a6151a95ac` · session `01Lzbh4XPYTAgCKg1dciFS3Q`  
**Live deep link:** https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/?record=H-a6151a95ac  
**Spine:** `docs/FILM-FINAL-RUN-2026-08-29.md` · voiceover `film/voiceover-vo.mp3` · subtitles `film/subtitles.srt`

---

## 1 · Preflight (must exit 0)

```bash
cd ~/CODE/hack-fleet-ata   # or your clone path
git pull origin main
./film/preflight.sh
```

**Green means:** canonical numbers · 8 voiceover/subtitle beats · `./demo.sh` cold · `/health` live · row `H-a6151a95ac` on `/audit` · PR #1 `verify-claims` = **failure** (red by design).

**Local only (gitignored):** `.hold_api_token` — same value as GitHub secret `HOLD_API_TOKEN` / Cloud Run env. Preflight passes without it (public `/audit` probe); keep the file for break-glass on camera and export probe.

**Fast rehearsal:**

```bash
PAUSE_SEC=5 ./film/capture.sh    # eight beats with pauses
./demo.sh --film                   # compact terminal output
```

---

## 2 · Record (≤4:00 · unedited)

### Terminal (for `./demo.sh --film` beat)

| Setting | Value |
|---------|--------|
| App | **Terminal.app** (macOS) |
| Profile | **Pro** or **Basic** dark |
| Font | **SF Mono** (fallback: Menlo) |
| Size | **18 pt** |
| Window | ~100×28 cols/rows · hide tab bar · full-screen or clean crop |

Say **THE AGENT WORK RECORD WITNESS** in full at least twice. Never "HOLD" as the product name.

### Capture order (matches voiceover)

| Time | On camera |
|------|-----------|
| 0:00 | Board question |
| 0:10 | `/hold/?record=H-a6151a95ac` — moat line at click |
| 0:28 | PR #1 checks · `verify-claims` + `witness-findings` red |
| 0:52 | `./demo.sh --film` |
| 1:22 | UNVERIFIABLE → HOLD · gate never runs commands from report |
| 1:42 | Corpus mid-beat: 78,618 · 41.7→8.1 |
| 2:08 | `/health` · `python3 contract/eligibility.py` — **3/3 with ADC and 1/3 cold** |
| 2:32 | *Run your agents. Check the math.* |

**Banned on camera:** Seed button · "required check" (branch protection off) · unqualified "3 of 3" · org lift at n=2.

**Optional live once:** break-glass write with real reason (token in `.hold_api_token`).

---

## 3 · Upload

- [ ] Screen recording ≤4:00 · unedited
- [ ] Burn subtitles from `film/subtitles.srt` (or editor import)
- [ ] Voiceover track: `film/voiceover-vo.mp3` if not recorded live
- [ ] Review: no stale record IDs · no "required check" · both eligibility numbers said

---

## 4 · Devpost fields (paste only from `SUBMISSION-PACK.md` §1)

| Field | Value |
|-------|--------|
| Name | THE AGENT WORK RECORD WITNESS |
| Tagline | Run your agents. Check the math. |
| Track | Fortified Enterprise Fleet |
| Live URL | https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/ |
| Repo | https://github.com/Morkeeth/agent-work-record-witness-ata |
| Built with | Python · Google Cloud Run · Firestore · GitHub Actions · Vertex Gemini · ADK |

**Before submit button:**

1. Fill `docs/SEALED-PREDICTION-2026-08-29.md` (handbook #72 — no edits after)
2. Attach `docs/architecture.png`
3. Share repo with `testing@devpost.com` **and** `cloudhackathons@google.com`

Full field copy: `SUBMISSION-PACK.md` §1 · partner block: `docs/PARTNER-INTEGRATION-DEEP-DIVE-2026-08-29.md` §8 · honest bullets: `docs/DEVPOST-CHECKLIST.md`.

**Deadline:** Mon 31 Aug 2026 · **17:00 PDT**
