# The thesis

*One page. Pasteable into the Devpost long description. Every claim carries its evidence.*

---

## The primitive

Turn a sentence into a probe. Run the probe against the object. Refuse when you cannot.

That is the whole of it, and it is three operations, not one. The first two are the easy half:
you can turn "committed as `deadbee`" into `git cat-file -t deadbee` and get an answer.
The third is the half everyone skips. "All 14 tests pass" is also a sentence, and the only way
to check it is to run a command lifted out of agent prose — so this gate refuses. It says
UNVERIFIABLE and holds, rather than guessing. Run `./demo.sh` in a fresh clone with no account
and no network: the honest report passes with exit 0, the false one blocks with exit 1, and the
test claim is held with exit 2. The exit code is the verdict.

A checker that only ever says no is not a checker. A checker that says yes when it does not
know is worse. The refusal is the product.

## Why it has to be built at the record, not the check

The check is a moment. The question people actually ask arrives weeks later, from someone who
was not in the room: *what did the agent think it was doing?* The regulator asks for proof that
no agent shipped unverified code. The VP Eng asks after the incident. The CFO asks where the
10x went. Four buyers, four unrelated pressures, one missing artifact.

So the gate is the intake and the record is the product. A held claim in
THE AGENT WORK RECORD WITNESS opens back to the session that produced it — record
`H-a6151a95ac` carries `Trace · Claude Code session 01Lzbh4XPYTAgCKg1dciFS3Q`, and that join is
the thing no observability tool, no code reviewer and no compliance product holds, because none
of them keeps the transcript. Zenity governs actions. Norm Ai does content compliance. Qodo
reviews the diff. Langfuse scores the trace. Ask any of them what the agent believed before it
wrote the sentence and there is nothing to open.

## The first thing it measured was us

Before this was pointed at anyone else it was pointed at a month of our own agent output:
78,618 assistant messages out of 144,306 in the corpus, across 40 repositories. Both numbers
travel together, always, because a result quoted against the wrong denominator is precisely
what this catches.

The first pass said **41.7%** of commit claims disagreed with the repository. That number was
wrong and the error was ours: 73 of the 103 failures were real commits in a **sibling repository
on the same disk**, because an agent's recorded working directory is where it was standing, not
where it committed. Ten more were shas inside shell commands, six of them our own test fixture,
found in transcripts about building this gate. Corrected: **8.1%**, 19 of 236.

"42% of agent claims are wrong" was a real number from a real corpus and it was false by five
times. The only reason it never shipped is that the denominator was written down before anyone
looked. Neither figure is an incidence rate and neither is presented as one — hand-labelling put
extractor precision at 13 of 40 on conversational prose, and the labelled sample ships so you
can disagree with it.

That is the argument for the whole category, made against ourselves. A verification layer that
has never caught its own author is a verification layer nobody has tested.

## Refusal is the load-bearing part, and it is designed in

- The probe runs inside the customer's own checkout, where the repository already is. Only the
  verdict and a session pointer cross the network. This product never needs read access to code.
- The model explains a verdict and never overrules one. Gemini 3.5 through the ADK writes the
  paragraph a human reads under a HOLD; deterministic Python decides. Reverse those two and the
  gate becomes another thing that guesses fluently.
- The eligibility check for this very submission calls its three services instead of importing
  them, because v1 of that file checked `sys.modules` and reported 3 of 3 while the store was
  a local file and the agent had never been constructed. Today it prints **3 of 3 and exits 0**
  with credentials, and **1 of 3 and exits 1** on a fresh clone without them — deliberately, in
  public, because import is not call and credentials you do not have do not count.
- Nothing in the live record has ever cleared. `GET /audit` reads `pct_cleared_without_hold:
  0.0`. One real agent pull request went through the gate, went red on purpose, and is held.
  That is the honest state, not a broken demo.

## What this entry is the first instrument of

The same primitive has three surfaces, and only one of them is submitted here.

**Claims about work** — this entry. A sentence in a pull request, probed against the repository.
**Claims about a system** — an agent's `AGENTS.md` or `CLAUDE.md` says the code does X;
the code is the object; the verification is the same shape. That is Mountain of Helicon.
**Claims about authorship** — which turns in a transcript a human actually wrote, so that a
claim can be attributed before it is checked. That is Transcripto, drawn on the architecture
diagram outside the submission boundary and labelled roadmap, because it needs a corpus a judge
cannot verify.

One primitive, three objects: the repository, the system, the transcript. Nothing here is a
platform play. The layer only earns the name once the same probe-and-refuse discipline holds
across all three, and the honest position tonight is that it has been shipped against one.

## What is missing, said plainly

A single install by somebody who is not us. Zero. The 2026-08-27 foreign-repo run does not
count — we wrote the test organisation and scripted its pull requests, which proves the chain
and not adoption. `verify-claims` is advisory until branch protection requires it, and calling
it a required check today would be exactly the kind of sentence this product exists to catch.
Practice propagation on a field of two stays UNMEASURED_FOR_ORG_CLAIM.

And the open problem, which is the first contribution we are asking for: separating a citation
from a claim. "Committed as X" and "commit X landed" are the same string. Only the speech act
differs, and that is why precision on prose is 13 of 40. We shipped the two cheap halves —
scope to a declared report region, drop machinery — and refused to build a classifier, because
the labelled set does not exist and inventing one is the failure this product exists to catch.
