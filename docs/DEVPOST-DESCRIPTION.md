## Inspiration

I run a lot of coding agents. Overnight, in parallel, across a dozen repositories. I could see exactly what they cost me and I could not see whether anything they told me was true.

The moment it stopped being a vague worry: my own overnight fleet reported "done" on an eligibility check while the object disagreed. It had imported three services and called none of them, and the script printed 3 of 3. Nothing lied. A check simply verified something adjacent to the thing it claimed to verify, and every document downstream inherited the answer.

That is not an agent problem. That is a missing artifact. An agent's prose is a production surface that nobody governs, and once it scrolls past, nothing remembers it. Weeks later somebody who was not in the room asks what the agent thought it was doing, and there is nothing to open.

## What it does

You can see how many agent seats you bought. You cannot see what those agents actually did, or how much of what they reported was true.

THE AGENT WORK RECORD WITNESS is the system of record for agent work: who claimed what, whether the object agreed, who overrode a hold and the reason they typed, and the session behind each claim. Recorded when the report carried one, recorded as absent when it did not, and never invented.

The gate is how it gets installed and how the record fills. An agent-authored pull request hits a check. Each claim is turned into a probe and run against the object: `git cat-file` for a commit, `stat` for a path. Claims the object contradicts fail closed and land in the Hold queue. Humans only look when something is red. Break-glass is recorded with a typed reason. Auditors export the log.

The third operation is the one everybody skips. "All 14 tests pass" is also a sentence, and the only way to check it is to run a command lifted out of agent prose. So the gate refuses. It returns UNVERIFIABLE and holds, rather than guessing. A checker that only ever says no is not a checker. A checker that says yes when it does not know is worse.

The part nobody else can build is the join: a held claim opens back to the session that produced it. Zenity governs agent actions. Norm Ai does content compliance. Qodo reviews the diff. Langfuse scores the trace. None of them holds the transcript, so none of them can answer what happened before the claim was written.

Not observability. Not code review. Not a claims inbox.

## How we built it

- **Gemini 3.5 via Vertex AI**, exercised on the service path. The eligibility probe calls it rather than importing it.
- **Google ADK**, an LlmAgent constructed on the gateway and visible in `/health`.
- **Cloud Run** as the gateway service, **Firestore** as the record, **Secret Manager** holding the operator token so no revision ever stores it in plaintext.
- **GitHub Actions**, an agent-scoped workflow that posts to `/clearance`.
- Deterministic Python decides CLEAR or HOLD. Gemini writes the paragraph a human reads underneath. Reverse those two and the gate becomes another thing that guesses fluently.

The probe runs inside the customer's own checkout, where the repository already is. Only the verdict and a session pointer cross the network. This product never needs read access to your code.

`python3 contract/eligibility.py` calls all three services instead of importing them. With credentials it prints **3 OF 3 MET** and exits 0. On a fresh clone with none it prints **1 OF 3 MET** and exits 1, deliberately and in public, because import is not call and credentials you do not have do not count.

## Challenges we ran into

Pointed at a real corpus, the gate reported that **41.7%** of agent commit claims disagreed with the repository, 103 of 247. It is a wonderful number. It is the number you build a company slide around.

It was wrong, and the error was ours. The probe only ever asked the agent's recorded working directory, so a commit made in a sibling repository on the same disk read as a lie. 73 of the 103 failures evaporated once we asked the other repositories. Eleven more were machinery: a SHA inside a shell command the agent was running, or inside git output it was reading. Six of the hand-labelled sample were `deadbee`, this repository's own test fixture, surfacing in transcripts about building this gate. The tool for catching false claims found its own test data and would have counted it as an agent claim.

Corrected: **8.1%**, 19 of 236.

Building the control for that fix surfaced a second defect nobody was looking for. When an agent's recorded working directory no longer exists, the probe short-circuited to BLOCK before running at all. An agent was being called a liar by a check that never ran.

We caught ourselves with our own gate four times in one day. Every one of those catches came from opening the object, never from re-reading the note.

## Accomplishments that we're proud of

**The refusal.** UNVERIFIABLE is a first-class verdict with its own exit code, not an error path. A tool that reports false claims does not get to make one about itself.

**The first thing it measured was us.** A verification layer that has never caught its own author is a verification layer nobody has tested. The corrected number is in the product, the raw one is printed beside it rather than deleted, and the labelled sample ships so you can disagree with us.

**It runs cold.** Clone the public repository and run `./demo.sh`. No account, no network, no API key, no install. The honest report passes with exit 0, the false one blocks with exit 1, the test claim holds with exit 2. The exit code is the verdict.

**Nothing in the live record has ever cleared.** `GET /audit` reads `pct_cleared_without_hold: 0.0`. One real agent pull request went through the gate, went red on purpose, and is still held. We published that number rather than seeding the demo to look busier.

## What we learned

**Write the denominator down before you look at the numerator.** It is the only reason 41.7% is a story about a caught error instead of a story about a shipped one.

**A green check proves nothing until you have watched it go red.** Strip the input and confirm the probe fails before you trust it passing. A gate never watched fire is a claim, not a control.

**Import is not call.** Version one of our own eligibility script checked `sys.modules` and reported 3 of 3 while the store was a local file and the agent had never been constructed. It was correct about the wrong object.

**The position holding the most context is the one least able to check itself.** Every wrong number in this build came from a document being re-read rather than an object being opened, and every catch came from someone who had not read that document.

## What's next for THE AGENT WORK RECORD WITNESS

**Separate a citation from a claim.** "Commit X landed" and "Committed as X" are the same string. Only the speech act differs, and that is why precision on conversational prose is 13 of 40. We shipped the two cheap halves, scope to a declared report region and drop machinery, and refused to build a classifier because the labelled set does not exist and inventing one is the failure this product exists to catch. It is the first contribution we are asking for.

**One install by somebody who is not us.** Today, zero. We wrote the test organisation and scripted its pull requests, which proves the chain and not adoption.

**A GitHub App with Check Runs**, so install is one click and the check can honestly be called required. It is advisory today, and calling it required while branch protection is off would be exactly the kind of sentence this product exists to catch.

**Survival scoring per actor**: what share of an engineer's agent claims were still standing a month later. Then probes beyond SHA and path, for deploys, migrations and CI outcomes.
