# Stranger pass · 29 Aug 2026

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
- No `required check` anywhere in output (branch protection off)

## Probed locally (same repo, 2026-08-29)

```
test_demo.sh
  ok    demo.sh exits 0
  ok    an honest report PASSES
  ok    a false report BLOCKS
  ok    a test claim HOLDS, never guessed
  ok    reads no transcript database
  PASS
```

**Receipt:** `tests/test_demo.sh` grades `./demo.sh`; this doc is the handbook exhibit line.

## Re-verified · 2026-09-01 UTC (night wave)

Fresh shallow clone into `/tmp/stranger-test-witness`, no branch flag, no local config:

```bash
git clone --depth 1 https://github.com/Morkeeth/agent-work-record-witness-ata /tmp/stranger-test-witness
cd /tmp/stranger-test-witness
env -i PATH="$PATH" HOME="$HOME" ./demo.sh
```

**Result:** exit **0**. Verdicts: `GATE: PASS` (honest report) · `GATE: BLOCK` (deadbee + missing path) · `GATE: HOLD` (UNVERIFIABLE test claim). No traceback. Demo ends with live console URL `https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/`.

**Regression gate on workspace `main` after fixture scrub:**

```bash
bash tests/test_demo.sh
```

All checks **PASS**, including `does not say required check anywhere in demo output`.

## Not claimed

- `witness-corpus --db` on a judge machine (needs local transcript DB + `pip install -e .`)
- Live `/hold/` write without token (by design — reads open)

## Oscar addendum (optional)

- [ ] Run on a machine that is not the author dev box
- [ ] Screenshot or log paste below

---

_Log: agent run 2026-08-29 · handbook Phase 5 closure for cold clone path._
_Log: re-verified 2026-09-01 · night wave stranger cold path + required-check scrub in fixture._
