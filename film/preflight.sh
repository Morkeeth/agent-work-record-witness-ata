#!/usr/bin/env bash
# FAIL LOUD if any on-camera surface disagrees with the repo.
set -euo pipefail
FILM_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$FILM_DIR/.." && pwd)"
# shellcheck source=film/numbers.env
source "$FILM_DIR/numbers.env"

cd "$ROOT"
PY="${PYTHON:-python3}"
FAIL=0

red() { printf '\033[31mPREFLIGHT FAIL:\033[0m %s\n' "$*" >&2; FAIL=1; }
grn() { printf '\033[32mok:\033[0m %s\n' "$*"; }

grn "checking canonical numbers in voiceover + SUBMISSION.md"
grep -q "78,618\|78618" "$FILM_DIR/voiceover.txt" || red "voiceover missing corpus 78,618"
grep -q "41.7" "$FILM_DIR/voiceover.txt" || red "voiceover missing 41.7"
grep -q "8.1" "$FILM_DIR/voiceover.txt" || red "voiceover missing 8.1"
grep -q "41.7" "$ROOT/docs/SUBMISSION.md" || red "SUBMISSION.md missing 41.7"
grep -q "8.1" "$ROOT/docs/SUBMISSION.md" || red "SUBMISSION.md missing 8.1"

VO_LINES="$(grep -cve '^[[:space:]]*$' "$FILM_DIR/voiceover.txt" || true)"
SR_CUES="$(grep -cE '^[0-9]+$' "$FILM_DIR/subtitles.srt" || true)"
if [ "$VO_LINES" != "$SR_CUES" ]; then
  red "voiceover ($VO_LINES lines) vs subtitle cues ($SR_CUES) mismatch"
else
  grn "$VO_LINES spoken lines match $SR_CUES subtitle blocks"
fi

grn "./demo.sh (cold, no network)"
if ! env -i PATH="$PATH" HOME="$HOME" "$ROOT/demo.sh" >/tmp/witness-demo-preflight.log 2>&1; then
  red "./demo.sh exited non-zero — see /tmp/witness-demo-preflight.log"
else
  grn "demo.sh exit 0"
fi

URL="$(cat "$ROOT/.cloud_run_url" 2>/dev/null || echo "https://fleet-wedge-33kamss2jq-uc.a.run.app")"
grn "/health live payload"
HEALTH="$(curl -sS --max-time 30 "$URL/health" 2>/dev/null || true)"
if [ -z "$HEALTH" ]; then
  red "/health unreachable at $URL/health"
else
  echo "$HEALTH" | "$PY" -c "
import json,sys,os
d=json.load(sys.stdin)
want={'product':os.environ['PRODUCT_NAME'],'auth_required':True,'demo_seed_enabled':False,'store':'firestore'}
for k,v in want.items():
    if d.get(k)!=v:
        print(f'  mismatch {k}: got {d.get(k)!r} want {v!r}')
        sys.exit(1)
print('  health fields match')
" || red "/health JSON mismatch (see above)"
fi

grn "record row $RECORD_ID"
if [ ! -f "$ROOT/.hold_api_token" ]; then
  red ".hold_api_token missing (gitignored — create locally for preflight)"
else
  TOKEN="$(cat "$ROOT/.hold_api_token")"
  FOUND="$(
    curl -sS --max-time 30 "$URL/audit/export" -H "X-HOLD-Token: $TOKEN" \
      | "$PY" -c "import json,sys; ev=json.load(sys.stdin).get('events',[]); print(any(e.get('id')==sys.argv[1] for e in ev))" "$RECORD_ID" 2>/dev/null || echo False
  )"
  if [ "$FOUND" != "True" ]; then
    red "audit export missing $RECORD_ID"
  else
    grn "record $RECORD_ID present"
  fi
fi

grn "PR #$PR_NUMBER verify-claims red-by-design"
PR_JSON="$(curl -sS --max-time 20 "https://api.github.com/repos/$PR_REPO/pulls/$PR_NUMBER" 2>/dev/null || true)"
if [ -z "$PR_JSON" ]; then
  red "GitHub PR API unreachable"
else
  echo "$PR_JSON" | "$PY" -c "
import json,sys
d=json.load(sys.stdin)
if d.get('state')!='open':
    print('  PR state:', d.get('state'), '(expected open)')
    sys.exit(1)
print('  PR open')
" || red "PR #1 not open"
  if command -v gh >/dev/null 2>&1; then
    if gh pr checks "$PR_NUMBER" --repo "$PR_REPO" 2>/dev/null | grep -q verify-claims; then
      if gh pr checks "$PR_NUMBER" --repo "$PR_REPO" 2>/dev/null | grep verify-claims | grep -qv fail; then
        red "verify-claims not failing — demo story broken"
      else
        grn "verify-claims failing as designed"
      fi
    else
      grn "verify-claims check present (confirm red in UI before filming)"
    fi
  else
    grn "gh not installed — confirm verify-claims FAILURE manually on GitHub"
  fi
fi

if [ "$FAIL" -ne 0 ]; then
  echo >&2
  echo "Preflight FAILED — do not record until all checks pass." >&2
  exit 1
fi
echo
echo "PREFLIGHT PASS — safe to run ./film/capture.sh and record."
exit 0
