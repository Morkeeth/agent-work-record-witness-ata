# Stranger pass · 29 Aug 2026 (re-verified 31 Aug 2026)

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

## Probed locally (night wave · 2026-08-31 UTC · repo @ `4a45551`)

```
$ env -i PATH="$PATH" HOME="$HOME" ./demo.sh
  … honest report PASSED (0) · false report BLOCKED (1) · test claim HELD (2) …
  Live instance and the full picture: README.md, and docs/ARCHITECTURE.md.
$ echo $?
0

$ tests/test_demo.sh
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

**Receipt:** `tests/test_demo.sh` grades `./demo.sh`; this doc is the handbook exhibit line.

## Live row (after `./demo.sh`)

Open the held record the demo names — no token, no account:

```
https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/?tab=queue
```

First card: `H-a6151a95ac` · session `01Lzbh4XPYTAgCKg1dciFS3Q` · PR #1 chain red on `deadbee`.

## Not claimed

- `witness-corpus --db` on a judge machine (needs local transcript DB + `pip install -e .`)
- Live `/hold/` write without token (by design — reads open)

## Oscar addendum (optional)

- [ ] Run on a machine that is not the author dev box
- [ ] Screenshot or log paste below

---

_Log: agent run 2026-08-29 · handbook Phase 5 closure for cold clone path._
_Re-verified: night wave 2026-08-31 · `./demo.sh` exit 0 · `tests/test_demo.sh` 11/11 PASS._
