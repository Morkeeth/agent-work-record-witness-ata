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

## Probed locally (2026-09-02 UTC · this run)

```
$ env -i PATH="$PATH" HOME="$HOME" ./demo.sh
  … (full walkthrough; ends with live console URLs)
$ echo $?
0

$ ./tests/test_demo.sh
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

## Live row (optional second tab)

After `./demo.sh`, open the console queue (no token):

https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/?tab=queue

Hero record `H-a6151a95ac` — same `deadbee` probe as PR #1, re-probed 2026-09-02.

## Not claimed

- `witness-corpus --db` on a judge machine (needs local transcript DB + `pip install -e .`)
- Live `/hold/` write without token (by design — reads open)

## Oscar addendum (optional)

- [ ] Run on a machine that is not the author dev box
- [ ] Screenshot or log paste below

---

_Log: agent run 2026-08-29 · handbook Phase 5 closure for cold clone path._
_Log: re-verified 2026-09-02 · `./demo.sh` exit 0 · `test_demo.sh` 11/11._
