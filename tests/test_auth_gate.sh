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
# L10 sweep 2026-08-31 07:0x -- PORT was hard-coded to 8791. Proven live at 07:0x:
#   lsof -nP -iTCP:8791 -sTCP:LISTEN
#   Python 12395 morkeeth ... TCP *:8791 (LISTEN)   started Fri Aug 28 19:23:05 2026
# A stale `python3 -m cloud.service` from three days earlier owned the port, so this script's own
# server could not bind, and every curl below hit the ORPHAN. Output was five security FAILures
# about a process that is not the product under test:
#   FAIL anon POST /clearance -> 201 / /policy -> 200 / /wedge -> 500 ...
# Two changes: take a free port from the OS, and refuse to grade anything that is not the server
# this script started. A setup failure now exits 9 and says so, instead of printing security FAILs.
cd "$(dirname "$0")/.."
PORT=$(python3 -c 'import socket;s=socket.socket();s.bind(("127.0.0.1",0));print(s.getsockname()[1]);s.close()')
export PORT
python3 -m cloud.service >/tmp/hold_test.log 2>&1 &
SRV=$!
trap "kill $SRV 2>/dev/null" EXIT
up=0
for i in $(seq 1 40); do curl -sf "http://127.0.0.1:$PORT/health" >/dev/null 2>&1 && { up=1; break; }; sleep 0.25; done
if [ "$up" != "1" ]; then
  echo "  SETUP FAILURE  server did not answer /health on 127.0.0.1:$PORT -- the product was NOT tested."
  sed 's/^/    | /' /tmp/hold_test.log | tail -20
  exit 9
fi
if ! kill -0 "$SRV" 2>/dev/null; then
  echo "  SETUP FAILURE  the server this script started (pid $SRV) is dead; something else answered :$PORT."
  exit 9
fi
OWNER=$(lsof -nP -iTCP:"$PORT" -sTCP:LISTEN -t 2>/dev/null | tr '\n' ' ')
case " $OWNER " in
  *" $SRV "*) : ;;
  *) echo "  SETUP FAILURE  :$PORT is served by pid(s) [$OWNER], not by the server this script started (pid $SRV)."
     echo "                 Refusing to grade a process that is not the product. Nothing below was run."
     exit 9 ;;
esac
echo "  setup  pid $SRV serving 127.0.0.1:$PORT (verified owner)"
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
