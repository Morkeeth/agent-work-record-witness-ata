# Stranger pass · 22 Sep 2026 (night wave)

**Handbook Phase 5:** a stranger attacks the core claim in one click — no wallet, no install, no keys.

Replaces the exhibit line in [`STRANGER-PASS-2026-08-29.md`](STRANGER-PASS-2026-08-29.md) with output from **this run**.

---

## One command (stock Python, no network)

```bash
git clone https://github.com/Morkeeth/agent-work-record-witness-ata
cd agent-work-record-witness-ata
env -i PATH="$PATH" HOME="$HOME" ./demo.sh
```

Then open the live row:

- Hold queue: https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/?tab=queue
- PR #1 checks: https://github.com/Morkeeth/agent-work-record-witness-ata/pull/1/checks

---

## Probed this run (2026-09-22T00:12Z UTC)

| Field | Value |
|-------|--------|
| Host | cloud agent VM |
| Clone commit | measured at `/tmp/stranger-witness-pass` from `origin/main` at pull time |
| Command | `env -i PATH="$PATH" HOME="$HOME" ./demo.sh` |
| Exit | **0** |
| Verdicts | honest report **PASS (0)** · false report **BLOCK (1)** · test claim **HOLD (2)** |
| Network | none (env stripped) |
| Traceback | none |
| Phrase `"required check"` in demo stdout | **absent after fixture scrub** (was present via `fixtures/agent-false-done-PR-BODY.md` header — caught by tightened `tests/test_demo.sh`) |

### Verbatim tail (this run)

```
  Honest report PASSED (0). False report BLOCKED (1). Test claim HELD (2).

  Finding-level verdicts: PASS · BLOCK · UNVERIFIABLE.
  Gate-level outcomes:    PASS · BLOCK · HOLD (HOLD means UNVERIFIABLE, nothing BLOCKed).

  ...
  no network · no API key · no account · no pip install
  ...
      the console      https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/
EXIT:0
```

### Graded

```
$ bash tests/test_demo.sh
test_demo.sh
  ok    demo.sh exits 0
  ok    an honest report PASSES
  ok    a false report BLOCKS
  ok    a test claim HOLDS, never guessed
  ok    UNVERIFIABLE finding maps to HOLD gate
  ok    the SHA probe output is shown, not summarised
  ok    the path probe output is shown, not summarised
  ok    does not say required check (branch protection off)
  ok    reads no transcript database
  ok    no traceback
  PASS
```

---

## Baseline arm (naive, two hours, no gate)

Same shop-shaped claims a competent person checks by hand:

| Claim | Naive command | Result this run |
|-------|---------------|-----------------|
| `committed as deadbee` | `git cat-file -t deadbee` | exit 128 · `fatal: Not a valid object name` |
| `wrote docs/auth-migration-2026.md` | `test -f docs/auth-migration-2026.md` | exit 1 |

**Finding:** the naive arm catches both BLOCK claims. What it does not do — and what `./demo.sh` shows — is refuse `"all 14 tests pass"` as **UNVERIFIABLE** (never runs a command from the report) and write a durable record with session join. If the pitch is "we catch false SHAs," the baseline ties us. If the pitch is "refuse what you cannot check, and keep the receipt," the baseline has no answer.

---

## Eligibility honesty (re-derived at the object, same night)

Do **not** pipe without `pipefail` — `| tee` made exit 0 look green while `n < 3`.

| Arm | Command shape | Measured | Exit |
|-----|---------------|----------|------|
| Pip-free cold | `PYTHONNOUSERSITE=1 python3 contract/eligibility.py` | **0 OF 3 MET** | **1** |
| ADK installed, no ADC | `python3 contract/eligibility.py` (user site has `google-adk`) | **1 OF 3 MET** | **1** |
| ADC + Firestore + Vertex | not available on this VM (`gcloud` missing, no ADC file) | **unmeasured tonight** | — |

Docs that said only "1 of 3 cold" were wrong for a pip-free clone. Corrected in README + SUBMISSION-PACK this night.

---

## Not claimed

- Live `/hold/` write without token (by design — reads open)
- Rewriting the live Firestore `report_preview` on `H-a6151a95ac` (still carries the pre-scrub fixture header until a new clearance is posted — Oscar token)
- `witness-corpus` without `pip install`

---

_Log: night wave 2026-09-22 · stranger cold path re-verified at the object._
