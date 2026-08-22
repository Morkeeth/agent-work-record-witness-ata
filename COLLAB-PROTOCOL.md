# COLLAB PROTOCOL — two builders, one tree

**Oscar's ruling 2026-08-22: Cursor AND Claude are both on this repo.** The fleet law's
"one agent per repo" is waived by him — so the safety has to be mechanical instead.

## File ownership — do not write outside your column

| Cursor owns | Claude owns | Shared, append-only |
|---|---|---|
| `fleet/**` · `fleet_cli.py` · `fixtures/**` · `README.md` · `tests` · `cloud/**` | `docs/**` · `surface/**` · `contract/**` · `PITCH.md` · `CLOSE.md` · `PHASE-0.md` · `CONTEXT.md` · `LANE.md` · `FOR-CURSOR.md` · `PHASE-TRACKER.md` | `CURSOR-LOG.md` · `COLLAB-PROTOCOL.md` · `COLLAB-REVIEW.md` |

To change a file you do not own: **write the finding into `CURSOR-LOG.md` and let the owner
apply it.** Never edit it directly. Read-modify-write from two agents is last-writer-wins and
the loss is silent.

## Committing

- **NEVER `git add -A`.** Explicit paths only. On 2026-08-22 a `git add -A` swept Cursor's
  entire working `fleet/` module into a Claude docs commit (`04b7e35`) and attributed it wrongly.
  That is the whole reason this file exists.
- Commit your own files only. Leave the other builder's untracked work untracked.
- One concern per commit; say which column it touched.

## The shared log

`CURSOR-LOG.md` is append-only, newest at the bottom. One entry per finding:
**date · what was checked · the object cited (path, command, output) · the ruling.**
A finding without pasted output is a claim, not a receipt.

## Outward acts
Push, deploy, publish, submit, spend — **Oscar's alone.** Neither builder performs them and
neither may authorise the other to.
