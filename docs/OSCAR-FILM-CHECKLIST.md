# Oscar film checklist · one take · Mon 31 Aug 17:00 PDT

**Hero record:** `H-a6151a95ac` · session `01Lzbh4XPYTAgCKg1dciFS3Q`  
**Deep link:** https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/?record=H-a6151a95ac  
**Spine:** `docs/FILM-FINAL-RUN-2026-08-29.md` · voiceover `film/voiceover-vo.txt` · subtitles `film/subtitles.srt`

---

## 1 · Preflight (stop if red)

```bash
cd ~/CODE/hack-fleet-ata
git pull
./film/preflight.sh
```

Expect every line green: numbers · 8 voiceover/subtitle beats · `./demo.sh` cold · `/health` · record row · PR #1 `verify-claims` **failure**.

Optional rehearsal (no camera):

```bash
PAUSE_SEC=1 ./film/capture.sh
./demo.sh --film
```

---

## 2 · Record (≤4:00 · unedited)

| Step | Action |
|------|--------|
| Terminal | **SF Mono Regular 14 pt** · dark profile · **100×32** window · zoom so gate output fills frame |
| Browser | `/hold/?record=H-a6151a95ac` tab pre-loaded · PR #1 checks tab queued |
| Order | Follow 8 beats in `FILM-FINAL-RUN-2026-08-29.md` (record first, corpus mid, close on tagline) |
| Audio | Voiceover from `film/voiceover-vo.txt` or live read · burn `film/subtitles.srt` in edit |
| Never say | "required check" · "HOLD" as product name · unqualified "3 of 3" |

**On camera beats:** board question → hold deep link + moat → PR #1 red → `./demo.sh --film` → verdict map → corpus 78,618 / 41.7→8.1 → `/health` + eligibility (3/3 **and** 1/3 cold) → *Run your agents. Check the math.*

---

## 3 · Upload

- [ ] Export ≤4:00 MP4 (unedited per Devpost rules)
- [ ] Attach `docs/architecture.png` in Devpost form
- [ ] Repo shared: `testing@devpost.com` + `cloudhackathons@google.com`

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

**Before submit button:** complete `docs/SEALED-PREDICTION-2026-08-29.md`.

Honest bullets (include ≥1): PR #1 red by design · row `H-a6151a95ac` · `clear: 0` · zero non-author installs · cold eligibility 1/3.

Full field checklist: `docs/DEVPOST-CHECKLIST.md`.
