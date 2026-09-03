# Stranger pass · 29 Aug 2026 (re-verified 3 Sep 2026)

**Handbook Phase 5:** a stranger attacks the core claim in one click — no wallet, no install, no keys.

---

## Command (stock macOS Python, no network)

```bash
git clone https://github.com/Morkeeth/agent-work-record-witness-ata
cd agent-work-record-witness-ata
env -i PATH="$PATH" HOME="$HOME" ./demo.sh
```

**Live row (no login):** `https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/?record=H-a6151a95ac`

## Expected

- Exit **0**
- `GATE: PASS` on honest report
- `GATE: BLOCK` on false commit claim
- `GATE: HOLD` on test claim (never guessed)
- No `Traceback` · no `.trace/trace.db` read · no `required check` in output

## Probed locally (night wave · 2026-09-03)

```
test_demo.sh
  ok    demo.sh exits 0
  ok    an honest report PASSES
  ok    a false report BLOCKS
  ok    a test claim HOLDS, never guessed
  ok    UNVERIFIABLE finding maps to HOLD gate
  ok    the SHA probe output is shown, not summarised
  ok    the path probe output is shown, not summarised
  ok    does not say required check (branch protection off)
  ok    does not say required check
  ok    fixture and demo output do not leak required check
  ok    reads no transcript database
  ok    no traceback
  PASS
```

**Receipt:** `tests/test_demo.sh` grades `./demo.sh`; this doc is the handbook exhibit line.

## Not claimed

- `witness-corpus --db` on a judge machine (needs local transcript DB + `pip install -e .`)
- Live `/hold/` write without token (by design — reads open)

## Oscar addendum (optional)

- [ ] Run on a machine that is not the author dev box
- [ ] Screenshot or log paste below

---

_Log: agent run 2026-08-29 · handbook Phase 5 closure for cold clone path._
_Log: night wave 2026-09-03 · re-ran `env -i PATH="$PATH" HOME="$HOME" ./demo.sh` (exit 0) and `tests/test_demo.sh` (PASS)._
