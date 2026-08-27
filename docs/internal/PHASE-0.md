# Phase 0 — the entry gate

**Event:** All Things Agentic · Devpost · **Aug 31 2026, 5:00pm PDT**
**Track:** Fortified Enterprise Fleet — *"a scalable network of institutional agents"*
**Class:** JUDGED (target is not frozen; score is not a function of attempts) → the run-of-show table runs unchanged.

## The contract

Org-level fleet and prompt management, built on the **transcripto** corpus.
Shows a company what its people actually prompt, which prompts work, who is good at it,
and **propagates** the best operator's prompt into the org skill file — by the ADK supervisor,
unattended. See `docs/WEDGE.md`.

## The kill condition — named before the first line of code

**No GCP + no Gemini key by Aug 26.** Not the billing task itself (one hour) — the risk is
tasks downstream of it, run by someone who has never deployed ADK or Cloud Run, compressed
against a one-take video. If Aug 26 passes without them, the entry stops.

*(Gemini alone is NOT blocked: an AI Studio key needs no credit card and enabling billing
actually deletes the free tier. Cloud Run needs `gcloud run deploy --source` — Cloud Build,
so no local Docker and no Colima.)*

**Probe 2026-08-22:** ADC no · gcloud project none · GEMINI_API_KEY unset · **4 days left.**

## The ladder — all four before building

### 1 · Day-two user named
**Whoever owns the AI rollout** — VP Eng, Head of Platform, Head of Enablement. On day two they
open it to answer the question their exec asked them: *"is this working, and how do we get
better at it?"* They can see seats and spend today. They cannot see **practice**.
Not a judge. ✅

### 2 · Scope calibrated in hours
| Slice | Est. | Video-critical? |
|---|---|---|
| Ingest + `is_human` gate on transcripto spine | 6h | yes |
| One performance signal (survive vs abandon) | 10h | yes |
| Agent propagation (ADK + 3 tools) — *the wedge* | 10h | **yes** |
| People view (thin OK) | 6h | stretch |
| Cloud Run + Firestore + ADK supervisor | 10h | yes |
| Diagram · stranger pass · video | 10h | yes |
| **Total** | **~52h** | |

**Oscar calibration (Aug 22, post-EYES):** 52h is the **floor**, not the ceiling. Primary time
for 9 days (~6h/day). Submission-critical path = rows marked yes above (see `docs/WEDGE.md`).
People view and full org multi-seat ingest are stretch — not cut from the vision, sequenced after
the one loop ships. Cloud Run + billing **must land by Aug 26** (10h slice pulled forward).
Diagram + stranger + video starts Aug 28 earliest. Under-ambition is the risk, not overrun —
but the video shows **one unattended propagation loop**, not five half dashboards.

✅

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

## EYES panel (Aug 22)

Unanimous **HOLD → proceed with reframe.** Full synthesis in `CURSOR-LOG.md`. Key change:
Surface 5 must show the **agent acting** (propagate + prove), not a coaching card.

## Under-ambition check
The three ideas killed to get here — a claim-checker, a measurement bench, a replication feed —
were each *correct* and each a **feature**. See [[hackathon#THE IDEATION LAW]]. This one is
gated on being a company, not on being defensible.

## Phase 0 status

**PASS** — all four ladder rungs climbed. Phase 1 spec extract: `docs/SPEC-EXTRACT.md`.
