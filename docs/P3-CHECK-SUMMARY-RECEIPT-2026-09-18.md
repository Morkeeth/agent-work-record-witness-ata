# P3 check-run summary · receipt · 2026-09-18

**Slice:** partner depth P3 — `gate/check_run_summary.py` on the Action path.

## Wired on main path?

**Yes.** Composite action `action.yml` step `summary` always runs:

```yaml
- id: summary
  shell: bash
  if: always()
  env:
    GITHUB_TOKEN: ${{ github.token }}
    HEAD_SHA: ${{ inputs.head-sha }}
    REPO: ${{ inputs.repo }}
  run: python3 "$GITHUB_ACTION_PATH/gate/check_run_summary.py"
```

Workflow `.github/workflows/outcome-gate.yml` uses `uses: ./`, so every agent-labelled PR gets it.

## Object proof (PR #1)

```bash
gh pr checks 1
# verify-claims     fail  …/actions/runs/33252027654/job/99099237081
# witness-findings  fail  …/runs/99099248806

gh api repos/Morkeeth/agent-work-record-witness-ata/check-runs/99099248806 \
  --jq '{name,conclusion,title:.output.title,summary:.output.summary}'
```

Measured 2026-09-18:

| Field | Value |
|-------|-------|
| name | `witness-findings` |
| conclusion | `failure` |
| title | `Witness gate: BLOCK` |
| summary | `**BLOCK** — 2 BLOCK · 0 UNVERIFIABLE · 0 PASS` |

## Unit test (this run)

```bash
PYTHONPATH=. python3 tests/test_check_run_summary.py
# all green
```

## Doc status

`docs/PARTNER-REMAINING.md` previously said "coded · push + PR sync". Updated to **live on PR #1** with the check-run id above.
