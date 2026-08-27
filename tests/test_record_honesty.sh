#!/bin/bash
# Regression gate, 2026-08-27. /clearance returned {"ok": true} unconditionally, so a
# failed store was reported to CI as a recorded decision. For a product whose deliverable
# is an audit trail, that is the exact class of true-looking claim it exists to block.
# A broken store must produce ok=false and recorded=false, while the VERDICT still stands.
set -u
export HOLD_API_TOKEN=test-token-abc HOLD_DEMO_MODE=0
fail=0
probe() { # $1=label $2=FLEET_STORE $3=expect_recorded
  export FLEET_STORE="$2" FLEET_STORE_PATH=/tmp/honesty-$$.jsonl PORT=$4
  rm -f "$FLEET_STORE_PATH"
  python3 -m cloud.service >/tmp/honesty-$$.log 2>&1 & local srv=$!
  for i in $(seq 1 40); do curl -sf "http://127.0.0.1:$4/health" >/dev/null 2>&1 && break; sleep 0.25; done
  local out
  out=$(curl -sS -X POST -H 'Content-Type: application/json' -H "X-HOLD-Token: $HOLD_API_TOKEN" \
        -d '{"report":"Committed as deadbee\nSession: TESTSESSION123","pr":"1","repo":"r"}' \
        "http://127.0.0.1:$4/clearance")
  kill $srv 2>/dev/null; wait $srv 2>/dev/null
  python3 - "$out" "$3" "$1" <<'PY'
import json,sys
d=json.loads(sys.argv[1]); want=sys.argv[2]=="yes"; label=sys.argv[3]
c=d.get("clearance",{}); bad=[]
if d.get("recorded") is not want: bad.append(f"recorded={d.get('recorded')} want={want}")
if d.get("ok") is not want:       bad.append(f"ok={d.get('ok')} want={want}")
if c.get("gate")!="BLOCK":        bad.append(f"verdict lost: gate={c.get('gate')}")
if not d.get("ci_should_fail"):   bad.append("ci_should_fail is not set on a BLOCK")
if c.get("session")!="TESTSESSION123": bad.append(f"session lost: {c.get('session')}")
print(("  FAIL  " if bad else "  PASS  ")+label+((": "+"; ".join(bad)) if bad else ""))
sys.exit(1 if bad else 0)
PY
}
probe "working store: ok=true, verdict + session intact" jsonl yes 8801 || fail=1
probe "BROKEN store: ok=false, verdict + session still intact" bogus-backend no 8802 || fail=1
rm -f /tmp/honesty-$$.jsonl /tmp/honesty-$$.log
exit $fail
