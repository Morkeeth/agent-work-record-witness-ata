# eval/ — does our gate beat the two-hour version of itself?

Tests prove the code runs. This directory exists to answer the other question: **is the
outcome gate better than the obvious alternative any competent team would build in an
afternoon?** Until 2026-08-29 this repo had 306 test files and no eval. That is the gap.

Everything below the line "WHAT WOULD FALSIFY THIS" was written and committed **before the
harness was run once**. `git log --follow eval/README.md` is the receipt: the falsifiers
commit precedes the results commit. If you find the falsifiers were edited after the
numbers landed, the result is void — that is the point of putting them in git first.

---

## THE OBJECT — read this before quoting any number

This eval measures **a claim-checker's verdict accuracy on 40 hand-labelled extractions**.

It does **not** measure:

- how often agents are wrong (that is a base rate; `docs/CORPUS-MEASUREMENT-2026-08-27.md`
  explains at length why this machine cannot publish one, n = 13);
- how the gate behaves on a whole PR body (the unit here is a 200-character context
  window, see *Limits*);
- anything about a population. One operator, one machine, 40 items.

A number from this directory quoted as "X% of agent claims are wrong" is quoting it about
the wrong object.

## The corpus

`fixtures/corpus-sample-40.json`, at the repo root. Rows, labels, shas and context windows
are the ones committed on 2026-08-27; the only later edit is that repository **paths** in
`cwd` and in the context text were replaced by opaque labels — see *Pseudonymised repository
paths* below. It is a seeded random sample
of 40 SHA extractions drawn from 78,618 real assistant messages in `~/.trace/trace.db`, each
hand-labelled by reading its context window:

| label | n | what it is |
|---|---:|---|
| DONE | 13 | the agent asserts it completed work at this sha — a real claim |
| CITE | 13 | a commit cited as evidence, never claimed |
| META | 8 | a sha inside a shell command the agent was running |
| FIXTURE | 6 | test input, including this repo's own `deadbee` |

No new data was created for this eval. The labels are the ones already committed on
2026-08-27, and their weakest link is stated in the source document and repeated under
*Limits*: they were assigned by an agent, not by an independent human.

## The two arms

**ARM A — naive baseline.** `eval/arms.py::arm_a`. What a competent team ships in two
hours, frozen here so it cannot be tuned after the fact:

- regex `\b[0-9a-f]{7,40}\b` for SHA-shaped tokens, kept only when one of
  `commit|committed|sha|landed|pushed|merged|as` appears within the preceding 40
  characters (without this filter the baseline flags every hex token and is strictly
  worse — the baseline is given its best honest form, not a strawman);
- regex for path-shaped tokens after `wrote|added|created|updated`;
- existence check **in the recorded `cwd` only**: no sibling-repo search, no
  known-fixture list, no claim-type discrimination;
- **no refusal category.** Every token it extracts gets a PASS or a BLOCK. That is the
  design difference under test.

**ARM B — ours.** `gate/outcome_gate.py::check_report`, **unmodified**, called the way the
shipped corpus reader calls it (`gate/corpus_scan.py`, CORRECTED pass):

```python
check_report(ctx, repo=cwd, sibling_repos=<the 82 repos>, exclude_fixtures=True)
```

`exclude_fixtures=True` is not a knob invented for this eval: the docstring in
`outcome_gate.py` says it is opt-in and "skipped only when a caller says it is reading a
corpus", and this is a corpus. The pure-defaults configuration is reported anyway, as
ablation **B0**, because a reader is entitled to see what the gate does with no flags at all.

## Ground truth

Per item, from the committed hand label plus a **frozen** existence oracle
(`eval/fixtures/sha_oracle.json`, built once on this machine by `eval/build_oracle.py`,
which records what `git cat-file -t <sha>` actually returned in every repo probed):

| hand label | oracle | gold verdict |
|---|---|---|
| DONE | the sha is a commit in the `cwd` or in any repo on disk | **PASS** |
| DONE | the sha is a commit nowhere on disk | **BLOCK** |
| CITE / META / FIXTURE | — | **NO_CLAIM** (this was never an agent's done-claim) |

## The metric, and why refusal is scored

An arm returns one of four things for an item: `PASS`, `BLOCK`, `REFUSE` (an explicit
UNVERIFIABLE finding), or `SILENT` (it never flagged this token). The scoring matrix lives in
`eval/arms.py::score_item` with this rationale beside it:

| gold | correct answers | zero | penalised |
|---|---|---|---|
| PASS | `PASS` | `REFUSE`, `SILENT` | `BLOCK` — a false accusation on a good PR |
| BLOCK | `BLOCK` | `REFUSE`, `SILENT` | `PASS` — a false claim waved through |
| NO_CLAIM | `REFUSE`, `SILENT` | — | `PASS`, `BLOCK` — adjudicating something nobody claimed |

**Why refusal earns credit where it does.** Our differentiator is that the gate returns
UNVERIFIABLE instead of guessing. A metric where abstaining is free everywhere would let an
arm refuse all 40 items and score 100%, so abstention is **never** rewarded on a real claim —
there it scores zero, exactly like a wrong answer, and is reported separately as an
abstention rather than as a false accusation. It is rewarded only where silence is the
correct answer: on the 27 items that were never claims. An arm with no refusal category has
to guess on those 27, and a wrong guess is penalised. That asymmetry is the hypothesis under
test, not a thumb on the scale.

Four numbers per arm, all reported, none suppressed:

1. **Accuracy** = correct / 40, with a **95% Wilson interval** (n is small; a bare point
   estimate here would be dishonest).
2. **False-accusation rate** = `BLOCK` where gold is not `BLOCK`, / 40, Wilson interval.
   Refusal is never a false accusation. Lower is better.
3. **Missed false claims** = `PASS` where gold is `BLOCK`.
4. **Penalised score** = mean of (+1 correct, 0 abstained, −1 wrong answer).

Paired comparison: **exact two-sided McNemar** on per-item correctness (the arms see
identical items, so the paired test is the right one).

## Reproduce

```
env -i /usr/bin/python3 eval/run_eval.py
```

No network, no API key, no `$HOME`, stdlib only, deterministic. The oracle is frozen JSON,
so the run does not touch git or the filesystem outside this repo. `eval/build_oracle.py`
is the machine-bound step that produced that JSON; it is **not** needed to reproduce the
table, only to rebuild the oracle on a machine that has those 82 repos.

Outputs: `eval/out/results.json` (every item, row by row: mid, sha, label, gold, each arm's
verdict) and `eval/out/equivalence.txt` (the receipt that arm B run against the frozen
oracle returns byte-identical verdicts to arm B run against live git on this machine — proof
the oracle substituted an *effect*, never a rule).

## Pseudonymised repository paths

Every repository path in `eval/fixtures/sha_oracle.json`, `eval/out/results.json`,
`eval/out/equivalence.txt` and `fixtures/corpus-sample-40.json` is an **opaque label** —
`/code/repo-01` … `/code/repo-82` — and not a real directory. This repository is public. The
real ones are 82 repositories on one laptop, most of them private, and shipping the oracle
keyed by absolute paths would have published that inventory and the home-directory layout
around it as a side effect of publishing an eval.

**What was mapped.** One label per repository, assigned once in the frozen `sibling_repos`
order and applied to *every* key and value: the `<repo> ||| <command>` probe keys, the
`code_root`, the `sibling_repos` list, `sibling_resolution_receipts.recorded_cwd` and
`.resolved_in`, the per-item `evidence` strings, the corpus `cwd` field, and the `~/CODE/…`
paths that appear inside the recorded transcript text. Additionally, the commit **subject**
in each `git_log_1` receipt is replaced by a `sha256:` commitment of that subject: those
subjects are private-repo content, one of them personal, and a commitment keeps the
redaction checkable instead of turning it into a rewrite.

**What was NOT changed.** The separator (`" ||| "`), the probe command strings, the recorded
stdout and return codes, the number of entries (1,091 git probes, 82 siblings, 11 receipts),
the shas, the hand labels, the context text apart from those path substitutions, the
gold rule, the scoring matrix, and
`gate/outcome_gate.py`. The mapping is one-to-one and order-preserving, so the sibling search
visits the same repositories in the same order and stops at the same one.

**The table is deliberately not shipped.** It lives outside the repo at
`~/.claude/ata-eval-repo-map.json` (override with `$ATA_EVAL_REPO_MAP`), mode 0600, and it
holds both directions plus the plaintext of the redacted subjects. Committing it — or
committing anything derived from it — would undo the redaction in one step, which is exactly
why the labels are sequential and carry no information about the name they replace. Nothing
in the offline run reads it: the corpus carries labels and the oracle is keyed by labels, so
`run_eval.py` resolves every key with no table present. Only `eval/build_oracle.py`, the
machine-bound recorder, loads it — it translates label → real directory immediately before a
live probe and keys the result by the label (`eval/oracle.py`, the `realpath` hook). A
rebuild without the table therefore fails loudly rather than recording 82 missing-directory
probes as if they were observations.

**The equivalence receipt still holds.** `eval/out/equivalence.txt` records 40/40 identical
verdicts between arm B against live git and arm B against the frozen oracle, measured on
2026-08-29 before this renaming; the renaming touched no recorded effect, so the receipt is
still a receipt about the same recording. The check that this is true is the run itself:
after pseudonymisation the whole table reproduces unchanged — arm A 22.5%, arm B 45.0%, the
always-silent null 67.5%, B0 defaults 25.0%, exact McNemar b=0 c=9 p=0.0039, negative control
0/200, sensitivity 25.7% vs 37.1%, no falsifier fired — and a field-by-field diff of
`results.json` before against after, with paths mapped forward, is empty. A redaction that
moved a number would be a redaction that broke the experiment.

---

## WHAT WOULD FALSIFY THIS

Written 2026-08-29, before the first run. Any of these means we did not show what we set out
to show, and it gets reported in the table and in the summary, not quietly dropped.

1. **No win.** If arm B's accuracy 95% Wilson interval overlaps or sits below arm A's point
   estimate, we do not claim the gate beats the baseline. n = 40 and the intervals are wide;
   this is the likely failure mode and it will be stated plainly.
2. **No paired difference.** If the exact McNemar p ≥ 0.05, we report "no significant paired
   difference" and do not describe the gap as a result.
3. **The edge is a collision artifact.** Arm B's advantage is expected to come largely from
   sibling-repo resolution — searching 82 repos for a 7-hex prefix. A 7-hex prefix is 1 in
   268,435,456, so across ~10^5 commits on this disk the a-priori chance of a spurious hit is
   ~0.04%; but that reasoning is not a measurement. **Negative control, pre-registered:** 200
   seeded random 7-hex strings are probed through the identical 82-repo search. **If ≥ 5% of
   them resolve, sibling-based PASSes are noise-dominated**, every sibling-resolved item is
   discounted, and arm B's edge is reported as unsupported.
4. **Gold is circular.** If arm B's advantage disappears when sibling-resolved DONE items are
   excluded from the gold set entirely (reported as a sensitivity row), the metric was
   defining the answer in our favour and the headline is withdrawn.
5. **The baseline was crippled.** If arm A can be improved by a change that takes under two
   hours and that a competent engineer would obviously make, the baseline was a strawman. Its
   rule is frozen above so this is checkable by anyone reading it.

## Limits, stated up front

- **n = 40; 13 real claims.** Every interval here is wide and none of it generalises.
- **The unit is a 200-character context window, not a message.** Fenced blocks and
  shell-command lines are cut by the window, so arm B's machinery-stripping under-fires
  compared with how it behaves on a whole message. Arm B's discrimination here is therefore a
  **lower bound** on its full-message behaviour — which is a limit that works against us, and
  it is not corrected for. Rerunning on whole messages would need `~/.trace/trace.db`, which
  is personal data and does not enter this repo.
- **The hand labels were assigned by an agent**, the same one that wrote the measurement
  document. That is the weakest link in the whole chain. The labels are committed so anyone
  can re-label them and rerun.
- **Existence is survivorship-biased.** A rebased or garbage-collected commit reads as
  "not a commit" although the claim was true when made, which pushes gold toward BLOCK. Three
  of the six cwd-level disagreements are known to be merge SHAs from a rebase-and-merge flow.
- **A sibling match is not proof the agent meant that repo.** Falsifier 3 bounds the risk; it
  does not eliminate it. The oracle records `git log -1` for each sibling-resolved DONE sha so
  a human can read the commit message and judge for themselves.
- **Path claims are extracted by both arms and scored by neither.** The corpus is SHA-only, so
  there are no path labels. Path findings are counted in `results.json` and left unscored.
- **Test-claim refusals are counted, never scored** — the same rule as the pre-registration.
  The corpus contains no labelled test claims.

---

## WHAT THE RUN FOUND — appended 2026-08-29, after the run

**Nothing above this line was edited after the run.** `git diff <falsifiers-commit>..HEAD --
eval/README.md` is append-only, and the harness commit precedes the results commit.

Reproduce: `env -i /usr/bin/python3 eval/run_eval.py`

```
arm                accuracy (95% Wilson)   false accusations   miss  abst    pen  discrim adjud
NULL always-silent 27/40  67.5% [52.0,79.9]  0/40   0.0%          0    13  +0.68  27/27    0/13
A naive baseline    9/40  22.5% [12.3,37.5] 18/40  45.0%          0     1  -0.53   2/27    7/13
B (headline)       18/40  45.0% [30.7,60.2]  2/40   5.0%          0     1  -0.07   6/27   12/13
B0 defaults        10/40  25.0% [14.2,40.2] 17/40  42.5%          0     1  -0.47   3/27    7/13
B siblings only    15/40  37.5% [24.2,53.0]  5/40  12.5%          0     1  -0.23   3/27   12/13
B fixtures only    13/40  32.5% [20.1,48.0] 14/40  35.0%          0     1  -0.33   6/27    7/13
B + scope          27/40  67.5% [52.0,79.9]  0/40   0.0%          0    13  +0.68  27/27    0/13
```

Exact McNemar, A vs B: b=0, c=9, 9 discordant pairs, **p = 0.0039**. Every one of the nine
items the arms disagreed on went B's way; none went A's way.

**No pre-registered falsifier fired.** Arm B beats arm A: accuracy 45.0% vs 22.5% with the
lower bound of B's interval (30.7%) above A's point estimate (falsifier 1 survived), a
significant paired difference (falsifier 2 survived), and the win holds when every
sibling-resolved gold row is dropped — 37.1% vs 25.7% on the remaining 35 (falsifier 4
survived). The negative control returned **0 of 200** random 7-hex strings resolving anywhere
in the 82-repo search, so the sibling matches are not collisions (falsifier 3 survived; the
a-priori estimate of ~0.04% was right).

### The uncomfortable half, which matters more than the win

**A trivial arm that says nothing scores 67.5% and beats both real arms on the metric this
directory pre-registered.** 27 of the 40 rows are not claims, silence is the correct answer on
all 27, and an arm that abstains everywhere collects them for free. That is a defect in *my*
metric, found by this eval's own ablation (`B + scope` is that arm in practice), and it is
disclosed here rather than repaired by swapping in a metric where we look better. Two things
were added to the harness after the run — the `NULL always-silent` row and the
discrimination/adjudication split — and **both of them make the result look worse**. The
pre-registered scoring itself is unchanged.

What the split shows, and it is the real finding:

- **Adjudication — the 13 rows that were real claims: B 12/13, A 7/13.** This is where the
  product earns its keep. Arm A wrongly BLOCKs five true done-claims because it looks only in
  the recorded `cwd`; arm B finds those commits in a sibling repo and passes them. That is the
  documented repo-resolution fix, measured against an alternative for the first time.
- **False accusations — B 2/40 (5.0%) vs A 18/40 (45.0%).** A gate that calls an honest agent
  a liar 45% of the time is unusable regardless of its accuracy. This is the number to quote.
- **Discrimination — the 27 rows nobody claimed: B 6/27, A 2/27.** Both are bad. Ours is
  three times less bad and still bad. **The gate cannot tell a claim from a citation**, which
  is exactly what `docs/CORPUS-MEASUREMENT-2026-08-27.md` said in prose (32% extractor
  precision) and what this eval now says with a control arm beside it. The ablation locates it
  precisely: `B0 defaults` scores 25.0% — statistically indistinguishable from the two-hour
  baseline. **Shipped defaults ≈ naive regex.** The entire measured advantage comes from two
  opt-in arguments, `sibling_repos` and `exclude_fixtures`, which only the corpus reader
  passes.

### What this does not show

- **gold BLOCK n = 1.** Twelve of the thirteen real claims were true. The headline capability —
  catching a false done-claim — is therefore effectively **untested** here: every arm scores
  0 missed false claims out of a single opportunity. Do not read "miss = 0" as evidence of
  anything. A corpus with more false claims is the single highest-value thing to build next.
- **`B + scope` is degenerate on this corpus, not good.** It abstains on all 13 real claims;
  its 67.5% is the null model wearing our name. Scoping to a declared report section cannot
  work on a 200-character window that contains no headings, which is why the README above
  flagged it as measuring the window rather than the gate.
- The limits listed before the run all still stand, unrevised.
- **Read the sibling receipts before you believe the sibling fix.** They are in
  `eval/out/results.json` under `sibling_resolution_receipts`, with `git log -1` for each. The
  strongest is `a99ac61ed43ff6c92615f8796bbbdc1ff57ea2bf` — 40 hex characters, a collision is
  not physically plausible. The weakest is `2b2d68f`, claimed while standing in `zup` and
  resolved to a `mountain-of-helicon` commit; that is cross-repo work if you believe the commit
  message and a mislabel if you do not. Falsifier 4 exists because of rows like it, and the
  win survives dropping every one of them.
