# Sealed prediction · ATA · All Things Agentic

**Handbook #72:** write **before** the Devpost submit button. Do not edit after results.

---

## Metadata

| Field | Value |
|-------|--------|
| Event | All Things Agentic Hackathon · Fortified Enterprise Fleet |
| Repo | https://github.com/Morkeeth/agent-work-record-witness-ata |
| Sealed at | **OSCAR_ONLY** — timestamp before submit |
| Agent draft filled | **2026-08-30 UTC** (measured numbers below) |
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

## Measured anchors (probed 2026-08-30 · not carried from docs)

Commands run on Cloud Agent VM against live service + GitHub object:

| Anchor | Measured | Command |
|--------|----------|---------|
| Preflight | **11/11 PASS** | `./film/preflight.sh` |
| `./demo.sh` cold | **exit 0** | `env -i PATH="$PATH" HOME="$HOME" ./demo.sh` |
| `tests/test_demo.sh` | **11/11 PASS** | `tests/test_demo.sh` |
| Stranger cold clone | **exit 0** | `git clone … && env -i PATH="$PATH" HOME="$HOME" ./demo.sh` |
| Live `/health` store | **firestore** | `curl -sS …/health \| jq .store` |
| Live auth gate | **auth_required: true** | `curl -sS …/health \| jq .auth_required` |
| Demo seed off | **demo_seed_enabled: false** | `curl -sS …/health \| jq .demo_seed_enabled` |
| Anon `POST /clearance` | **401** | `curl -sS -o /dev/null -w '%{http_code}' -X POST …/clearance` |
| Audit **clear** count | **0** | `curl -sS …/audit \| jq '[.events[] \| select(.decision=="CLEAR" or .gate=="PASS")] \| length'` |
| Audit total events | **36** | `curl -sS …/audit \| jq '.events \| length'` |
| Hero record | **H-a6151a95ac** present | `curl -sS …/audit/export \| jq 'any(.events[]; .id=="H-a6151a95ac")'` |
| Hero gate / decision | **BLOCK / HOLD** | same export, `.gate` + `.decision` |
| Hero session join | **01Lzbh4XPYTAgCKg1dciFS3Q** | same export, `.session` |
| Hero agent invoked | **true** (gemini-3.5-flash-lite) | same export, `.agent_explanation.invoked` |
| PR #1 state | **OPEN** | `gh pr view 1 --json state` |
| PR #1 `verify-claims` | **conclusion=failure** | `gh api repos/…/commits/<head>/check-runs --jq '…verify-claims…'` |
| PR #1 `witness-findings` | **conclusion=failure** | same check-runs API |
| `/hold/` page title | **THE AGENT WORK RECORD WITNESS** | `curl -sS …/hold/ \| grep '<title>'` |
| Non-author installs | **0** | honest-state table in SUBMISSION-PACK §3 (not re-counted tonight) |
| Local `eligibility.py` (this VM) | **0 OF 3 MET, exit 1** | `python3 contract/eligibility.py` — no google-adk, no ADC |

Live URL: `https://fleet-wedge-33kamss2jq-uc.a.run.app`

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

**Agent-filled:** placement, primary prediction, confidence, falsifiers, rubric self-call, measured anchors (2026-08-30 night-wave run).

**Draft SHA-256** (content above this line, UTF-8, LF endings):

```
b9f29219ccdf95d484c82869c0b2cb06d3885228a82d874d965175a9abe266e5
```
