# TRANSCRIPTO — the enterprise fleet, and the watcher on top

*Oscar's words, 2026-08-22. The corpus is the spine; the fleet supervisor is the watcher.*

> ## ⚠️ ELIGIBILITY: **ONE of three** mandatory technologies is met.
> **✅ Gemini 3.5+ — MET AT RUNTIME.** `fleet/task_class.classify` → `contract/gemini_impl` makes a
> live call to `generativelanguage.googleapis.com` on every wedge run.
> **❌ Google agent framework —** `cloud/agent.py` imports `google.adk` only inside `build_agent()`,
> and nothing calls `build_agent()`.
> **❌ Google Cloud service —** `cloud/store.py`'s `get_store()` defaults to `FLEET_STORE=jsonl`;
> `FirestoreStore`'s `google.cloud.firestore` import sits behind that env var and it is not set.
>
> `cloud/` is scaffolding with a real, swappable seam — one environment variable from live, which is
> the right shape to be in. **But "the seam exists" is not "the service is called", and a judge
> checks the second.**
>
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

**The moat is already built, it was not obvious, and it is measured.** **At fleet scale, 95.1% of
the `type: user` records in a transcript were not written by the human** — 10,866 records against
537 real prompts over one three-day window. On a single-terminal day the same gate reads ~46%.
**The number is a function of fleet size**, because injected traffic scales and a person's typing
does not — which is exactly why an org rolling out agents at scale is the customer and a solo
developer is not.

**And it is not one gate. It is at least THIRTEEN record shapes, measured on this machine today
(16,078 `type: user` records, 1,138 written by the human), with a trap in both directions:**

1. A **tool result arrives as `type: "user"` with `promptSource: null`.** It looks like a person
   typing.
2. Injected skill bodies, sub-agent prompts and cross-session peer messages arrive the same way,
   separated only by `promptSource` and `isMeta`.
3. **`type: "queue-operation"` carries its text in a top-level `content` field, not
   `message.content`** — so a parser reading the obvious field **sees nothing at all**. Some of
   those are genuinely the human. But there were **4,596 of them against 537 real prompts**, and
   widening the gate to catch the real ones **inflates the corpus to 1,992 and fills it with the
   fleet's own words.**

Plus `system`, `last-prompt`, `mode`, `ai-title`, `permission-mode`, `file-history-snapshot`,
`file-history-delta`, `bridge-session`, `atis-latch`, `pr-link`, `frame-link`. **`queue-operation`
alone is 6,636 records.**

**And the deepest one is not a record type at all — it is a field that changes type.** On real
sessions a human turn's `message.content` is a plain **string**; hand-written fixtures use a list of
blocks. A parser written against the fixture form returns **empty for 98.8% of real human turns**,
with no exception and no warning, and every test stays green. *(Found and fixed here today: 556 of
563 empty before, 0 of 567 after.)*

**And it is worse for a competitor than even that, because it is per-harness.** Measured on this
machine: Cursor's transcript jsonl has **no `promptSource` key at all** — its records are
`{message, role, status, type}` with types like `turn_ended`. The Claude Code authorship gate cannot
run on it. So *"a field that changes type within one tool"* becomes *"a different authorship schema
per tool"* across them: multi-harness coverage needs a separate human-vs-agent model for each, and
Cursor gives you nothing to gate on. A single-harness limitation is actually a per-harness barrier.

**A competitor who does not know this ships a corpus of its own agents talking to themselves, and
its report reads fine.** That is the defensibility claim, and it is the only one here that was
measured rather than argued.

**Second question, same corpus:** *which of our skills, rules and CLAUDE.md files actually change
behaviour?* Every team writing them is guessing.
**Second customer:** the enablement lead, who today buys prompt training written by strangers, and
would rather ship the prompt their own best engineer already wrote.
**Priced per engineer**, against a budget that exists: developer productivity and enablement.

**Why the customer is an org and not a judge — measured, not asserted.** The product's value claim is
that a propagated prompt raises the next engineer's landed-rate. That lift is a contrast *across
operators*, and a single machine cannot produce it: on one operator's real corpus the specified-vs-
vague split collapses (this builder is one high-level orchestrator, so almost every opener is
high-level and specification emerges downstream). **The population lift is literally the first thing
the first customer's corpus proves** — the absence of it on a single machine is the argument for who
buys this, not a gap in it. The demo runs on one corpus; the value runs on an org's.

## 3 · THE PROOF — runnable, not asserted

**`python3 contract/task_class.py`** — exits **1**.

```
classify_substring         3 / 8      the component that ships today
classify_always_different  3 / 8      a stub that never reads its input
```

```
gemini-3.5-flash-lite      7 / 8      <- the same eight rows, live
```

**Indistinguishable stubs, and a model that beats them by four rows.** That is the runnable answer
to *"why is a model here at all?"*, and it beats any architecture slide: without task classification the product
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

**Live on real-shaped sessions:** `LANDED` is computed from a real `tool_use` record rather than by
counting assistant turns, and episodes carry a real score instead of every survivor scoring 1.

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
