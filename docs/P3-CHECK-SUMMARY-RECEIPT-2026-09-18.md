# P3 · check run summary · receipt · 18 Sep 2026

**Module:** `gate/check_run_summary.py`  
**Wired on main path:** `action.yml` step `id: summary` → `python3 "$GITHUB_ACTION_PATH/gate/check_run_summary.py"`  
**Workflow:** `.github/workflows/outcome-gate.yml` uses `./` (composite action).

---

## Unit test (this run)

```bash
PYTHONPATH=. python3 tests/test_check_run_summary.py
# → all green (8 PASS)
```

## Live object (PR #1)

```bash
gh pr checks 1
# verify-claims     fail
# witness-findings  fail

gh api repos/Morkeeth/agent-work-record-witness-ata/commits/c99589111f82ca4b8a074220cbb5a358b33f5941/check-runs
# witness-findings id=99099248806 conclusion=failure
#   output.title   = "Witness gate: BLOCK"
#   output.summary = "**BLOCK** — 2 BLOCK · 0 UNVERIFIABLE · 0 PASS"
```

P3 is not aspirational: the Checks API check named `witness-findings` is present on the film PR and carries the markdown builder's title/summary shape.

---

## README pointer

Judge path already shows PR checks URL. P3 is the `witness-findings` row beside `verify-claims`.
