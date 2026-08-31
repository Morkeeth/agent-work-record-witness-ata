# Pitch — read this first when you're back

**TL;DR:** "Where does the data come from?" is answered. You have one real row in the record. Film + Devpost are the only moves left.

---

## The one-liner

**THE AGENT WORK RECORD WITNESS** connects what an agent *claims* to what the repo *contains* — and keeps a record your CI fills automatically. A keyed store, not an append-only log: the API never deletes, but closing a hold rewrites that clearance in place.

---

## Three data pipes (don't mix them)

1. **Gate** — `./demo.sh` · synthetic repo · stranger-safe · **already green**
2. **Record** — PR #1 tonight · Action posted **`H-a6151a95ac`** · traceable to session · **solved tonight**
3. **Corpus** — customer's Transcripto DB · sample in repo · **day-two, not Monday-critical**

---

## What I did while you were out

- Created label `agent` (was missing).
- Opened **PR #1** with the false-done body (`deadbee`).
- GitHub Action ran → local probe BLOCK → posted to Cloud Run → **recorded in Firestore**.
- Receipt: `docs/DATA-SOURCE-RECEIPT-2026-08-28.md`

**Open these two tabs:**

- https://github.com/Morkeeth/agent-work-record-witness-ata/pull/1 (red check = success)
- https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/ (row `H-a6151a95ac`)

---

## Film spine (≤4:00) — use this order

| Time | Beat |
|---|---|
| 0:00 | Problem — seats ≠ practice; agents claim work you can't verify |
| 0:30 | `./demo.sh` — stranger catches false claim, no account |
| 1:30 | PR #1 — agent label → `verify-claims` + `witness-findings` fail on deadbee |
| 2:30 | `/hold/` — open the hold; click through to session |
| 3:15 | GCP — `/health` · say full product name twice |
| 3:45 | Honest close — corpus is opt-in; record fills from your PRs |

**Banned:** Seed button · "42%" without denominator · shortening the name.

---

## Devpost

Paste from `SUBMISSION-PACK.md`. Repo is public — no judge invite. Submit before **Mon Aug 31 17:00 PDT**.

**Data field (paste-ready):**

> Demo gate: in-repo `./demo.sh` (no external data). Live record: populated by this repo's GitHub Action posting clearance decisions from agent-labelled PRs to Cloud Run/Firestore. Corpus measurement: optional Transcripto transcript DB; committed sample `fixtures/corpus-sample-40.json` for reproducibility.

---

## Optional (not blocking)

- Enable branch protection requiring `verify-claims` on `main`.
- Merge or leave PR #1 open for the film — open is better on camera.

---

## Autonomous mode (Oscar away)

Heartbeat every **30 minutes** → `docs/AUTONOMOUS-HEARTBEAT-LOG.md` (probe: demo, PR #1, H-a6151a95ac, live endpoints).

---

## Queue context

NeurIPS still #1 (blocked on OpenReview login · Sun deadline). ATA is **film-only** now — no more build.
