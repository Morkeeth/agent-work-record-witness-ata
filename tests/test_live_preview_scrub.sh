#!/usr/bin/env bash
# Live embarrassment control — must be able to go RED.
# Fails when the hero export preview or (optional) PR body still says "required check".
# A green result here is only meaningful after Oscar edits PR #1 body + re-clearance.
set -u
BASE="${HOLD_BASE_URL:-https://fleet-wedge-33kamss2jq-uc.a.run.app}"
HERO="${HOLD_HERO_ID:-H-a6151a95ac}"
fail=0

echo "test_live_preview_scrub.sh"
preview="$(curl -sS "$BASE/audit/export" | python3 -c "
import json,sys
data=json.load(sys.stdin)
hero=next((e for e in data.get('events',[]) if e.get('id')=='$HERO'), None)
print('' if not hero else (hero.get('report_preview') or ''))
")"

if printf '%s' "$preview" | grep -qi 'required check'; then
  echo "  RED   $HERO report_preview still contains 'required check' (Oscar: edit PR #1 body + re-run clearance)"
  fail=1
else
  echo "  ok    $HERO report_preview clean of 'required check'"
fi

if command -v gh >/dev/null 2>&1; then
  body="$(gh pr view 1 --json body -q .body 2>/dev/null || true)"
  if [ -n "$body" ] && printf '%s' "$body" | grep -qi 'required check'; then
    echo "  RED   PR #1 body still contains 'required check'"
    fail=1
  elif [ -n "$body" ]; then
    echo "  ok    PR #1 body clean of 'required check'"
  else
    echo "  skip  PR #1 body (gh unavailable or empty)"
  fi
else
  echo "  skip  gh not installed"
fi

[ $fail = 0 ] && { echo "  PASS"; exit 0; } || { echo "  FAILED (expected until Oscar rewrite)"; exit 1; }
