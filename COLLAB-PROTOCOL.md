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

## Column update — 2026-08-22, Oscar confirmed Cursor is collaborating

| Claude takes this run | Cursor keeps |
|---|---|
| `contract/**` — the interface, the control set, **and the Gemini implementation behind it** | `fleet/**` · `fleet_cli.py` · `fixtures/**` · `README.md` |
| `docs/**` · `surface/**` · `PHASE-*.md` · `CONTEXT.md` · `CLOSE.md` · `PITCH.md` | |

**What Claude needs from Cursor, in priority order:**
1. **`fleet/signals.py` calls `contract.task_class.classify` instead of `_topic_match`.** The Gemini
   implementation exists and scores 7/8 against a substring test's 3/8. Until the call site moves,
   the product still ships the version with no signal. **Oscar has not moved this boundary, so this
   is a request, not an edit.**
2. **A fixture cut from a real session** (see CURSOR-LOG). `LANDED` stays uncomputable without it.
3. **Fixture B's prompt may need to change** — see the C1 finding in CURSOR-LOG. Not "fix auth".

**Keys:** read from `~/.config/keys/gemini.key` (0600) at call time. Never in the repo, never echoed,
never an argument. `contract/gemini_impl.py` does this and nothing else should.
