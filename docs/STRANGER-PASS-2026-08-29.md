# Stranger pass · 30 Aug 2026

**Handbook Phase 5:** a stranger attacks the core claim in one click — no wallet, no install, no keys.

---

## Command (stock macOS Python, no network)

```bash
git clone https://github.com/Morkeeth/agent-work-record-witness-ata
cd agent-work-record-witness-ata
env -i PATH="$PATH" HOME="$HOME" ./demo.sh
```

## Expected

- Exit **0**
- `GATE: PASS` on honest report
- `GATE: BLOCK` on false commit claim
- `GATE: HOLD` on test claim (never guessed)
- No `Traceback` · no `.trace/trace.db` read
- No "required check" in output (branch protection off)

## Probed locally (2026-08-30 night-wave)

**Cold clone** (`/tmp/stranger-test-50c5`, depth 1):

```
Cloning into 'stranger-test-50c5'...
…
  GATE: PASS — every claim confirmed against the repo.
…
  GATE: BLOCK — 2 claim(s) the repo disproves. Do not auto-merge.
…
  GATE: HOLD — finding UNVERIFIABLE (gate holds; probe never runs commands from a report).
…
  Honest report PASSED (0). False report BLOCKED (1). Test claim HELD (2).
```

Exit code: **0**

**In-repo harness** (`env -i PATH="$PATH" HOME="$HOME" ./tests/test_demo.sh`):

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

**Live row** (read-only, no token): https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/?record=H-a6151a95ac

## Not claimed

- `witness-corpus --db` on a judge machine (needs local transcript DB + `pip install -e .`)
- Live `/hold/` write without token (by design — reads open)
- `python3 contract/eligibility.py` on stock Python without `pip install -r requirements.txt` (prints 0/3, not 1/3)

## Oscar addendum (optional)

- [ ] Run on a machine that is not the author dev box
- [ ] Screenshot or log paste below

---

_Log: agent run 2026-08-30 · night-wave re-verification · handbook Phase 5 closure for cold clone path._
