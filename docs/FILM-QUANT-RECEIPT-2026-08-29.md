# Film quant receipt · ATA · 30 Aug 2026

**Runner:** Cloud Agent night-wave (preflight + quant probes)  
**Repo:** `Morkeeth/agent-work-record-witness-ata` @ night-wave branch  
**Live URL:** `https://fleet-wedge-33kamss2jq-uc.a.run.app`  
**Probed at:** 2026-08-30 (UTC)

---

## Summary

| Metric | Result |
|--------|--------|
| Preflight checks | **11 ok / 11 total** |
| `./demo.sh --film` exit code | **0** |
| Voiceover / film beat count | **8** (8 spoken lines = 8 subtitle cues) |
| Hero record `H-a6151a95ac` in `/audit/export` | **yes** · `head_sha=c995891…` · `agent_explanation.invoked=true` |
| PR #1 checks | `verify-claims` **FAILURE** · `witness-findings` **FAILURE** (P3) |
| Live `/health` eligibility fields | `auth_required` · `demo_seed_enabled` · `store` |
| Live `/hold/` Google Material theme | **yes** (`--primary: #1a73e8` · `--sans: "Google Sans"` · `--shadow-1`) |

**Verdict:** PREFLIGHT PASS — safe for Oscar to roll `./film/capture.sh`.

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

## `./demo.sh --film`

| Field | Value |
|-------|-------|
| Exit code | **0** |
| Beat count | **8** (voiceover `film/voiceover.txt` · preflight 8 lines = 8 SRT cues) |
| Verdicts shown | PASS (0) · BLOCK (1) · HOLD (2) |

---

## Hero record · `/audit/export`

| Field | Value |
|-------|-------|
| Record ID | `H-a6151a95ac` |
| Present in export | **yes** |
| Session | `01Lzbh4XPYTAgCKg1dciFS3Q` |

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
- [ ] `docs/SEALED-PREDICTION-2026-08-29.md` Oscar timestamp block (agent draft filled 2026-08-30)
- [ ] Devpost submit
- [ ] Deploy without this receipt

---

*Live service re-probed 2026-08-30 (UTC) · preflight 11/11 PASS*
