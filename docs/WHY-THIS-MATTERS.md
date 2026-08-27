# Why this matters, four times over

*2026-08-27. The EU AI Act story was carrying the whole pitch alone, which made this look like
a compliance tool. It is not. Four different people are asking the same unanswerable question
for four unrelated reasons, and only one of them is a regulator.*

**The question, in its plainest form:**

> **Your agents did work. How do you know they did it?**

Nobody can answer. Not because the tooling is immature, but because **the sentence an agent
writes about its work and the work itself have never been connected.** Spend dashboards count
tokens. Trace tools score reasoning. Diff review reads code. None of them checks a claim against
the object.

---

## 1 · The regulator. Forced, dated, and already on a slide.

**Who:** whoever signs the compliance attestation.
**The force:** the EU AI Act, and SOC 2 auditors who have started asking.
**Their sentence:** *"Prove no agent shipped unverified code to production."*

This one is not speculative and it is not sold, it is **required**. The date is on a calendar
and the fine is on a schedule. What makes it a product rather than a checkbox is that **there is
no artifact to hand over.** Not a bad artifact. None. The honest current answer is a spend graph
and the word of four hundred engineers.

**Why we win it:** an append-only record of every claim, whether the object agreed, every
override with the reason someone typed, and a link to the run behind each entry. That is a
document, and a document is what an auditor takes.

**Weakness, stated:** compliance buyers move slowly and buy from incumbents. This story opens
doors; it does not close deals fast.

---

## 2 · The incident. It already happened, twice, in public.

**Who:** the VP Eng writing the postmortem at 2am.
**The force:** it has occurred and it will occur again.
**Their sentence:** *"What did the agent think it was doing?"*

Our own PRD cites two: **an agent deleted a production database at Replit**, and **Amazon's Kiro
tore down a CloudFormation stack.** (Sourced from `docs/COMPANY.md`; treat as RELAYED until
re-verified before any public claim.)

The postmortem is the point. After a human incident you read the commits, the tickets, the Slack.
**After an agent incident you have the diff and nothing else.** You cannot reconstruct what it
believed it was doing, what it claimed afterwards, or whether anyone checked. The trail stops at
the artifact.

**Why we win it:** a held claim opens back to the session that produced it. **The postmortem
becomes readable.** That is the one capability no CI product can copy, structurally, because
none of them holds the transcript.

**This is the strongest story and it should probably open the pitch**, because it is a fear
everyone already has and nobody has articulated.

---

## 3 · The CFO. The productivity case is unproven in both directions.

**Who:** whoever signed for four hundred seats.
**The force:** money, and a renewal date.
**Their sentence:** *"We bought 10x. Where did it go?"*

The bottleneck inverted. Code became 5 to 10x faster to write, so **verification before merge
became the constraint instead of generation.** If engineers cannot trust an agent's "done", they
re-verify by hand, and the speed they bought is paid straight back in review time.

**Nobody can measure this today, in either direction.** The vendor cannot prove the gain. The
CFO cannot prove the loss. The renewal conversation is two people trading anecdotes.

**Why we win it:** honesty rate per actor over time, and whether the work survived. That is the
first number that makes the agent ROI argument falsifiable, and **falsifiable is what a CFO
actually wants**, including when the answer is unflattering.

**Weakness, stated:** we have never run this on a real fleet. The record currently holds zero
real claims.

---

## 4 · The customer. Your buyers have started asking about you.

**Who:** the enterprise sales engineer on a security questionnaire.
**The force:** their procurement, not yours.
**Their sentence:** *"Did AI write any of the code you shipped us, and who checked it?"*

This is the one that arrives without warning and has a deadline attached to a deal. The
questionnaire lands, and the honest answer today is **"we do not know."** That answer does not
lose the deal outright; it triggers a security review, and the review costs a quarter.

**Why we win it:** the same export, pointed outward instead of upward. It turns an unanswerable
question into an attachment.

**Weakness, stated:** the least validated of the four. We have not spoken to anyone who has
received this questionnaire.

---

## The shape of the four

| | Who asks | Force | Timeline | Their words |
|---|---|---|---|---|
| 1 | the regulator | law | dated, unavoidable | *prove nothing shipped unverified* |
| 2 | the VP Eng | an incident | already happened | *what did it think it was doing* |
| 3 | the CFO | money | renewal | *we bought 10x, where did it go* |
| 4 | your customer | their procurement | mid-deal, no warning | *did AI write this, who checked* |

**Four buyers. Four forces. One missing artifact.**

That is why this is not a CI check with a compliance story bolted on. **Four independent
pressures are converging on a record that does not exist yet**, and the reason it does not exist
is that everyone builds tools that read the diff, the trace, or the spend, and nobody connects
the claim to the object.

---

## The line

> **Run your agents. Check the math.**

Oscar's, said in passing today, and better than anything written in this repo.

---

## What is honest to say on camera, and what is not

**True today:** the gate is live and enforcing. A held claim carries the session that produced
it. The export exists and is Firestore-backed.

**Not true today, and must be stated as roadmap:** the record holds **zero real agent claims** —
4 clearances, all four staged by us, and `GET /audit` reports **`clear: 0`**, so nothing has ever
passed the gate because nothing real has ever gone through it; the check has never fired on a real
pull request; the Gemini call does not happen inside the container; the ADK agent is constructed
and never invoked.

**One real agent pull request moves the first four of those.** The last two need the key mounted
and a Runner wired.
