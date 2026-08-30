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

## Probed cold clone (2026-08-30 · night-wave re-verify)

```bash
cd /tmp && rm -rf witness-stranger-test
git clone --depth 1 https://github.com/Morkeeth/agent-work-record-witness-ata witness-stranger-test
cd witness-stranger-test
env -i PATH="$PATH" HOME="$HOME" ./demo.sh
echo "exit=$?"
```

Output tail:

```
  Honest report PASSED (0). False report BLOCKED (1). Test claim HELD (2).
  ...
      the console      https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/
exit=0
```

Grader (in-repo after pull):

```bash
tests/test_demo.sh
```

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

## Not claimed

- `witness-corpus --db` on a judge machine (needs local transcript DB + `pip install -e .`)
- Live `/hold/` write without token (by design — reads open)

## Oscar addendum (optional)

- [ ] Run on a machine that is not the author dev box
- [ ] Screenshot or log paste below

---

_Log: agent run 2026-08-29 handbook Phase 5 closure · re-verified 2026-08-30 night-wave (cold clone + test_demo.sh 11/11)._
