# Data source — solved, 2026-08-28

**Problem:** three data layers were conflated — gate (local probe), record (Firestore), corpus (Transcripto). The record had zero real agent claims.

**Solve:** one real ingestion path ran end-to-end while Oscar was out.

## The three sources (say this on camera)

| Layer | Where data comes from | Judge / stranger |
|---|---|---|
| **Gate** | Git object under test — `./demo.sh` builds a throwaway repo | ✅ `./demo.sh` only |
| **Record** | Agent PR → GitHub Action → `POST /clearance` → Firestore → `/hold/` | ✅ after they label a PR `agent` |
| **Corpus** | Customer's Transcripto DB — `witness-corpus --db <yours>` | ❌ day-two opt-in; sample in `fixtures/corpus-sample-40.json` |

No single magic database. Three intentional pipes.

## What ran tonight

| Step | Result |
|---|---|
| GitHub vars/secrets | `HOLD_POLICY_URL` + `HOLD_API_TOKEN` already set |
| Label `agent` | created (was missing — blocked first PR attempt) |
| PR #1 | https://github.com/Morkeeth/agent-work-record-witness-ata/pull/1 |
| Workflow | `verify-claims` **failed on purpose** (BLOCK deadbee) — that is the product working |
| Record | **`H-a6151a95ac`** · `kind=clearance` · `source=github-action` · `traceable=true` |
| Session join | `01Lzbh4XPYTAgCKg1dciFS3Q` from PR body trailer |
| Findings | `deadbee` not a commit · `docs/auth-migration-2026.md` missing |

Probe before: 4 staged clearances, 0 github-action rows.  
Probe after: **1 real github-action clearance** (+ older staged rows still visible).

```bash
URL=$(cat .cloud_run_url)
TOKEN=$(cat .hold_api_token)
curl -sS "$URL/audit/export" -H "X-HOLD-Token: $TOKEN" | python3 -c \
  "import sys,json; ev=json.load(sys.stdin)['events']; print([e for e in ev if e.get('source')=='github-action'])"
```

## Film beats this unlocks

1. **PR tab** — red `verify-claims` on PR #1 (link in browser).
2. **`/hold/`** — row `H-a6151a95ac` opens to session (not seed, not probe).
3. **`./demo.sh`** — stranger path unchanged; say "gate needs no corpus."

## Still honest limits

- Population / org lift still requires customer corpus (n=2 on this machine — not claimed).
- `41.7% → 8.1%` is **method on Oscar's trace.db**, not shipped data — use `fixtures/corpus-sample-40.json` for reproducible sample.
- Branch protection not enabled — check runs on label, does not block merge yet. Optional before film.

## Oscar clicks when back

1. Open PR #1 + `/hold/` — confirm the row matches the pitch.
2. Film (≤4 min) — `FILM-SHOT-LIST-2026-08-28.md` + this receipt.
3. Devpost — `SUBMISSION-PACK.md` · deadline Mon Aug 31 17:00 PDT.
