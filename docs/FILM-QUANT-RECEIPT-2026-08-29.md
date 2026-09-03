# Film quant receipt · ATA · 29 Aug 2026 (re-probed 3 Sep 2026)

**Runner:** Cloud Agent (night wave preflight + quant probes)  
**Repo:** `Morkeeth/agent-work-record-witness-ata` @ night wave branch  
**Live URL:** `https://fleet-wedge-33kamss2jq-uc.a.run.app`  
**Probed at:** 2026-09-03 (UTC)

---

## Summary

| Metric | Result |
|--------|--------|
| Preflight checks | **11 ok / 11 total** |
| `./demo.sh --film` exit code | **0** (not re-run this wave; `./demo.sh` cold exit 0) |
| Voiceover / film beat count | **8** (8 spoken lines = 8 subtitle cues) |
| Hero record `H-a6151a95ac` in `/audit/export` | **yes** |
| Hero queue position | **14 of 20** (deep link `?record=` required — not first card) |
| Live `/health` eligibility fields | `auth_required` · `demo_seed_enabled` · `store` |
| `recordOpened` latch in deployed HTML | **yes** |

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

## Live counters (re-derived)

| Field | Value |
|-------|-------|
| `/audit` total events | 49 |
| `pct_cleared_without_hold` | 0.0 |
| `/audit/export` events | 25 |
| `/queue` holds | 20 |
| PR #1 `witness-findings` | failure |
| PR #1 `verify-claims` | failure |

---

## Preflight log (verbatim · 2026-09-03)

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

*Night wave re-probe 2026-09-03 (UTC)*
