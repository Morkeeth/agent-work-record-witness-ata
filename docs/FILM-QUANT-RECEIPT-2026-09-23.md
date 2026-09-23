# Film quant receipt · ATA · 23 Sep 2026

**Runner:** Cloud Agent (night wave · seal + stranger)  
**Repo:** `Morkeeth/agent-work-record-witness-ata` @ `4a45551` (main tip at probe start)  
**Live URL:** `https://fleet-wedge-33kamss2jq-uc.a.run.app`  
**Probed at:** 2026-09-23T00:10–00:15Z

---

## Summary

| Metric | Result |
|--------|--------|
| Preflight checks | **11 ok / 11 total** |
| `./demo.sh` cold (stranger clone) exit | **0** |
| Voiceover / subtitle beat count | **8** = **8** |
| "required check" in `film/voiceover.txt` · `voiceover-vo.txt` · `subtitles.srt` | **0** (`rg` clean) |
| Hero record `H-a6151a95ac` in `/audit/export` | **yes** (events[13]) |
| PR #1 `verify-claims` | **failure** (red by design) |
| PR #1 `witness-findings` (P3) | **failure** (posted) |

**Verdict:** PREFLIGHT PASS — film assets match scrubbed copy; safe for Oscar to roll `./film/capture.sh` when he chooses (this agent did **not** run capture).

---

## Preflight log (verbatim, this run)

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

Command: `git pull origin main && ./film/preflight.sh 2>&1 | tee /tmp/preflight-start.log`

---

## Hero record · `/audit/export` (re-derived)

| Field | Value |
|-------|-------|
| `exported_at` | `2026-09-23T00:12:01+00:00` |
| `n_events` | **25** |
| Record ID | `H-a6151a95ac` |
| `gate` | `BLOCK` |
| `decision` | `HOLD` |
| `open` | `true` |
| `head_sha` | `c99589111f82ca4b8a074220cbb5a358b33f5941` |
| `session` | `01Lzbh4XPYTAgCKg1dciFS3Q` |
| `pr` | `1` |
| `agent_explanation.invoked` | `True` |
| `agent_explanation.model` | `gemini-3.5-flash-lite` |
| Clear-like rows in export | **0** |

---

## PR #1 (asserted at GitHub object)

```
gh pr view 1 --json statusCheckRollup
  verify-claims     conclusion=FAILURE
  witness-findings  conclusion=FAILURE
```

Head OID: `c99589111f82ca4b8a074220cbb5a358b33f5941`

---

## Film spine scrub (EYES B6)

| Asset | "required check" | Notes |
|-------|------------------|-------|
| `film/voiceover.txt` | none | says `verify-claims` · both eligibility numbers |
| `film/voiceover-vo.txt` | none | matches spoken lines |
| `film/subtitles.srt` | none | 8 cues = 8 spoken lines |
| Live `/hold/` Install tab | advisory wording | "do not call it a required check while protection is off" |

---

## P3 check summary

`gate/check_run_summary.py` is on the composite action path (`action.yml` step `summary`).  
PR #1 already carries the `witness-findings` check run. Unit test:

```
PYTHONPATH=. python3 tests/test_check_run_summary.py   # all green (8 PASS)
```

---

## Not done (Oscar)

- [ ] `./film/capture.sh` / screen record ≤4:00
- [ ] Devpost submit
- [ ] Branch protection enable

---

*Prior receipt: `docs/FILM-QUANT-RECEIPT-2026-08-29.md` (superseded for numbers; kept for history).*
