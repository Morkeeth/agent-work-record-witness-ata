#!/usr/bin/env bash
# B1 — Cloud Run deploy (Aug 26 gate). No local Docker — Cloud Build only.
#
# Prerequisites (Oscar, once):
#   gcloud auth login
#   gcloud auth application-default login
#   gcloud config set project hack-fleet   # or your project id
#   Billing enabled on the project
#
# Usage:
#   ./scripts/deploy_cloud_run.sh
#   PROJECT=my-gcp-project REGION=us-central1 ./scripts/deploy_cloud_run.sh
#
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PROJECT="${GOOGLE_CLOUD_PROJECT:-${PROJECT:-hack-fleet}}"
REGION="${REGION:-us-central1}"
SERVICE="${SERVICE:-fleet-wedge}"

if ! command -v gcloud >/dev/null 2>&1; then
  echo "ERROR: gcloud not installed. Install: https://cloud.google.com/sdk/docs/install"
  exit 1
fi

echo "==> project=$PROJECT region=$REGION service=$SERVICE"

gcloud config set project "$PROJECT"

echo "==> enabling APIs (idempotent)"
gcloud services enable run.googleapis.com cloudbuild.googleapis.com \
  artifactregistry.googleapis.com aiplatform.googleapis.com --quiet

echo "==> deploy (Cloud Build — no local docker)"
gcloud run deploy "$SERVICE" \
  --source . \
  --region "$REGION" \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars "GEMINI_MODEL=gemini-3.5-flash-lite,GOOGLE_CLOUD_PROJECT=${PROJECT},FLEET_STORE=jsonl,FLEET_STORE_PATH=/tmp/fleet-propagations.jsonl" \
  --memory 512Mi \
  --timeout 120 \
  --max-instances 3 \
  --quiet

URL="$(gcloud run services describe "$SERVICE" --region "$REGION" --format='value(status.url)')"
echo ""
echo "DEPLOYED: $URL"
echo ""
echo "Smoke:"
echo "  curl -s ${URL}/healthz | jq ."
echo "  curl -s -X POST ${URL}/wedge -H 'Content-Type: application/json' -d '{}' | jq ."
echo ""
echo "Note: /wedge uses Vertex ADC on Cloud Run (service account). Ensure the runtime SA has"
echo "  roles/aiplatform.user. AI Studio key fallback only works if ~/.config/keys/gemini.key"
echo "  is baked in — do NOT do that; use Vertex on Cloud Run."
