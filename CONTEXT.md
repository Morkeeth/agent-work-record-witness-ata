# CONTEXT — what this repo is and what it is not

## The product

A management tool for an organisation's agent fleet, built on its transcript corpus.

**The problem:** companies handed agents to hundreds of engineers and have no idea what any of
them are typing, which prompts work, or who needs help. They can see seats and spend. They
cannot see practice.

**The wedge (Surface 5):** the ADK fleet supervisor finds a high-survival prompt from the org's
best operator and **propagates it** — writes the org skill/rule and applies it on the next run.
The rollout owner sees the outcome; the agent removes the friction of hunting for "who prompts
well on this?" See `docs/WEDGE.md`.

## The moat — and it is already solved

`transcripto` (`~/CODE/transcripto`, Morkeeth/transcripto) found this at fleet scale:

> **~95% of the `user` turns in a transcript are not the user** — they are tool output,
> injected skill files, sub-agent prompts, and messages from other terminals.

Separating what a human actually typed from everything else is the hard part of this entire
category. `promptSource` typed/queued gating solves it (`transcripto.py:129-146`). EYES panel
measured **94.48%** non-human on this machine (Aug 22) — probe reproducible via transcripto DB.

Nobody else found it because nobody else ran a fleet big enough to hit it. **Claude Code only
today** — Cursor/other tools are expansion, not submission-critical.

## The five surfaces

1. **The corpus** — transcripto at org scale
2. **Prompt performance** — which prompts land, loop, or get abandoned
3. **People** — who is good at this, and what are they doing that others are not
4. **Agent behaviour** — what the agents actually do, where they fail, what they touch
5. **Improvement** — the supervisor **propagates** the best operator's prompt into the org skill
   file and proves it landed — unattended

**Surface 5 is the company.** Everything else reports; this one acts, from the org's own corpus.
The best prompt for your codebase already exists — someone wrote it last Tuesday and nobody
else will ever see it until the supervisor spreads it.

## Trust model (honest scope for the hackathon)

- **Day one:** opt-in team corpus on Claude Code transcripts the org chooses to index locally
  or upload to Firestore — not "hundreds of seats" on submit day.
- **Day two buyer:** whoever owns the AI rollout (VP Eng, Head of Platform, Head of Enablement).
- Nothing extracted from a transcript is ever executed. Propagation writes **curated, reviewed
  prompt text** to a named skill path — not raw transcript replay.

## What it is NOT — pre-answers for a judge

- **Not GitHub Agent HQ / Mission Control** (Oct 2025, free in Copilot). That assigns and tracks
  *tasks* and ships Copilot usage metrics. This analyses *authorship-gated human prompts* and
  *propagates* the best ones. Different object.
- **Not Langfuse / AgentOps / Copilot OTel tracing.** Those instrument agent *traces* and cost.
  They do not separate human-typed turns from the ~95% noise, and they do not close the loop
  from "operator A survived" to "operator B's skill file updated."
- **Not Mount Helicon.** Helicon is one operator's system of record. This is multi-person and
  org-level, and it is about the humans.
- **Not DX / GitClear / Jellyfish.** They sell code-turnover on merged code. This starts one
  step earlier, at what was typed.

## GEAP — the sponsor stack line

> **GEAP governs the agents. Nothing governs the prompts.**

Gemini Enterprise Agent Platform ships registry, runtime, identity, guardrails. We measure and
improve the *humans driving them* — then the supervisor acts on that measurement.

## Inherited from `~/CODE/agent-claims-inbox` — spine only, product is new

| Source | LOC | Role here |
|---|---|---|
| `claims_inbox.py` discovery | 257 | the ingest — already reads the transcripto spine + `~/.claude` walk |
| `engine/witness.py` | 590 | trace-witness → an outcome signal |
| `repo_witness.py` | 176 | ground truth: did the work land |
| `cloud/store.py` | 113 | Jsonl \| Firestore, one env var — verbatim |
| `cloud/service.py` + `Dockerfile` | 110 | the Cloud Run shell — verbatim |
| `cloud/agent.py` | 99 | ADK-wraps-plain-functions pattern → **propagation tools** |

~1,300 LOC of plumbing. **The product is new** (performance signals, propagation, people view).
`ci_gate.py` is NOT inherited. Witness lines verify *claims*; they do not substitute for prompt
performance ranking or propagation logic.

## The laws this repo keeps

- Nothing extracted from a transcript is ever executed.
- Every verdict names the probe that produced it.
- `UNMEASURED` is printed, never guessed, and never rounded to clean.
- A stranger test that clones into an empty `HOME` before anything is called ready.
