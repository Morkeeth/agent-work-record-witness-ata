# P3 · check run summary · receipt · 22 Sep 2026

**Claim:** `gate/check_run_summary.py` is on the install path and produces the
`witness-findings` check judges see on PR #1.

---

## Wiring (repo object)

| Location | What |
|----------|------|
| `action.yml` → step `summary` | `python3 "$GITHUB_ACTION_PATH/gate/check_run_summary.py"` · `if: always()` |
| Env | `GITHUB_TOKEN` · `HEAD_SHA` · `REPO` · `HOLD_FINDINGS` (exported from probe; also written to `GITHUB_ENV`) |
| Check name | `witness-findings` |

**Fix this night:** the probe step used to read `os.environ["HOLD_FINDINGS"]` in the
**same** step that only wrote it to `GITHUB_ENV` (which reaches *later* steps). That is
the import-is-not-call shape. Probe now reads the shell `FINDINGS` path it just wrote,
`export`s `HOLD_FINDINGS` for the current step, and the summary step takes
`HOLD_FINDINGS: ${{ env.HOLD_FINDINGS }}` explicitly.

---

## Unit test (this run)

```
$ PYTHONPATH=. python3 tests/test_check_run_summary.py
  PASS  BLOCK conclusion
  PASS  HOLD conclusion
  PASS  PASS conclusion
  PASS  title has gate
  PASS  summary counts BLOCK
  PASS  text has table
  PASS  text has honesty line
  PASS  load_findings
all green
```

---

## Live object · PR #1

```
$ gh pr view 1 --json statusCheckRollup
verify-claims     conclusion=FAILURE
witness-findings  conclusion=FAILURE

$ gh api repos/Morkeeth/agent-work-record-witness-ata/check-runs/99099248806
name: witness-findings
conclusion: failure
output.title: "Witness gate: BLOCK"
output.summary: "**BLOCK** — 2 BLOCK · 0 UNVERIFIABLE · 0 PASS"
html_url: https://github.com/Morkeeth/agent-work-record-witness-ata/runs/99099248806
```

P3 is not "coded only" — the check exists on the red-by-design PR with a summary built
by this module.

---

## Still Oscar / next PR

Re-running outcome-gate on PR #1 after merge of the `HOLD_FINDINGS` fix will prove the
same-step export path end-to-end. Not done tonight (no outward sync of the demo PR).
