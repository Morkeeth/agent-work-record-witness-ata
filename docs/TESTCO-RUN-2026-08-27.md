# End to end on a repo that is not this one: install, false claim held, true claim cleared

> **This is not an adoption.** Northwind Parcel is a test company this lane wrote, and the agent PRs
> were scripted by the same author as the product. `Installs by a person who is not the author`
> stays **zero**. What this run proves is the CHAIN — that the product installs into a foreign repo,
> holds a false done-claim at exit 1, and clears a true one at exit 0. Calling it a customer would
> be exactly the class of claim this product exists to block.

**Lane:** T4 · **Date:** 2026-08-27 · **Test company:** `~/CODE/testco-northwind-parcel` (local git, no remote)
**Status:** the chain ran end to end, both directions, on a repo outside this one. `clear` is no longer 0.
**Not done, and it is Oscar's click:** no GitHub repo, no push, no deploy, no GitHub-hosted Action run.

> **`clear` is still 0 on every judge-facing surface, and must stay that way.** The CLEAR below went
> to a scratch `FLEET_STORE_PATH`, which is what `0c54850` exists to make happen. Live Firestore
> still reads `clear: 0, hold: 4, exception: 2`. A local result is not a live fact.

---

## What was run

Northwind Parcel is a small parcel-rating service with its own git history, 9 passing tests, and no
code relationship to this repo. The product was installed into it the way a customer would, a pull
request was opened whose done-report was false, and the same path was run again with a report that
was true. The org, the PRs and the reports were all authored by this lane — the foreignness being
tested is the REPO, not the operator.

| | PR #41 `agent/rate-cache` | PR #42 `agent/freight-label` |
|---|---|---|
| The report says | committed as `a41c9f2`; wrote `cache.py`; updated `validators.py`; **all 14 tests pass** | committed as `26d963f`; updated `rates.py`; added the test case |
| True? | SHA is not in the repo · `validators.py` does not exist (`validate.py` does) · suite is 9 tests and was never run in the report | every assertion true |
| Gate | **BLOCK**, exit 1 | **PASS**, exit 0 |
| Gateway | `H-ab655345b2` **HOLD** | `H-89e48fe5d5` **CLEAR** |
| CI exit the PR sees | **1** | **0** |

### Run 1 — the false claim

```
gate/outcome_gate.py -> BLOCK  exit 1
   BLOCK         committed as a41c9f2                       NOT a commit in this repo
   PASS          wrote src/northwind/cache.py               exists
   BLOCK         wrote src/northwind/validators.py          NO SUCH PATH in the repo
   UNVERIFIABLE  tests pass                                 a test claim needs the suite RUN; this gate ne...

gateway: H-ab655345b2  HOLD/BLOCK  recorded=True  ci_should_fail=True
queue  : calm=False  open holds=1  -> ['H-ab655345b2']
break-glass: E-2db09ae2e0  EXCEPTION by platform-lead@northwind
queue  : calm=True  open holds=0
```

The one true assertion in a false report still passed. The gate refused the test claim rather than
running a command lifted from a PR body, which is the right refusal.

### Run 2 — the true claim

```
gate/outcome_gate.py -> PASS  exit 0
   PASS          committed as 26d963f                       is a commit
   PASS          wrote src/northwind/rates.py               exists

gateway: H-89e48fe5d5  CLEAR/PASS  ci_should_fail=False  ci_should_warn=False
EXIT CODE THE PR SEES: 0
```

### The record

```
exported_at 2026-08-27T17:30:48+00:00  ·  3 events
  clearance  H-89e48fe5d5   CLEAR      pr=42 open=False
  exception  E-2db09ae2e0   EXCEPTION  pr=None open=False
  clearance  H-ab655345b2   HOLD       pr=41 open=False
 decisions: {'CLEAR': 1, 'EXCEPTION': 1, 'HOLD': 1}
 duplicate ids: none
```

---

## What the run found — six defects, five fixed, one residual limit stated

### 1. FIXED (`74bd71c`) · The product could not be installed as documented

The installed workflow's first command is `python3 gate/outcome_gate.py --json`. **That file ships
only in the vendor's repo.** A customer who installs the workflow gets:

```
can't open file '.../testco-northwind-parcel/gate/outcome_gate.py': [Errno 2] No such file or directory
```

The failure is then **swallowed** — the step ends `|| true`, so CI continues, writes a 0-byte
findings file, and the next step dies on it:

```
next Action step dies with: JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

A customer sees a JSON parse error, not "the gate is missing". Vendoring `gate/` into the customer
repo was the only way to make the installed workflow run, and that is what this run did.
**The gate needs to ship as a published action or a pip package.**

### 2. STILL OPEN · The README has no install section

Measured: **0 mentions of `HOLD_POLICY_URL`, 0 of `secrets.`/`vars.`/"required check"/"branch
protection".** The Quickstart explains how to run *this* repo, not how to adopt the product. There
is no documented step for the workflow file, the `HOLD_POLICY_URL` variable, the `HOLD_API_TOKEN`
secret, or making the check required. Every value used in this run was read out of the workflow's
own YAML, which is not a thing a customer should have to do.

`examples/customer-workflow.yml` now carries those four steps in its header comment, so the
instructions exist — they are just not in the README, which is where someone looks. Re-verified
after T3's rewrite: still 0 mentions. **`README.md` is T3's; this row stays open until T3 lands it.**

### 3. FIXED · The jsonl store duplicated rows instead of updating them

`FirestoreStore.put` overwrites by document id; `JsonlStore.put` appended unconditionally. Closing a
hold through `/break-glass` therefore wrote a **second** row with the same `H-` id, and
`/audit/export` carried the same clearance twice — the record double-counting its own decisions on
the path a customer without GCP actually runs. Fixed in `fc39cfc`; the run above exports 3 events
with no duplicate ids.

### 4. FIXED · A local run wrote to production

`get_store()` never consulted `FLEET_STORE_PATH`, so naming a scratch file on a credentialed machine
still wrote to production Firestore. Fixed in `0c54850`.

### 5. WITHDRAWN · "The session join is never populated by the real install path"

**This finding was wrong, and it was mine.** `cloud/hold_api.make_clearance_record` already does
`session_ref = (session or "").strip() or extract_session_ref(report)`. The Action sends `report` —
the PR body — and the server recovers the session from it. No `session` key in the payload is needed
and never was.

`session: None` in the first run was a property of **my fixture**: I wrote two PR bodies with no
session reference in them, then reported that absence as a shipped defect. Posting the exact Action
payload shape (`report / findings / pr / repo / actor / source`, no session key):

```
A · body with no session reference        session=None                        traceable=False
B · body carries claude.ai/code/session_… session='01MS5iomniNWozqMjFTkLfUz'  traceable=True
C · body carries "Claude-Session: …"      session='01MS5iomniNWozqMjFTkLfUz'  traceable=True
```

Building the "fix" would have made it worse: extracting the session client-side puts the parser on
**both sides of the wire**, which is the drift it was supposed to prevent. One parser, server side,
reading the report the Action already sends, is the right design and it shipped.

What *was* missing is smaller: nothing tells anyone to put a session reference in the body, and
nothing said when the join failed. `gate/post_clearance.py` now prints it:

```
RED   · no session → UNTRACEABLE — no session reference in the PR body, so this decision cannot be
                     opened back to the run that produced it. … No id is ever invented for you.
GREEN · session    → TRACEABLE — this HOLD opens back to session 01MS5iomniNWozqMjFTkLfUz
```

The queue shows both states side by side:

```
H-658f42ee78  HOLD  pr=43  ->  session 01MS5iomniNWozqMjFTkLfUz
H-c762de433e  HOLD  pr=41  ->  UNTRACEABLE — no session in the report
```

### 6. FIXED (`74bd71c`) · An exception did not name what it let through

The exception record carried `pr: None, repo: None`. It now inherits `pr`, `repo`, `session` and
`excepted_decision` from the clearance it excepts, rather than expecting the break-glass caller to
retype what the record already knows. Verified at the surface that matters — `/audit/export`, read
alone, with no join:

```
clearance_id      = 'H-d215e8d12e'
excepted_decision = 'HOLD'
pr                = '43'
repo              = 'northwind-parcel/northwind-parcel'
session           = '01MS5iomniNWozqMjFTkLfUz'
actor             = 'platform-lead@northwind'
reason            = 'Report errors, not code errors. Merging under exception.'
```

### 7. FIXED, with a residual limit stated (`74bd71c`) · The gate rewarded vague reports

The path parser matched `wrote foo.py` but not `added the case to foo.py`. **A loosely-worded report
therefore got FEWER probes than a precise one** — the gate rewarded vagueness. A closed whitelist of
up to four connective words now bridges the verb and the path.

It is a whitelist and not `\w+` on purpose. A match that leaps across a sentence attributes an
unrelated path to a verb and produces a **false BLOCK on someone's good pull request**, and a false
BLOCK costs more than a missed probe.

**The residual limit, stated rather than discovered later:** `added coverage for the parser in
tests/test_gate.py` is still not probed — five filler words including a noun the whitelist does not
carry. *The gate probes what a report states plainly and says nothing about what it states vaguely.
It no longer rewards vagueness, but it cannot punish it either.*

### Also stale after R3

`README.md` still shows `/health` returning `"agent":"google.adk.agents.llm_agent.LlmAgent"` as a
flat string. Since `bd436e5` that field is an object carrying the run receipt. Not edited here —
`README.md` belongs to another lane.

---

## Reproduce

```bash
# 1. the gateway, writing to a scratch store — never production
HOLD_API_TOKEN=nw-testco FLEET_STORE_PATH=/tmp/nw.jsonl \
  GATE_REPO=$HOME/CODE/testco-northwind-parcel PORT=8801 \
  python3 ~/CODE/hack-fleet-ata/cloud/service.py &

# 2. what the composite action runs, from the customer's working directory.
#    Note the customer repo has NO gate/ — the action carries it.
cd ~/CODE/testco-northwind-parcel
export GITHUB_ACTION_PATH=$HOME/CODE/hack-fleet-ata
export HOLD_POLICY_URL=http://localhost:8801 HOLD_API_TOKEN=nw-testco
export HOLD_FINDINGS=/tmp/hold-findings.json PR_NUMBER=43 REPO=northwind-parcel/northwind-parcel
export PR_BODY="$(cat the-pr-body.md)"

printf '%s' "$PR_BODY" | python3 "$GITHUB_ACTION_PATH/gate/outcome_gate.py" --json > "$HOLD_FINDINGS"
python3 "$GITHUB_ACTION_PATH/gate/post_clearance.py"
```

**Never verified, and it is inside Oscar's push:** `uses: Morkeeth/hack-fleet-ata@main` cannot
resolve until the repo is pushed with `action.yml` at its root. Everything the action *runs* was run
exactly as the action runs it; that GitHub resolves the reference is not something this lane can
test. No GitHub-hosted Action has ever run this.

*T4. Local git only. No remote, no push, no deploy, no GitHub Action run — that step needs Oscar.*
