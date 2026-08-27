# The first run by an organisation that is not the author

**Lane:** T4 · **Date:** 2026-08-27 · **Test company:** `~/CODE/testco-northwind-parcel` (local git, no remote)
**Status:** the chain ran end to end, both directions. `clear` is no longer 0.
**Not done, and it is Oscar's click:** no GitHub repo, no push, no deploy, no GitHub-hosted Action run.

---

## What was run

Northwind Parcel is a small parcel-rating service with its own git history, 9 passing tests, and no
relationship to this repo. The product was installed into it the way a customer would, an agent
opened a pull request whose done-report was false, and the same path was run again with a report
that was true.

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

## What the run found — six defects, three fixed

### 1. BLOCKER · The product cannot be installed as documented

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

### 2. BLOCKER · The README has no install section

Measured: **0 mentions of `HOLD_POLICY_URL`, 0 of `secrets.`/`vars.`/"required check"/"branch
protection".** The Quickstart explains how to run *this* repo, not how to adopt the product. There
is no documented step for the workflow file, the `HOLD_POLICY_URL` variable, the `HOLD_API_TOKEN`
secret, or making the check required. Every value used in this run was read out of the workflow's
own YAML, which is not a thing a customer should have to do.

### 3. FIXED · The jsonl store duplicated rows instead of updating them

`FirestoreStore.put` overwrites by document id; `JsonlStore.put` appended unconditionally. Closing a
hold through `/break-glass` therefore wrote a **second** row with the same `H-` id, and
`/audit/export` carried the same clearance twice — the record double-counting its own decisions on
the path a customer without GCP actually runs. Fixed in `fc39cfc`; the run above exports 3 events
with no duplicate ids.

### 4. FIXED · A local run wrote to production

`get_store()` never consulted `FLEET_STORE_PATH`, so naming a scratch file on a credentialed machine
still wrote to production Firestore. Fixed in `0c54850`.

### 5. OPEN · The session join is never populated by the real install path

`f35e54b` added the join so a held claim opens back to the session that produced it. The Action's
payload is `report / findings / pr / repo / actor / source` — **there is no `session` field**, so
every clearance a real customer files records `session: None`. The feature exists and the shipped
caller cannot reach it.

### 6. OPEN · Two smaller gaps

- The exception record carries `pr: None, repo: None`. An auditor reading exceptions alone cannot
  see which PR was let through without joining back on `clearance_id`.
- The gate's path parser did not probe *"Added the case to tests/test_rates.py"* — it matches
  `added <path>`, not `added the case to <path>`. Not a false pass: an unprobed claim. Worth
  knowing, because an agent that words its report loosely gets fewer probes, not more.

### Also stale after R3

`README.md` still shows `/health` returning `"agent":"google.adk.agents.llm_agent.LlmAgent"` as a
flat string. Since `bd436e5` that field is an object carrying the run receipt. Not edited here —
`README.md` belongs to another lane.

---

## Reproduce

```bash
cd ~/CODE/testco-northwind-parcel && git checkout agent/rate-cache
HOLD_API_TOKEN=nw-testco FLEET_STORE_PATH=/tmp/nw.jsonl \
  GATE_REPO=$HOME/CODE/testco-northwind-parcel PORT=8796 \
  python3 ~/CODE/hack-fleet-ata/cloud/service.py &
python3 gate/outcome_gate.py --json < the-pr-body.md    # BLOCK, exit 1
# POST findings to localhost:8796/clearance with source=github-action
```

*T4. Local git only. No remote, no push, no deploy, no GitHub Action run — that step needs Oscar.*
