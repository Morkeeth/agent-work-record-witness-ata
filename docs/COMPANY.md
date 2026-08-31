# From hackathon repo to a real company

**The line that governs this whole doc:** it is a project until a stranger installs it, and a
company when they keep it installed. Everything below is built backwards from that one event.

---

## The one-sentence company

**The gate that blocks an AI agent's pull request when the repo disproves what the agent said it
did** — free to install in five minutes, paid when a team wants the record across all of it.

Not code review (Qodo, $70M, reviews the diff). Not observability (scores the trace). We check
whether the agent's *"done, tests pass, committed as X"* is **true against the object** — the class
of failure that ships a "clean 200 and a confident lie" past both.

---

## Why now (validated, not asserted — see gate/MARKET.md)

- **53% of enterprises** run coding agents in production; a third of Razorpay's agent PRs merge with
  **no human in the loop.**
- The bottleneck **inverted**: code is 5–10× faster to write, so verification-before-merge is the
  constraint. Qodo's own framing: *"code generation is no longer the bottleneck; trust is."*
- The incidents wrote the budget: Replit deleted a prod DB; Amazon's Kiro tore down a
  CloudFormation stack → senior sign-off now mandated.

The window: agent-PR volume is exploding *this year*, and no one owns claim-vs-outcome yet.

---

## The staged path to real users (bottom-up, the Snyk/Sentry/CodeRabbit motion)

### Stage 0 — THE WEDGE: a free, open-source GitHub Action (get the first 100 non-Oscar users)
Already built (`.github/workflows/outcome-gate.yml` + `gate/outcome_gate.py`). Ship it to the
**GitHub Marketplace**, MIT-licensed, zero-config. An individual dev running Claude Code / Copilot
agents adds it to one repo in five minutes. The first week it blocks a real agent PR that claimed a
commit that does not exist — **that screenshot is the growth loop** (the same shape as the viral
"AI deleted my prod DB" posts).
- **First-user experiment (this week):** ship the Action, post one real caught-lie screenshot, get
  **10 installs by people who are not Oscar.** That single number is the difference between a
  hackathon entry and a startup. Nothing else matters until it clears.

### Stage 1 — TEAM: the record across all agent PRs (first dollars)
Once a team has it on several repos, they want the surface: which agents/engineers ship claims that
**survive** (shipped and stayed vs reverted), an audit of every blocked claim, cross-repo.
Paid per active repo or per seat. This is where "prompt propagation" becomes ONE feature, not the
product.

### Stage 2 — ENTERPRISE: the compliance record (the hard budget)
"Prove no agent shipped to production unverified" for SOC2 / EU AI Act. The audit log becomes the
artifact a security team hands an auditor. Hard budget, board-level urgency, exactly the pain the
2026 incidents created. This is the painkiller that funds the company; Stages 0–1 are how you earn
the right to sell it.

---

## Why this is not a feature GitHub absorbs next quarter

1. **Harness-agnostic.** Claude Code, Cursor, Copilot, Codex each store transcripts in a *different*
   schema (measured: Cursor has no `promptSource` field at all). GitHub Agent HQ sees only GitHub.
   Verifying claim-vs-*trace* needs the agent's full execution transcript, which lives outside the PR.
2. **The corpus compounds.** Every verified claim across an org's whole agent history is an asset a
   single-PR reviewer cannot build. A competitor starting later has no history.
3. **We check the report, not the code.** GitHub/Qodo review the artifact; the confident-lie failure
   is orthogonal to code quality and neither is built to catch it.

---

## Pricing (dev-tool PLG standard)
Free forever for individuals + open-source (the wedge). Team tier per active repo/seat (the record).
Enterprise tier for the compliance log + SSO + on-prem trace ingestion (the painkiller).

---

## The honest risks, named
- **Retention, not installs, is the question.** A PR check people mute is dead. It must block a
  *real* lie often enough to stay on. The first-user experiment measures exactly this: do the 10
  keep it after week one.
- **Narrow wedge.** "Check the claim" is less surface than "review the diff." That is the point
  (faster, orthogonal), but it means Stage 1 must arrive before a team asks "why not just use Qodo."
- **The corpus/trace ingestion is the build cost** — Stage 1+ needs the transcript pipeline
  (transcripto) productized per harness, which is real work and the actual technical moat.

---

## What the hackathon is, in this frame
Not the product — the **launch moment**. A public repo a stranger can run, a 4-min video that is the
caught-lie demo, and a submission that puts the free Action in front of the exact audience (people
building agents) who are the Stage-0 users. Win or not, the submission is the first distribution.
