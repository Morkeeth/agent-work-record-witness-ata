# How Gemini actually behaves on this workload

Checked 2026-08-22 against Google's pricing and structured-output docs. **RELAYED from
documentation — nothing called.** Slice 0 confirms at the console.

## 1. The classifier contract is a NATIVE Gemini feature, not a prompt trick

Gemini structured output supports **`enum` for classification** and **JSON Schema**, with `anyOf`
for conditional shapes.

`contract/task_class.py` declares `classify(a, b) -> SAME | DIFFERENT | UNDECIDABLE`. That is
literally an enum. So the model is **constrained by the schema to answer one of the three** — it
cannot wander, and it cannot omit `UNDECIDABLE`.

**Why that matters more than convenience:** the refusal primitive stops depending on prompt
discipline and becomes **enforced by the response schema.** Three lanes independently invented a
verdict that declines (UNKNOWN · UNMEASURED · UNDECIDABLE); on this stack it is a type, not a
convention.

`anyOf` also lets `UNDECIDABLE` carry a required `reason` field that `SAME`/`DIFFERENT` do not —
so a refusal is structurally unable to arrive bare.

## 2. The Batch API is ON-BRIEF, not a cost optimisation

Batch gives a **50% cost reduction** for asynchronous workloads.

The event's own framing sentence: *"agents that run in the **background**… automate complex
workflows **asynchronously**."* Nightly batch classification of the day's episodes **is** the
product's natural shape. Choosing batch is an architecture argument for the 30% criterion, and it
halves the bill as a side effect.

## 3. Cost at org scale — the question a judge will ask

One classification is two prompts in (~200 tokens) and an enum out (~10 tokens).

| | Gemini 3.5 Flash | via Batch |
|---|---|---|
| per classification | ~$0.0004 | ~$0.0002 |
| **10,000 episodes** | **~$4** | **~$2** |

**Negligible, and say the number rather than the adjective.** Context caching at **$0.15/M** (vs
$1.50/M fresh input, 10×) is the right pattern for the org's stable context — its conventions and
task taxonomy — re-sent on every call otherwise.

## 4. MODEL CHOICE — 3.7 Flash is newer AND cheaper than 3.5 Flash

The requirement reads *"Gemini 3.5 **or newer**."* From the pricing page:

| Model | Input /1M | Output /1M | Context |
|---|---|---|---|
| **Gemini 3.7 Flash** | **$0.75** | **$3.75** | — |
| Gemini 3.5 Flash | $1.50 | $9.00 | **1M** |
| Gemini 3.5 Flash-Lite | $0.30 | $2.50 | — |

**3.7 Flash is half the price of 3.5 Flash and satisfies the requirement.** Its rate is marked
*"through Dec 31 2026, doubled Jan 1 2027"* — promotional, and irrelevant to a hackathon ending
Aug 31.

> **CORRECTION, 2026-08-22.** I earlier reported that `gemini-3.7-flash` was *"not in the live
> models list on this key."* **That was false, and the error was mine.** The model was in the
> response I had already fetched. My print statement ended in a slice of twelve and I **read my own
> truncation as absence.** Re-checked: 50 models, 17 of them `gemini-3*`, `gemini-3.7-flash` among
> them. A sibling lane called it and got HTTP 200.
>
> **The rule gains its second half.** *Documentation is not availability* still holds — but **an
> incomplete enumeration is not absence either.** You cannot prove absence with a query you did not
> verify was complete, and a slice in a print is a display limit, not a result.
>
> Third pipeline artefact reported as an API fact in one afternoon. **Check the pipeline before
> attributing behaviour to the remote.**

**But `cloud/agent.py`'s existing rule stands and is right: never hardcode a model id.** A guessed
or retired id fails at deploy time with a confusing error, which is the one failure the demo cannot
afford. `GEMINI_MODEL` stays an environment variable; this table informs the default, it does not
become one.

## 5. The 1M context window unlocks a signal that is currently uncomputable

`docs/SIGNAL-SPEC.md` lists `REOPENED` — the same file touched again in a later episode within 48h —
as **not computable**, because it needs cross-session reach.

A 1M-token window holds many sessions at once. Combined with GEAP `ListEvents`, cross-session
analysis stops being an architecture problem and becomes a prompt. **`REOPENED` is the honest
survival signal**, and it is the one that makes "did the work last" mean something beyond "did it
merge".

---

## What must be confirmed at the console before any of this is claimed
- [ ] enum-constrained structured output returns one of exactly three values, **including
      `UNDECIDABLE` when the input warrants it** — watch it choose the refusal, do not assume it can
- [ ] Batch API is reachable on a pay-as-you-go project without an enterprise agreement
- [ ] 3.7 Flash is actually available on the free/PAYG tier, not enterprise-only
- [ ] context caching works against a corpus-sized stable prefix

**Every row above is documentation, not observation.** The control set in
`contract/task_class.py` is what will decide whether any of it is true here — and it is RED today,
so nothing can be tuned to a result and then called a pass.
