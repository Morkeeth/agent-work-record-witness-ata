# Stranger pass · 23 Sep 2026 (night wave)

**Handbook Phase 5:** a stranger attacks the core claim in one click — no wallet, no install, no keys.

**Runner:** Cloud Agent · `cursor/night-wave-seal-stranger-ea3a` · probed `2026-09-23T00:15:07Z`  
**Object:** fresh shallow clone at `/tmp/stranger-clone`, not the author working tree.

---

## Command (stock Python, no network)

```bash
git clone https://github.com/Morkeeth/agent-work-record-witness-ata
cd agent-work-record-witness-ata
env -i PATH="$PATH" HOME="$HOME" ./demo.sh
```

## This run — measured at the object

| Probe | Command | Result |
|-------|---------|--------|
| Clone | `git clone --depth 1 … /tmp/stranger-clone` | exit **0** |
| Cold demo | `env -i PATH=… HOME=… ./demo.sh` in that clone | exit **0**, 98 lines |
| Grade | `./tests/test_demo.sh` in that clone | **PASS** (11 ok) |
| Live URL row in demo output | grepped from demo stdout | `https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/` |
| Live GET `/hold/?tab=queue` | `curl -sS -o /dev/null -w '%{http_code}'` | **200** |
| Live GET `/health` | same | **200** · `auth_required:true` · `demo_seed_enabled:false` · `store:firestore` |

### `tests/test_demo.sh` (verbatim)

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

### Live URL row from `./demo.sh` (verbatim)

```
      the console      https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/
      the record       GET /audit          every claim and its verdict
      the artifact     GET /audit/export   the thing you hand a regulator
```

## Eligibility — two colds, both measured (do not collapse them)

| Arm | How | Result |
|-----|-----|--------|
| **Bare stock Python** (no `pip install`) | `env -i … /usr/bin/python3 contract/eligibility.py` | **0 OF 3 MET**, exit **1** |
| **Deps, no GCP** (`pip install -r requirements.txt`, empty HOME, no ADC) | venv + stripped env | **1 OF 3 MET** (ADK only), exit **1** |

Judge-facing copy that says only "1 of 3 cold" without naming the deps arm is incomplete. Both exits are non-zero by design.

## Not claimed

- `witness-corpus --db` on a judge machine (needs local transcript DB + `pip install -e .`)
- Live `/hold/` write without token (by design — reads open)
- Warm eligibility 3/3 (needs ADC on a Firestore + Vertex project — not this runner)

---

_Log: night-wave agent · 2026-09-23 · stranger path re-verified from a cold clone._
