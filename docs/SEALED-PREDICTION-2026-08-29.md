# Sealed prediction · ATA · All Things Agentic

**Handbook #72:** write **before** the Devpost submit button. Do not edit after results.

---

## Metadata

| Field | Value |
|-------|--------|
| Event | All Things Agentic Hackathon · Fortified Enterprise Fleet |
| Repo | https://github.com/Morkeeth/agent-work-record-witness-ata |
| Sealed at | **2026-08-29T20:52:00Z** — agent draft (Oscar signs before submit) |
| Deadline | Mon 31 Aug 2026 · 17:00 PDT |
| Probed commit | `5b97eaf` (main after pull) |

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

## Measured at object (2026-08-29 night wave)

Probed live — not carried from docs.

| Probe | Command | Measured |
|-------|---------|----------|
| Live health | `curl -sS https://fleet-wedge-33kamss2jq-uc.a.run.app/health` | `auth_required: true` · `demo_seed_enabled: false` · `store: firestore` · ADK `constructed: true` · product name full |
| Audit export | `curl -sS …/audit/export \| python3 -c '…'` | **12 events** · **0 clear** · hero `H-a6151a95ac` present |
| Hero record | same export, id filter | `gate: BLOCK` · `decision: HOLD` · **2 BLOCK** findings · `agent_invoked: true` · `head_sha: c99589111f82…` · `pr: 1` · `stored_at: 2026-08-29T12:15:09Z` |
| PR #1 checks | `gh pr view 1 --json statusCheckRollup` | `verify-claims` → **FAILURE** · `witness-findings` (P3) → **FAILURE** · PR **OPEN** |
| Stranger demo | `env -i PATH="$PATH" HOME="$HOME" ./demo.sh` | exit **0** · PASS / BLOCK / HOLD shown |
| Demo receipt | `bash tests/test_demo.sh` | **PASS** (11 assertions) |
| P3 unit | `PYTHONPATH=. python3 tests/test_check_run_summary.py` | **PASS** (8 assertions) |
| Preflight | `./film/preflight.sh 2>&1 \| tail -5` | **PREFLIGHT PASS** (11/11) |
| Eligibility cold | `env -i PATH="$PATH" HOME="$HOME" python3 contract/eligibility.py` | **0 OF 3** (no `google-adk` on bare clone) · exit **1** |
| Eligibility + ADK only | after `pip install google-adk`, same cold env | **1 OF 3** (ADK constructed) · exit **1** |
| Eligibility live path | `/health` fields above | Firestore + ADK on deployed service ≡ **3/3 on the path judges click** |

**Honest ceiling numbers for film/Devpost:** say **3/3 with ADC on deployed `/health`** and **0–1/3 on cold `eligibility.py`** depending on whether the clone has `google-adk` installed — never unqualified "3 of 3".

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
**Agent-filled:** placement, primary prediction, confidence, falsifiers, rubric self-call, measured-at-object table (2026-08-29 night wave).

**Draft SHA-256:** `20dbf954597b41956a8e4b0b05b31bb21b11663f2965995c2a5229617c681ac8`
