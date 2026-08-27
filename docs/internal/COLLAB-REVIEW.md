# COLLAB REVIEW — full state + build plan for Claude × Cursor

**Date:** 2026-08-22 · **Repo:** `~/CODE/hack-fleet-ata` · **Branch:** `main` @ `8329110`  
**Purpose:** Single object both builders read before the next commit. Supplements `docs/BUILD-PLAN.md`
(do not replace it — this adds review verdicts and handoffs).

---

## 1 · VERDICT FIRST

| | |
|---|---|
| **Vision** | ✅ Sound — org practice visibility · propagate literal best prompt · GEAP line |
| **Ambition** | ✅ `docs/BUILD-PLAN.md` ceiling (Pub/Sub, GEAP) stays diagram-only |
| **Submission eligibility** | ❌ **0/3 mandatory Google requirements at runtime** |
| **Wedge loop** | ✅ Runs — `operator: "a"` · propagate · `VERIFIED-BY-REPO` |
| **Classifier** | ❌ 3/8 = negative control; **fails C4–C6 false-positive traps** |
| **LANDED signal** | ❌ Uncomputable — zero `tool_use` in fixtures |
| **Collab hygiene** | ⚠️ Protocol stale · no remote · Cursor fixes uncommitted |

**The product is right. The plumbing is absent. That is the better failure mode nine days out.**

---

## 2 · WHAT EACH BUILDER SHIPPED

### Claude (15 commits today) — docs · contract · surface · honesty

| Artifact | Value |
|---|---|
| `docs/COMPLIANCE-AUDIT.md` + `CLOSE.md` | Caught disqualification before more features |
| `contract/task_class.py` | 8 controls + negative control; binds **live** `_topic_match` |
| `docs/SIGNAL-SPEC.md` | Pins denominator; admits LANDED uncomputable today |
| `surface/gate1-directions.html` | UNMEASURED first-class; self-caught fabricated LANDED |
| `docs/GEMINI-FIT.md` | Enum schema = native fit for SAME/DIFFERENT/UNDECIDABLE |
| `docs/BUILD-PLAN.md` v2 | **Split gate:** Gemini key free today · GCP Aug 26 |
| `PITCH.md` | Judge narrative in Oscar's voice; moat scoped to fleet scale |

**Claude's best move:** STOP building surfaces that print verdicts the data cannot support.  
**Claude's self-corrections to trust:** frozen-copy contract bug · fixture-rewrite withdrawn · `git add -A` lesson.

### Cursor (local, uncommitted) — fleet · fixtures · wedge

| Artifact | Value |
|---|---|
| `fleet/signals.py` | Task-class overlap heuristic — **demo pair only** |
| `fleet/propagate.py` | Operator `"a"` fix · witness byte consistency |
| `fleet_cli.py` + fixtures | End-to-end wedge on synthetic transcripts |
| `CLOUD-HANDOFF.md` | Cloud agent brief (untracked) |

**Cursor overlap heuristic today:** passes C1,C3,C8 · **fails C2,C4,C5,C6,C7** — would ship wrong rankings on traps.

---

## 3 · HACKATHON PHASE MAP (`hackathon.md`)

| Phase | Gate | State | Owner next |
|---|---|---|---|
| 0 Entry | 4-rung ladder | ⚠️ Rung 2 hours — **PHASE-0.md says ✅, PHASE-TRACKER says OPEN** | Oscar: one canonical ruling |
| 1 Spec | Quoted checkboxes | ✅ | — |
| 2 Wedge | Gate B story-bank | ✅ | — |
| 3 Vision | Doc + design owner | ⚠️ `WEDGE.md` yes · **design owner unnamed** | Oscar names owner · Claude A4 journey |
| 4 Build | Nothing ahead of submission-killer | ▶️ | A1 classifier (blocks everything) |
| 5 Exhibit | Stranger one-click | ⛔ | After B3 deploy |
| 6 Freeze | Oscar degraded path | ⛔ | Calendar Aug 29 |
| 7 Submit | Artifact + **sealed prediction** | ⛔ | Aug 31 Oscar |

**Multi-model review done:** product thesis (EYES Aug 22) · next-steps plan (EYES Aug 22).  
**Not done:** user journey EYES · full submission package EYES · sealed prediction (correctly later).

---

## 4 · UNIFIED BUILD PLAN — three builders, nine days

*Merged from `docs/BUILD-PLAN.md` v2 + EYES panel + live probes.*

### LANE 0 — Oscar (outward acts)

| When | Slice | Done when |
|---|---|---|
| **Tonight** | AI Studio Gemini key (no billing) | `curl` models list → 200 · key in env not committed |
| **Tonight** | Devpost $150 credits form | Screenshot submitted |
| **Tonight** | `gh repo create` + push | `git remote -v` non-empty |
| **Tonight** | Name design owner | Name in `PHASE-TRACKER.md` |
| **Tonight** | Hours calibration one line | Resolves PHASE-0 vs PHASE-TRACKER conflict |
| **Aug 26** | GCP project + billing | `gcloud run services list` works |
| **Aug 29–31** | Phase 6 · video · sealed prediction · submit | Non-delegable |

### LANE A — NOW → Aug 26 (no GCP)

| # | Slice | Owner | Done when | Risk |
|---|---|---|---|---|
| **A1** | Gemini `classify()` → `contract/task_class.py` | **Cursor** implements · Claude owns interface | ≥7/8 controls · beats negative control · C5/C6 pass | UNDECIDABLE refusal |
| **A2** | Real fixture from transcripto | **Cursor** | ≥1 `tool_use` in fixture · `is_human_turn` rejects toolUseResult | redaction |
| **A3** | Episode scoring (narrow) | **Cursor** | survive/abandon + classifier wired · **not** full n≥3 on 2 fixtures | UNMEASURED on camera OK if honest |
| **A4** | `docs/USER-JOURNEY.md` | **Claude** | Day-0→day-2 rollout owner + judge path + stranger path | — |
| **A5** | Surface direction pick + 3 probes | **Claude** | Oscar picks direction · render · metric-vs-data · adjacency | needs C1 design owner |
| **A6** | ADK wrap locally | **Cursor** | `build_agent()` runs against Gemini key | after A1 |

**Critical path:** A1 ∥ A2 → A3 → A6. **A4 parallel now.**

### LANE B — Aug 26+ (GCP)

| # | Slice | Done when |
|---|---|---|
| **B1** | Hello-world Cloud Run `--source` | URL + screenshot |
| **B2** | GEAP checks (1h max) | ListEvents OR fallback Firestore documented |
| **B3** | Deploy supervisor + surface | Judge-visible URL |
| **B4** | Pub/Sub fan-out | **First cut** |

### LANE C — Gates (never cut)

C4 cold pass · C5 architecture diagram (Claude) · C6 Oscar degraded · C7 one-take video · C8 sealed prediction

**Cut order if behind:** B4 → A6 polish → surface polish. **Never cut:** A1 · A2 · C4 · C6 · C7.

---

## 5 · COLUMN OWNERSHIP — UPDATE NEEDED

`COLLAB-PROTOCOL.md` is stale. Proposed:

| Cursor | Claude | Shared append-only |
|---|---|---|
| `fleet/**` · `fleet_cli.py` · `fixtures/**` · `README.md` · `tests/` · `cloud/**` | `docs/**` · `surface/**` · `contract/**` · `PITCH.md` · `CLOSE.md` · `PHASE-*.md` · `CONTEXT.md` · `LANE.md` · `FOR-CURSOR.md` | `CURSOR-LOG.md` · `COLLAB-PROTOCOL.md` · `COLLAB-REVIEW.md` |

**Cross-column rule unchanged:** finding → `CURSOR-LOG.md` → owner applies. **Never `git add -A`.**

---

## 6 · CLAUDE — YOUR NEXT THREE COMMITS

1. **`docs/USER-JOURNEY.md`** (A4) — three actors: rollout owner · engineer B · ADK supervisor.  
   Map to video beats in `docs/BUILD-PLAN.md`. Use *propagate*, not *rewrite*.

2. **Update `COLLAB-PROTOCOL.md`** — add `contract/` · `surface/` · `PITCH.md` · `CLOSE.md` to your column.

3. **Reconcile docs conflict** — `PHASE-TRACKER.md` rung 2 vs `PHASE-0.md` ✅: either ask Oscar
   for one line or mark PARTIAL until he rules.

**Do not:** edit `fleet/` · invent `tool_use` records · print LANDED without tool data · `git add -A`.

---

## 7 · CURSOR — YOUR NEXT THREE COMMITS

1. **Commit wedge fixes** — `fleet/signals.py` · `fleet/propagate.py` · `CLOUD-HANDOFF.md` (explicit paths).

2. **A1: `contract/classify_gemini.py`** (or implement in `contract/` per Claude's interface) —  
   structured enum output · run `python3 contract/task_class.py` until green.

3. **A2: cut fixture** from real session per CURSOR-LOG shape probe (`tool_use` in assistant ·
   `toolUseResult` as `type:user`).

**Do not:** edit `docs/` · `surface/` · deploy without Oscar.

---

## 8 · OSCAR — DECISIONS THAT UNBLOCK BOTH

| # | Decision | Blocks |
|---|---|---|
| 1 | Gemini key tonight | A1 · A6 · requirement 1 |
| 2 | Git push | Cloud agent · collaboration |
| 3 | Design owner name | A5 · Phase 3 |
| 4 | Surface direction pick (gate1 HTML) | A5 build |
| 5 | Hours calibration one line | Phase 0 canonical |
| 6 | May Cursor edit `contract/classify` impl while Claude owns interface? | A1 collision |

---

## 9 · COMPLIANCE MATRIX (living)

| Req | Artifact | Status |
|---|---|---|
| Gemini 3.5+ | `classify()` + smoke test | ⛔ |
| ADK | `cloud/agent.py` local run | ⛔ |
| GCP service | Cloud Run URL in video | ⛔ Aug 26 |
| Repo + README | `README.md` | ⚠️ partial |
| Architecture diagram | — | ⛔ C5 |
| ≤4min video | — | ⛔ C7 |
| Sealed prediction | — | ⛔ C8 |

---

## 10 · THE ONE LINE FOR BOTH BUILDERS

> **GEAP governs the agents. Nothing governs the prompts. The supervisor propagates the org's
> literal best prompt and proves it landed — or prints UNMEASURED and refuses to lie.**

That is the vision. Everything else is plumbing to make it eligible and visible.
