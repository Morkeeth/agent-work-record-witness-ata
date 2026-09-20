# Stranger pass · refreshed 20 Sep 2026 12:13Z (originally 29 Aug)

**Handbook Phase 5:** a stranger attacks the core claim in one click — no wallet, no install, no keys.

---

## One command (stock Python, no network after clone)

```bash
git clone https://github.com/Morkeeth/agent-work-record-witness-ata
cd agent-work-record-witness-ata
env -i PATH="$PATH" HOME="$HOME" ./demo.sh
```

Then open the live row the demo prints:

```
https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/?tab=queue
```

PR checks (red by design): https://github.com/Morkeeth/agent-work-record-witness-ata/pull/1/checks

---

## Expected

- Exit **0**
- `GATE: PASS` on honest report
- `GATE: BLOCK` on false commit claim
- `GATE: HOLD` on test claim (never guessed)
- No `Traceback` · no `.trace/trace.db` read
- No phrase `required check` (branch protection is off)

---

## Probed this run · 2026-09-20T12:13Z

### A · Cold GitHub clone of `main` (before this branch merges)

```bash
git clone --depth 1 https://github.com/Morkeeth/agent-work-record-witness-ata.git /tmp/stranger-gh
cd /tmp/stranger-gh
env -i PATH="$PATH" HOME="$HOME" ./demo.sh
# DEMO_EXIT:0
```

Verdicts (verbatim):

```
  GATE: PASS — every claim confirmed against the repo.
  …
  GATE: BLOCK — 2 claim(s) the repo disproves. Do not auto-merge.
  …
  GATE: HOLD — finding UNVERIFIABLE (gate holds; probe never runs commands from a report).

  Honest report PASSED (0). False report BLOCKED (1). Test claim HELD (2).

  no network · no API key · no account · no pip install
```

**Embarrassment found at the object:** that cold `main` clone still prints the fixture comment
`# Used to prove HOLD as a required check without…` inside the GATE: BLOCK report preview.
Exit stays 0; the phrase is theater. Fixed on this branch in
`fixtures/agent-false-done-PR-BODY.md` + `tests/test_demo.sh` now bans any `required check`
substring. Until this branch lands on `main`, a stranger on GitHub `main` still sees the leak.

### B · Cold clone of this branch (post-push) · 2026-09-20T12:16Z

```bash
git clone --depth 1 -b cursor/night-wave-sealed-stranger-d503 \
  https://github.com/Morkeeth/agent-work-record-witness-ata.git /tmp/stranger-branch
cd /tmp/stranger-branch
env -i PATH="$PATH" HOME="$HOME" ./demo.sh
# DEMO_EXIT:0 · rg -i 'required check' → no matches (BRANCH_CLONE_CLEAN)
```

### C · This working tree (post-scrub) · command run at 12:13Z

```bash
env -i PATH="$PATH" HOME="$HOME" ./demo.sh
# exit 0 · rg -i 'required check' on stdout → no matches
```

```
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
  ok    does not say Required check
  ok    reads no transcript database
  ok    no traceback
  PASS
```

### Live URL row (same minute)

| Probe | Result |
|-------|--------|
| `GET /health` | 200 · auth_required true · demo_seed false · firestore · ADK constructed |
| `GET /hold/?tab=queue` | 200 · brand THE AGENT WORK RECORD WITNESS |
| `GET /queue` | count **20** |
| `GET /audit` | open **21** · closed **3** · pct_cleared_without_hold **0.0** |
| Hero `H-a6151a95ac` in `/audit/export` | present · BLOCK · pr 1 · head_sha `c9958911…` · open true |
| PR #1 checks | `verify-claims` fail · `witness-findings` fail |

---

## Not claimed

- `witness-corpus --db` on a judge machine (needs local transcript DB + `pip install -e .`)
- Live `/hold/` write without token (by design — reads open)
- `python3 contract/eligibility.py` **3 of 3** on a cold machine — bare clone tonight measured **0 of 3** (no ADC, no `google-adk`). The "1 of 3 cold" figure in older copy assumes ADK is installed.

## Oscar addendum (optional)

- [ ] Run on a machine that is not the author dev box
- [ ] After merge: re-clone `main` and confirm `required check` is gone from demo stdout

---

_Log: agent run 2026-08-29 · handbook Phase 5 closure for cold clone path._
_Re-probed 2026-09-20T12:13Z · cold main still leaked fixture wording · working-tree scrub verified · live URL row re-measured._
