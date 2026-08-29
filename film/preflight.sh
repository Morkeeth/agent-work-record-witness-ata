#!/usr/bin/env bash
# Pre-flight for the 3-minute demo film.
# FAILS LOUD if any on-camera surface disagrees with film/fixed.json.
# Watch each check go red before you trust it green:
#   ./film/preflight.sh --probe-break   # forces one intentional FAIL
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY="${PYTHON:-python3}"
RED='\033[1;31m'
GREEN='\033[1;32m'
RESET='\033[0m'

fail() {
  printf '\n%sPREFLIGHT FAILED%s — do not roll until every surface is green.\n' "$RED" "$RESET" >&2
  exit 1
}

pass_banner() {
  printf '\n%sPREFLIGHT PASSED%s — live equals fixed-by-hash. Safe to run ./film/capture.sh\n' "$GREEN" "$RESET"
}

if [[ "${1:-}" == "--probe-break" ]]; then
  echo "probe-break: showing intentional FAIL on health hash"
  "$PY" "$ROOT/film/check_surfaces.py" --json | "$PY" -c "
import json,sys
rows=json.load(sys.stdin)
for r in rows:
    mark='FAIL' if r['name']=='health' else ('PASS' if r['ok'] else 'FAIL')
    print(f'[{mark}] {r[\"name\"]}: {r[\"detail\"]}')
sys.exit(1)
"
  fail
fi

echo "film preflight — proving live == fixed-by-hash"
echo "fixed: film/fixed.json"
echo "spine: docs/SUBMISSION.md §7"
echo

if ! command -v gh >/dev/null 2>&1; then
  printf '%sFAIL%s gh CLI required for PR #1 check\n' "$RED" "$RESET" >&2
  fail
fi

OUT="$("$PY" "$ROOT/film/check_surfaces.py" --json)" || true
CODE=$?

printf '%s\n' "$OUT" | "$PY" -c "
import json,sys
rows=json.load(sys.stdin)
for r in rows:
    mark='PASS' if r['ok'] else 'FAIL'
    color='\033[1;32m' if r['ok'] else '\033[1;31m'
    reset='\033[0m'
    print(f'{color}[{mark}]{reset} {r[\"name\"]}: {r[\"detail\"]}')
sys.exit(0 if all(r['ok'] for r in rows) else 1)
"
CHECK_CODE=$?

if [[ "$CHECK_CODE" -ne 0 ]]; then
  fail
fi

# Subtitles must agree line-for-line with voiceover
VO="$ROOT/film/voiceover.txt"
SRT="$ROOT/film/subtitles.srt"
if [[ ! -f "$VO" ]]; then
  printf '%sFAIL%s voiceover.txt missing\n' "$RED" "$RESET" >&2
  fail
fi
if [[ ! -f "$SRT" ]]; then
  printf '%sFAIL%s subtitles.srt missing — run: %s film/generate_subtitles.py\n' "$RED" "$RESET" "$PY" >&2
  fail
fi
"$PY" "$ROOT/film/generate_subtitles.py" --check || fail

pass_banner
exit 0
