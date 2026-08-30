# Sealed prediction · ATA · All Things Agentic

**Handbook #72:** write **before** the Devpost submit button. Do not edit after results.

---

## Metadata

| Field | Value |
|-------|--------|
| Event | All Things Agentic Hackathon · Fortified Enterprise Fleet |
| Repo | https://github.com/Morkeeth/agent-work-record-witness-ata |
| Sealed at | **OSCAR_ONLY** — timestamp before submit |
| Deadline | Mon 31 Aug 2026 · 17:00 PDT |
| Agent draft filled | 2026-08-30 UTC (measured anchors below) |

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

> Judge never clicks live URL · field full of GEAP-native fleet managers with richer Memory/Registry stories · our film misses the cold 1/3 eligibility line (after `pip install -r requirements.txt`, not stock Python) · another entry ships the same claim-vs-repo wedge with real adoption numbers.

---

## Measured anchors (probed 2026-08-30 UTC — not carried from notes)

| Anchor | Command | Measured |
|--------|---------|----------|
| Live `/health` | `curl -sS https://fleet-wedge-33kamss2jq-uc.a.run.app/health` | `auth_required: true` · `demo_seed_enabled: false` · `store: firestore` · ADK `constructed: true` · `invoked: false` (per-process) |
| Hero record | `curl -sS …/audit \| jq '.events[] \| select(.id=="H-a6151a95ac")'` | `gate: BLOCK` · `decision: HOLD` · `head_sha: c99589111f82ca4b8a074220cbb5a358b33f5941` · `session: 01Lzbh4XPYTAgCKg1dciFS3Q` · `agent_invoked: true` · `agent_explanation.invoked: true` · `model: gemini-3.5-flash-lite` · 2 BLOCK findings |
| Record counts | `curl -sS …/audit \| jq '[.events[] \| .decision] \| group_by(.) \| map({(.[0]): length})'` | `clear: 0` · `HOLD: 9` · 36 total events · 4 `github-action` rows |
| PR #1 checks | `gh pr view 1 --json statusCheckRollup` | OPEN · `verify-claims` **FAILURE** · `witness-findings` **FAILURE** (P3 check summary live) |
| Stranger demo | `env -i PATH="$PATH" HOME="$HOME" ./demo.sh` | exit **0** · PASS / BLOCK / HOLD verdicts · no network |
| Cold eligibility (no GCP, ADK installed) | `pip install -r requirements.txt && env -i PATH="$PATH" python3 contract/eligibility.py` | **1 OF 3 MET** (ADK only) · exit 1 |
| Cold eligibility (stock Python) | `env -i PATH="$PATH" python3 contract/eligibility.py` (no pip) | **0 OF 3 MET** · exit 1 |
| Preflight | `./film/preflight.sh` | **11/11 PASS** |

**Non-author installs:** zero (unchanged — not re-measurable tonight).

---

## Scoring rubric self-call (pre-submit)

| Criterion | Weight | Our honest score | Why |
|-----------|--------|------------------|-----|
| Innovation & utility | 40% | 7/10 | four verdicts + session join + corpus self-audit; niche is real but adoption is zero |
| Architecture | 30% | 8/10 | local probe · verdict-only network · diagram · eligibility exercised not imported · P3 witness-findings on PR #1 |
| Demo readiness | 30% | 7/10 | `./demo.sh` + live `/hold/` + preflight green; video still Oscar-only |

---

## After results (do not fill before submit)

| Actual | Prediction hit? | Lesson # to distil |
|--------|-----------------|-------------------|
| | | |

---

**OSCAR_ONLY:** final seal timestamp and signature before Devpost button.

**Agent-filled:** placement, primary prediction, confidence, falsifiers, rubric self-call, measured anchors (2026-08-30 night-wave run).

**Draft SHA-256** (body above this line, LF-normalized):

```
6a88a0fc33c823a2df8e39f3626ccd5cd31ddffdc76e760dcc3eb665e255aae1
```
