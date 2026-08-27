> ⛔ **SUPERSEDED 2026-08-27 — do not read as current.** The canonical doc is `hack.md` at the repo root.
> This file is kept for history only. It described a narrower product than the one being built.

# BUILD PLAN — three builders, nine days

**Supersedes the earlier version of this file** (pre-dated the compliance audit, the GEAP
tailoring and the Gemini fit study). Written 2026-08-22. **Owner column is binding —
`COLLAB-PROTOCOL.md`.**

---

## THE RE-ORDERING THAT CUTS THE RISK — read this first

`PHASE-0.md` treats **one** Aug-26 gate. There are actually **two, and they are not the same gate.**

| Requirement | Needs | Blocked? |
|---|---|---|
| **1 · Gemini 3.5+** | an **AI Studio key** | **NO. No credit card. Billing disabled is the free tier — enabling billing DELETES it.** Unblocked today |
| **2 · Google agent framework (ADK)** | `pip install google-adk` + a model to call | needs #1 only |
| **3 · Google Cloud service** | GCP billing + `gcloud` | **YES — the real Aug 26 gate** |

**Consequence: the classifier — the single highest-risk piece, the one that turns the control set
green and makes the wedge work — can be built and proven BEFORE Aug 26**, on a free key, with no
spend and no billing decision.

**That means Aug 26 stops being the day everything starts.** It becomes the day the *deploy* starts,
against a classifier already green. That is the difference between a swap and an integration written
under deadline.

**Ask Oscar for the Gemini key now. It costs nothing and it is not the GCP decision.**

---

## VERIFIED STATE — probed 2026-08-22, not recalled

| | |
|---|---|
| ✅ wedge loop runs end to end | `find → propagate → witness`, money line now prints `"operator": "a"` |
| ✅ byte mismatch fixed | propagate and witness agree at 250 |
| ❌ **classifier carries no signal** | `contract/task_class.py` → **3/8, identical to a stub that ignores its input** |
| ❌ **`LANDED` uncomputable** | zero `tool_use` records in any fixture |
| ❌ **0 of 3 mandatory requirements** at runtime | `docs/COMPLIANCE-AUDIT.md` |
| ⚠️ Phase 3 design owner unnamed · direction unpicked · hours uncalibrated | Oscar |

---

## LANE A — NOW → Aug 26. Nothing here needs GCP.

| # | Slice | Owner | Unblocks |
|---|---|---|---|
| **A1** | **Gemini key + the classifier behind `contract/task_class.py`.** Enum-constrained structured output; `UNDECIDABLE` is one of exactly three schema values. **Watch it choose the refusal — do not assume it can.** | Oscar (key) → **Cursor** (`fleet/`) | requirement 1 · the wedge's only real defect · C1 goes green and the demo gets a comparison |
| **A2** | **Cut fixtures from a REAL session.** Not an invented `tool_use` record — an inherited shape cannot be wrong about what a tool call looks like. `~/CODE/transcripto` is the corpus. | **Cursor** | `LANDED` becomes computable · the demo stops printing `UNMEASURED` for everyone |
| **A3** | Episode-based scoring per `docs/SIGNAL-SPEC.md`. `CORRECTIVE_TURNS` · `LANDED` · `ABANDONED`, each naming its probe. **n<3 prints `UNMEASURED` and is watched printing it.** | **Cursor** | the denominator |
| **A4** | **`docs/USER-JOURNEY.md`** — flagged missing in `CLOUD-HANDOFF.md`. Every step, ranked, three actors. | **Claude** | Phase 3 · the video script |
| **A5** | Build the picked direction as the real surface, then run **all three probes** on it: render · metric-vs-data · adjacency. | **Claude** (needs the pick) | the exhibit |
| **A6** | ADK supervisor wrapping the three existing plain functions. Runs locally on the Gemini key. | **Cursor** | requirement 2 |

**A1 and A2 are the critical path. Everything else can slip.**

## LANE B — Aug 26 onward. All of it needs GCP.

| # | Slice | Owner |
|---|---|---|
| **B1** | `gcloud run deploy --source` a hello-world. **Cloud Build — no local Docker, no Colima, avoids the ARM/amd64 trap.** Screenshot it. | Cursor + Oscar |
| **B2** | **GEAP console checks, one hour, timeboxed.** `ListEvents` callable on PAYG · events carry function calls · a user event is distinguishable from a tool result · Memory Bank read/write. **Fallback decided in advance: if it resists, Firestore + Cloud Run satisfies requirement 3 and the wedge is unaffected.** | Cursor |
| **B3** | Deploy the supervisor + surface. Hosted URL. | Cursor |
| **B4** | Pub/Sub fan-out — the analyst network. **First thing cut.** | Cursor |

## LANE C — the gates. These are what get cut under pressure, so they are listed as slices.

| # | Gate | Owner | Why it is here |
|---|---|---|---|
| **C1** | **Name a design owner + run `/design`** | **Oscar** | Phase 3. *"The exhibit was advice rather than a gate, so it got cut as polish — that is the entire Overturn loss."* |
| **C2** | **EYES on the user journey end-to-end** | Cursor cloud | ⛔ never run |
| **C3** | **EYES on the full submission package** | Cursor cloud | ⛔ never run |
| **C4** | **Cold pass by a lane that has never seen these fixtures** | coordinator routes | a builder cannot see his own screen — proved four times today |
| **C5** | Architecture diagram **rendered and looked at** | Claude | required component |
| **C6** | Phase 6 — **Oscar** drives the degraded path himself, no keys, fresh browser | **Oscar, not delegable** | — |
| **C7** | Record: **one take, unedited** | Oscar | *"undeniable proof of execution"* |
| **C8** | Sealed prediction, then **submit** | Oscar alone | outward |

---

## THE ORDER, compressed

```
NOW      Gemini key (free) ──> A1 classifier ──> control set GREEN ──┐
         A2 real fixtures  ──> A3 episodes    ──> LANDED computable ─┼─> A5 surface + 3 probes
         A4 user journey   ─────────────────────────────────────────┘
AUG 26   GCP ──> B1 hello-world ──> B2 GEAP (timeboxed) ──> B3 deploy ──> [B4 fan-out, cuttable]
AUG 29   C4 cold pass ──> C5 diagram ──> C6 Oscar drives it degraded
AUG 30   C7 record, one take
AUG 31   C8 submit
```

**Cut order, decided now so it is not decided at 2am:** B4 → A6 → the surface's polish.
**Never cut:** A1, A2, C4, C6, C7.

## Standing rules for all three builders
- **Never `git add -A`.** Explicit paths. It already misattributed `04b7e35` once.
- Cross-column findings go in `CURSOR-LOG.md` as a request; the owner applies them.
- **Outward acts are Oscar's alone** — remote, push, deploy, spend, submit.
- **No Colima, no container build.** Disk is at 99%, and Colima was the 99 GiB hog last time.
