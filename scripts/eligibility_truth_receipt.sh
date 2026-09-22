#!/usr/bin/env bash
# Control: measure eligibility at the object and refuse a green exit when n < 3.
# Lesson: never trust `| tee` for the exit code — use PIPESTATUS / this script.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY="${PYTHON:-python3}"
OUT="$(mktemp)"
set +e
"$PY" contract/eligibility.py >"$OUT" 2>&1
EC=$?
set -e
N="$("$PY" -c "
import re,sys
t=open(sys.argv[1]).read()
m=re.search(r'(\d+) OF 3 MET', t)
print(m.group(1) if m else -1)
" "$OUT")"
echo "eligibility_truth_receipt: n=$N exit=$EC"
tail -12 "$OUT"
# Control that can go red: exit must be 0 iff n==3, else 1
if [ "$N" = "3" ]; then
  [ "$EC" = "0" ] || { echo "CONTROL FAIL: n=3 but exit=$EC"; exit 2; }
else
  [ "$EC" = "1" ] || { echo "CONTROL FAIL: n=$N but exit=$EC (want 1)"; exit 2; }
fi
echo "CONTROL PASS: exit matches n"
rm -f "$OUT"
exit 0
