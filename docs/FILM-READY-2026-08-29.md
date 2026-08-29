# Film ready — 2026-08-29

**Lane:** green except face-on-camera. Oscar films, submits Devpost, redeploys if he chooses.

**Verified:** 2026-08-28T20:32Z · `879d4fd` · local == `origin/main`

---

## `./demo.sh`

| | |
|---|---|
| **Status** | ✅ PASS · exit 0 |
| **When** | 2026-08-28T20:32Z |
| **Notes** | All three beats: PASS (8670db7) · BLOCK (deadbee + missing path) · HOLD (tests unverifiable). No network, no credentials. |

---

## `/health`

| Field | Value |
|---|---|
| **HTTP** | 200 |
| **URL** | `https://fleet-wedge-33kamss2jq-uc.a.run.app/health` |
| **product** | `THE AGENT WORK RECORD WITNESS` |
| **auth_required** | `true` |
| **demo_seed_enabled** | `false` |
| **store** | `firestore` |
| **agent** | `constructed: true` · `invoked: false` · `last_run: never invoked in this process` |

Also probed: `GET /hold/` → 200 · anon `POST /prove` → 401 · `python3 -V` → 3.12.5 (film with this interpreter for 3 OF 3).

---

## Record row `H-a6151a95ac`

| Field | Value |
|---|---|
| **id** | `H-a6151a95ac` |
| **kind** | `clearance` |
| **source** | `github-action` |
| **traceable** | `true` |
| **session** | `01Lzbh4XPYTAgCKg1dciFS3Q` |
| **gate** | `BLOCK` |
| **decision** | `HOLD` |
| **pr** | `1` |
| **repo** | `Morkeeth/agent-work-record-witness-ata` |
| **stored_at** | `2026-08-29T12:15:09+00:00` |
| **findings** | `deadbee` not a commit · `docs/auth-migration-2026.md` missing |

Console: https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/

```bash
URL=$(cat .cloud_run_url)
curl -sS "$URL/audit/export" | python3 -c \
  "import sys,json; ev=json.load(sys.stdin)['events']; print([e['id'] for e in ev if e.get('source')=='github-action'])"
# ['H-a6151a95ac', ...]
```

---

## PR #1 · `verify-claims`

| | |
|---|---|
| **URL** | https://github.com/Morkeeth/agent-work-record-witness-ata/pull/1 |
| **State** | OPEN |
| **Check** | `verify-claims` → **FAILURE** |
| **Verdict** | **Red by design** — the PR body claims `deadbee` and a missing path; the gate BLOCKed, posted clearance `H-a6151a95ac`, and the workflow exited 1 with `ci_should_fail: true`. |

No fix applied. A green check would mean the false-done demo stopped working.

Workflow log (2026-08-28T17:33:22Z): gate `BLOCK` · `recorded: true` · `TRACEABLE — this HOLD opens back to session 01Lzbh4XPYTAgCKg1dciFS3Q` · `##[error]Process completed with exit code 1`.

---

## What's missing for Devpost

Deadline: **Mon Aug 31 2026 · 17:00 PDT** · https://allthingsagentichackathon.devpost.com/

| Item | Status |
|---|---|
| Unedited ≤4:00 video | ❌ not recorded |
| Devpost form submit | ❌ Oscar |
| Paste from `SUBMISSION-PACK.md` | ✅ ready — **update §3 honest state first** (still says record empty / check never fired; PR #1 closed both tonight) |
| `docs/architecture.png` export for form | ❌ not exported |
| Share repo with `testing@devpost.com` + `cloudhackathons@google.com` | ❌ Oscar |
| Live demo beats | ✅ `./demo.sh` · PR #1 red · `/hold/` row · `/health` |
| Break-glass write on camera | ❌ deliberately not pre-run (keeps export clean until Oscar does it live) |
| Branch protection requiring `verify-claims` | optional — not enabled; check runs on label but does not block merge |

---

## Redeploy (Oscar only — do not run autonomously)

Only needed if HEAD diverges from what's live. Current probes match film needs; **no redeploy required for filming.**

```bash
cd ~/CODE/hack-fleet-ata
export GOOGLE_CLOUD_PROJECT=hack-fleet
export REGION=us-central1
export SERVICE=fleet-wedge
# HOLD_API_TOKEN must be set, or present in .hold_api_token
./scripts/deploy_cloud_run.sh
```

Post-deploy smoke:

```bash
URL=$(cat .cloud_run_url)
curl -sS "$URL/health"
curl -sS -o /dev/null -w "hold: %{http_code}\n" "$URL/hold/"
curl -sS -o /dev/null -w "prove anon: %{http_code}\n" -X POST -H 'Content-Type: application/json' -d '{}' "$URL/prove"
./demo.sh
```

---

## Oscar must rule

1. **Film** — shot 0a (`./demo.sh` cold open) vs 0b (`witness-corpus` kind failure); spine in `docs/PITCH-WHEN-YOU-ARE-BACK.md` + `FILM-SHOT-LIST-2026-08-28.md`.
2. **Break-glass** — perform live once on camera (token in `.hold_api_token`).
3. **PR #1** — leave open for film (recommended) or merge after.
4. **Branch protection** — enable before film if you want "required check" language on camera.
5. **Devpost** — record video, refresh honest-state paste, submit before deadline.
6. **`python3 -V`** — confirm 3.12.x before rolling eligibility shot (stock 3.9.6 prints 1 OF 3).

---

## References

- `docs/DATA-SOURCE-RECEIPT-2026-08-28.md` — three pipes, what ran tonight
- `FILM-SHOT-LIST-2026-08-28.md` — verbatim beats, six catches
- `docs/PITCH-WHEN-YOU-ARE-BACK.md` — ≤4:00 spine
- `SUBMISSION-PACK.md` — paste-ready Devpost copy
