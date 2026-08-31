## Inspiration

Software just changed hands. Most of the code being written this year is written by agents, and the constraint moved with it: writing is cheap now, and **knowing what was actually done is the expensive part**. Every company can tell you how many agent seats it bought and how many tokens burned. Not one can tell you what those agents did, or how much of what they reported was true.

That gap has no artifact. There is no equivalent of the audit log, the flight recorder, the lab notebook. An agent finishes, writes a paragraph about what it did, and that paragraph gets read by an auto-merge rule and then scrolls away forever. It is a production surface that nobody governs and nothing remembers.

The moment it stopped being abstract for me: my own overnight fleet reported "done" on an eligibility check while the object disagreed. It had imported three services and called none of them, and the script printed 3 of 3. Nothing lied. A check verified something *adjacent* to the thing it claimed to verify, and every document downstream inherited the answer.

Within five years, "what fraction of our merged code carries a claim nobody checked?" will be a question a board asks and an insurer prices. Today no company on earth can answer it.

## What it does

**THE AGENT WORK RECORD WITNESS is the system of record for agent work.** Who claimed what, whether the object agreed, who overrode a hold and the reason they typed, and the session behind every entry.

The primitive is three operations: **turn a sentence into a probe, run the probe against the object, and refuse when you cannot.**

An agent-authored pull request hits a check. Each claim becomes a probe run against the thing it is about. `git cat-file` for a commit, `stat` for a path. Claims the object contradicts fail closed and land in the Hold queue. Humans look only when something is red. Break-glass is recorded with a typed reason. Auditors export the log.

The third operation is the one everyone skips. "All 14 tests pass" is also a sentence, and the only way to check it is to run a command lifted out of agent prose. So the gate refuses: UNVERIFIABLE, and it holds. **A checker that only ever says no is not a checker. A checker that says yes when it does not know is worse.** The refusal is the product.

And the part nobody else can build is the join: **a held claim opens back to the session that produced it.** Zenity governs agent actions. Norm Ai does content compliance. Qodo reviews the diff. Langfuse scores the trace. None of them holds the transcript, so none can answer what the agent believed before it wrote the sentence.

One primitive, three objects. Claims about **work**: a sentence in a pull request, probed against the repository. That is this entry. Claims about a **system**: an AGENTS.md says the code does X, and the code is the object. Claims about **authorship**: which turns in a transcript a human actually wrote. Same shape, three surfaces. The layer earns its name when the discipline holds across all three.

Not observability. Not code review. Not a claims inbox.

## How we built it

- **Gemini 3.5 via Vertex AI**, exercised on the service path. The eligibility probe calls it rather than importing it.
- **Google ADK**, an LlmAgent constructed on the gateway and visible in `/health`.
- **Cloud Run** as the gateway, **Firestore** as the record, **Secret Manager** holding the operator token so no revision ever stores it in plaintext.
- **GitHub Actions**, an agent-scoped workflow posting to `/clearance`.
- Deterministic Python decides CLEAR or HOLD. **Gemini writes the paragraph a human reads underneath, and never overrules a probe.** Reverse those two and the gate becomes another thing that guesses fluently.

The architecture is the moat, not the model. The probe runs **inside the customer's own checkout**, where the repository already is. Only the verdict and a session pointer cross the network. This product never needs read access to your code, which is what makes it installable at a bank.

`python3 contract/eligibility.py` calls all three services instead of importing them. With credentials it prints **3 OF 3 MET**, exit 0. On a fresh clone with none it prints **1 OF 3 MET**, exit 1. Deliberately, in public, because import is not call.

## Challenges we ran into

Pointed at a real corpus, the gate reported **41.7%** of agent commit claims disagreed with the repository, 103 of 247. It is a wonderful number. It is the number you build a company slide around.

It was wrong, and the error was ours. The probe only asked the agent's recorded working directory, so a commit made in a sibling repository read as a lie. 73 of 103 failures evaporated once we asked the other repositories. Eleven more were machinery. Six were our own test fixture, surfacing in transcripts about building this gate. The tool for catching false claims found its own test data and would have counted it.

Corrected: **8.1%**, 19 of 236.

Building the control surfaced a second defect nobody was looking for: when an agent's recorded working directory no longer exists, the probe short-circuited to BLOCK before running. **An agent was being called a liar by a check that never ran.**

It happened again on the final day. Wiring in a second explainer, we concluded across eight configurations that the model could not do the job. Then one control overturned it: same model, same prompt, a different transport, and it worked first try in half a second. The conclusion had been correct about the wrong object.

**Twice in one week, on the people building the checker.** That is the finding. It is not that agents lie. It is that **verification is where the errors live**, and the first thing that checks will be wrong too. Which is precisely why it has to be able to catch itself.

## Accomplishments that we're proud of

**The refusal.** UNVERIFIABLE is a first-class verdict with its own exit code, not an error path. A tool that reports false claims does not get to make one about itself.

**The first thing it measured was us.** A verification layer that has never caught its own author is a verification layer nobody has tested. The corrected number is in the product, the raw one printed beside it rather than deleted, and the labelled sample ships so you can disagree.

**It runs cold.** Clone the public repository, run `./demo.sh`. No account, no network, no key, no install. Honest report passes exit 0, false one blocks exit 1, test claim holds exit 2. The exit code is the verdict.

**Nothing in the live record has ever cleared.** `pct_cleared_without_hold: 0.0`. One real agent pull request went through, went red on purpose, and is still held. We published that rather than seeding the demo to look busier.

## What we learned

**Write the denominator down before you look at the numerator.** It is the single reason 41.7% is a story about a caught error instead of a shipped one.

**A green check proves nothing until you have watched it go red.** A gate never watched fire is a claim, not a control.

**Import is not call.** Our own v1 checked `sys.modules` and reported 3 of 3 while the agent had never been constructed. Correct about the wrong object.

**The position holding the most context is the one least able to check itself.** Every wrong number here came from a document re-read rather than an object opened.

## What's next for THE AGENT WORK RECORD WITNESS

**Make the record priceable.** Hash-chain and sign each entry so the export is evidence rather than JSON, and it produces one number: **verified-merge rate**, the share of agent-authored merges carrying a passing probe. That is a KPI a CTO reports to a board and an insurer can underwrite. It is the business.

**Own the labelled set.** Separating a citation from a claim is the open problem. "Commit X landed" and "Committed as X" are the same string, and only the speech act differs, which is why precision on prose is 13 of 40. No labelled corpus for this exists. Building it is the moat; we refused to invent a classifier without one, because that is the failure this product is named after. **It is the first contribution we are asking for.**

**A probe registry.** Two probes today. The list is obvious: CI outcome, deploy landed, migration applied, ticket closed, dependency added. Each probe is a small contract anyone can contribute. That is how this stops being a tool and becomes a standard.

**A GitHub App with Check Runs**, so install is one click and the check can honestly be called required. It is advisory today, and saying otherwise would be exactly the sentence this product exists to catch.

**And the one that matters most. One install by somebody who is not us.** Today, zero. Every number above gets more valuable and more falsifiable the moment a stranger's repository starts producing rows.
