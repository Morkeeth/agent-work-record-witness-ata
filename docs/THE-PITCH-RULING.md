# Gate or record — a first stab, for Oscar to rule in two minutes

*Written 2026-08-27 while he slept. This is not a survey. It is one recommendation with the case
against it stated honestly, so the ruling takes two minutes instead of another week.*

---

## The question

Everything downstream of this is stuck: the name, the film, the pitch deck, and whether the
hackathon is worth four more days.

**Are we pitching THE GATE (it blocks false agent claims at merge) or THE RECORD (the system of
record for what your agent workforce actually did)?**

---

## What each one actually is

**THE GATE.** A required check reads a pull request body, probes each claim against the object,
and fails red when the object disagrees. Install is a YAML file. Five minutes.

**THE RECORD.** Every claim, whether it held, who made it, whether the work survived, and the
session that produced it. Install is the same YAML file. You keep it because of what accumulates.

They are the same product. **The question is only which half you point at a judge and an investor.**

---

## The recommendation: THE RECORD

**Three reasons, in order of how much I trust them.**

**1 · The gate is a two-hour build and you already said so.** A check that greps a body for a SHA
and a path is a weekend. Zenity ($125M), Qodo ($70M), or any competent platform team ships it. If
that is the pitch, the honest response is "nice script." You have said "this is plumbing" three
times today and this is the thing you were pointing at.

**2 · The record is the only part nobody can copy.** Separating the small fraction of turns a human
actually typed from the injected remainder took months and compounds weekly. A competitor starting
in January has no history. Zenity governs agent actions. Norm Ai ($1.2B) does content compliance.
Qodo reviews the diff. Langfuse scores the trace. **Not one of them holds the agent's transcript**,
so not one of them can answer "what actually happened before this claim was written."

**3 · It is the only version that survives the buyer.** A VP Eng does not buy a check. They buy the
answer to the question their board asked: *prove no agent shipped unverified.* That answer is a
document, and a document is a record.

---

## The case against, stated properly

**The record is empty.** Measured today: 48 stored records, 4 clearances, **all four staged**, zero
real agent claims. Pitching the record means pitching a surface with nothing in it, which is worse
on camera than a red check that visibly works.

**The gate demos in fifteen seconds.** The record demos in a week of accumulated data you do not have.

**That is a real objection and it has a cheap answer:** one real pull request. Ten minutes of yours.
After that the record has something in it, and the gate beat still exists inside the record story
as the moment a claim gets caught. **You lose nothing by leading with the record; you only need one
row in it.**

---

## What the ruling decides, immediately

| | If GATE | If RECORD |
|---|---|---|
| **Name** | a verb: **HOLD** | a noun: **WITNESS** |
| **Demo opens on** | a red check | a week of your fleet, and one caught claim |
| **The line** | "nothing merges on a false claim" | "you cannot see what your agents actually did. Now you can." |
| **Day-two buyer** | a platform engineer | whoever owns the AI rollout and has the budget |
| **Honest ceiling** | a good CI tool | a company |

---

## My answer

**RECORD. Name it WITNESS. Keep "Hold" as the name of the queue inside it.**

`witness_propagation()` already returns `VERIFIED-BY-REPO` in your own code, so the word is not
imported, it is the thing the codebase already calls this. A witness observes what happened and can
testify to it later, which is both halves: the gate observes, the record testifies. It survives the
move from CI check to compliance artifact. **HOLD does not** — nobody buys a company called Hold.

---

## To rule it

Reply with one word: **record** or **gate**. Everything else follows from it and I will do the rest.

If you rule **record**, the only thing that must happen before filming is the one real pull request,
because the record needs one true row in it. That is still ten minutes.
