#!/usr/bin/env bash
# Scripted terminal replay — eight beats from SUBMISSION-PACK §2 / voiceover.txt
set -euo pipefail
FILM_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$FILM_DIR/.." && pwd)"
# shellcheck source=film/numbers.env
source "$FILM_DIR/numbers.env"

cd "$ROOT"
PY="${PYTHON:-python3}"
PAUSE="${PAUSE_SEC:-8}"

beat() { printf '\n\033[1;34m▶ BEAT %s\033[0m\n' "$1"; sleep "$PAUSE"; }

echo "THE AGENT WORK RECORD WITNESS — film capture"
echo "Hold URL: $HOLD_URL?record=$RECORD_ID"
echo "Pause: ${PAUSE}s (PAUSE_SEC=1 for fast rehearsal)"
echo

beat "1 · board question (0:00)"
sed -n '1p' "$FILM_DIR/voiceover.txt"

beat "2 · hold + moat (0:10)"
sed -n '2p' "$FILM_DIR/voiceover.txt"
echo "$HOLD_URL?record=$RECORD_ID"

beat "3 · PR #1 + row (0:28)"
sed -n '3p' "$FILM_DIR/voiceover.txt"
echo "https://github.com/$PR_REPO/pull/$PR_NUMBER/checks"
if command -v gh >/dev/null 2>&1; then
  gh pr checks "$PR_NUMBER" --repo "$PR_REPO" 2>/dev/null | head -8 || true
fi

beat "4 · ./demo.sh --film (0:52)"
sed -n '4p' "$FILM_DIR/voiceover.txt"
env -i PATH="$PATH" HOME="$HOME" TERM="${TERM:-xterm-256color}" "$ROOT/demo.sh" --film

beat "5 · verdict mapping (1:22)"
sed -n '5p' "$FILM_DIR/voiceover.txt"

beat "6 · corpus mid-beat (1:42)"
sed -n '6p' "$FILM_DIR/voiceover.txt"

beat "7 · health + eligibility (2:08)"
sed -n '7p' "$FILM_DIR/voiceover.txt"
URL="$(cat "$ROOT/.cloud_run_url" 2>/dev/null || echo "https://fleet-wedge-33kamss2jq-uc.a.run.app")"
curl -sS --max-time 15 "$URL/health" | "$PY" -c "import json,sys; d=json.load(sys.stdin); print('  store',d.get('store'),'auth',d.get('auth_required'))" 2>/dev/null || true
"$PY" contract/eligibility.py 2>&1 | tail -5 || true

beat "8 · close (2:32)"
sed -n '8p' "$FILM_DIR/voiceover.txt"

echo
echo "Capture complete. Preflight: ./film/preflight.sh · Voice: film/voiceover-vo.mp3"
