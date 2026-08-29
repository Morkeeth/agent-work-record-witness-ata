# Handbook pass · ATA · 29 Aug 2026

**Process door:** `vault/01 Projects/Hackathons/hackathon.md`  
**Index:** `hackathon-handbook-INDEX.md` §5 (ATA live entry)  
**Partner + submit chapter:** `hackathon-partner-submission.md`  
**Canonical ship board:** [`hack.md`](../hack.md)

Handbook rule **#86:** this file exists so the retro is not the first time the handbook opened.

---

## Ladder · where we are (Aug 29 ~65% elapsed)

| Phase | Gate | Status | Evidence |
|-------|------|--------|----------|
| **0 · Entry** | Contract + kill condition + four rungs | ✅ | `docs/internal/PHASE-0.md` · kill: GCP by Aug 26 **surpassed** |
| **1 · Spec extract** | Quoted checkboxes + URL | ✅ | `docs/SPEC-EXTRACT.md` · partner § below |
| **2 · Wedge** | Tagline + story-bank | ✅ | `docs/WEDGE.md` · Gate B closed in PHASE-TRACKER |
| **3 · Vision lock** | Doc overrides code | ✅ | `hack.md` canonical · `docs/SUBMISSION.md` |
| **3 · Design owner** | Named for filmed screen | ✅ **ruled** | Oscar · `/hold/` console (`surface/hold/index.html`) |
| **4 · Build** | Judge sees delta · #85 rank | ✅ exiting | P1+P2 coded · credibility scrub 29 Aug |
| **5 · Exhibit** | Stranger one-click, no keys | ✅ | `./demo.sh` · `tests/test_demo.sh` 8/8 |
| **6 · Freeze & prove** | Oscar degraded path | ⛔ **Oscar** | cold clone + live URL + film |
| **6b · Pre-camera** | LIVE = FIXED by hash | ⛔ **Oscar** | `./film/preflight.sh` before take |
| **7 · Submit** | Artifact + **sealed prediction** | ⛔ **Oscar** | `docs/SEALED-PREDICTION-2026-08-29.md` |
| **8 · Post-result** | Distil lesson | ⛔ after | — |

**Phase 4 clause (b) #85:** video is the hard-fail artifact. Rank tasks against film/Devpost until Mon.

---

## Phase 1 · Submission extract (quoted checkboxes)

Source: https://allthingsagentichackathon.devpost.com/ · fetched 2026-08-22 · re-checked deadline 2026-08-27

| Deliverable | Quoted rule | Status |
|-------------|-------------|--------|
| Gemini 3.5+ | *"Gemini 3.5 or newer accessed through Gemini API or Vertex AI"* | ✅ eligibility + `/agent/run` |
| Agent framework | *"At least one Google Agent Framework…"* | ✅ ADK |
| GCP service | *"At least one Google Cloud infrastructure service…"* | ✅ Cloud Run + Firestore |
| Track | Fortified Enterprise Fleet | ✅ |
| Repo + README | *"Code repository URL… setup instructions in README.md"* | ✅ judge path in README |
| Architecture diagram | *"Architecture diagram showing system connections"* | ✅ `docs/architecture.png` |
| Video ≤4:00 | *"Demo video, max 4 minutes"* | ⛔ Oscar |
| Text description | features, technologies, data sources, learnings | ⛔ Devpost paste PACK §1 |
| Pre-existing code | disclosed | ✅ SUBMISSION-PACK §4 disclosure |
| Deadline | *"Aug 31, 2026 @ 5:00pm PDT"* | ⛔ |
| Hosted URL | *"(if available)… highly encouraged"* | ✅ live `/hold/` |
| Judge repo share | Devpost + Google emails | ⛔ Oscar |
| Licence | OSI | ✅ MIT `LICENSE` |

**30% Demo sub-checks:**

- [x] **Proof of Action** — unedited live execution planned (`SUBMISSION-PACK.md` §2)
- [x] **Documentation** — diagram + `./demo.sh` in README
- [ ] **Cloud Deployment Proof** — film must show `*.run.app` /health (#69)

---

## Phase 1 · Partner extract (handbook extension)

| Mandatory | Quoted / probed | Rung | Status |
|-----------|-----------------|------|--------|
| Gemini 3.5+ Vertex | `contract/eligibility.py` **calls** classify | 3 | ✅ 3/3 ADC · 1/3 cold |
| Google ADK | `build_agent()` + `POST /agent/run` + P1 explain HOLD | 3–5 | ✅ coded · deploy D1 |
| Cloud Run | live gateway | 4 | ✅ |
| Firestore | append-only record `H-57b130f397` | 4 | ✅ |
| GitHub Actions | `verify-claims` → `/clearance` | 4 | ✅ PR #1 |

**Load-bearing sentence:** *Without Cloud Run + Firestore, the CI probe has nowhere to write the receipt the auditor exports.*

**GEAP seven surfaces (honest):** Gateway ✅ · Observability ✅ (export) · Identity ✅ (token) · Runtime partial · Memory/Registry/Armor **roadmap** — `docs/GEAP-GAP-2026-08-27.md`

**Theater list — scrubbed 29 Aug:** no "required check" · no Memory Bank claim · no "Gemini decides merge"

Full depth: `docs/PARTNER-INTEGRATION-DEEP-DIVE-2026-08-29.md` · **remaining:** `docs/PARTNER-REMAINING.md`

---

## Phase 5 · Exhibit checklist (#63 · one click)

- [x] `./demo.sh` — no wallet, no install, no keys, no network (`env -i`)
- [x] Stranger sees **BLOCK** on false claim, not green tick
- [x] One command reproduces (`git clone` → `./demo.sh`)
- [x] Live `/hold/` readable without token (reads open; writes gated)
- [ ] Oscar cold-browser pass after any deploy (#78-II)

---

## Phase 6 · Freeze & prove (Oscar)

- [ ] Private window · no sessionStorage from build session
- [ ] Clone fresh · run judge path from README
- [ ] `./film/preflight.sh` PASS immediately before record
- [ ] Eligibility: run **both** warm 3/3 and cold 1/3; say both on film
- [ ] Re-probe anon `POST /clearance` → 401 after deploy

Receipt: `docs/STRANGER-PASS-2026-08-29.md`

---

## Phase 6b · Pre-camera gate

- [ ] Non-builder cold-pass `/hold/` at recording viewport
- [ ] LIVE equals FIXED by hash on filmed URL
- [ ] `grep story-bank` done for film script (Gate B)

---

## Phase 7 · Submit

- [ ] Devpost from `SUBMISSION-PACK.md` §1 only · `docs/DEVPOST-CHECKLIST.md`
- [ ] Attach `docs/architecture.png`
- [ ] **Seal prediction first** — `docs/SEALED-PREDICTION-2026-08-29.md` · then button (#72)

---

## Kill-or-ship memo

| Axis | Verdict | One line |
|------|---------|----------|
| **PARTNER READY** | YES (after D1 deploy for P1 on film) | 3/3 + 1/3 eligibility · GEAP honest five-of-seven max |
| **SUBMIT READY** | NO — film + Devpost + sealed prediction | Mechanical gap only; product path green |
| **BLOCKED** | Nothing technical | Oscar outward acts |

---

## Log

- 2026-08-29 · Handbook pass written; PHASE-TRACKER refreshed; design owner ruled Oscar.
