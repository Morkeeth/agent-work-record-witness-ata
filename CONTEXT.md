# CONTEXT — what this repo is and what it is not

## The product

A management tool for an organisation's agent fleet, built on its transcript corpus.

**The problem:** companies handed agents to hundreds of engineers and have no idea what any of
them are typing, which prompts work, or who needs help. They can see seats and spend. They
cannot see practice.

## The moat — and it is already solved

`transcripto` (`~/CODE/transcripto`, Morkeeth/transcripto) found this at fleet scale:

> **~95% of the `user` turns in a transcript are not the user** — they are tool output,
> injected skill files, sub-agent prompts, and messages from other terminals.

Separating what a human actually typed from everything else is the hard part of this entire
category. `promptSource` typed/queued gating solves it. Nobody else found it because nobody
else ran a fleet big enough to hit it.

## The five surfaces

1. **The corpus** — transcripto at org scale
2. **Prompt performance** — which prompts land, loop, or get abandoned
3. **People** — who is good at this, and what are they doing that others are not
4. **Agent behaviour** — what the agents actually do, where they fail, what they touch
5. **Improvement** — *here is the better prompt, taken from your own best operator*

**Surface 5 is the company.** Everything else reports; this one coaches, from the org's own
corpus. The best prompt for your codebase already exists — someone wrote it last Tuesday and
nobody else will ever see it.

## What it is NOT — pre-answers for a judge

- **Not GitHub Agent HQ / Mission Control** (Oct 2025, free in Copilot). That assigns and tracks
  *tasks*. This analyses *prompts and people*. Different object.
- **Not Mount Helicon.** Helicon is one operator's system of record. This is multi-person and
  org-level, and it is about the humans.
- **Not DX / GitClear / Jellyfish.** They sell code-turnover on merged code. This starts one
  step earlier, at what was typed.

## Inherited from `~/CODE/agent-claims-inbox` — spine only, product is new

| Source | LOC | Role here |
|---|---|---|
| `claims_inbox.py` discovery | 257 | the ingest — already reads the transcripto spine + `~/.claude` walk |
| `engine/witness.py` | 590 | trace-witness → an outcome signal |
| `repo_witness.py` | 176 | ground truth: did the work land |
| `cloud/store.py` | 113 | Jsonl \| Firestore, one env var — verbatim |
| `cloud/service.py` + `Dockerfile` | 110 | the Cloud Run shell — verbatim |
| `cloud/agent.py` | 99 | ADK-wraps-plain-functions pattern |

~1,300 LOC of plumbing. **The product is new.** `ci_gate.py` is NOT inherited.

## The laws this repo keeps

- Nothing extracted from a transcript is ever executed.
- Every verdict names the probe that produced it.
- `UNMEASURED` is printed, never guessed, and never rounded to clean.
- A stranger test that clones into an empty `HOME` before anything is called ready.
