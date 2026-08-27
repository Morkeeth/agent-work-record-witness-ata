# What 144,306 real agent messages say about claim-checking

**Result: we cannot publish a base rate yet, and the reason is the finding.**
Measured against `~/.trace/trace.db` — 144,306 messages, 2,672 transcripts, 40 repos, 100 sessions.
Denominator fixed in advance: [`CORPUS-PREREGISTRATION-2026-08-27.md`](CORPUS-PREREGISTRATION-2026-08-27.md).

## The number that looked like a headline

Running the shipped probe, `gate/outcome_gate.py::check_report`, over every assistant message whose
`cwd` is a git repo that still exists:

```
SHA  : 262 checkable · 110 disagree with the repo · 42.0%
PATH :  68 checkable ·  33 disagree with the repo · 48.5%
TEST : 357 claims, never scored — the gate refuses to run a command from a report
```

**"42% of agent commit claims are wrong" is a headline, and it is false.** It is two artifacts
stacked, and the pre-registration is the only reason it did not ship.

### Artifact one: the probe was aimed at the wrong repo

Every one of the 110 "disagreeing" SHAs was searched against all 88 git repos on this disk:

```
FOUND IN ANOTHER REPO (cwd is not where the commit landed): 74
FOUND NOWHERE ON DISK                                     : 36
```

**Two thirds of the failures are the agent being right and the probe looking in the wrong place.**
`cae8c30` and `863f5e6` are real commits in `rekt-capital`; `7b3256d`, `c4c628d`, `0eef89f` are real
in `helicon`; `da23d89`, `a727646`, `0b2f3f9` are real in `mountain-of-helicon`. The agent's `cwd`
is where it was standing, not where it committed — and an agent that `cd`s into a sibling repo, or
works across the `helicon` / `mountain-of-helicon` pair, breaks the assumption silently.

That alone takes the ceiling from 42% to **36/262 = 13.7%**. This is a defect in how the check
resolves a repo, and it is the same wrong-object failure the product is named after.

## What the claims actually were

A seeded random sample of 40 extracted SHA claims, hand-labelled by reading each context window:

| label | n | what it is |
|---|---:|---|
| **DONE** | **13** | the agent asserts it completed work at this sha — a real claim |
| CITE | 13 | *"Commit `7b3256d` landed on…"* — a commit cited as evidence, never claimed |
| META | 8 | a sha inside a shell command the agent was running (`echo "was b6ec7b4"`) |
| FIXTURE | 6 | test input — **including this product's own `deadbee`** |

**Artifact two — precision of the shipped extractor on free-form agent prose: 13/40 = 32%.**

Two thirds of what it flags are not claims at all. The regex requires only `commit|sha|as` within
24 characters of a hex token, which is exactly how a citation reads. And 15% of its hits are
**`deadbee`, this repo's own test fixture**, surfacing in transcripts about building the gate — the
extractor found its own fixture and would have counted it as a false agent claim.

Among the 13 hand-confirmed done-claims, 6 disagree with the repo. **n = 13. That is not a base
rate and it is not reported as one.**

## Why this matters more than the number would have

The product's pitch is *point it at what your agents say*. This is the first time it was pointed at
a real corpus rather than a PR body, and the result is a **domain-shift failure**: the extractor was
built for short first-person done-reports and it does not survive conversational prose. An
enterprise fleet's output is conversational prose.

**A gate with 32% precision is not a gate.** In a PR body it fires on the one paragraph that is a
claim; in a transcript it fires on everything that mentions a commit. Nobody had measured that,
because nobody had run it on anything but the artifact it was designed for.

## What the fix has to be

Not a better regex — the failure is structural. A citation and a claim are the same string; only
**speech act** separates them. Three directions, in cost order:

1. **Scope, not pattern.** Extract only from a designated report region (a PR body, a final
   `## Done` block), never from the whole message. Cheap, and it is how the gate is already used in
   CI — the corpus run is what proved the difference matters.
2. **Exclude the machinery.** Shell commands, fenced blocks and known fixtures are not claims.
   Mechanical, and it recovers 14 of the 27 false positives in the sample.
3. **Classify the speech act.** Needs a model, and the honest thing to say is that a claim/citation
   classifier would itself need a labelled set this machine does not have.

## Honest limits

- **n = 13** for the base rate. Any number quoted from it is a direction, not a measurement.
- **One operator, one machine.** Nothing generalises to a population.
- **Hand labels were assigned by the same agent writing this report.** That is the weakest link
  here; the sample and labels are committed so anyone can re-label them.
- **The base rate is an upper bound even so** — a rebased or garbage-collected commit reads as
  "not a commit" though the claim was true, and 3 of the 6 disagreements are merge SHAs from a
  rebase-and-merge flow.
- **The 42% was computed before the confounds were tested.** It is left in this document on
  purpose: deleting it would hide the one thing worth learning.
- **Both artifacts point the same way — toward a smaller number.** Not one of the corrections found
  more wrongness than the raw figure claimed, which is itself worth noticing: the naive measurement
  was biased against the agents, not for them.

*T4. Sample and labels: `/tmp/sample40_labelled.json`, committed alongside as `fixtures/corpus-sample-40.json`.*
