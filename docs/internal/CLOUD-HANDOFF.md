# CLOUD HANDOFF — Cursor Cloud Agent lane

**Paste this entire file into a new Cursor Cloud Agent on this repo.**
Oscar runs Claude Code locally + Cursor locally + this cloud lane. Git is the mailbox.

## Before you start

1. **Repo must be on a remote** — cloud agents clone from GitHub/origin, not Oscar's laptop.
   Oscar: push first (`origin` skill or `gh repo create`). No remote = cloud lane cannot start.
2. **Read order:** `COLLAB-PROTOCOL.md` → `PHASE-TRACKER.md` → `CONTEXT.md` → `docs/WEDGE.md` →
   `docs/BUILD-PLAN.md` → `docs/SIGNAL-SPEC.md` → `CURSOR-LOG.md` (newest last).
3. **You are the Cursor cloud column.** Local Cursor owns `fleet/**` · `fixtures/**` · `fleet_cli.py`.
   Local Claude owns `docs/**` · `surface/**` · `CONTEXT.md` · `PHASE-*.md`. Do not edit outside
   your column unless Oscar explicitly waives protocol.

## Your mission

**Hold vision + hackathon gates while local builders ship.**

| Check | Object | Pass condition |
|---|---|---|
| Vision | `CONTEXT.md` + `docs/WEDGE.md` | Surface 5 = agent **propagates** literal best prompt, never rewrites |
| Ambition | `docs/BUILD-PLAN.md` | Pub/Sub network + GEAP in diagram; wedge loop is submission-critical |
| Hackathon phase | `PHASE-TRACKER.md` | No phase marked ✅ until gate object proves it |
| Collab | `COLLAB-PROTOCOL.md` | Never `git add -A`; explicit paths only |
| Kill condition | Aug 26 | GCP + Gemini — Oscar only; you prepare, do not deploy |

## What is NOT done yet — do not pretend

| Gate | Status | Owner |
|---|---|---|
| EYES multi-model on **product thesis** | ✅ Aug 22 (Cursor session) | — |
| EYES on **full submission package** | ⛔ NOT RUN | Cloud or Oscar |
| EYES on **user journey end-to-end** | ⛔ NOT RUN | Cloud or Oscar |
| **Sealed prediction** (#72, Phase 7) | ⛔ Correctly absent until pre-submit | Oscar |
| **USER-JOURNEY.md** | ⛔ Missing | Claude column (`docs/`) |
| **Design owner + `/design`** (Phase 3) | ⛔ Open per PHASE-TRACKER | Oscar names owner |
| **SIGNAL-SPEC implemented** | ⛔ Spec exists, code is heuristic | Cursor column |
| **Fixtures with real tool_use records** | ⛔ Requested in CURSOR-LOG | Cursor column |
| **Cloud Run hello-world** (Slice 0) | ⛔ Blocked on GCP | Oscar Aug 26 |

## Cloud lane tasks (priority order)

### 1. Review audit — append to `CURSOR-LOG.md` only
Run a structured pass and append findings (with command output):

```bash
python3 fleet_cli.py wedge --topic "refactor auth"
python3 -c "from fleet.signals import score_session; import json; \
  paths=['fixtures/operators/operator-a-refactor.jsonl','fixtures/operators/operator-b-refactor.jsonl']; \
  print(json.dumps({p: score_session(p,'refactor auth') for p in paths}, indent=2))"
```

Verify: operator **a** beats **b** · propagate · witness · no `"operator"` string bug.

### 2. User journey draft — REQUEST Claude column
Do **not** write `docs/USER-JOURNEY.md` yourself. Append to `CURSOR-LOG.md` a outline for Claude:

- **Day-0:** rollout owner connects opt-in corpus
- **Day-1:** sees 95% gate + who prompts well on task class X
- **Day-2:** supervisor propagates operator A's prompt → org skill → witness
- **Judge path:** stranger runs `fleet_cli.py wedge` on fixtures in empty HOME

### 3. Submission flow checklist — append to `CURSOR-LOG.md`
Map `hackathon.md` phases 4–7 to concrete artifacts:

| Phase | Artifact | Exists? |
|---|---|---|
| 4 Build | wedge CLI + Cloud Run | partial |
| 5 Exhibit | stranger one-click | no |
| 6 Freeze | Oscar degraded path | no |
| 6b Pre-camera | cold pass + LIVE=FIXED hash | no |
| 7 Submit | repo + diagram + video + **sealed prediction** | no |

### 4. Optional — EYES panel on user journey
If Oscar says **EYES on journey**: dispatch 3 models on the draft journey + BUILD-PLAN demo beats +
WEDGE loop. Verdict axis: **JUDGE-BELIEVABLE / NOT**.

## Outward acts — refuse

Push · deploy · GCP billing · Gemini keys · Devpost submit · video — route to Oscar.

## Commit discipline

```bash
git add CURSOR-LOG.md   # or your column's files only
git commit -m "cloud lane: <one concern>"
```

Never `git add -A`. Never commit `.DS_Store` or `__pycache__`.

## Success signal for this cloud session

One append to `CURSOR-LOG.md` with:
- Phase tracker corrections (if any object disagrees with a ✅)
- User journey outline handed to Claude column
- Submission-gap table filled with object citations
- Explicit ruling: **vision + ambitious plan aligned?** YES/NO/PARTIAL + one sentence why
