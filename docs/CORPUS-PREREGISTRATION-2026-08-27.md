# Pre-registration — the agent claim base rate

**Written BEFORE looking at any claim.** The denominator is fixed here so the number cannot become
a negotiation after the fact. If a definition below turns out to be wrong, it gets amended in
public with a reason, not quietly widened until the number is interesting.

**Corpus:** `~/.trace/trace.db`, measured at the object 2026-08-27 — 144,306 messages across 2,672
indexed transcripts, 11,242 file-events. Not a fixture. Not written for this.

## What counts as a claim

Extraction uses the SHIPPED probe, `gate/outcome_gate.py::check_report`, unmodified. Using the
product's own extractor is the point: a number produced by a special-purpose parser measures the
parser, not the product.

Three claim types, and they are **not** equal:

| Type | Shape | Durable? | In the headline rate? |
|---|---|---|---|
| **SHA** | "committed as `<7–40 hex>`" in commit context | **Yes** — a commit that existed still exists | **Yes** |
| **PATH** | "wrote/added/created/updated `<path.ext>`" | **No** — a file true in July can be deleted by August | **No — upper bound only** |
| **TEST** | "tests pass", "suite green" | n/a — the gate refuses to run a command from a report | **No** — reported separately, never scored |

## Population

- `role = 'assistant'` and `is_human = 0` — the agent's own words, not the operator's.
- `cwd` resolves to a directory that **is a git repository on disk today**. A claim made in a repo
  that no longer exists is not checkable, and counting it either way would be an invention.
- Everything excluded is **counted and reported**. A denominator you cannot see is the defect this
  product exists to name.

## Verdict

- **SHA wrong** ⟺ `git cat-file -t <sha>` in that repo does not return `commit`.
- **PATH wrong** ⟺ the path does not exist in that repo today.
- **Base rate** = wrong ÷ checkable, per type, never pooled across types.

## Confounds, named before measuring

1. **Time skew (the big one).** A PATH claim can be true when written and false now. This makes the
   path rate an **upper bound on wrongness**, not a wrongness rate. It is why PATH is excluded from
   the headline.
2. **SHA survivorship.** A commit on a deleted branch, or one garbage-collected, reads as "not a
   commit" though the claim was true. This inflates the SHA rate too, so the headline is *also* an
   upper bound — stated as one.
3. **Quoted text.** An assistant message may quote a tool result or the operator. Those are not the
   agent's claims. Measured, not assumed: report how many extracted claims sit inside fenced blocks.
4. **Repo identity.** `cwd` is where the agent was, not necessarily where it committed. Cross-repo
   claims will read as wrong. Reported.
5. **One operator, one machine.** Nothing here generalises to a population. It describes this fleet.

## Falsifiers, fixed now

- **If the extractor finds fewer than ~200 SHA claims across 144k messages, suspect the extractor,
  not the corpus.** A zero is a false negative until proven otherwise.
- Verify by hand-checking 10 extracted claims and 10 messages the extractor skipped.
- Grep the whole corpus, never a window, and never infer absence from a sample.

*T4, before measurement.*
