# THIRTY-DAY PLAN — prompt immune system → category product

**Written 2026-08-22.** Objective: not "ship a hackathon demo," but **prove and harden an institutional prompt immune system** that a VP Eng would pay for — then expand it into a category product.

**North star (day 30):** A stranger can connect an opt-in corpus, see who lands prompts with fewer corrective turns on a task class, and the supervisor **propagates the literal winner** into the org skill file — witnessed, refuse-when-thin, hosted, with GEAP (or honest Firestore fallback) on the diagram.

**Law:** every claim names its probe. `UNMEASURED` prints. Never cut the witness.

**Calendar anchor:** today = Day 0 (Aug 22). Hackathon submit = Day 9 (Aug 31). Day 30 = Sep 21.

**Owners:** Oscar (outward) · Cursor (`fleet/`, `cloud/`, fixtures) · Claude (`docs/`, `surface/`, `contract/`).

**Cut order (decided now):** Pub/Sub fan-out theater → surface polish → GEAP Memory Bank stretch → people leaderboard stretch.  
**Never cut:** pairwise ranking · literal propagate · witness · eligibility on judge path · one-take video (Week 0) · stranger one-click.

---

## Week 0 — Days 0–9 · SUBMIT OR DON'T ENTER
*Ambition = win the track. Scope = wedge + proof. EYES tiers bind.*

### Day 0–1 (Aug 22–23) — eligibility + Claude docs
| # | Outcome | Done when | Owner | Size |
|---|---|---|---|---|
| 0.1 | Judge path loads Gemini + ADK + Firestore modules | `python3 contract/eligibility.py` → **3/3** | Cursor | M |
| 0.2 | `docs/MOONSHOT-PLAN.md` + video beat sheet (M3 center) | File exists; EYES tier table adopted | Claude | S |
| 0.3 | `docs/USER-JOURNEY.md` — 3 actors | Rollout owner · eng B · stranger mapped to probes | Claude | M |
| 0.4 | Gate 1 direction **picked** + design owner named | One sentence in `PHASE-TRACKER.md` | **Oscar** | S |
| 0.5 | Hours calibration one-liner | Resolves PHASE-0 vs tracker conflict | **Oscar** | S |

### Day 2–3 (Aug 24–25) — surface + honest controls
| # | Outcome | Done when | Owner | Size |
|---|---|---|---|---|
| 0.6 | Surface direction built from pick | HTML/app renders A-vs-B corrective-turn delta from live JSON | Claude | L |
| 0.7 | Three probes on surface | render · metric-vs-data · adjacency — all logged | Claude | M |
| 0.8 | Architecture diagram (honest two-path) | GEAP box **or** labeled Firestore fallback; looked at | Claude | M |
| 0.9 | Classifier variance appendix | N=10 table; C1 red named; no "8/8" seal | Cursor | S |

### Day 4 (Aug 26) — GCP gate
| # | Outcome | Done when | Owner | Size |
|---|---|---|---|---|
| 0.10 | Cloud Run hello → wedge API | `./scripts/deploy_cloud_run.sh` · public URL · `/healthz` 200 | Cursor + Oscar | L |
| 0.11 | GEAP 1h console box | Registry + one Memory Bank write **or** written fallback | Cursor | M |
| 0.12 | `FLEET_STORE=firestore` on deploy | Live `put` on `/wedge` (not import-only) | Cursor | M |

### Day 5–6 (Aug 27–28) — exhibit
| # | Outcome | Done when | Owner | Size |
|---|---|---|---|---|
| 0.13 | Hosted stranger path | cold machine · `POST /wedge` · witness · surface reads JSON | Cursor | M |
| 0.14 | Cold pass (never-seen-fixtures lane) | Exit 0 + notes in CURSOR-LOG | coordinator | M |
| 0.15 | Video script locked to USER-JOURNEY | Beat sheet ≤4 min · M3 center · authorship trap shown | Claude | S |

### Day 7–8 (Aug 29–30) — freeze + film
| # | Outcome | Done when | Owner | Size |
|---|---|---|---|---|
| 0.16 | Oscar degraded path | Fresh browser · no keys · full loop | **Oscar** | M |
| 0.17 | One-take unedited video | YouTube/Vimeo URL · unedited | **Oscar** | L |
| 0.18 | Sealed prediction | Written before submit; classifier claim = C5/C6 traps not "8/8" | **Oscar** | S |

### Day 9 (Aug 31) — submit
| # | Outcome | Done when | Owner | Size |
|---|---|---|---|---|
| 0.19 | Devpost package complete | Repo · diagram · video · description · pre-existing disclose · track selected | **Oscar** | M |
| 0.20 | Submit before 17:00 PDT | Confirmation screenshot | **Oscar** | S |

**Week 0 ambition check:** if 0.10–0.13 slip, cut 0.11 GEAP stretch first — keep hosted wedge + M3 video.

---

## Week 1 — Days 10–16 · REAL CORPUS + HARDEN THE METRIC
*Ambition = the demo stops being two fixtures.*

| # | Outcome | Done when | Owner | Size | Risk |
|---|---|---|---|---|---|
| 1.1 | Ingest path from transcripto DB (read-only) | ≥50 real sessions scored; redaction gate documented | Cursor | L | PII / redaction |
| 1.2 | n≥3 floor enforced | Thin classes print `UNMEASURED` and are watched doing it | Cursor | M | — |
| 1.3 | C1 control rewritten or second contract | Prompt-vs-prompt only; C1 green **or** honest kill | Claude+Cursor | M | Contract shape |
| 1.4 | Operator identity model | Stable operator IDs across sessions (not filename stem) | Cursor | M | — |
| 1.5 | Propagation dry-run + approve gate | Default = propose; auto-write only with flag | Cursor | M | Trust |
| 1.6 | Surface wired to live corpus API | No fixture JSON in production path | Claude | L | — |
| 1.7 | Eval harness | Golden set of 20 episode pairs; CI gate | Cursor | M | — |

**Week 1 done when:** a real (redacted) corpus run names a best operator with `episodes_matched ≥ 3` or correctly refuses.

---

## Week 2 — Days 17–23 · PRODUCT LOOP + MULTI-SEAT
*Ambition = rollout owner daily driver, not demo.*

| # | Outcome | Done when | Owner | Size | Risk |
|---|---|---|---|---|---|
| 2.1 | Opt-in team onboarding | Day-0 checklist · corpus connect · skill path config | Claude | M | — |
| 2.2 | People view (thin) | Ranked operators per task class + corrective-turn delta | Claude | L | Design |
| 2.3 | Task-class clusters over time | Same class across weeks; drift probe named | Cursor | L | Classifier drift |
| 2.4 | Propagation history + rollback | Witness log · revert skill file to prior SHA | Cursor | M | — |
| 2.5 | Slack/email "best prompt landed" notify | One outbound channel on successful witness | Cursor | S | — |
| 2.6 | GEAP Memory Bank as prompt store (if Week 0 box passed) | Ranked prompts read/write Memory Bank | Cursor | L | GEAP console |
| 2.7 | Security review | No transcript text executed · secrets scan · RLS/IAM notes | Cursor | M | — |

**Week 2 done when:** a second fictional team seat can receive a propagated skill without SSH.

---

## Week 3 — Days 24–30 · FLEET NETWORK (EARNED MOONSHOT)
*Ambition = institutional network — only after metric + corpus are real. This is where M2 was killed for Week 0; it returns here if earned.*

| # | Outcome | Done when | Owner | Size | Risk |
|---|---|---|---|---|---|
| 3.1 | Async ingest worker | New transcripts → episode signals → queue (Cloud Run job or Pub/Sub) | Cursor | L | Ops |
| 3.2 | Analyst agent (one, not N) | ADK agent summarizes task-class health nightly | Cursor | M | Cost |
| 3.3 | Cross-repo skill targets | Propagate to `.cursor/rules` **and** Claude skill path | Cursor | M | — |
| 3.4 | Survival after propagate | Measure eng B corrective turns **after** skill land (the 30s falsifier) | Cursor | L | Causal claim |
| 3.5 | Pricing narrative + ICP page | Per-engineer vs enablement budget; not vapor | Claude | S | — |
| 3.6 | Architecture prize pack | Updated diagram · GEAP Registry · Memory Bank · queue · wedge API | Claude | M | — |
| 3.7 | Public README + stranger script v2 | Empty HOME · one command · hosted URL optional | Cursor | S | — |

**Week 3 / Day 30 done when:** you can show **before/after corrective turns** for operator B after propagation — or the system refuses to claim improvement (`UNMEASURED`). That is the product thesis falsifier from EYES, and it is the moonshot.

---

## Stretch after Day 30 (do not schedule; park)
- Multi-harness ingest (Cursor IDE transcripts)
- Pub/Sub fan-out to N analysts (only if 3.1–3.4 green)
- Marketplace of org prompts (privacy nightmare — design first)
- GEAP Agent Runtime 7-day jobs

---

## Dependency spine (what unblocks what)

```
eligibility 3/3 ──┐
USER-JOURNEY ─────┼─→ surface + video script ─→ one-take ─→ SUBMIT (D9)
Cloud Run URL ────┘         │
                            ▼
              real corpus (W1) ─→ n≥3 refuse ─→ approve-gate propagate
                            │
                            ▼
              people view (W2) ─→ Memory Bank optional
                            │
                            ▼
              before/after delta (W3) ← THE MOONSHOT PROOF
```

---

## Ambition vs honesty

| Claim we want | What must be true first |
|---|---|
| "Best operator in the org" | n≥3 episodes · pairwise SAME · named probe |
| "Propagation improves the fleet" | before/after corrective turns (slice 3.4) |
| "GEAP-native architecture" | 1h console proof or labeled fallback |
| "95% authorship moat" | Shown on camera / in product, not only in PITCH.md |

---

## How to use this plan

1. **Week 0 is law until Aug 31.** Do not steal days for Week 3.
2. After submit, **re-plan Week 1 from reality** — this file is disposable.
3. Each morning: pick the top unchecked slice · `/frame` it · ship · probe · log.
4. Oscar stops the agent when the current slice is done — that is the loop.

**Step 1 right now:** Claude writes `docs/MOONSHOT-PLAN.md` + `docs/USER-JOURNEY.md` while Cursor holds eligibility 3/3 and Oscar picks Gate 1.
