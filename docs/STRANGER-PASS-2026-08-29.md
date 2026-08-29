# Stranger pass · 29 Aug 2026

**Handbook Phase 5:** a stranger attacks the core claim in one click — no wallet, no install, no keys.

---

## Command (stock macOS Python, no network)

```bash
git clone https://github.com/Morkeeth/agent-work-record-witness-ata && cd agent-work-record-witness-ata && ./demo.sh
```

Shorthand (same verdicts, prints live row URL):

```bash
git clone https://github.com/Morkeeth/agent-work-record-witness-ata && cd agent-work-record-witness-ata && ./demo.sh && echo "Live row: https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/?record=H-a6151a95ac"
```

## Expected

- Exit **0**
- `GATE: PASS` on honest report
- `GATE: BLOCK` on false commit claim
- `GATE: HOLD` on test claim (never guessed)
- No `Traceback` · no `.trace/trace.db` read · no `required check` in output

## Probed locally (cold clone, 2026-08-29 night wave)

Fresh clone to `/tmp/stranger-test-witness`, then `env -i PATH="$PATH" HOME="$HOME" ./demo.sh`:

```
GATE: PASS — every claim confirmed against the repo.
GATE: BLOCK — 2 claim(s) the repo disproves. Do not auto-merge.
GATE: HOLD — finding UNVERIFIABLE (gate holds; probe never runs commands from a report).
Honest report PASSED (0). False report BLOCKED (1). Test claim HELD (2).
exit 0
```

`tests/test_demo.sh` on same commit (`5b97eaf`):

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
  ok    does not print required check anywhere (branch protection off)
  ok    reads no transcript database
  ok    no traceback
  PASS
```

**Receipt:** `tests/test_demo.sh` grades `./demo.sh` (12 assertions); this doc is the handbook exhibit line.

## Not claimed

- `witness-corpus --db` on a judge machine (needs local transcript DB + `pip install -e .`)
- Live `/hold/` write without token (by design — reads open)

## Oscar addendum (optional)

- [ ] Run on a machine that is not the author dev box
- [ ] Screenshot or log paste below

---

_Log: agent run 2026-08-29 night wave · cold clone re-verified · handbook Phase 5 closure._
