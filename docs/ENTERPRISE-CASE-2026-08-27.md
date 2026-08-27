# What an enterprise actually gets

**Every number and every block of output on this page was produced by running the command above it.**
Nothing here is illustrative.

---

## 1. The question an enterprise asks

Not *"does the gate work"* — it does, on a PR body, and that is easy to show. The question is
**"what does my fleet look like after a month of this."**

We could not answer that honestly until we pointed the product at a month of real fleet output.
So we did, and the first thing it found was our own defect.

## 2. Pointed at 78,618 real agent messages

```
$ python3 gate/corpus_scan.py --db ~/.trace/trace.db --code-root ~/CODE

  78,618 messages examined, of 144,306 in the corpus · 83 repos on disk
  filter: role='assistant' and is_human=0 and text is not null and length(text) > 20
  52,878 of those were written in a directory that is still a git repo today

  RAW          247 sha claims ·  103 disagree · 41.7%
  CORRECTED    236 sha claims ·   19 disagree · 8.1%

      11 dropped — shell commands, fenced output, and this repo's own test fixtures
      73 resolved in a SIBLING repo — the agent was right, the probe was aimed at the wrong repo
       5 path claims dropped — a code identifier, not a file
       1 path claims dropped — a hostname, not a repository path
       1 path claims dropped — an absolute path outside the repository
```

**41.7% → 8.1%.** The gap is the product of this lane, and it was entirely our error, not the
agents'.

- **73 of 103** "wrong" commit claims were **real commits in another repo on the same disk**.
  `cae8c30` is real in `rekt-capital`. `7b3256d` is real in `helicon`. `da23d89` is real in
  `mountain-of-helicon`. An agent's `cwd` is where it was standing, not where it committed — and
  the check was aimed at the wrong object, which is the exact failure this product is named after.
- **7 path claims were never checkable at all** — `github.com`, `/tmp/harness.html`, and code
  identifiers a probe read as filenames: the database column `task_runs.run_id`, the attribute
  `oracle.signing.digest`, the method call `_INDEX_OK.pop`. The probe was right and the claim was
  never a claim. **Each is counted with its reason rather than silently deleted** — a filter that
  quietly shrinks a finding list is the flattering version, and the refusal is the product.
- **11** were machinery: a SHA inside a shell command the agent was *running*, or inside fenced
  git output it was *reading*. And six of those, across the sample, were **`deadbee` — this repo's
  own test fixture**, surfacing in transcripts about building this gate. The tool for catching false
  claims about work counted its own test data as agent claims.

### The number we did not ship, and why

**Two of those were our own staged demo strings.** `docs/auth-migration-2026.md` is the literal
false-done text in `cloud/service.py` and `fixtures/agent-false-done-PR-BODY.md`, and `abc1234` is
the placeholder in `gate/outcome_gate.py`. They reach a corpus because real messages discuss the
demo while it is being built, so a judge who greps the repo would find our tool reporting **our own
seed text as a caught claim**. Excluded on the corpus path, and still blocking in the product's own
demo where they are deliberately false.

**Two rows are left in and unprobed on purpose.** `wrote _jed.py` and `wrote needs.ts` survive every
filter and nobody has checked them. They stay listed and labelled unprobed rather than guessed in
either direction.

**"42% of agent commit claims are wrong" was a real number from a real corpus and it was false by
5x.** It survives in [`CORPUS-MEASUREMENT-2026-08-27.md`](CORPUS-MEASUREMENT-2026-08-27.md) on
purpose.

The only reason it did not become a slide is that the denominator was written down **before anyone
looked at a claim** — [`CORPUS-PREREGISTRATION-2026-08-27.md`](CORPUS-PREREGISTRATION-2026-08-27.md)
fixes what counts as a claim, which claim types can carry a headline, and five named confounds,
including the one that turned out to matter. **That document is the method, and the method is the
product.** A vendor who shows you a number without one is showing you a negotiation.

### What this page will not tell you

**8.4% is not an incidence rate and neither was 41.7%.** Hand-labelling a seeded random sample of 40
extractions put the extractor's precision on conversational prose at **13/40** — the rest were
citations (*"Commit 7b3256d landed on…"*), shell commands, and fixtures. Of those 13 real claims, 6
disagreed with the repo. **n = 13.** That is a direction, not a measurement, and no number on this
page is presented as your fleet's error rate. The sample and its labels ship in
`fixtures/corpus-sample-40.json` so you can re-label them and disagree.

## 3. The same gate, on the artifact it was built for

A test company, `northwind-parcel`, with its own history and tests. An agent opens a PR whose
done-report claims a commit that does not exist, a file that nearly exists, and a test run that
never happened.

```
$ python3 gate/outcome_gate.py --json < pr-body.md
gate: BLOCK exit_hint 1
   BLOCK         committed as a41c9f2                NOT a commit in this repo (no sibling repos checked)
   PASS          wrote src/northwind/cache.py        exists
   BLOCK         wrote src/northwind/validators.py   NO SUCH PATH in the repo
   UNVERIFIABLE  tests pass                          a test claim needs the suite RUN; this gate never
                                                     executes a command lifted from a report

gateway: H-03fe9c5e10 HOLD/BLOCK traceable=True session=01MS5iomniNWozqMjFTkLfUz
```

The one true claim in a false report still passes. The test claim is **refused, not guessed** — the
gate never runs a command that came out of a report. The hold opens back to the session that
produced it.

**Disclosure, unchanged from the first run and not buried:** we wrote Northwind and we scripted its
PRs. Installs by a person who is not the author: **zero**. What that run proves is the chain — the
product installs into a foreign repo, holds a false claim at exit 1, clears a true one at exit 0.
It does not prove adoption. See [`TESTCO-RUN-2026-08-27.md`](TESTCO-RUN-2026-08-27.md).

## 4. Install it

```yaml
- uses: Morkeeth/hack-fleet-ata@main
  with:
    pr-body:    ${{ github.event.pull_request.body }}
    policy-url: ${{ vars.HOLD_POLICY_URL }}
    api-token:  ${{ secrets.HOLD_API_TOKEN }}
```

Twelve lines, nothing vendored. With no gateway configured the probe still runs and still fails the
check on a false claim; you get the gate and nothing accumulates.

## 5. Where to contribute

The corpus run is an invitation, not a result. Three things are open and each is a real gap we can
name precisely:

1. **Run `corpus_scan.py` on your own corpus and post the two numbers.** Ours is one operator on one
   machine; nothing here generalises to a population, and one second machine changes that.
2. **Re-label `fixtures/corpus-sample-40.json`.** Our labels were assigned by the same agent that
   wrote the report — the weakest link on this page, and the cheapest one to fix.
3. **Separate a citation from a claim.** *"Commit X landed"* and *"Committed as X"* are the same
   string; only the speech act differs. We shipped the two cheap halves — scope to a declared report
   region, exclude machinery — and deliberately did **not** build a classifier, because the labelled
   set does not exist and inventing one is the failure this product exists to catch.

*T4, 2026-08-27. Local. Nothing published.*
