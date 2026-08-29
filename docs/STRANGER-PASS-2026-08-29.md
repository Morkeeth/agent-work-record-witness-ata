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
- No `required check` in output (branch protection off)

## Probed locally (night wave · 2026-08-29T20:47Z · commit `5b97eaf`)

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
  ok    does not say required check anywhere in demo output
  ok    reads no transcript database
  ok    no traceback
  PASS
```

Direct run:

```bash
env -i PATH="$PATH" HOME="$HOME" ./demo.sh; echo EXIT:$?
# EXIT:0
```

**Receipt:** `tests/test_demo.sh` grades `./demo.sh`; this doc is the handbook exhibit line.

## Live row (optional second click)

After `./demo.sh`, open the hold console hero row from README:

```
https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/?record=H-a6151a95ac
```

Probed: `curl -sS …/audit/export` → hero present · PR #1 checks red at object.

## Not claimed

- `witness-corpus --db` on a judge machine (needs local transcript DB + `pip install -e .`)
- Live `/hold/` write without token (by design — reads open)

## Oscar addendum (optional)

- [ ] Run on a machine that is not the author dev box
- [ ] Screenshot or log paste below

---

_Log: agent night wave 2026-08-29 · stranger path re-verified at object · fixture scrubbed (no "required check" in demo output)._
