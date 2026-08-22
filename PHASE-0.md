# Phase 0 — the entry gate

**Event:** All Things Agentic · Devpost · **Aug 31 2026, 5:00pm PDT**
**Track:** Fortified Enterprise Fleet — *"a scalable network of institutional agents"*
**Class:** JUDGED (target is not frozen; score is not a function of attempts) → the run-of-show table runs unchanged.

## The contract

Org-level fleet and prompt management, built on the **transcripto** corpus.
Shows a company what its people actually prompt, which prompts work, who is good at it,
and coaches better prompts **from that org's own best operator**.

## The kill condition — named before the first line of code

**No GCP + no Gemini key by Aug 26.** Not the billing task itself (one hour) — the risk is
tasks downstream of it, run by someone who has never deployed ADK or Cloud Run, compressed
against a one-take video. If Aug 26 passes without them, the entry stops.

*(Gemini alone is NOT blocked: an AI Studio key needs no credit card and enabling billing
actually deletes the free tier. Cloud Run needs `gcloud run deploy --source` — Cloud Build,
so no local Docker and no Colima.)*

## The ladder — all four before building

### 1 · Day-two user named
**Whoever owns the AI rollout** — VP Eng, Head of Platform, Head of Enablement. On day two they
open it to answer the question their exec asked them: *"is this working, and how do we get
better at it?"* They can see seats and spend today. They cannot see **practice**.
Not a judge. ✅

### 2 · Scope calibrated in hours — NEEDS OSCAR'S CALIBRATION
| Slice | Est. |
|---|---|
| Ingest at org scale on the transcripto spine | 6h |
| Prompt-performance signals (loop / abandon / retry / survive) | 10h |
| The people view | 6h |
| The coaching surface — *the wedge* | 10h |
| Cloud Run + Firestore + ADK supervisor | 10h |
| Diagram · stranger pass · video | 10h |
| **Total** | **~52h** |

**PASS requires Oscar's written calibration or an explicit hours ruling.** Agents are
structurally blind to duration and propose scopes systematically too small for a $180K field.
⛔ **OPEN — Oscar must rule.**

### 3 · Expansion path named
- **Second use case:** the same corpus answers *"which of our skills, rules and CLAUDE.md files
  actually change behaviour?"* — MAGNET's job, at org scale.
- **Paying use case:** an AI-rollout owner with hundreds of seats and no evidence of return.
  Budget already exists under dev productivity + enablement.
- **General surface:** the transcript corpus itself. Every feature is a question asked of it,
  so features grow rather than dead-end.
✅

### 4 · Rubric read
Innovation & Operational Utility **40%** (*"friction the agent removes on its own"*) ·
Architectural Discipline & Stack **30%** · Demo & Production Readiness **30%**
(*"unedited, live execution"* + *"visual proof of Google Cloud deployment"*).
Required: Gemini 3.5+ · a Google agent framework · ≥1 GCP service.
Submission: repo URL + architecture diagram + ≤4-min video + text description.
Hosted URL is *"(if available)… highly encouraged"* — **optional**.
✅

## Under-ambition check
The three ideas killed to get here — a claim-checker, a measurement bench, a replication feed —
were each *correct* and each a **feature**. See [[hackathon#THE IDEATION LAW]]. This one is
gated on being a company, not on being defensible.
