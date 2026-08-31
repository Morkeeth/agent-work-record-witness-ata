# The repository count: "40" was never measured. The number is 74.

*Read 2026-08-31, 04:5x CEST, wave 4. Every number below carries the command that produced it.*

## What was claimed, and what stood behind it

`across 40 repositories` shipped on four surfaces:

```
$ grep -rnI "40 repo\|40 repositories" --exclude-dir=.git .
surface/hold/index.html:284
docs/THE-THESIS.md:40           <- routed to the Devpost LONG DESCRIPTION
docs/SUBMISSION.md:95
docs/SUBMISSION.md:162
docs/CORPUS-MEASUREMENT-2026-08-27.md:5   <- the only source
```

`CORPUS-MEASUREMENT-2026-08-27.md:5` reads *"2,672 transcripts, 40 repos, 100 sessions"* — a
sentence with **no command beside it**. Nothing in the repo produces 40 for that object:

- `gate/corpus_scan.py` emits `repos_on_disk = len(siblings)` (**83** — every repo under
  `--code-root`, not the corpus), and `messages_in_a_live_repo`. It never emits a distinct-repo
  count over the corpus.
- The frozen artifact `surface/witness-corpus.json` has **no repository-count field at all**.

Waves 2 and 3 correctly refused to change it: they measured **80** on the *live, grown* database,
which is a different population from the frozen 78,618, so it could not disprove 40. Swapping an
unsupported number for an unproven one is the defect this product is named after.

## What changed: the frozen population turned out to be recoverable

`~/.trace/trace.db` has a `ts` column, so the 27-Aug snapshot can be reconstructed by cutting the
corpus at a timestamp instead of measuring today's database. Bisecting for the cut that reproduces
the frozen `corpus_total_messages`:

```
$ TOTAL 144306 reached exactly at ts = 2026-08-26T07:33:25.934Z
```

**Three independent controls, all exact** — the reconstruction is the same population the scan ran on:

| field | frozen `surface/witness-corpus.json` | reconstructed at `ts <= 2026-08-26T07:33:25.934Z` | |
|---|---|---|---|
| `corpus_total_messages` | 144,306 | **144,306** | MATCH |
| `examined_messages` | 78,618 | **78,618** | MATCH |
| `messages_in_a_live_repo` | 52,878 | **52,878** | MATCH |

The third is the decisive one. `messages_in_a_live_repo` is a function of *exactly* the
(population × repo-set) pair the scan used. Reproducing it to the message means the repo set below
**is** the repo set the scan walked.

Fourth control: all **16** repositories named by the 44 shipped BLOCK claims sit inside the
reconstructed set (`listed <= names` → `True`, zero missing).

## The measurement

```python
EX  = "role='assistant' and is_human=0 and text is not null and length(text)>20"
CUT = "2026-08-26T07:33:25.934Z"
cwds  = distinct cwd  from messages where ts <= CUT and EX and cwd is not null   -> 1157
roots = [d for d in cwds if os.path.exists(os.path.join(d, ".git"))]             ->   75
names = {os.path.basename(d.rstrip("/")) for d in roots}                         ->   74
```

`os.path.exists(cwd/'.git')` is `gate/corpus_scan.py`'s own repo test, used verbatim.

- **75** distinct repository-root directories.
- **74** distinct repository names. The one collision is `paris-portfolio`, checked out twice
  (`~/CODE/Paris Portfolio/paris-portfolio` and `~/CODE/paris-portfolio`).
- **1,157** distinct working directories examined, of which 75 are repository roots.

## The verdict, and what actually pins it

**74 is the number. 40 was never measured.** It understates by a factor of 1.85.

The obvious worry is that `os.path.exists(cwd/'.git')` is evaluated **today**, not on 27 Aug, and
that error runs **both** ways: a repository deleted since is lost, and a directory that was plain
then and has been `git init`-ed since is gained. So the "today" test alone would give a number that
could be high or low, and an earlier draft of this file claimed the error was one-directional. That
was wrong, and it is corrected rather than deleted.

**What pins it is the exact `messages_in_a_live_repo = 52,878` match.** That figure is the count of
examined messages whose cwd is in the repo set — a function of the (population × repo-set) pair.
Every cwd in the set of 75 carries examined messages, so adding a repository to the set inflates
that count and removing one deflates it. Reproducing 52,878 **to the message** therefore pins the
set itself, not just its size. There is no reading of this measurement under which 40 survives.

Note this is a different object from the `83 repos on disk` on the same page: that one is
`len(siblings)` over `--code-root ~/CODE`, it has a receipt, and it is unchanged.

## Where "40" probably came from — named as a hypothesis, not asserted

The only receipted 40s in the repo are the hand-label sample size: *"Of 40 randomly sampled
extractions, only 13 were claims at all"* (`gate/corpus_scan.py:16`), which ships as
`extractor precision 13 of 40`. A sample size reused as a population count is the adjacency error
this product exists to name. **This is a hypothesis. It is not evidence, and nothing was changed
on the strength of it** — the change below rests on the measurement above.

## What was changed, with the post-edit grep

`40` → `74` on all four judge-facing surfaces. `docs/CORPUS-MEASUREMENT-2026-08-27.md:5` **keeps
its 40** as the preserved record of the wrong number, now annotated with the correction in the same
block — the same convention the 42%/8.1% pairing uses.

```
$ grep -rnI "40 repo\|40 repositories" --exclude-dir=.git \
    --exclude=NIGHTRUN-2026-08-31.md --exclude=CORPUS-REPO-COUNT-RECEIPT-2026-08-31.md .
docs/CORPUS-MEASUREMENT-2026-08-27.md:5:2,672 transcripts, 40 repos, 100 sessions.
docs/CORPUS-MEASUREMENT-2026-08-27.md:7:> **`40 repos` is wrong and is kept here as the record of it: the measured figure is 74.** This
```

Zero judge-facing surfaces still carry it. **Revert is one command:**

```
git revert 6bfdcf4      # "across 40 repositories" was never measured. It is 74.
```

That commit contains the `40`→`74` change and nothing else — tonight's other fixes (the
append-only correction, the chain-link guard) live in `a5ec00c` and are untouched by the revert.
Dry-run 2026-08-31: `git revert --no-commit 6bfdcf4` applied cleanly and restored `40` on all
four surfaces; the tree was then reset back.

Also corrected on the same pass: `THE-THESIS.md` no longer writes "78,618 across N repositories",
because the 78,618 span **1,157** working directories and only 75 of those are repository roots.
The 74 belongs to the 52,878, not to the 78,618. Attaching a count to the adjacent number instead
of its own is the error this product is named after, and the fix would have shipped it.
