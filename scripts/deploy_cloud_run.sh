#!/usr/bin/env bash
# B1 — Cloud Run deploy. No local Docker — Cloud Build only.
set -euo pipefail
export PATH="${HOME}/google-cloud-sdk/bin:${PATH}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PROJECT="${GOOGLE_CLOUD_PROJECT:-${PROJECT:-hack-fleet}}"
REGION="${REGION:-us-central1}"
SERVICE="${SERVICE:-fleet-wedge}"

echo "==> project=$PROJECT region=$REGION service=$SERVICE"
gcloud config set project "$PROJECT" --quiet

echo "==> enabling APIs"
gcloud services enable run.googleapis.com cloudbuild.googleapis.com \
  artifactregistry.googleapis.com aiplatform.googleapis.com firestore.googleapis.com --quiet

# Runtime SA needs Vertex + Firestore
PROJECT_NUMBER="$(gcloud projects describe "$PROJECT" --format='value(projectNumber)')"
RUNTIME_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"
echo "==> IAM for $RUNTIME_SA"
gcloud projects add-iam-policy-binding "$PROJECT" \
  --member="serviceAccount:${RUNTIME_SA}" \
  --role="roles/aiplatform.user" --quiet >/dev/null || true
gcloud projects add-iam-policy-binding "$PROJECT" \
  --member="serviceAccount:${RUNTIME_SA}" \
  --role="roles/datastore.user" --quiet >/dev/null || true

echo "==> deploy (Cloud Build — no local docker)"
# HOLD_API_TOKEN: prefer env, else local .hold_api_token (gitignored)
if [ -z "${HOLD_API_TOKEN:-}" ] && [ -f "$ROOT/.hold_api_token" ]; then
  HOLD_API_TOKEN="$(tr -d '\n' < "$ROOT/.hold_api_token")"
fi
if [ -z "${HOLD_API_TOKEN:-}" ]; then
  echo "ERROR: set HOLD_API_TOKEN or create $ROOT/.hold_api_token" >&2
  exit 1
fi
# HOLD_DEMO_MODE default off (no Seed button /seed endpoint for film)
HOLD_DEMO_MODE="${HOLD_DEMO_MODE:-0}"

# Secret Manager: the token is a SECRET and must never sit in a Cloud Run revision as a
# plaintext env-var (a revision cannot be un-written). Provision/rotate the secret, then
# mount it with --set-secrets so only a reference is stored on the service. This also makes
# Secret Manager a real, claimable Google Cloud integration.
SECRET_NAME="${SECRET_NAME:-hold-api-token}"
if ! gcloud secrets describe "$SECRET_NAME" --project "$PROJECT" >/dev/null 2>&1; then
  echo "==> creating Secret Manager secret $SECRET_NAME"
  gcloud secrets create "$SECRET_NAME" --project "$PROJECT" --replication-policy=automatic --quiet
fi
printf '%s' "$HOLD_API_TOKEN" | gcloud secrets versions add "$SECRET_NAME" --project "$PROJECT" --data-file=- --quiet
# grant the runtime service account read on the secret (idempotent)
SA="$(gcloud iam service-accounts list --project "$PROJECT" --format='value(email)' --filter='displayName:Compute Engine default' | head -1)"
[ -n "$SA" ] && gcloud secrets add-iam-policy-binding "$SECRET_NAME" --project "$PROJECT" \
  --member="serviceAccount:${SA}" --role=roles/secretmanager.secretAccessor --quiet >/dev/null 2>&1 || true

gcloud run deploy "$SERVICE" \
  --source . \
  --region "$REGION" \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars "GEMINI_MODEL=gemini-3.5-flash-lite,GOOGLE_CLOUD_PROJECT=${PROJECT},FLEET_STORE=firestore,HOLD_DEMO_MODE=${HOLD_DEMO_MODE},EXPLAINER=${EXPLAINER:-gemma},GEMMA_MODEL=${GEMMA_MODEL:-google/gemma-4-31b-it}" \
  --set-secrets "HOLD_API_TOKEN=${SECRET_NAME}:latest,OPENROUTER_API_KEY=openrouter-api-key:latest" \
  --memory 1Gi \
  --timeout 300 \
  --max-instances 3 \
  --quiet

URL="$(gcloud run services describe "$SERVICE" --region "$REGION" --format='value(status.url)')"
echo ""
echo "DEPLOYED: $URL"
echo "$URL" > "$ROOT/.cloud_run_url"
echo ""
echo "Smoke:"
echo "  curl -s ${URL}/health"
echo "  curl -s ${URL}/config"
echo "  curl -s ${URL}/hold/"
echo "  # writes need: -H \"X-HOLD-Token: \$HOLD_API_TOKEN\""
echo "  curl -s -X POST ${URL}/prove -H 'Content-Type: application/json' -d '{}'"
