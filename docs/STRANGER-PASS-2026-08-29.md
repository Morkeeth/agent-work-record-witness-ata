# Stranger pass · refreshed 16 Sep 2026 (film morning)

**Handbook Phase 5:** a stranger attacks the core claim in one click — no wallet, no install, no keys.

---

## One command (README top · cold clone path)

```bash
git clone https://github.com/Morkeeth/agent-work-record-witness-ata
cd agent-work-record-witness-ata
./demo.sh
```

Live URL row (no account):

```
https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/?record=H-a6151a95ac
https://github.com/Morkeeth/agent-work-record-witness-ata/pull/1/checks
```

---

## Command run THIS night (2026-09-16)

```bash
env -i PATH="$PATH" HOME="$HOME" ./demo.sh
# exit 0

./tests/test_demo.sh
```

### `./demo.sh` (verbatim tail)

```
5 · What this demo did not touch
  no network · no API key · no account · no pip install
  no transcript database, no ~/.trace, no file outside this clone
  the repository it probed was /tmp/witness-demo.*/shop, created and deleted by this script

6 · And the gate is not the product
  …
      the console      https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/
      the record       GET /audit
      the artifact     GET /audit/export
```

**Exit code:** `0`

### `tests/test_demo.sh` (verbatim)

```
test_demo.sh
  ok    demo.sh exits 0
  ok    an honest report PASSES  (the check can say yes)
  ok    a false report BLOCKS
  ok    a test claim HOLDS, never guessed
  ok    UNVERIFIABLE finding maps to HOLD gate
  ok    the SHA probe output is shown, not summarised
  ok    the path probe output is shown, not summarised
  ok    does not say required check (branch protection off)
  ok    does not say required check
  ok    reads no transcript database
  ok    no traceback
  PASS
```

**Exit code:** `0`

### Live URL row (probed THIS run)

| URL | Result |
|-----|--------|
| `GET /health` | 200 · `auth_required=true` · `store=firestore` |
| `GET /hold/?record=H-a6151a95ac` | 200 · Playwright: detail opens with session `01Lzbh4XPYTAgCKg1dciFS3Q` |
| PR #1 checks | `verify-claims=FAILURE` · `witness-findings=FAILURE` (red by design) |

---

## Expected

- Exit **0**
- `GATE: PASS` on honest report
- `GATE: BLOCK` on false commit claim
- `GATE: HOLD` on test claim (never guessed)
- No `Traceback` · no `.trace/trace.db` read

## Not claimed

- `witness-corpus --db` on a judge machine (needs local transcript DB + `pip install -e .`)
- Live `/hold/` write without token (by design — reads open)
- Eligibility **3 of 3** on a cold clone (needs ADC). Cold with `pip install -r requirements.txt` and no ADC: **1 of 3**, exit 1. Bare clone with no pip: **0 of 3**.

## Oscar addendum (optional)

- [ ] Run on a machine that is not the author dev box
- [ ] Screenshot or log paste below

---

_Log: agent run 2026-09-16 · stranger path re-verified for film morning · replaces 2026-08-29 exhibit line with THIS run's command output._
