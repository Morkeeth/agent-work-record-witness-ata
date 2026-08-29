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
export PORT=8791
python3 -m cloud.service >/tmp/hold_test.log 2>&1 &
SRV=$!
trap "kill $SRV 2>/dev/null" EXIT
for i in $(seq 1 40); do curl -sf "http://127.0.0.1:$PORT/health" >/dev/null 2>&1 && break; sleep 0.25; done
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
