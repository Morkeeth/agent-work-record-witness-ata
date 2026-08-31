#!/bin/bash
# Proves every mutating route rejects an anonymous caller when HOLD_API_TOKEN is set.
# Regression gate for the 2026-08-27 finding: /wedge and /prove were unauthenticated,
# and /wedge wrote an arbitrary `target` path with apply defaulting to true. An anonymous
# caller created /tmp/pwned.md. This asserts every mutating route rejects anon with 401,
# that reads stay open, and that no file is written. Run: tests/test_auth_gate.sh
set -u
export HOLD_API_TOKEN=test-token-abc
export FLEET_STORE=memory
export HOLD_DEMO_MODE=0
export HOLD_AGENT_EXPLAIN=0
# Pick a port nothing is on. 2026-08-31: an orphaned gateway from an earlier session was
# listening on the hard-coded 8791 with auth_required=false. This script bound nothing,
# never noticed, and graded THAT process — reporting five security FAILures against a
# codebase that was fine. A test that does not check it is talking to its own server is a
# test that can be correct about the wrong object, which is the failure this repo exists
# to catch. So: find a free port, then prove the health response came from OUR process.
PORT=""
for p in $(seq 8791 8830); do
  if ! (exec 3<>/dev/tcp/127.0.0.1/$p) 2>/dev/null; then PORT=$p; break; fi
  exec 3<&- 2>/dev/null; exec 3>&- 2>/dev/null
done
[ -n "$PORT" ] || { echo "  FAIL  no free port in 8791-8830"; exit 1; }
export PORT
python3 -m cloud.service >/tmp/hold_test.log 2>&1 &
SRV=$!
trap "kill $SRV 2>/dev/null" EXIT
for i in $(seq 1 40); do curl -sf "http://127.0.0.1:$PORT/health" >/dev/null 2>&1 && break; sleep 0.25; done
if ! kill -0 "$SRV" 2>/dev/null; then
  echo "  FAIL  the test gateway died before the probes ran — nothing below would be about it:"
  tail -3 /tmp/hold_test.log
  exit 1
fi
if ! curl -sS "http://127.0.0.1:$PORT/health" | grep -q '"auth_required": true'; then
  echo "  FAIL  the server on :$PORT reports auth_required=false — it is not this test's server"
  exit 1
fi
echo "  (test gateway pid $SRV on :$PORT, auth on)"
fail=0
for route in /clearance /break-glass /policy /wedge /prove; do
  code=$(curl -sS -o /dev/null -w '%{http_code}' -X POST -H 'Content-Type: application/json' \
         -d '{"topic":"x","target":"/tmp/pwned.md"}' "http://127.0.0.1:$PORT$route" 2>/dev/null)
  if [ "$code" = "401" ]; then echo "  PASS  anon POST $route -> 401"; else echo "  FAIL  anon POST $route -> $code (expected 401)"; fail=1; fi
done
code=$(curl -sS -o /dev/null -w '%{http_code}' "http://127.0.0.1:$PORT/health")
[ "$code" = "200" ] && echo "  PASS  GET /health still 200 (reads stay open)" || { echo "  FAIL  GET /health -> $code"; fail=1; }
[ -f /tmp/pwned.md ] && { echo "  FAIL  anonymous caller wrote /tmp/pwned.md"; fail=1; } || echo "  PASS  no file written by an anonymous caller"
exit $fail
