---
doc: hack
project: The Agent Work Record Witness
phase: SHIP
last-touched: 2026-08-29
canonical: true
event: All Things Agentic · Devpost · Mon 31 Aug 2026 17:00 PDT
supersedes: docs/THIRTY-DAY-PLAN.md (immune-system era — history only)
---

# Agent Work Record Witness — hack.md

> **Until Mon 17:00 PDT:** this file is the 48-hour submit plan. **`docs/SUBMISSION.md`** is the pitch;
> **`SUBMISSION-PACK.md`** is Devpost paste. **Handbook ladder:** [`docs/HANDBOOK-PASS-2026-08-29.md`](docs/HANDBOOK-PASS-2026-08-29.md).
> Phase detail: [`docs/internal/PHASE-TRACKER.md`](docs/internal/PHASE-TRACKER.md).

---

## 🪜 HANDBOOK LADDER (Aug 29 · ~65% elapsed)

| Phase | Gate | Status |
|-------|------|--------|
| 5 · Exhibit | `./demo.sh` one-click | ✅ [`STRANGER-PASS`](docs/STRANGER-PASS-2026-08-29.md) |
| 6 · Freeze | Oscar degraded + film | ⛔ `./film/preflight.sh` → [`OSCAR-FILM-CHECKLIST`](docs/OSCAR-FILM-CHECKLIST.md) |
| 7 · Submit | Devpost + **sealed prediction** | ⛔ [`SEALED-PREDICTION`](docs/SEALED-PREDICTION-2026-08-29.md) |

**#85:** film is the hard-fail artifact. **#72:** seal prediction before button. Full pass: HANDBOOK-PASS.

---

## ⭐ NORTH STAR

**Your agents write reports about work they did. This keeps the receipt.**

Four verdicts: **PASS · BLOCK · UNVERIFIABLE · HOLD.** Never runs a command from a report.

---

## 📣 PROMISE LINE

**Promise.** When an agent says it shipped, CI **checks each claim against the repo before merge**
and writes what held to an append-only record your auditor can sample.

**Constraint.** Code decides what is confirmed — never the model.

**Tagline (Devpost):** `Run your agents. Check the math.` Promise line in body only — not tagline field.

---

## 👁 EYES · pitch / product / flow (29 Aug)

Multi-model panel (Grok · Composer · GPT) on aspects **beyond** partner depth (P1/P2).
**Overall: WINNABLE · med confidence.** A + handbook pass implemented 29 Aug.

### One spine (panel consensus)

| Layer | Line |
|-------|------|
| Problem | You can count agent seats; you cannot count true claims. |
| Product | Append-only **receipt** — who claimed what, what the repo said, who overrode. |
| Mechanism | Probes decide; Gemini explains; never runs commands from a report. |
| Moat | Zenity/Qodo/Langfuse don't hold the transcript — can't open a blocked claim to the run. |

Use that spine in README top, Devpost ¶1, film 0:00, `/hold/` header — **one story, not three docs.**

### Claims · panel verdicts

| # | Claim | A / B / C | Ruling |
|---|-------|-----------|--------|
| 1 | Board question beats four-verdicts as *open* | all PARTIAL | **Both:** Priya hook in 0:00–0:15, four verdicts by 0:30 |
| 2 | Deploy P1 + `/hold/` UI = top product ROI | 2× DISAGREE, 1× PARTIAL | **After** credibility scrub + film; P1 invisible without UI |
| 3 | Film closes on live flow, not 41.7→8.1 | all AGREE | **Rule:** finale = demo → PR #1 → `/hold/` join |
| 4 | Stale honest-state tables hurt credibility | 2× AGREE, 1× PARTIAL | **Scrub** USER-JOURNEY, README, WHY-THIS-MATTERS |
| 5 | Tagline split confuses Devpost/film | 2× AGREE, 1× PARTIAL | **Rule:** tagline = short; promise = body only |
| 6 | "Required check" = theater (protection off) | 2× AGREE, 1× PARTIAL | **Scrub** everywhere judge-facing — see list below |
| 7 | Week-zero corpus underused in film | all PARTIAL | **15–20s mid-beat** only; don't live-run unreproducible corpus |
| 8 | Moat sentence in first 30s cold open | 2× DISAGREE, 1× PARTIAL | **At `/hold/` click** + Devpost ¶1, not second 0 |

### Strongest objections (ranked — address or say on camera)

1. **Self-contradiction** — "required check" in SUBMISSION, voiceover, `/hold/` Install tab while README/PACK ban it and branch protection is off.
2. **Film spine wrong** — voiceover/subtitles still say "required check"; SUBMISSION §7 closes on corpus math judges can't re-run.
3. **Live surface ≠ rules** — `/hold/` brands **HOLD** not full product name; Install tab says "Required check".
4. **Join structurally thin** — one author PR, Claude-specific session patterns; say "chain proof, not adoption."
5. **P1 as hero risks "Gemini decided"** — only show if framed explain-only + visible on record.
6. **`architecture.png`** — verify in repo before Devpost attach (board said exists Aug 28; re-probe before paste).

### Suggested slices (review → check to adopt)

#### A · Credibility scrub (~1.5h agent) — **panel #1 priority**

- [x] **A1** Replace "required check" → "verify-claims" / "clearance check" in judge-facing copy
- [x] **A2** Sync honest-state tables to SUBMISSION-PACK §3 truth
- [x] **A3** `/hold/` UI: full product name header + Install tab advisory copy
- [x] **A4** SUBMISSION §8 tagline + film voiceover/subtitles (PACK spine)

#### B · Film spine (Oscar ~3–4h) — **panel #2 priority**

- [ ] **B1** Close on live chain: `./demo.sh` → PR #1 red → `/hold/` row → session/head_sha join
- [ ] **B2** Moat sentence at **hold click**, not cold open: *"None of them holds the transcript."*
- [ ] **B3** Corpus 41.7→8.1 = **mid-beat** (credibility), not finale
- [ ] **B4** Say both eligibility numbers: 3/3 (ADC) · 1/3 (cold)
- [ ] **B5** Optional 15s: `/health` JSON + "Gemini explains; Python decides" if P1 deployed
- [ ] **B6** Ban on camera: Seed · "required check" · unqualified "3 of 3"

#### C · Devpost one paste source (~45m)

- [ ] **C1** Paste **only** from SUBMISSION-PACK §1 — do not mix SUBMISSION §8 fields
- [ ] **C2** Moat sentence in "What it does" ¶1 (already in PACK — verify before submit)
- [ ] **C3** Partner block in "How we built it" from `docs/PARTNER-INTEGRATION-DEEP-DIVE-2026-08-29.md` §8
- [ ] **C4** Attach architecture PNG — ✅ `docs/architecture.png` exported

#### D · Product surface (after A+B, if time)

- [x] **D1** Redeploy Cloud Run — P1+P2 live · revision `fleet-wedge-00010-xww` 29 Aug
- [x] **D2** Re-trigger outcome-gate on PR #1 — run `33250194854` · `witness-findings` check posted
- [x] **D3** `/hold/` detail panel renders `agent_explanation` + `head_sha`
- [x] **D4** README judge path at top

#### E · Defer past Mon (panel agreement)

- P3 check summary · P4 Cloud Trace · org-lift n=2 · live corpus run on film
- Leading with vendor names (Zenity/Qodo/Langfuse) in first 30s
- Enabling branch protection *unless* you want "required" language in v2

### Panel · top 3 if we only do three things

1. **A · Credibility scrub** (copy + UI + voiceover sync)
2. **B · Film spine** (Oscar re-record affected lines)
3. **C · Devpost one paste source**

P1 deploy + D3 UI = **fourth**, not first.

---

## 📊 REVIEW · 29 Aug (2 days left)

### Already strong (do not rebuild)

| Asset | Status |
|-------|--------|
| **Product + pitch one doc** | `docs/SUBMISSION.md` — ten adoption cases §4, Google stack §5, film §7 |
| **Live proof** | Cloud Run `/health` · Firestore · PR #1 red · record `H-a6151a95ac` |
| **Cold demo** | `./demo.sh` · `tests/test_demo.sh` 8/8 · preflight green |
| **Corpus honesty** | 41.7→8.1 preregistered · sample in fixtures |
| **Architecture** | `docs/architecture.png` + `docs/ARCHITECTURE.md` |
| **User journey / P3 persona** | `docs/USER-JOURNEY.md` (Priya) |
| **Devpost copy** | `SUBMISSION-PACK.md` §1–4 (refresh honest-state row for PNG) |

**Stale board items killed:** BUILD-RUN "ten cases not done" / "two pitch docs" / "no Google doc" —
wrong; merged into SUBMISSION.md Aug 28–29.

### Honest gaps (say on camera)

| Gap | Measured | Fix in 48h? |
|-----|----------|-------------|
| **Film + Devpost** | not submitted | **Oscar** — only critical path |
| **Non-author installs** | zero | No — roadmap; say honestly |
| **Nothing cleared** | `clear: 0` | No — HOLD row is the demo |
| **Branch protection** | not enabled | Optional — don't say "required" on film |
| **Eligibility cold** | 1/3 without ADC | Say **both** 3/3 (ADC) and 1/3 (cold) on film |
| **witness-corpus stranger** | needs `pip install .` | **Buildable** — README one-liner + smoke |
| **SUBMISSION-PACK stale** | PNG + agent_invoked wording | **Buildable** — slice C4 + A4 |
| **Doc schism** | SUBMISSION/USER-JOURNEY vs PACK | **closed 29 Aug** — EYES A scrub |
| **Live UI schism** | `/hold/` says HOLD + required check | **closed 29 Aug** — EYES A3 + D3 |
| **voiceover MP3** | script only | **Buildable** — Kokoro if kvenv exists |
| **Repo share judges** | not confirmed | **Oscar** — testing@ + cloudhackathons@ |

### Judging map (Fortified Enterprise Fleet)

| Criterion | Weight | Best evidence |
|-----------|--------|---------------|
| Innovation & utility | 40% | Four verdicts + session join + corpus self-audit |
| Architecture | 30% | Local probe in CI, verdict only crosses network · diagram |
| Demo readiness | 30% | `./demo.sh` + live `/hold/` + red PR #1 · **video** |

---

## ✅ 48-HOUR PLAN (Sat–Mon)

### Oscar only (cannot delegate)

- [ ] **0. Film** — `./film/preflight.sh` → record ≤4:00 (SUBMISSION §7 or SUBMISSION-PACK §2)
- [ ] **0b. Devpost submit** — paste from SUBMISSION-PACK §1 · attach `architecture.png`
- [ ] **0c. Share repo** — `testing@devpost.com` + `cloudhackathons@google.com`
- [ ] **0d. Film language** — never "required check" (branch unprotected) · cold eligibility 1/3

### Agents can build (Sat–Sun)

- [x] **1. Refresh SUBMISSION-PACK §3** — P1 wording; PNG export attempted
- [x] **2. Stranger receipt** — `docs/STRANGER-PASS-2026-08-29.md` (demo.sh via test_demo.sh)
- [x] **3. Commit film assets** — voiceover + subtitles updated (EYES B spine)
- [x] **4. README judge path** — clone → `./demo.sh` → live URL
- [x] **5. DEVPOST-CHECKLIST.md** — `docs/DEVPOST-CHECKLIST.md`

### Partner depth (optional — see `docs/PARTNER-INTEGRATION-DEEP-DIVE-2026-08-29.md`)

- [x] **P1 · ADK explain on HOLD** — Gemini narrates BLOCK findings; probe still decides (~4h) **best ROI**
- [x] **P2 · Action posts session/actor/sha** — richer join metadata on clearance JSON (~1h)
- [x] **P3 · Check run summary** — `gate/check_run_summary.py` · needs push + PR sync to see on GitHub
- [ ] **P4 · Cloud Trace on /clearance** — trace_id on record (~4–6h, only if film time safe)

### Optional (only if film done early)

- [ ] **6. Branch protection** — require `verify-claims` on main (then may say "required" in v2)
- [ ] **7. `pip install` smoke in CI** — one workflow step proving witness-corpus entrypoint
- [ ] **8. Org-lift ruling** — ship / hold / kill n=2 pages (Oscar)

### Do NOT start (2-day trap)

- GitHub App · Pub/Sub fan-out · GEAP Memory Bank · org-lift on film · ten *new* case studies
- Second corpus run · prompt propagation · new product features in `gate/`

---

## 🎯 NOW

**RUN COMPLETE 29 Aug.** P1+P2+P3 live · preflight PASS. Oscar: **film** → `SEALED-PREDICTION` → Devpost.

---

## POST-SUBMIT (after Mon)

### Week 1

- [ ] Stranger not on Oscar's machine · external PR · named user quote (`docs/ADOPTION-RECEIPT.md`)

### Week 2–4

- [ ] Second adoption case · `docs/GOOGLE-STACK.md` standalone · org-lift ruling · branch protection

---

## 🪵 LOG

- 2026-08-29 · Full 48h review; pre-submit plan replaces post-only hack.md.
- 2026-08-29 · Probed: preflight PASS · eligibility 3/3 · branch unprotected · P1+P2 coded.
- 2026-08-29 · Handbook pass: HANDBOOK-PASS, SEALED-PREDICTION template, PHASE-TRACKER refresh, STRANGER-PASS, voiceover/preflight sync.
