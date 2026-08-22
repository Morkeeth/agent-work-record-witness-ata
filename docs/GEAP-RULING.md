# GEAP — bet or fold. RULED: BET.

`FOR-CURSOR.md` round 1 asked for this ruling before the schedule depends on it. Answered
2026-08-22 from public sources; **re-verify at the console before slice 0 spends an hour on it.**

## What GEAP is
**Gemini Enterprise Agent Platform is the April 2026 rebrand of Vertex AI**, GA, announced at
Google Cloud Next '26. It ships: **Agent Registry** (catalog + governance for agents, tools and MCP
servers), **Agent Runtime** (async agents for up to seven days), **Memory Bank** (long-term memory,
Gemini 3.5 Flash as the default model), identity, gateway, guardrails, observability.

## The fold case, and why it fails
The fear was an enterprise tier a solo entrant cannot reach. **It is not gated that way:**
- $300 free credits, pay-as-you-go, full feature set
- Free Agent Engine runtime — **first 50 vCPU-hours/month**
- Agent compute ≈ **$0.085/vCPU-hour**, agent storage ≈ $0.30/GiB-month
- Vertex free tier still gives rate-limited Gemini access

Solo developers do flag **cost** as the common complaint, not access. So the risk is a bill, not a
door — and a bill is bounded by the free runtime hours plus the $150 hackathon credits.

## Why BET rather than the obvious stack
1. **It satisfies a mandatory requirement natively.** The rule reads *"Gemini 3.5 or newer accessed
   through Gemini API **or Vertex AI**"* — and GEAP *is* Vertex AI. Not a bolt-on.
2. **Differentiation on the 30% architecture criterion.** A 600-entry field submits
   Gemini + ADK + Cloud Run. GEAP is the sponsor's newest strategic product and almost nobody will
   reach for it.
3. **Agent Runtime's seven-day async execution is the track's own sentence.** *"Agents that run in
   the background… asynchronously."* Our analyst fan-out is exactly that shape.
4. **Memory Bank is the corpus's natural home** — and it removes a bespoke store from the diagram.

## The threat, answered rather than ignored
GEAP already ships registry, identity, guardrails and observability. A product that "manages a
fleet" risks reading as a skin over the sponsor's own platform. **The answer goes in the pitch:**

> **GEAP governs the agents. Nothing governs the prompts.**

Google's registry knows which agents exist and what they may touch. It does not know which human in
the building writes prompts that produce work that lands — because that signal is not in the agent,
it is in the transcript.

## What slice 0 must actually prove, inside one hour
- [ ] An agent registers in the Agent Registry from a personal pay-as-you-go project
- [ ] Memory Bank accepts a write and a semantic read
- [ ] `gcloud run deploy --source` puts a hello-world ADK+Gemini agent live (Cloud Build — **no local
      Docker, no Colima, and it dodges the ARM-Mac / linux-amd64 image trap**)
- [ ] Screenshot each. That screenshot is the Phase-4 "a judge would see something different" receipt.

**Fallback, decided in advance so it is not decided at 2am:** if the Registry resists for more than
one hour, drop to Firestore + ADK + Cloud Run and keep the fan-out. **The wedge does not depend on
GEAP.** Losing it costs architecture points, not the product.

*Sources: Google Cloud GEAP docs (Agent Registry, Memory Bank), Google Cloud Next '26 coverage, G2 and
Google Cloud pricing pages. All RELAYED from search summaries — none opened at the console yet.*
