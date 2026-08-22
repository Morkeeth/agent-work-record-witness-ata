# Build plan — the ambitious version

**Phase 2/3 material.** Follows `vault 01 Projects/Hackathons/hackathon.md`.
Riskiest-first. Nothing runs ahead of the one thing that can fail the submission.

---

## The wedge — one line, and six theses died for it

> **GEAP governs the agents. Nothing governs the prompts.**

Google's own platform ships the Agent Registry, identity, guardrails and observability.
Every entry that "manages a fleet" is building a skin on it. **We measure the humans driving
them** — what they typed, whether it worked, and who in the building is good at it.

**Killed to get here:** claim verification · a measurement bench · a replication registry ·
agent HR/headcount · survival-rate scoring · a governance dashboard. Each was correct.
Each was a feature. See `hackathon.md` THE IDEATION LAW.

---

## The architecture — a real network, because the track is a network

*"Build a scalable network of institutional agents"* is the track's own sentence. One agent with
tools is not a network. This is a fan-out, and the fan-out is the architecture story that plays
for the 30% Architectural Discipline criterion.

```
transcripto spine  ──►  INGEST          normalises any harness
                          │              (Claude Code · Cursor · Copilot · Codex)
                          ▼
                    Pub/Sub topic
                          │
        ┌─────────┬───────┴───────┬─────────────┐
        ▼         ▼               ▼             ▼
    ANALYST   ANALYST         ANALYST       ANALYST      ← N ADK agents on Cloud Run,
    prompt    outcome         failure       cost/tools     registered in GEAP Agent Registry,
    quality   (did it land)   patterns                     scaled horizontally
        └─────────┴───────┬───────┴─────────────┘
                          ▼
                   GEAP Memory Bank  +  BigQuery Vector Search
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
        SYNTHESIS agent          COACH agent   ← THE WEDGE
        the org's picture        "here is the better prompt,
                                  taken from your own best operator"
```

**Every seam is replaceable and each is a defensible engineering choice:**
harness-agnostic ingest · one analyst per dimension so a new dimension is a new worker, not a
rewrite · GEAP for registry/memory rather than a bespoke store · the coach reads the corpus and
never writes to it.

## The stack ruling — GEAP, deliberately

| Layer | Choice | Why not the obvious one |
|---|---|---|
| Model | **Gemini 3.5** | required |
| Framework | **ADK** for the analysts | required; ADK wraps plain functions so the analysis is testable without it |
| Platform | **GEAP** — Agent Registry, Memory Bank | a 600-entry field submits Gemini+ADK+Cloud Run. GEAP is the sponsor's newest strategic product and almost nobody will use it |
| Compute | **Cloud Run**, deployed with `gcloud run deploy --source` | Cloud Build — no local Docker, no Colima, no ARM/amd64 trap |
| Bus | **Pub/Sub** | the fan-out is the track |
| Retrieval | **BigQuery Vector Search** | semantic retrieval over prompts is the coach's engine |

**GEAP is a bet and it is written down as one.** It is new, and new means thin docs. Slice 0
buys the information before the schedule depends on it. See the Cursor ask.

---

## Slices — riskiest first

| # | Slice | Proves | Risk |
|---|---|---|---|
| **0** | **`gcloud run deploy --source` a hello-world ADK+Gemini agent. Screenshot it.** Same day, probe GEAP: does the Agent Registry accept a registration in under an hour? | the submission can exist at all | **HIGHEST — everything downstream dies here.** If GEAP resists, fall back to Firestore and keep moving. Decide inside one hour, not one day |
| **1** | Ingest at org scale on the transcripto spine. **The 95% gate must fire visibly** — show human turns separated from injected ones | the corpus is real and nobody else has it | medium |
| **2** | Two analysts (prompt quality · outcome) fanned out over Pub/Sub | the network is a network | medium |
| **3** | **The COACH.** Retrieve the org's best-performing prompt for an intent and adapt it | **the wedge** | the product dies without this |
| **4** | Synthesis surface — the org's picture in one screen | the buyer's view | low |
| **5** | Remaining analysts (failure patterns · cost) | depth | **first to cut** |
| **6** | Architecture diagram **rendered and looked at** · stranger pass on a cold clone · README | required components | never cut |
| **7** | The 4-min video, **one take, unedited** | 30% of the score | never cut |

## The demo — one take, in order

| t | Beat |
|---|---|
| 0:00 | **The credibility beat.** Point it at a real corpus: *"~95% of the `user` turns in these transcripts are not the user."* Show the gate separating them. This is the beat that proves the data is ours |
| 0:45 | Fan-out running live — N analysts on Cloud Run, visible in the console |
| 1:30 | **"Who is best at this?"** → it names a person and prints their prompt |
| 2:15 | **THE WEDGE. "Give me their version of what I am about to do."** → the coach rewrites your prompt from the org's own best pattern. Impossible without the corpus |
| 3:00 | Cloud Run + GEAP registry visible in the browser |
| 3:30 | Architecture diagram |

**Beat 4 is the entry.** Everything else is setup for it.

## What is honestly hard, stated before a judge finds it
- **"Best operator" needs a defensible definition.** An unpinned denominator is the failure this
  whole stack exists to catch. Define it before building: fewest retries to a landed change, on
  comparable task classes — and print the denominator on screen.
- **Privacy.** Reading a company's prompts is reading its people. The product must show what it
  never stores, and that boundary should be architectural, not a policy sentence.
- **The corpus is Oscar's today.** A judge cannot run this on their own org. Answer: the ingest is
  harness-agnostic and slice 1 must demo on a second, non-Oscar source, even a small one.
