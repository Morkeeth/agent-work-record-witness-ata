# Film quant receipt · ATA · 29 Aug 2026

**Runner:** Cloud Agent (night wave · preflight + quant probes)  
**Repo:** `Morkeeth/agent-work-record-witness-ata` @ `5b97eaf`  
**Live URL:** `https://fleet-wedge-33kamss2jq-uc.a.run.app`  
**Probed at:** 2026-08-29 night (UTC)

---

## Summary

| Metric | Result |
|--------|--------|
| Preflight checks | **11 ok / 11 total** |
| `./demo.sh --film` exit code | **0** |
| Voiceover / film beat count | **8** (8 spoken lines = 8 subtitle cues) |
| Hero record `H-a6151a95ac` in `/audit/export` | **yes** (12 events) |
| Live `/health` eligibility fields | `auth_required` · `demo_seed_enabled` · `store` |
| PR #1 `verify-claims` + `witness-findings` | both **failure** (red by design) |
| `tests/test_demo.sh` | **12/12** ok · PASS |
| `tests/test_check_run_summary.py` | **8/8** · all green |

**Verdict:** PREFLIGHT PASS — safe for Oscar to roll `./film/capture.sh`.

---

## Probe commands (re-run any claim)

```bash
./film/preflight.sh
env -i PATH="$PATH" HOME="$HOME" ./demo.sh
curl -sS https://fleet-wedge-33kamss2jq-uc.a.run.app/health | python3 -m json.tool
curl -sS https://fleet-wedge-33kamss2jq-uc.a.run.app/audit/export | python3 -c \
  "import json,sys; ev=json.load(sys.stdin).get('events',[]); print(len(ev),'events'); print(any(e.get('id')=='H-a6151a95ac' for e in ev))"
gh api repos/Morkeeth/agent-work-record-witness-ata/commits/$(gh pr view 1 --json headRefOid -q .headRefOid)/check-runs \
  --jq '.check_runs[] | {name, conclusion}'
PYTHONPATH=. python3 tests/test_check_run_summary.py
```

---

## Preflight checks (named)

| # | Check | Result |
|---|-------|--------|
| 1 | Canonical numbers in voiceover + `docs/SUBMISSION.md` (78,618 · 41.7 · 8.1) | **PASS** |
| 2 | `/hold/` console on-camera surface (41.7 ? 8.1 · `H-a6151a95ac` · finding + stack tabs) | **PASS** |
| 3 | Voiceover lines vs subtitle blocks (8 = 8) | **PASS** |
| 4 | `./demo.sh` cold, no network | **PASS** |
| 5 | `demo.sh` exit 0 | **PASS** |
| 6 | `/health` live payload | **PASS** |
| 7 | Record row `H-a6151a95ac` probe | **PASS** |
| 8 | Record `H-a6151a95ac` present in export | **PASS** |
| 9 | PR #1 verify-claims red-by-design probe | **PASS** |
| 10 | PR #1 open | **PASS** |
| 11 | `verify-claims` conclusion = `failure` (asserted at object) | **PASS** |

**Note (non-blocking):** `.hold_api_token` missing locally — create before live break-glass on camera.

---

## Voiceover / subtitles scrub

| Check | Result |
|-------|--------|
| `grep -i "required check" film/voiceover.txt film/subtitles.srt` | **0 matches** |
| Moat line present | "None of them holds the transcript." |
| Eligibility line | "three of three with credentials here; one of three on a cold clone without GCP" |

---

## Hero record · `/audit/export`

| Field | Value |
|-------|-------|
| Record ID | `H-a6151a95ac` |
| Present in export | **yes** |
| `gate` | `BLOCK` |
| `head_sha` | `c99589111f82ca4b8a074220cbb5a358b33f5941` |
| Session | `01Lzbh4XPYTAgCKg1dciFS3Q` |
| `agent_explanation.invoked` | `true` |
| `agent_explanation.model` | `gemini-3.5-flash-lite` |

---

## Live `/health` · eligibility fields

Probe: `GET https://fleet-wedge-33kamss2jq-uc.a.run.app/health`

| Field | Value | Eligibility meaning |
|-------|-------|---------------------|
| `auth_required` | `true` | Writes gated · anon probe closed |
| `demo_seed_enabled` | `false` | No demo seed on live surface |
| `store` | `firestore` | GCP Firestore default store |

Additional payload (informational): `product` = THE AGENT WORK RECORD WITNESS · `ok` = true · ADK agent constructed.

---

## Preflight log (verbatim)

```
ok: checking canonical numbers in voiceover + SUBMISSION.md
ok: hold console carries 41.7 -> 8.1, H-a6151a95ac, finding + stack screens
ok: 8 spoken lines match 8 subtitle blocks
ok: ./demo.sh (cold, no network)
ok: demo.sh exit 0
ok: /health live payload
  health fields match
ok: record row H-a6151a95ac
ok: record H-a6151a95ac present
  note: .hold_api_token missing — create before live break-glass on camera (read probe passed without it)
ok: PR #1 verify-claims red-by-design
ok: PR #1 open
ok: verify-claims conclusion=failure (red by design, asserted at the object)

PREFLIGHT PASS — safe to run ./film/capture.sh and record.
```

---

## Not done (Oscar / post-receipt)

- [ ] Screen recording ?4:00
- [ ] `docs/SEALED-PREDICTION-2026-08-29.md` Oscar timestamp block (draft filled + hashed)
- [ ] Devpost submit
- [ ] Deploy without this receipt

---

*Live revision `fleet-wedge-00012-5w6` · re-probed 2026-08-29 night (UTC)*
