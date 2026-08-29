#!/usr/bin/env bash
# Scripted terminal replay — six beats from docs/SUBMISSION.md §7. Run before recording.
set -euo pipefail
FILM_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$FILM_DIR/.." && pwd)"
# shellcheck source=film/numbers.env
source "$FILM_DIR/numbers.env"

cd "$ROOT"
PY="${PYTHON:-python3}"
PAUSE="${PAUSE_SEC:-8}"

beat() { printf '\n\033[1;34m▶ BEAT %s\033[0m\n' "$1"; sleep "$PAUSE"; }

echo "THE AGENT WORK RECORD WITNESS — film capture rehearsal"
echo "Hold URL: $HOLD_URL"
echo "Pause between beats: ${PAUSE}s (override PAUSE_SEC=)"
echo

beat "1 · promise (0:00)"
sed -n '1,3p' "$FILM_DIR/voiceover.txt"

beat "2 · ./demo.sh (0:25)"
env -i PATH="$PATH" HOME="$HOME" TERM="${TERM:-xterm-256color}" "$ROOT/demo.sh"

beat "3 · PR #$PR_NUMBER red on $FALSE_SHA (1:10)"
echo "https://github.com/$PR_REPO/pull/$PR_NUMBER"
if command -v gh >/dev/null 2>&1; then
  gh pr view "$PR_NUMBER" --repo "$PR_REPO" --json title,state,statusCheckRollup --jq '.title, .state' 2>/dev/null || true
  gh pr checks "$PR_NUMBER" --repo "$PR_REPO" 2>/dev/null | head -5 || true
else
  curl -sS "https://api.github.com/repos/$PR_REPO/pulls/$PR_NUMBER" | "$PY" -c "import json,sys; d=json.load(sys.stdin); print(d.get('html_url'), d.get('state'))"
fi

beat "4 · record $RECORD_ID (1:50)"
echo "$HOLD_URL"
URL="$(cat "$ROOT/.cloud_run_url" 2>/dev/null || echo "https://fleet-wedge-33kamss2jq-uc.a.run.app")"
if [ -f "$ROOT/.hold_api_token" ]; then
  curl -sS "$URL/audit/export" -H "X-HOLD-Token: $(cat "$ROOT/.hold_api_token")" \
    | "$PY" -c "
import json,sys
rid=sys.argv[1]
for e in json.load(sys.stdin).get('events',[]):
    if e.get('id')==rid:
        import pprint;pprint.pp({k:e.get(k) for k in ('id','gate','decision','session','findings')})
        break
else:
    sys.exit('record not found')
" "$RECORD_ID"
fi

beat "5 · four verdicts (2:20)"
echo "PASS · BLOCK · UNVERIFIABLE · HOLD — shown in demo.sh above (exits 0 · 1 · 2)"
"$PY" -m gate.outcome_gate --help 2>/dev/null | head -3 || true

beat "6 · honest close (2:40)"
echo "Corpus: $CORPUS_EXAMINED of $CORPUS_TOTAL messages · $REPOS_COUNT repos"
echo "Raw $RAW_PCT% → corrected $CORRECTED_PCT% — our error, not the agents'"
sed -n '6p' "$FILM_DIR/voiceover.txt"

echo
echo "Capture rehearsal complete. Run ./film/preflight.sh before the real take."
