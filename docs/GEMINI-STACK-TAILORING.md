# Tailoring to the Gemini stack — the decision, and what it fixes

**Ruled by Oscar 2026-08-22.** Not a narrowing of the product. The Google stack becomes the
**native** path; harness-agnostic ingest stays as the expansion. See `hackathon.md` THE IDEATION LAW —
we do not shrink the idea to fit the event.

---

## The finding: GEAP already stores the exact shape this product reads

**Gemini Enterprise Agent Platform ships a Sessions API.** Quoted from Google's docs:

> *"A session contains the chronological sequence of messages and actions (`SessionEvents`) for an
> interaction between a user and your agent."*

Three operations: **`CreateSession`** · **`AppendEvent`** · **`ListEvents`**. Events cover
*"user messages, agent responses, tool actions."*

And **ADK's own Event model** captures *"user messages, agent replies, requests to use tools
(function calls), tool results, state changes, control signals, and errors."*

**That is the same object we have been reading out of `~/.claude/projects/**/*.jsonl` all day.**

| What we read today (Claude Code JSONL) | GEAP / ADK equivalent |
|---|---|
| `type: "user"` with `promptSource: typed\|queued` | a user-role `SessionEvent` |
| `type: "user"` with `toolUseResult` set — **looks like a human turn, is not** | a tool-result event |
| `type: "assistant"` with a `tool_use` content block | a **function call** event |
| session file per conversation | a **Session**, read back with `ListEvents` |

**Same shape. Different source.** The ingest becomes an adapter, not a rewrite.

---

## What this fixes — three open problems collapse into one slice

### 1. It fixes the computability defect that is currently blocking the metric

`docs/SIGNAL-SPEC.md` COMPUTABILITY AUDIT: `LANDED` is uncomputable because **zero tool-call
records exist in any fixture**, and the rule is *ground truth from tool calls, never from the
agent's prose.*

**GEAP session events carry function calls and tool results natively.** So on a GEAP session,
`LANDED` is computable *by construction* — the field the hand-written fixtures lack is one the
platform emits by default. The defect was never in the metric. It was in the corpus.

### 2. It satisfies the mandatory stack with load-bearing components, not costume

`docs/COMPLIANCE-AUDIT.md`: today the artifact is **0 of 3**.

| Requirement | Satisfied by | Load-bearing because |
|---|---|---|
| **Gemini 3.5 via Gemini API or Vertex AI** | the task-class classifier behind `contract/task_class.py` | without it there is no comparison at all — the substring test scores identically to a stub that ignores its input |
| **A Google Agent Framework (ADK)** | the supervisor running discover → select → propagate → witness, and the **ADK Event model as the ingest contract** | the framework is the data model, not a wrapper around it |
| **A Google Cloud service** | **GEAP Sessions + Memory Bank**, Cloud Run for the deploy | Sessions is the corpus; Cloud Run is also the *"visual proof of Google Cloud deployment"* the 30% demands |

### 3. It answers the "why are you reading competitors' transcripts at a Google hackathon" question

It does not need dodging — it is the strongest line available:

> **The Agent Registry knows which agents exist. Nothing knows which humans drive them well.**

An org running Gemini Enterprise agents has the identical problem, and a harness-agnostic corpus
means Google's runtime is **one more source rather than the only one**. That is more valuable to
Google, not less. Ingest adapters for other harnesses are the expansion path named in Phase 0.

---

## The architecture change

```
BEFORE                          AFTER
~/.claude walk ─┐               GEAP ListEvents ─┐   <- native, and carries tool calls
                ├─> ingest      ~/.claude walk  ─┤
transcripto ────┘               transcripto ─────┴─> ingest adapter -> one Event contract
                                                        │
                                                        ├─> classifier (Gemini 3.5)
                                                        ├─> analysts (ADK, fanned out)
                                                        └─> Memory Bank (the corpus)
                                                              + Agent Registry (the join)
```

**The seam that matters:** ingest normalises every source to one event contract, so no analyst
knows where a session came from. Adding a harness is an adapter; it is never a rewrite.

**The join nobody else can make:** Agent Registry says which agents an org runs. Our side says which
humans drive them well. Neither half is interesting alone.

---

## UNVERIFIED — do not build on these until a console confirms them

Everything above about GEAP is read from documentation and search results. **Nothing has been run.**
Slice 0 must confirm, inside one hour:

- [ ] `ListEvents` is callable from a personal pay-as-you-go project (not enterprise-gated)
- [ ] a session event carries a distinguishable **function call** and **tool result**
- [ ] a user-role event can be told apart from a tool-result event — **the 95% gate must have a
      GEAP equivalent, or the corpus is polluted the same way and nobody notices**
- [ ] Memory Bank accepts a write and a semantic read

**Fallback, decided in advance:** if Sessions resists, ingest stays on the local corpus and the GCP
requirement is met by Cloud Run + Firestore alone. **The wedge does not depend on GEAP.**

*Sources: Google Cloud GEAP docs (Memory Bank / Sessions), ADK Events documentation. All RELAYED
from documentation, none executed.*
