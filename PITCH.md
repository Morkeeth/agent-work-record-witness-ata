# TRANSCRIPTO — the enterprise fleet, and the watcher on top

*Oscar's words, 2026-08-22. The corpus is the spine; the fleet supervisor is the watcher.*

> ## ⛔ VERDICT FIRST: THE ENTRY IS INELIGIBLE TODAY.
> All Things Agentic requires **Gemini 3.5 · a Google agent framework · a Google Cloud service.**
> At runtime this repo has **none of the three** — 199 lines of stdlib Python and a static page.
> **Aug 26 is not a schedule risk. It is the line between entering and not entering.**
> Everything below is real, and none of it can be submitted until that changes.

---

## 1 · THE COMPANY

**A company can see seats and spend. It cannot see practice.**

It handed coding agents to hundreds of engineers and has no idea what any of them type, which
prompts work, or who is actually good at this. **The answer is already sitting in transcripts it
owns and nobody reads.**

Transcripto is the corpus. The watcher reads it, finds the prompt that produced work that lasted,
and **writes it into the team's shared file — unasked.** The next engineer starts from it without
opening anything.

> **GEAP governs the agents. Nothing governs the prompts.**

## 2 · WHY NOW, AND WHY IT HOLDS

**The corpus compounds.** Every week of sessions makes the next answer better, and a competitor
starting in January has no history at all. This is the rare asset that cannot be bought.

**The moat is already built and it was not obvious.** At fleet scale **~95% of the `user` turns in a
transcript are not the user** — they are tool output, injected skill files, sub-agent prompts,
messages from other terminals. Separating the human from that is the hard part of the whole
category. Nobody found it because nobody ran a fleet big enough to hit it. *(A tool result even
arrives as `type: "user"`. It looks like a person typing.)*

**Second question, same corpus:** *which of our skills, rules and CLAUDE.md files actually change
behaviour?* Every team writing them is guessing.
**Second customer:** the enablement lead, who today buys prompt training written by strangers, and
would rather ship the prompt their own best engineer already wrote.
**Priced per engineer**, against a budget that exists: developer productivity and enablement.

## 3 · THE PROOF — runnable, not asserted

**`python3 contract/task_class.py`** — exits **1**.

```
classify_substring         3 / 8      the component that ships today
classify_always_different  3 / 8      a stub that never reads its input
```

**Indistinguishable. Not partial credit — no signal.** That is the runnable answer to *"why is a
model here at all?"*, and it beats any architecture slide: without task classification the product
cannot tell that `"fix auth"` and `"Refactor the auth module: extract validate_token…"` open the
same work — so the demo has no comparison and the submission has no Gemini.

| Artifact | Path | SHA |
|---|---|---|
| The screen — three directions, real data, rendered | `surface/gate1-directions.html` | `69b24cc` |
| The classifier contract, RED on purpose | `contract/task_class.py` | `792c3aa` |
| Compliance — 0 of 3 | `docs/COMPLIANCE-AUDIT.md` | `f62e9de` |
| Gemini stack fit + GEAP Sessions mapping | `docs/GEMINI-STACK-TAILORING.md` · `docs/GEMINI-FIT.md` | HEAD |
| Three probe classes | `surface/GATE-2-SELF-REVIEW.md` | `69b24cc` |

Branch `main`. **No remote — the push is Oscar's.** `fsck` clean through a full-disk outage.

**The screen's own discipline is the product's argument:** it prints `UNMEASURED` rather than
crediting the winner, because no tool record in that session can prove anything landed. **A metric
that refuses is the only kind a buyer can trust.**

## 4 · HONEST VERDICT

**The surface is a feature.** A stranger watches a screen that says which prompt won, why, and when
it will not say.

**The ineligibility outranks everything else here.** Three defects were caught today; those were
wrong answers. This is not being allowed to answer.

**The plumbing is absent and the product is right** — the better of the two ways to be wrong nine
days out, and only if Aug 26 holds.

**What I got wrong, and it is the reusable finding:** I killed a direction for inventing numbers,
then shipped an invented verdict in the two I kept. **I caught the fabrication that looked fake and
shipped the one that looked real.** Three probe classes, and none subsumes another — *render and
look* · *check the metric against the data* · *does the layout assert a relationship the data does
not hold*. A Gate-2 pass runs only the first.

**Blocked on Oscar, all five his alone:**
**① GCP + Gemini key by Aug 26 — eligibility, not schedule** · ② direction pick (1 Ledger / 2
Marginalia) · ③ hours calibration · ④ Phase 3 design owner · ⑤ may this lane take `fleet/signals.py`.
