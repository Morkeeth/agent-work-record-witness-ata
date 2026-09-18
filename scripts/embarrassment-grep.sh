#!/usr/bin/env bash
# Embarrassment grep — judge-facing surfaces must not carry the banned bigram.
#
# History (2026-09-18): ./demo.sh printed "required check" from a fixture comment
# while tests/test_demo.sh grepped two near-miss strings and stayed green.
# A control that has not been watched going RED is not a control — this script
# is proven RED on main@4a45551 and GREEN on the scrubbed branch.
#
# Exit 0 = clean. Exit 1 = leak. Missing surfaces fail closed (not green-on-empty).
set -euo pipefail
cd "$(dirname "$0")/.."

BIGRAM='required check|Required check'
SURFACES=(
  fixtures/agent-false-done-PR-BODY.md
  demo.sh
  README.md
  SUBMISSION-PACK.md
  docs/SUBMISSION.md
  docs/DEVPOST-CHECKLIST.md
  surface/hold/index.html
  film/voiceover.txt
  film/subtitles.srt
  film/voiceover-vo.txt
)

fail=0
for f in "${SURFACES[@]}"; do
  if [ ! -e "$f" ]; then
    echo "FAIL  missing surface: $f"
    fail=1
  fi
done
[ "$fail" = "0" ] || exit 1

# grep returns 1 on no match — that is SUCCESS here. Distinguish from real errors.
set +e
hits="$(grep -nE "$BIGRAM" "${SURFACES[@]}" 2>/dev/null)"
gc=$?
set -e
if [ "$gc" -gt 1 ]; then
  echo "FAIL  grep errored (exit $gc)"
  exit 1
fi
if [ -n "${hits}" ]; then
  echo "FAIL  banned bigram present on judge-facing surface(s):"
  printf '%s\n' "$hits"
  exit 1
fi

echo "ok    embarrassment-grep: no banned bigram on ${#SURFACES[@]} judge-facing surfaces"
exit 0
