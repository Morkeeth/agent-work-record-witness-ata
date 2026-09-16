# Stranger pass · 16 Sep 2026 (night wave)

**Handbook Phase 5:** a stranger attacks the core claim in one command — no wallet, no install, no keys.

---

## Command (cold tree, no network)

```bash
git clone https://github.com/Morkeeth/agent-work-record-witness-ata
cd agent-work-record-witness-ata
env -i PATH="$PATH" HOME="$HOME" ./demo.sh
```

This run used a local `git clone --local` of the working tree into `/tmp/stranger.*/repo`
(same files a GitHub clone would get; no network to the demo itself).

## Expected

- Exit **0**
- Honest report **PASS** · false commit claim **BLOCK** · test claim **HOLD**
- No `Traceback` · no `.trace/trace.db` read · does not say "required check"

## Probed this run · 2026-09-16

```
DEMO_EXIT=0
...
  Honest report PASSED (0). False report BLOCKED (1). Test claim HELD (2).
...
  no network · no API key · no account · no pip install
      the console      https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/
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
TEST_EXIT=0
```

**Commands run:**

```bash
git clone --local <repo> /tmp/stranger.*/repo
env -i PATH="$PATH" HOME="$HOME" ./demo.sh          # exit 0
./tests/test_demo.sh                                  # PASS · exit 0
```

## Live URL row (read-only, same session)

| Probe | Result |
|-------|--------|
| `GET /health` | 200 · `auth_required: true` · `demo_seed_enabled: false` · `store: firestore` · ADK constructed |
| `GET /hold/` | 200 |
| `GET /queue` | 200 · count **20** · hero `H-a6151a95ac` present · `decision: HOLD` · session `01Lzbh4XPYTAgCKg1dciFS3Q` |
| Anon `POST /clearance` `/break-glass` `/prove` | **401** |
| Anon `POST /demo/seed-hold` | **403** |
| PR #1 checks | `verify-claims` **failure** · `witness-findings` **failure** (red by design) |

## Eligibility (re-derived, not carried)

| Path | Result | Command shape |
|------|--------|----------------|
| Bare / no `google-adk` | **0 OF 3 MET**, exit **1** | `env -i PATH=… python3 contract/eligibility.py` |
| `pip install -r requirements.txt`, no ADC | **1 OF 3 MET** (ADK), exit **1** | strip `GOOGLE_*` / key home |
| Docs that say only "1 of 3 cold" without naming the pip step | **under-specified** — fixed in README this run |

## Not claimed

- Live `/hold/` write without token
- Editing PR #1 body (gh write blocked to agents) — fixture scrubbed; live Firestore `report_preview` still carries the old comment until UI scrub is deployed
- Cloud Run redeploy of `surface/hold/index.html` (no `gcloud` in this environment)

---

_Log: night-wave agent · 2026-09-16 · stranger cold path re-verified at the object._
