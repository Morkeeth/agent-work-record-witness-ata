#!/usr/bin/env bash
# Pins ./demo.sh — the one command a judge runs on a cold clone.
#
# It asserts the three verdicts, that the demo exits 0, and that it never reads
# the author's transcript corpus. demo.sh grades itself; this grades demo.sh, so
# a change that quietly turns the demo into a green rubber stamp fails here.
set -u
cd "$(dirname "$0")/.."
PY="${PYTHON:-python3}"
OUT="$(PYTHON="$PY" ./demo.sh 2>&1)"; CODE=$?
fail=0
chk() { if printf '%s' "$OUT" | grep -q "$1"; then echo "  ok    $2"; else echo "  FAIL  $2"; fail=1; fi; }
nochk() { if printf '%s' "$OUT" | grep -q "$1"; then echo "  FAIL  $2"; fail=1; else echo "  ok    $2"; fi; }

echo "test_demo.sh"
[ "$CODE" = "0" ] && echo "  ok    demo.sh exits 0" || { echo "  FAIL  demo.sh exits $CODE, want 0"; fail=1; }
chk 'GATE: PASS'   'an honest report PASSES  (the check can say yes)'
chk 'GATE: BLOCK'  'a false report BLOCKS'
chk 'GATE: HOLD'   'a test claim HOLDS, never guessed'
chk 'finding UNVERIFIABLE' 'UNVERIFIABLE finding maps to HOLD gate'
chk 'NOT a commit in this repo' 'the SHA probe output is shown, not summarised'
chk 'NO SUCH PATH in the repo'  'the path probe output is shown, not summarised'
nochk 'As a required PR check' 'does not say required check (branch protection off)'
nochk 'As an required' 'does not say required check'
nochk 'required check' 'fixture and demo output do not leak required check'
nochk '\.trace/trace\.db'  'reads no transcript database'
nochk 'Traceback'          'no traceback'

[ $fail = 0 ] && { echo "  PASS"; exit 0; } || { echo "  FAILED"; exit 1; }
