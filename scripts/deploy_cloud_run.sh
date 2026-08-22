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
gcloud run deploy "$SERVICE" \
  --source . \
  --region "$REGION" \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars "GEMINI_MODEL=gemini-3.5-flash-lite,GOOGLE_CLOUD_PROJECT=${PROJECT},FLEET_STORE=firestore" \
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
echo "  curl -s -X POST ${URL}/wedge -H 'Content-Type: application/json' -d '{\"apply\":false}'"
echo "  curl -s -X POST ${URL}/prove -H 'Content-Type: application/json' -d '{}'"
