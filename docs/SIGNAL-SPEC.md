# SIGNAL SPEC — what "best operator" actually means

**Written because the current signal has no denominator.** `fleet/signals.py` scores every
survivor exactly `1`, so `max()` returns directory order and no ranking exists. This is the
unpinned-denominator failure inside a product whose entire pitch is that numbers are evidence.
It would not survive one question on camera.

**Column note:** this doc is the measure (Claude's column). The implementation is
`fleet/signals.py` (Cursor's column). Per `COLLAB-PROTOCOL.md` I do not edit it.

---

## The unit — pin this before anything else

**One EPISODE = one human intent, opened and closed.**

- **Opens** at a human turn (`is_human_turn`) that states an intent.
- **Closes** at whichever comes first:
  - a **durable artifact** — a tool call that wrote a file, committed, or ran a command that
    changed state — with no further corrective human turn on that same intent, **or**
  - **abandonment** — an explicit abandon marker, or the session ends with no durable artifact.

Everything below is counted per episode. An episode is the denominator. **Say the word "episode"
on camera** — the moment a judge hears a unit defined out loud, the number becomes evidence.

## The four observables — all read from the transcript, none inferred

| Signal | Definition | Why it is the honest one |
|---|---|---|
| `CORRECTIVE_TURNS` | human turns after the opener that **restate or narrow the same intent** | this is literally the cost of a bad prompt. A new intent is not a correction |
| `LANDED` | a durable artifact appeared — file write, commit, state change | ground truth from tool calls, **never from the agent's prose** |
| `ABANDONED` | explicit abandon marker, or closes with no durable artifact | the failure that silently disappears from every other metric |
| `REOPENED` | the same file or intent is touched again in a later episode within 48h | survival. A change that comes back was not done |

**Nothing here reads the assistant's summary.** The current signal counts assistant turns, which
measures verbosity — two turns of confused flailing scores identically to a landed change.

## The score — a ratio, and the denominator is printed next to it

```
landed-first-try rate  =  episodes LANDED with 0 CORRECTIVE_TURNS
                          ────────────────────────────────────────
                          episodes opened by that operator
                          ON THAT TASK CLASS
```

**Print it as `7/11 on refactor-a-module`, never as `0.64`.** A bare ratio hides its denominator;
a fraction cannot.

## THE TASK CLASS — this is the part that stops it rewarding easy work

An operator is compared to another operator **only within the same task class.** Without this,
whoever does the simplest work wins, and the metric is worse than useless — it is confidently wrong.

**Task class = the intent, classified from the opening prompt.** *refactor-a-module ·
add-a-test · fix-a-failing-build · write-a-migration · debug-an-error · add-a-feature.*

**This is where Gemini becomes load-bearing rather than decoration.** Classifying free-form
developer intent is a genuine language problem — no regex does it, and it is not a wrapper around
a deterministic core. It is the one place in the architecture where the model's judgment is the
product. *(It sits on the extraction side, not the verdict side: Gemini decides what class an
episode belongs to; the four observables decide the score, and they are deterministic.)*

## The comparison floor — and the refusal that proves the whole thing

**n ≥ 3 episodes on a task class, per operator, or the comparison prints `UNMEASURED`.**

Not "insufficient data" in grey text. `UNMEASURED`, with the counts shown, and **no verdict given.**

This is the same law as every other thing in this stack: *a threshold is unusable until its unit
is defined; saying so is the product.* **It is also the strongest 15 seconds available in the
demo** — show the tool declining to name a best operator on a thin task class, then show it
naming one where the data supports it. A metric that refuses is a metric a buyer can trust.

---

## FIXTURE REDESIGN — the demo currently has no loser

`fixtures/operators/operator-b-refactor.jsonl` returns `NO_MATCH` because the literal token
`refactor` is absent from its human turn. So "find the BEST operator" runs on a field of one.
**A judge watching the video sees best-of-one.**

**B must be in the same task class and lose on the signal, not on string matching.**

| Fixture | Task class | Opener | Episode shape | Outcome |
|---|---|---|---|---|
| **operator-a** | `refactor-a-module` | *"Refactor the auth module: extract `validate_token` into `auth/validate.py`, keep tests green, show me the diff before applying."* | opener → tool writes file → done | **LANDED, 0 corrective turns** |
| **operator-b** | `refactor-a-module` | *"clean up the auth stuff"* | opener → *"no, I meant the token bit"* → *"not that file, the validator"* → tool writes file | **LANDED, 2 corrective turns** |
| **operator-b-2** *(optional third)* | `refactor-a-module` | *"sort out auth"* | opener → two corrections → *"never mind"* | **ABANDONED** |

Now the demo says something true and visible in one screen:

> **Same task class. Same outcome. One operator got there cold; the other needed two corrections.
> That difference is a prompt, and it is transferable.**

And the propagated artifact is A's *specific* prompt — the one that names the file, names the
symbol, and asks for the diff first. **The pitch writes itself off the fixture.**

## Definition of done for this slice
- [ ] `score_session` returns episodes, not sessions
- [ ] `CORRECTIVE_TURNS`, `LANDED`, `ABANDONED`, `REOPENED` each computed and each naming its probe
- [ ] task class classified by Gemini, printed on every row
- [ ] ranking prints the fraction and the task class, never a bare number
- [ ] n<3 prints `UNMEASURED` and gives no verdict — **watch it print, do not assume it does**
- [ ] fixture B rewritten to lose on the signal
- [ ] the filename split fixed so the money line prints `a`, not `operator`

---

# COMPUTABILITY AUDIT — added 2026-08-22, and it invalidates part of the spec above

**A spec that pins a number nobody can compute is the same error as a fabricated one.** So every
observable above was checked against the data that actually exists, rather than against its own
description.

## Probe

```
$ python3 - (walk every record in fixtures/operators/*.jsonl, print keys + content block types)
  operator-a: [user text] [assistant text] [assistant text]
  operator-b: [user text] [assistant text] [user text]
$ grep -rlo "tool_use|tool_result|toolUseResult" fixtures/
  NONE
```

**Zero tool-call records exist in any fixture. Every record is text-only.**

## What that does to the four observables

| Observable | Definition above | Computable on the data that exists? |
|---|---|---|
| `ABANDONED` | explicit marker, or closes with no durable artifact | ✅ **yes** — the marker half. The "no durable artifact" half is not |
| `CORRECTIVE_TURNS` | human turns restating the SAME intent | ⚠️ **only with the classifier.** Not deterministic. Fine — that is its declared job |
| `LANDED` | *"a durable artifact appeared… ground truth from tool calls, **never from the agent's prose**"* | ❌ **NO. There are no tool calls.** Nothing to read |
| `REOPENED` | same file touched again within 48h | ❌ **NO.** Single-session fixtures, no second episode, no file identity |

**Therefore the headline score above — `landed-first-try rate` — has an uncomputable numerator.**

## The failure this actually is, stated plainly

`surface/gate1-directions.html` prints **"LANDED · 0 corrections"** for operator a in both surviving
directions. **That verdict is invented.** It is the same class of error as the `34%` / `72%` track
widths killed in `surface/GATE-2-SELF-REVIEW.md` — one commit earlier, by the same hand, in the same
surface. Killing the visible one did not catch the one wearing a real-looking label.

**The rule the spec broke is its own:** *ground truth from tool calls, never from the agent's prose.*
With no tool calls, "LANDED" was read from two assistant text turns — which is prose.

## The ruling

**The metric is sound on real data and wrong on this data.** Real Claude Code transcripts carry
`tool_use` / `toolUseResult` records; these hand-written fixtures do not. So the defect is in the
fixtures, not the measure.

Two branches, and the first is not mine to do:

1. **REQUEST TO CURSOR (owner of `fixtures/`):** the fixtures need to be shaped like real
   transcripts, including at least one `tool_use` writing a file in operator a's session. Without it
   the product cannot demonstrate the one signal it says it reads. **Better still: cut a fixture
   from a real session** so the shape is inherited rather than imagined.
2. **UNTIL THEN, the honest output is `UNMEASURED`, and the surface must say so.** Not "LANDED".
   The house law is that `UNMEASURED` is printed and never guessed, and this is exactly the case it
   was written for.

## And the honest version is a better demo beat, not a worse one

| operator | honest verdict on today's data |
|---|---|
| a | **`UNMEASURED`** — no tool record in this session, so the repo cannot confirm anything landed |
| b | **`ABANDONED`** — "never mind", read from the transcript |

That is still a real comparison, and it is a **stronger** 15 seconds: the tool declines to credit
operator a rather than flattering him, on camera, and then credits him once the data supports it.
**A metric that refuses is a metric a buyer can trust** — which is the argument this whole product
is making.

## Definition of done, corrected
- [ ] fixtures carry real `tool_use` records, or are cut from a real session — **Cursor's column**
- [ ] `LANDED` returns `UNMEASURED` when no tool record exists, and is watched printing it
- [ ] the surface renders `UNMEASURED` as a first-class verdict, not as a greyed-out failure
- [ ] no screen prints a verdict the data cannot support — **checked by rendering, not by reading**
