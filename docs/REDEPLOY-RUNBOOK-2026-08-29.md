# Cloud Run redeploy runbook — 2026-08-29

**Lane:** C1 · **Repo:** `hack-fleet-ata` · **Oscar only — do not run autonomously.**

This runbook documents the auth hole that motivated redeploy, the exact `gcloud` commands from `scripts/deploy_cloud_run.sh`, and post-deploy smoke curls. **No redeploy was executed to produce this document.**

**Film state:** see `docs/FILM-READY-2026-08-29.md` — live probes match film needs as of 2026-08-28T20:32Z (`879d4fd`). Redeploy only if `main` diverges from what is live.

---

## Live service URL

```
https://fleet-wedge-33kamss2jq-uc.a.run.app
```

Also stored locally after deploy: `.cloud_run_url`

| Default | Value |
|---|---|
| Project | `hack-fleet` |
| Region | `us-central1` |
| Service | `fleet-wedge` |

---

## Auth hole — URL and evidence

### What was wrong (2026-08-27)

Anonymous `POST /prove` on the **live** URL returned **HTTP 201**, wrote to the audit store, and returned org proof JSON (~1732 bytes, `ok: true`). Other mutating routes were already gated.

| Route | Anon caller (2026-08-27) |
|---|---|
| `POST /clearance` | **401** |
| `POST /break-glass` | **401** |
| `POST /prove` | **201** ← hole |

**Evidence source:** `docs/GEAP-GAP-2026-08-27.md` (F1), probed at `https://fleet-wedge-33kamss2jq-uc.a.run.app`.

Reproduce the *historical* finding (expected **401** today — hole closed):

```bash
U=https://fleet-wedge-33kamss2jq-uc.a.run.app
curl -s -o /dev/null -w "clearance: %{http_code}\n" -X POST "$U/clearance" -d '{}'
curl -s -o /dev/null -w "break-glass: %{http_code}\n" -X POST "$U/break-glass" -d '{}'
curl -s -o /dev/null -w "prove anon: %{http_code}\n" -X POST -H 'Content-Type: application/json' -d '{}' "$U/prove"
# 2026-08-27: prove was 201. Since 2026-08-28 redeploy: prove is 401.
```

### Code fix (repo)

Commit `c4f0e45` — *"Commit the HOLD product, and close the hole it was preaching against"* (2026-08-27). At HEAD, `cloud/service.py` gates `/prove` with `_require_token()` alongside `/clearance`, `/break-glass`, `/policy`, `/wedge`, and `/agent/run`.

Deployed revision `fleet-wedge-00007-zln` (2026-08-27 08:30:17Z) predated that fix by ~1.5h.

### Closure evidence (2026-08-28)

After redeploy, anon `POST /prove` → **401** `HOLD_API_TOKEN required`.

| When | Probe | Result |
|---|---|---|
| 2026-08-28 ~13:45 CET | `POST /prove` no auth | **401** — `docs/SMOKE-RECEIPT-2026-08-28.md` |
| 2026-08-28T20:32Z | `POST /prove` no auth | **401** — `docs/FILM-READY-2026-08-29.md` |
| Heartbeat 2026-08-28 | `prove_anon 401` | `docs/AUTONOMOUS-HEARTBEAT-LOG.md` |

`GET /health` on live (2026-08-28T20:32Z): `auth_required: true`, `demo_seed_enabled: false`, `store: firestore`.

**T4 probe footprint (disclosed):** two unauthenticated `POST /prove` calls during F1 measurement created audit rows; see `docs/GEAP-GAP-2026-08-27.md` §4. `scripts/purge_demo_rows.py` exists if cleanup is needed.

---

## When to redeploy

Redeploy if:

- Live behavior no longer matches `main` (e.g. anon mutating routes return non-401).
- You shipped code that changes runtime paths judges will probe (`/health`, `/hold/`, gate behavior, auth).

Do **not** redeploy for filming if `docs/FILM-READY-2026-08-29.md` probes still pass — current state says **no redeploy required for filming**.

---

## Prerequisites

```bash
cd ~/CODE/hack-fleet-ata
export GOOGLE_CLOUD_PROJECT=hack-fleet   # or PROJECT
export REGION=us-central1
export SERVICE=fleet-wedge
```

**Token (required):** set `HOLD_API_TOKEN` in the environment, or create gitignored `.hold_api_token` (one line, no newline). The deploy script reads `.hold_api_token` when the env var is unset.

**Optional:** `HOLD_DEMO_MODE=0` (default) — keeps `/seed` off for film.

**gcloud:** script prepends `$HOME/google-cloud-sdk/bin` to `PATH`.

---

## Deploy — exact commands from `scripts/deploy_cloud_run.sh`

The script runs these steps in order. Equivalent manual sequence:

```bash
cd ~/CODE/hack-fleet-ata
export PATH="${HOME}/google-cloud-sdk/bin:${PATH}"
export GOOGLE_CLOUD_PROJECT="${GOOGLE_CLOUD_PROJECT:-hack-fleet}"
export REGION="${REGION:-us-central1}"
export SERVICE="${SERVICE:-fleet-wedge}"

gcloud config set project "$GOOGLE_CLOUD_PROJECT" --quiet

gcloud services enable run.googleapis.com cloudbuild.googleapis.com \
  artifactregistry.googleapis.com aiplatform.googleapis.com firestore.googleapis.com --quiet

PROJECT_NUMBER="$(gcloud projects describe "$GOOGLE_CLOUD_PROJECT" --format='value(projectNumber)')"
RUNTIME_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
  --member="serviceAccount:${RUNTIME_SA}" \
  --role="roles/aiplatform.user" --quiet

gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
  --member="serviceAccount:${RUNTIME_SA}" \
  --role="roles/datastore.user" --quiet

# HOLD_API_TOKEN must be set or present in .hold_api_token before this step
HOLD_DEMO_MODE="${HOLD_DEMO_MODE:-0}"

gcloud run deploy "$SERVICE" \
  --source . \
  --region "$REGION" \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars "GEMINI_MODEL=gemini-3.5-flash-lite,GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT},FLEET_STORE=firestore,HOLD_API_TOKEN=${HOLD_API_TOKEN},HOLD_DEMO_MODE=${HOLD_DEMO_MODE}" \
  --memory 1Gi \
  --timeout 300 \
  --max-instances 3 \
  --quiet

gcloud run services describe "$SERVICE" --region "$REGION" --format='value(status.url)'
```

**One-liner (script):**

```bash
./scripts/deploy_cloud_run.sh
```

After success, the script writes the URL to `.cloud_run_url` and prints smoke hints.

---

## Post-deploy smoke curls

Run immediately after deploy. Allow cold start (first `/health` may need 25s+).

```bash
cd ~/CODE/hack-fleet-ata
URL=$(cat .cloud_run_url)
TOKEN=$(cat .hold_api_token)

# Reads — should stay open
curl -sS "$URL/health"
curl -sS "$URL/config"
curl -sS -o /dev/null -w "hold: %{http_code}\n" "$URL/hold/"

# Auth gate — anon mutating routes must be 401
curl -sS -o /dev/null -w "prove anon: %{http_code}\n" \
  -X POST -H 'Content-Type: application/json' -d '{}' "$URL/prove"

# Writes — need token
curl -sS -X POST "$URL/prove" \
  -H "X-HOLD-Token: $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{}'

# Local product demo (no network, no credentials)
./demo.sh

# Film record row still present after redeploy (if not purged)
curl -sS "$URL/audit/export" -H "X-HOLD-Token: $TOKEN" | python3 -c \
  "import sys,json; ev=json.load(sys.stdin)['events']; print([e['id'] for e in ev if e.get('source')=='github-action'])"
# expect: ['H-57b130f397'] unless export was reset
```

**Pass criteria:**

| Check | Expected |
|---|---|
| `GET /health` | 200 · `auth_required: true` · `demo_seed_enabled: false` |
| `GET /hold/` | 200 |
| `POST /prove` (no token) | **401** |
| `POST /prove` (with token) | 200/201 with JSON body |
| `./demo.sh` | exit 0 |

---

## References

- `docs/FILM-READY-2026-08-29.md` — verified film state, redeploy decision
- `docs/GEAP-GAP-2026-08-27.md` — F1 auth hole measurement
- `docs/SMOKE-RECEIPT-2026-08-28.md` — post-redeploy smoke
- `scripts/deploy_cloud_run.sh` — source of deploy commands
- `tests/test_auth_gate.sh` — local regression for all mutating routes
