# User journey: one person, one Monday

*Rewritten 2026-08-27. The previous version of this file was a shot list: every row had a
"Video" column, and its steps described prompt propagation, which is not the product being
built. It is preserved in git history. This one describes what a person does, not what a
camera sees, and the video is derived from it rather than the other way round.*

---

## The person

**Priya runs the AI rollout at a 400-engineer company.** Not a founder, not a researcher. She
signed the seat contract, she owns the budget line, and in March her CTO asked her a question
she could not answer.

She is not the person who writes prompts. She is the person who has to say whether letting
four hundred engineers point coding agents at production was a good idea.

**What she has today:** a seat count, a spend graph, and a vendor dashboard showing tokens.

**What she does not have:** any idea whether the work those agents said they did, they did.

---

## The question that starts everything

March, board deck review. Her CTO asks:

> *"If the regulator asks whether an AI agent shipped unverified code to production, what do we hand them?"*

Priya has no document. Not a bad document, **none**. Her options are a spend graph and the
word of four hundred engineers. She writes "compliance gap" on a slide and it stays there for
five months, because every vendor she asks solves an adjacent problem: one governs what agents
are *allowed to do*, one checks content against approved sources, one reviews the diff. **None
of them can tell her whether a claim an agent made was true.**

---

## Monday, week one. She installs it and nothing happens

She adds a YAML file to one repo. Five minutes. The `verify-claims` clearance check runs on pull requests
labelled `agent`.

**Nothing visible changes**, and that is the point. Engineers open pull requests. Most pass.
Her inbox does not fill up. There is no dashboard to learn and no login for anyone but her.

The first time it fires, an agent's pull request says *"committed as `deadbee`, wrote
`docs/auth-migration.md`, everything is done and merged."* The check probes each claim against
the repository. `deadbee` is not a commit. That path does not exist. **The merge stops.**

The engineer sees a red check with two lines under it. They fix it in four minutes and never
think about it again. **That is their entire relationship with this product, forever.**

## Monday, week four. She opens it for the first time

Four weeks of pull requests have gone through. She opens the console and sees something no
tool she has ever bought could show her:

- how many claims her agent fleet made
- how many the object disagreed with
- **which of those claims can be opened back to the session that produced them**
- who overrode a hold, and the reason they typed when they did

She clicks a held claim from a Tuesday. It opens to the transcript of the agent run that
produced it. She reads what actually happened before the sentence was written.

**No CI product can do that, and the reason is structural: none of them has the transcript.**

## Monday, week twelve. The question gets an answer

Her CTO asks again. She exports the record.

It is an append-only log of every claim an agent made against production code, whether the
object agreed, every override with its stated reason and author, and a link from each entry to
the run behind it.

**That is the answer to "prove no agent shipped unverified", and it is the first time anyone in
the company has had one.**

---

## What she is actually buying

Not a check. She could have a check written in an afternoon and she knows it.

**She is buying the ability to answer a question she has been unable to answer for five months**,
and the fact that it accumulates whether or not anyone remembers to use it.

---

## The three moments, and only these three

| | Who | Moment | Why it is not replaceable |
|---|---|---|---|
| 1 | The engineer | a red check, four minutes, then forgotten | zero new surface is why it survives contact |
| 2 | Priya, week four | a held claim opens to its own transcript | **nobody else holds the transcript** |
| 3 | Priya, week twelve | the export | it is a document, and a document is what a regulator takes |

Moment 2 is the product. Moment 1 is how it gets installed. Moment 3 is why it gets renewed.

---

## Honest state, 2026-08-29

Written so nobody has to guess which parts are real. Synced with `SUBMISSION-PACK.md` §3.

| Moment | Real today | Gap |
|---|---|---|
| 1 · the red check | **yes** — PR #1 · `verify-claims` **FAILURE** (red by design) | branch protection off · zero non-author installs |
| 2 · the trace | **yes** — `H-57b130f397` traceable · session on record · console renders join | Claude Code session patterns only today |
| 3 · the export | **yes**, `/audit/export`, Firestore-backed | **`clear: 0`** — real row is HOLD, not clear |

**One real agent PR is in the record.** What remains is adoption beyond the author and a first CLEAR.

---

## The pitch decision, ruled

**RULED by Oscar 2026-08-27: the product is THE RECORD. The gate is a feature inside it.** This
journey was already written for that ruling, so nothing here changes.

The demo **opens on week four** — a platform lead opening a held claim that resolves to the session
that produced it. The gate is how it got installed, and it is the moment a claim gets caught. It is
not the opening shot.

The product is named **THE AGENT WORK RECORD WITNESS** (ruled the same day). "Hold" is the name of
the queue inside it.

---

## Non-negotiables, unchanged

- Nothing from a transcript is ever executed.
- `UNMEASURED` prints wherever the field is too thin to support a claim.
- The model explains a decision and never overrules one. Object probes are the release authority.
- Composition blocks. Judgement is recorded and never gates.
