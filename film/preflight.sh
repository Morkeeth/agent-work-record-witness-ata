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
FOUND="$(
  curl -sS --max-time 30 "$URL/audit/export" \
    | "$PY" -c "import json,sys; ev=json.load(sys.stdin).get('events',[]); print(any(e.get('id')==sys.argv[1] for e in ev))" "$RECORD_ID" 2>/dev/null || echo False
)"
if [ "$FOUND" != "True" ]; then
  red "audit export missing $RECORD_ID"
else
  grn "record $RECORD_ID present"
fi
if [ -f "$ROOT/.hold_api_token" ] || [ -n "${HOLD_API_TOKEN:-}" ]; then
  grn "break-glass token available locally"
else
  echo "  note: .hold_api_token missing — create before live break-glass on camera (read probe passed without it)" >&2
fi

grn "PR #$PR_NUMBER verify-claims red-by-design"
PR_OK=0
if command -v gh >/dev/null 2>&1; then
  PR_STATE="$(gh pr view "$PR_NUMBER" --repo "$PR_REPO" --json state -q .state 2>/dev/null || true)"
  if [ "$PR_STATE" = "OPEN" ]; then
    PR_OK=1
    grn "PR #$PR_NUMBER open"
  else
    red "PR #$PR_NUMBER state=${PR_STATE:-<unknown>} (expected OPEN)"
  fi
else
  PR_JSON="$(curl -sS --max-time 20 "https://api.github.com/repos/$PR_REPO/pulls/$PR_NUMBER" 2>/dev/null || true)"
  if [ -z "$PR_JSON" ]; then
    red "GitHub PR API unreachable (install gh for authenticated probe)"
  else
    echo "$PR_JSON" | "$PY" -c "
import json,sys
d=json.load(sys.stdin)
if d.get('state')!='open':
    print('  PR state:', d.get('state'), '(expected open)')
    sys.exit(1)
print('  PR open')
" && PR_OK=1 || red "PR #$PR_NUMBER not open"
  fi
fi
if [ "$PR_OK" -eq 1 ]; then
  # Assert the conclusion AT THE OBJECT, and fail closed.
  # The previous test was `gh pr checks | grep verify-claims | grep -qv fail`, which
  # returns 1 on EMPTY input as well as on a failing check, so a gh outage or a
  # renamed check read as "failing as designed". A control that cannot go red is
  # not a control. This reads conclusion directly and treats anything that is not
  # the literal string `failure` as a stop.
  if command -v gh >/dev/null 2>&1; then
    _sha="$(gh pr view "$PR_NUMBER" --repo "$PR_REPO" --json headRefOid -q .headRefOid 2>/dev/null)"
    if [ -z "$_sha" ]; then
      red "could not read PR head sha — cannot prove verify-claims is red"
    else
      _concl="$(gh api "repos/$PR_REPO/commits/$_sha/check-runs" \
        --jq '.check_runs[] | select(.name=="verify-claims") | .conclusion' 2>/dev/null | head -1)"
      if [ "$_concl" = "failure" ]; then
        grn "verify-claims conclusion=failure (red by design, asserted at the object)"
      else
        red "verify-claims conclusion='${_concl:-<none>}' — expected failure. Demo story broken."
      fi
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
