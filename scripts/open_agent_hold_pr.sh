#!/usr/bin/env bash
# Open (or print) the real agent false-done PR path for HOLD film — no Seed.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
BODY_FILE="$ROOT/fixtures/agent-false-done-PR-BODY.md"
BRANCH="demo/hold-false-done-$(date +%Y%m%d)"

if [ ! -f "$BODY_FILE" ]; then
  echo "missing $BODY_FILE" >&2
  exit 1
fi

echo "==> HOLD real-PR recipe (Oscar still confirms push/PR)"
echo "Branch: $BRANCH"
echo "Label:  agent"
echo "Body:   $BODY_FILE"
echo "Check:  verify-claims (require on branch protection)"
echo ""

if ! command -v gh >/dev/null 2>&1; then
  echo "gh not found — create the PR manually with the body file above."
  exit 0
fi

# Do not auto-push unless explicitly asked
if [ "${HOLD_PR_PUSH:-}" != "1" ]; then
  cat <<EOF
Dry run only. To create the branch+PR from this machine:

  export HOLD_PR_PUSH=1
  ./scripts/open_agent_hold_pr.sh

Or manually:
  git checkout -b $BRANCH
  # optional tiny doc touch so PR is non-empty
  git push -u origin HEAD
  gh pr create --title "HOLD demo: agent false-done (deadbee)" \\
    --body-file fixtures/agent-false-done-PR-BODY.md \\
    --label agent
EOF
  exit 0
fi

if ! gh label list --json name -q '.[].name' 2>/dev/null | grep -qx agent; then
  gh label create agent --color "0E8A16" --description "Agent-authored PR — runs verify-claims" 2>/dev/null || true
fi

git fetch origin 2>/dev/null || true
git checkout -b "$BRANCH" 2>/dev/null || git checkout "$BRANCH"
# Ensure PR has a file change
mkdir -p docs
echo "HOLD false-done demo branch $(date -u +%Y-%m-%dT%H:%MZ)" >> docs/HOLD-DEMO-PR-MARKER.md
git add docs/HOLD-DEMO-PR-MARKER.md
git commit -m "demo: agent false-done PR marker for HOLD required check" || true
git push -u origin HEAD
gh pr create \
  --title "HOLD demo: agent false-done (deadbee)" \
  --body-file "$BODY_FILE" \
  --label agent \
  || gh pr view --web
echo "Add label 'agent' if the label did not exist yet."
echo "Require check verify-claims on this branch / main protection."
