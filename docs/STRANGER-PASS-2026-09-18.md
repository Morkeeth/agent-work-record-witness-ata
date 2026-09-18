# Stranger pass · night-wave re-verify · 2026-09-18

**Handbook Phase 5:** a stranger attacks the core claim in one command — no wallet, no install, no keys.

Prior exhibit: [`STRANGER-PASS-2026-08-29.md`](STRANGER-PASS-2026-08-29.md). This file is **tonight's** run at the object.

---

## One command (README top)

```bash
git clone https://github.com/Morkeeth/agent-work-record-witness-ata && cd agent-work-record-witness-ata && ./demo.sh
```

Then the live URL row:

| What | URL |
|------|-----|
| Hold console | https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/?tab=queue |
| Hero card | `H-a6151a95ac` (first in queue) |
| PR #1 checks | https://github.com/Morkeeth/agent-work-record-witness-ata/pull/1/checks |
| Health | https://fleet-wedge-33kamss2jq-uc.a.run.app/health |

---

## Expected

- Exit **0**
- `GATE: PASS` on honest report
- `GATE: BLOCK` on false commit claim
- `GATE: HOLD` on test claim (never guessed)
- No `Traceback` · no `.trace/trace.db` read
- No `required check` / `Required check` in demo stdout (branch protection off)

## Probed this run

**Method:** local cold clone of this worktree (`git clone --local`), then:

```bash
env -i PATH="$PATH" HOME="$HOME" ./demo.sh
env -i PATH="$PATH" HOME="$HOME" bash tests/test_demo.sh
curl -sS -o /dev/null -w "%{http_code}\n" https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/?tab=queue
curl -sS -o /dev/null -w "%{http_code}\n" https://fleet-wedge-33kamss2jq-uc.a.run.app/health
```

**Receipt (verbatim grades):**

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
  ok    does not say Required check
  ok    reads no transcript database
  ok    no traceback
  PASS
```

**Live HTTP (same session):** `/hold/?tab=queue` → **200** · `/health` → **200**

**Control fix shipped with this pass:** `tests/test_demo.sh` previously grepped only
`As a required PR check` / `As an required`, so a fixture comment containing
`as a required check` kept the control green while `./demo.sh` printed the banned
bigram. The control now greps the bigram itself; the fixture was scrubbed; demo
stdout on this run has **no** match for `required check`.

## Not claimed

- `witness-corpus --db` on a judge machine (needs local transcript DB + `pip install -e .`)
- Live `/hold/` write without token (by design — reads open)
- Live Cloud Run HTML redeploy of the Install-tab scrub (repo file fixed; live bytes still Oscar deploy)

## Oscar addendum (optional)

- [ ] Run on a machine that is not the author dev box
- [ ] Screenshot or log paste below

---

_Log: night-wave agent run 2026-09-18 · stranger cold path re-verified after scrub._
