#!/usr/bin/env bash
# Scripted terminal capture — one command replays SUBMISSION.md §7 in order.
# Deterministic timing, no hidden state. Oscar runs this while recording.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
FILM="$(cd "$(dirname "$0")" && pwd)"
PY="${PYTHON:-python3}"
URL="$(cat .cloud_run_url 2>/dev/null || echo 'https://fleet-wedge-33kamss2jq-uc.a.run.app')"
URL="${URL%/}"

# Timing between beats (seconds) — matches film/fixed.json beat_seconds tail pauses
if [[ "${FILM_FAST:-0}" == "1" ]]; then
  BEAT_PAUSE=(1 1 1 1 1 1)
else
  BEAT_PAUSE=(25 40 30 35 30 20)
fi

bold() { printf '\n\033[1m%s\033[0m\n' "$*"; }
dim()  { printf '\033[2m%s\033[0m\n' "$*"; }
rule() { printf '\033[2m%s\033[0m\n' "──────────────────────────────────────────────────────────────────────────"; }
pause() { sleep "${1:-2}"; }

bold "THE AGENT WORK RECORD WITNESS — film capture"
dim "spine: docs/SUBMISSION.md §7 · six beats · ≤3:00"
dim "preflight must have passed: ./film/preflight.sh"
rule
pause 2

# ── Beat 1 · Problem (voiceover only — terminal holds) ─────────────────────
bold "BEAT 1 / 6 · Problem"
dim "voiceover line 1 — seats and spend are visible; practice is not"
pause "${BEAT_PAUSE[0]}"

# ── Beat 2 · ./demo.sh cold clone ───────────────────────────────────────────
bold "BEAT 2 / 6 · Stranger gate — env -i stock python3"
dim '$ env -i HOME=/tmp PATH=/usr/bin:/bin LANG=C.UTF-8 /bin/bash ./demo.sh'
rule
env -i HOME=/tmp PATH=/usr/bin:/bin LANG=C.UTF-8 /bin/bash ./demo.sh
DEMO_CODE=$?
rule
dim "demo.sh exit $DEMO_CODE"
pause 3

# ── Beat 3 · PR #1 red check ────────────────────────────────────────────────
bold "BEAT 3 / 6 · PR #1 — verify-claims must be red"
dim '$ gh pr view 1 --repo Morkeeth/agent-work-record-witness-ata --json state,statusCheckRollup'
rule
if command -v gh >/dev/null 2>&1; then
  gh pr view 1 --repo Morkeeth/agent-work-record-witness-ata \
    --json state,statusCheckRollup,url,title \
    | "$PY" -m json.tool
else
  echo "  gh not found — open https://github.com/Morkeeth/agent-work-record-witness-ata/pull/1"
fi
rule
dim "verify-claims → FAILURE (red by design)"
pause "${BEAT_PAUSE[2]}"

# ── Beat 4 · /hold/ row H-57b130f397 ───────────────────────────────────────
bold "BEAT 4 / 6 · The record — open H-57b130f397"
dim "console: $URL/hold/"
dim '$ curl -sS "$URL/queue" | python3 -c "… select id==H-57b130f397 …"'
rule
curl -sS "$URL/queue" | "$PY" -c "
import json,sys
q=json.load(sys.stdin)
row=next(h for h in q.get('holds',[]) if h.get('id')=='H-57b130f397')
print(json.dumps({
  'id': row['id'],
  'kind': row['kind'],
  'source': row['source'],
  'traceable': row['traceable'],
  'session': row['session'],
  'gate': row['gate'],
  'decision': row['decision'],
  'pr': row['pr'],
  'repo': row['repo'],
  'stored_at': row['stored_at'],
  'findings': [f.get('assertion') for f in row.get('findings',[])],
}, indent=2))
"
rule
dim "click through in browser: $URL/hold/"
pause "${BEAT_PAUSE[3]}"

# ── Beat 5 · Four verdicts ──────────────────────────────────────────────────
bold "BEAT 5 / 6 · Four verdicts — PASS · BLOCK · HOLD · UNVERIFIABLE"
cat "$FILM/verdicts.txt"
rule
dim "exit codes: 0 PASS · 1 BLOCK · 2 HOLD"
pause "${BEAT_PAUSE[4]}"

# ── Beat 6 · Honest 41.7 → 8.1 close ─────────────────────────────────────────
bold "BEAT 6 / 6 · Honest close — forty-one point seven to eight point one"
dim "source: surface/fleet-report-page.html (window.__FLEET_REPORT__)"
cat "$FILM/corpus-close.txt"
rule
dim "The gap was ours — seventy-three sibling-repo probes, eleven machinery, seven never checkable."
pause "${BEAT_PAUSE[5]}"

bold "CAPTURE COMPLETE"
dim "six beats · voiceover: film/voiceover.txt · subtitles: film/subtitles.srt"
exit 0
