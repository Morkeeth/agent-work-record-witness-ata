#!/usr/bin/env bash
# ATA autonomous heartbeat — probe film-critical paths, append one log line.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
LOG="$ROOT/docs/AUTONOMOUS-HEARTBEAT-LOG.md"
TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

mkdir -p "$(dirname "$LOG")"
if [[ ! -f "$LOG" ]]; then
  cat >"$LOG" <<'HDR'
# ATA autonomous heartbeat log

One line per tick while Oscar is away. Film-critical probes only.

HDR
fi

LOCAL="$(git rev-parse --short HEAD 2>/dev/null || echo '?')"
REMOTE="$(git ls-remote origin HEAD 2>/dev/null | awk '{print substr($1,1,7)}' || echo '?')"
SYNC="ok"
[[ "$LOCAL" != "$REMOTE" && "$REMOTE" != "?" ]] && SYNC="DRIFT"

DEMO="?"
if ./demo.sh >/dev/null 2>&1; then DEMO="pass"; else DEMO="FAIL"; fi

URL="$(cat .cloud_run_url 2>/dev/null || echo '')"
TOKEN="$(cat .hold_api_token 2>/dev/null || echo '')"
HEALTH="?"
PROVE="?"
CLEAR="?"
if [[ -n "$URL" ]]; then
  HEALTH="$(curl -sS -o /dev/null -w '%{http_code}' "$URL/health" 2>/dev/null || echo err)"
  PROVE="$(curl -sS -o /dev/null -w '%{http_code}' -X POST -H 'Content-Type: application/json' -d '{}' "$URL/prove" 2>/dev/null || echo err)"
fi
if [[ -n "$URL" && -n "$TOKEN" ]]; then
  CLEAR="$(curl -sS "$URL/audit/export" -H "X-HOLD-Token: $TOKEN" 2>/dev/null | python3 -c "
import sys,json
try:
  ev=json.load(sys.stdin).get('events',[])
  ga=[e for e in ev if e.get('source')=='github-action']
  print(len(ga), ga[-1].get('id','') if ga else 'none', sep=',')
except Exception:
  print('err')
" 2>/dev/null || echo err)"
fi

PR_STATE="?"
if command -v gh >/dev/null 2>&1; then
  PR_STATE="$(gh pr view 1 --json state,statusCheckRollup -q '.state+" checks="+([.statusCheckRollup[]? | select(.name=="verify-claims") | .conclusion] | join(","))' 2>/dev/null || echo '?')"
fi

LINE="| $TS | git $SYNC $LOCAL/$REMOTE | demo $DEMO | health $HEALTH prove_anon $PROVE | ga_clearances $CLEAR | PR1 $PR_STATE |"
echo "$LINE" >>"$LOG"
echo "$LINE"
