#!/usr/bin/env bash
# Pins judge-facing surfaces against the theater list.
#
# A check that only exists in a doc is not a control. This script must be able
# to go RED: run it after any copy edit that reintroduces "required check" as
# present-tense truth, or collapses eligibility into a single "cold" number.
set -u
cd "$(dirname "$0")/.."
fail=0

ok()   { echo "  ok    $1"; }
bad()  { echo "  FAIL  $1"; fail=1; }

echo "test_judge_facing_scrub.sh"

# Film spoken assets — must stay scrubbed (EYES B6)
for f in film/voiceover.txt film/voiceover-vo.txt film/subtitles.srt; do
  if grep -qi 'required check' "$f"; then
    bad "$f contains 'required check'"
  else
    ok "$f clean of 'required check'"
  fi
done

# Live console source in repo — may mention the ban phrase; must not brand Install as Required check
if grep -E '>Required check<|>required check<' surface/hold/index.html >/dev/null; then
  bad "hold Install tab brands Required check"
else
  ok "hold UI does not brand Required check"
fi

# Eligibility: SUBMISSION-PACK must name the bare arm, not only "1 OF 3 cold"
if grep -q '0 OF 3 MET' SUBMISSION-PACK.md && grep -q '1 OF 3 MET' SUBMISSION-PACK.md; then
  ok "SUBMISSION-PACK names both 1/3 deps-cold and 0/3 bare"
else
  bad "SUBMISSION-PACK missing three-arm eligibility (need both 1 OF 3 and 0 OF 3)"
fi

# IAM label: partner paste block must not say IAM-gated APIs
if grep -q 'IAM-gated APIs' docs/PARTNER-INTEGRATION-DEEP-DIVE-2026-08-29.md; then
  bad "PARTNER deep dive still says IAM-gated APIs"
else
  ok "PARTNER deep dive no longer says IAM-gated APIs"
fi

# Outcome-gate workflow comment must not call the check Required while protection is off
if head -5 .github/workflows/outcome-gate.yml | grep -qi 'Required check for'; then
  bad "outcome-gate.yml still opens with Required check"
else
  ok "outcome-gate.yml does not open with Required check"
fi

[ $fail = 0 ] && { echo "  PASS"; exit 0; } || { echo "  FAILED"; exit 1; }
