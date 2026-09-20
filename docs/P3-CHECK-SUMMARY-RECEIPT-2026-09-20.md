# P3 check-run summary · receipt · 2026-09-20

**What:** `gate/check_run_summary.py` posts a GitHub Checks API run named `witness-findings`
(plus job summary + annotations) after the probe. Wired in the composite action at
`action.yml` step `summary` (`if: always()`).

**Main path:** `.github/workflows/outcome-gate.yml` → `uses: ./` → `action.yml` →
`python3 …/gate/check_run_summary.py`.

---

## Verified at the object (this run)

| Check | Command | Result |
|-------|---------|--------|
| Unit | `PYTHONPATH=. python3 tests/test_check_run_summary.py` | **all green** (8 PASS) |
| On PR #1 | `gh pr checks 1` | `witness-findings` **fail** (red by design, same as verify-claims) |
| Checks API body | `gh api repos/…/commits/<head>/check-runs` | title `Witness gate: BLOCK` · summary `**BLOCK** — 2 BLOCK · 0 UNVERIFIABLE · 0 PASS` |

Head SHA asserted: `c99589111f82ca4b8a074220cbb5a358b33f5941` (from PR #1 rollup + hero record).

---

## Judge-facing one-liner

The red check a judge opens on PR #1 is not only `verify-claims`. P3 adds
`witness-findings` with a markdown table of each probe verdict — same gate decision,
readable without opening the workflow log.

---

_Night wave 2026-09-20 · no code change required; was already on the action path; this receipt closes the "wire + document" slice._
