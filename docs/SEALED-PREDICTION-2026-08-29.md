# Sealed prediction · ATA · All Things Agentic

**Handbook #72:** write **before** the Devpost submit button. Do not edit after results.

---

## Metadata

| Field | Value |
|-------|--------|
| Event | All Things Agentic Hackathon · Fortified Enterprise Fleet |
| Repo | https://github.com/Morkeeth/agent-work-record-witness-ata |
| Sealed at | **AGENT_DRAFT** — 2026-08-29 night wave (Oscar timestamp before submit) |
| Probed commit | `5b97eafd4266ab66f970e69f69d95d1cdd1698dc` |
| Deadline | Mon 31 Aug 2026 · 17:00 PDT |

---

## Prediction (fill before submit)

**Placement:**

- [ ] Grand / category winner ($20K Fortified Enterprise Fleet)
- [ ] Architectural Design ($5K)
- [x] Honorable Mention ($2K)
- [ ] No prize · top quartile demo
- [ ] No prize · learning run

**Primary prediction (one sentence):**

> Top-five demo in Fortified Enterprise Fleet on honesty + live proof + cold stranger `./demo.sh`; not grand — zero non-author installs and PR #1 red-by-design cap the ceiling.

**Confidence:** med

**What would falsify it:**

> Judge never clicks live URL · field full of GEAP-native fleet managers with richer Memory/Registry stories · our film misses the cold 1/3 eligibility line · another entry ships the same claim-vs-repo wedge with real adoption numbers.

---

## Live evidence (measured at object · 2026-08-29 night)

Probes run on Cloud Agent VM against live Cloud Run + GitHub API. Commands in
[`docs/FILM-QUANT-RECEIPT-2026-08-29.md`](FILM-QUANT-RECEIPT-2026-08-29.md).

### `/health` · `GET https://fleet-wedge-33kamss2jq-uc.a.run.app/health`

| Field | Measured |
|-------|----------|
| `ok` | `true` |
| `product` | `THE AGENT WORK RECORD WITNESS` |
| `auth_required` | `true` |
| `demo_seed_enabled` | `false` |
| `store` | `firestore` |
| `agent.class` | `google.adk.agents.llm_agent.LlmAgent` |
| `agent.constructed` | `true` |
| `agent.invoked` | `false` (health probe only) |

### Anon write gates

| Route | HTTP |
|-------|------|
| `POST /clearance` (no token) | **401** |
| `POST /break-glass` (no token) | **401** |

### Hero record · `GET /audit/export` → `H-a6151a95ac`

| Field | Measured |
|-------|----------|
| Present in export | **yes** (12 events total) |
| `gate` | `BLOCK` |
| `head_sha` | `c99589111f82ca4b8a074220cbb5a358b33f5941` |
| `session_id` | `01Lzbh4XPYTAgCKg1dciFS3Q` |
| `agent_explanation.invoked` | `true` |
| `agent_explanation.model` | `gemini-3.5-flash-lite` |

### PR #1 · `Morkeeth/agent-work-record-witness-ata` (open)

| Check | Conclusion |
|-------|------------|
| `verify-claims` | **failure** (red by design · `deadbee` not a commit) |
| `witness-findings` | **failure** (P3 summary check) |
| Head SHA | `c99589111f82ca4b8a074220cbb5a358b33f5941` |

### Cold stranger path · fresh clone

| Probe | Result |
|-------|--------|
| `env -i PATH="$PATH" HOME="$HOME" ./demo.sh` | exit **0** |
| `tests/test_demo.sh` | **11/11** ok · PASS |
| `./film/preflight.sh` | **11/11** ok · PREFLIGHT PASS |

### Eligibility honesty (both numbers matter on film)

| Path | Measured this run |
|------|-------------------|
| Live `/health` | Firestore + ADK constructed on deployed path |
| `python3 contract/eligibility.py` on this VM (no ADC, no `google-adk`) | **0 OF 3 MET**, exit 1 |
| Documented cold clone with stock Python + `pip install -e .` | **1 OF 3** (ADK only) per SUBMISSION-PACK |

Say **both** 3/3 (ADC) and 1/3 (cold) on film — never unqualified "3 of 3".

---

## Scoring rubric self-call (pre-submit)

| Criterion | Weight | Our honest score | Why |
|-----------|--------|------------------|-----|
| Innovation & utility | 40% | 7/10 | four verdicts + session join + corpus self-audit; niche is real but adoption is zero |
| Architecture | 30% | 8/10 | local probe · verdict-only network · diagram · eligibility exercised not imported |
| Demo readiness | 30% | 7/10 | `./demo.sh` + live `/hold/` + preflight green; video still Oscar-only |

---

## After results (do not fill before submit)

| Actual | Prediction hit? | Lesson # to distil |
|--------|-----------------|-------------------|
| | | |

---

**OSCAR_ONLY:** final seal timestamp and signature before Devpost button.  
**Agent-filled:** placement, primary prediction, confidence, falsifiers, rubric self-call, live evidence table (2026-08-29 night wave).

---

**Draft SHA-256** (body above this line, excluding this footer): `6a8d4f90b234851e261162d4c4a5dedcce7b5bc4756f23db04ff839170376a5d`
