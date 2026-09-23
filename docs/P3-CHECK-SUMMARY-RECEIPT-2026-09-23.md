# P3 · Check run summary — on the main path

**Probed:** 2026-09-23 · night wave

## Where it lives

| Piece | Path | Role |
|-------|------|------|
| Builder | `gate/check_run_summary.py` | Step summary + Annotations + optional Checks API `witness-findings` |
| Wire | `action.yml` step `id: summary` | `python3 "$GITHUB_ACTION_PATH/gate/check_run_summary.py"` after the gate, `if: always()` |
| Dogfood | `.github/workflows/outcome-gate.yml` | `uses: ./` — customers get the same twelve lines |
| Test | `tests/test_check_run_summary.py` | conclusions + markdown shape |

## Done-when (ran)

```bash
PYTHONPATH=. python3 tests/test_check_run_summary.py
#   PASS  BLOCK conclusion
#   PASS  HOLD conclusion
#   PASS  PASS conclusion
#   PASS  title has gate
#   PASS  summary counts BLOCK
#   PASS  text has table
#   PASS  text has honesty line
#   PASS  load_findings
# all green
```

```bash
gh pr view 1 --json statusCheckRollup --jq '.statusCheckRollup[] | {name,conclusion}'
# {"conclusion":"FAILURE","name":"verify-claims"}
# {"conclusion":"FAILURE","name":"witness-findings"}
```

`witness-findings` on PR #1 is the live object proof that P3 posted — not a doc claim.

## What it does not do

- Does not enable branch protection.
- Does not rename the check to "required."
- Skips Checks API post when `GITHUB_TOKEN` / `REPO` / `HEAD_SHA` are incomplete (local dry runs still get step summary + annotations when in Actions).
