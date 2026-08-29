# Phase 1 — Spec extract

**Every literal constraint as a quoted checkbox.** Fetched from the Devpost site 2026-08-22.
Phase-1 gate exists because KYA died on an avatar rule that was knowable in hour one.

## Hard requirements — a missing box is a disqualification, not a lost point

- [ ] **"Gemini 3.5 or newer accessed through Gemini API or Vertex AI"**
- [ ] **"At least one Google Agent Framework: Google ADK, GenAI SDK, Antigravity SDK or GenKit"**
- [ ] **"At least one Google Cloud infrastructure service (such as Cloud Run, Cloud SQL, Firestore, GKE, Pub/Sub)"**
- [ ] Category selected — **The Fortified Enterprise Fleet**
- [ ] **Code repository URL** (GitHub / GitLab / Bitbucket) with **setup instructions in README.md**
- [ ] **Architecture diagram** showing system connections
- [ ] **Demo video, max 4 minutes**, on YouTube or Vimeo
- [ ] Text description: features, technologies, **data sources**, and learnings
- [ ] **Pre-existing code disclosed** — *"must disclose any other pre-existing code or work incorporated into the Project"*
- [ ] Submitted by **Aug 31 2026, 5:00pm PDT**

## Soft / optional — verified, do not treat as mandatory

- [ ] Hosted project URL — verbatim: *"Include a URL to the hosted Project **(if available)** for judging and testing"*, note: *"A hosted project is **highly encouraged**."* **OPTIONAL.**

## Scored — the three criteria, verbatim

| Weight | Criterion | The sentence judges are given |
|---|---|---|
| **40%** | Innovation & Operational Utility | *"How much real-world friction does the agent remove **on its own**?"* |
| **30%** | Architectural Discipline & Tech Stack | engineering choices and system design |
| **30%** | Demo & Production Readiness | *"the clarity of the technical documentation and the **undeniable proof of execution** in the video pitch"* |

The 30% breaks into three named sub-checks:
- **Proof of Action** — *"Does the video show an **unedited, live execution** of the agent performing its task?"*
- **Documentation** — *"Does the public GitHub repository feature a clean architecture diagram and reproducible setup instructions?"*
- **Cloud Deployment Proof** — *"Is there visual proof of Google Cloud deployment in the video?"*

**Consequence:** the video is one take. No cut may hide a failed run. A deterministic fixture is
not a shortcut here — it is the only way to satisfy "unedited" honestly.

## Deliverable status (handbook pass 2026-08-29)

| Box above | Status |
|-----------|--------|
| Gemini + ADK + GCP | ✅ probed |
| Track + repo + README | ✅ |
| Architecture diagram | ✅ `docs/architecture.png` |
| Video | ⛔ Oscar |
| Text description | ⛔ Devpost |
| Hosted URL | ✅ |
| Deadline | ⛔ Mon 17:00 PDT |

Full ladder: `docs/HANDBOOK-PASS-2026-08-29.md`

## The track, verbatim
**The Fortified Enterprise Fleet** — *"Build a scalable network of institutional agents."*
Event framing: *"agents that run in the background, handle the heavy lifting of massive datasets,
and automate complex workflows asynchronously."*

## Prizes — $180,000
Grand $50K · 3 category winners $20K · Startup Excellence $20K · **2× Individual/Hobbyist $10K** ·
**2× Architectural Design $5K** · 2× Multimodal UX $5K · 5× Honorable Mention $2K.
**No sponsor-specific or bonus prizes exist** — checked the resources page 2026-08-22.
Startup Excellence assumed out (needs an incorporated entity) — `UNVERIFIED`.

## The sponsor stack — checked, and it changes the build

Google Cloud is the sole sponsor. Offered:
Gemini API / AI Studio · **ADK** · **Antigravity SDK** · **Genkit** · Cloud Run · Firestore ·
**Gemini Enterprise Agent Platform (GEAP)** — *"Agent Registry, Agent Runtime, Memory Bank,
identity, gateway, guardrails, and observability tools."*

**$150 in Google Cloud credits** — *"request via the credit form"*. **ACTION FOR OSCAR: request
them now.** They are not automatic and they reduce the billing exposure.

### The GEAP ruling — this is the Phase-1 finding

GEAP cuts both ways and both readings must be answered before Phase 4:

- **Threat.** GEAP already ships an Agent Registry, identity, guardrails and observability. A
  product that manages a fleet risks reading as a skin over the sponsor's own platform.
- **Opportunity, and it is the larger one.** Most of a 600+ entry field will submit
  Gemini + ADK + Cloud Run — the obvious three. **Building on GEAP is the differentiated stack
  choice**, it is the sponsor's newest strategic product, and it maps directly onto this
  product: GEAP registers and governs the agents; we measure the *humans driving them*, which
  GEAP does not do.

**The line that resolves it, and it belongs in the pitch:**
> **GEAP governs the agents. Nothing governs the prompts.**
