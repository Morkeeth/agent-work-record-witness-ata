# Stranger pass · refreshed 18 Sep 2026

**Handbook Phase 5:** a stranger attacks the core claim in one click — no wallet, no install, no keys.

Prior exhibit: [`STRANGER-PASS-2026-08-29.md`](STRANGER-PASS-2026-08-29.md). This file is the **re-probe from this night-wave run**.

---

## One command (README top · cold)

```bash
git clone https://github.com/Morkeeth/agent-work-record-witness-ata
cd agent-work-record-witness-ata
env -i PATH="$PATH" HOME="$HOME" ./demo.sh
# then open the live row:
# https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/?tab=queue
```

## Expected

- Exit **0**
- `GATE: PASS` on honest report
- `GATE: BLOCK` on false commit claim
- `GATE: HOLD` on test claim (never guessed)
- No `required check` in stdout (branch protection off)
- No `Traceback` · no `.trace/trace.db` read

## Probed this run · 2026-09-18

```bash
env -i PATH="$PATH" HOME="$HOME" ./demo.sh; echo EXIT:$?
# EXIT:0

./tests/test_demo.sh
# PASS (10 ok) — including substring ban on "required check"
```

### Command output (ANSI stripped · this run)

```
0 · A repository to be honest or dishonest about
1 · An agent tells the truth
  GATE: PASS — every claim confirmed against the repo.
  exit 0

2 · The same agent shape — two false claims
  fixtures/agent-false-done-PR-BODY.md
  BLOCK         committed as deadbee
                probe: git cat-file -t deadbee  ->  NOT a commit in this repo
  BLOCK         wrote docs/auth-migration-2026.md
                probe: stat docs/auth-migration-2026.md  ->  NO SUCH PATH in the repo
  GATE: BLOCK — 2 claim(s) the repo disproves. Do not auto-merge.
  exit 1

3 · A claim it refuses to guess at
  GATE: HOLD — finding UNVERIFIABLE (gate holds; probe never runs commands from a report).
  exit 2

4 · What just happened
  Honest report PASSED (0). False report BLOCKED (1). Test claim HELD (2).

5 · What this demo did not touch
  no network · no API key · no account · no pip install

6 · And the gate is not the product
      the console      https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/
```

Live URL row verified separately: `GET /hold/?tab=queue` → HTTP 200; hero `H-a6151a95ac` present in `GET /audit/export`.

## Not claimed

- `witness-corpus --db` on a judge machine (needs local transcript DB + `pip install -e .`)
- Live `/hold/` write without token (by design — reads open)
- PR #1 body / stored `report_preview` scrub (Oscar — see embarrassment hunt)

---

_Log: night wave 2026-09-18 · cold clone path re-verified after fixture scrub._
