#!/usr/bin/env bash
# Judge-facing scrub: film + fixture must not say "required check".
# Baseline film-only grep is insufficient — see docs/EMBARRASSMENT-HUNT-2026-09-18.md.
set -u
cd "$(dirname "$0")/.."
fail=0
check_clean() {
  local f="$1"
  if grep -qi 'required check' "$f"; then
    echo "  FAIL  $f contains 'required check'"
    fail=1
  else
    echo "  ok    $f clean"
  fi
}
echo "test_judge_scrub.sh"
check_clean film/voiceover.txt
check_clean film/subtitles.srt
check_clean film/voiceover-vo.txt
check_clean fixtures/agent-false-done-PR-BODY.md
# Hold Install tab may say "do not call it a required check" — that is the ban, not theater.
# Affirmative "Required check" heading/label is banned:
if grep -E 'Required check|as a required check|→ required check' surface/hold/index.html >/dev/null; then
  echo "  FAIL  surface/hold/index.html affirmative required-check phrasing"
  fail=1
else
  echo "  ok    surface/hold/index.html no affirmative required-check phrasing"
fi
[ $fail = 0 ] && { echo "  PASS"; exit 0; } || { echo "  FAILED"; exit 1; }
