#!/usr/bin/env bash
# THE AGENT WORK RECORD WITNESS — the whole product in one command.
#
# Needs: git, and a python3 (3.9 or newer — stock macOS python3 is fine).
# Needs NOT: pip install, an account, a network call, an API key, a database,
#            or any file outside this clone and one throwaway temp directory.
#
#   ./demo.sh           # full walkthrough
#   ./demo.sh --film    # compact output for screen recording (same verdicts)
#
# It builds a real git repository, writes two agent done-reports about it — one
# honest, one false — and probes both against the repo. You watch a false claim
# get caught, and an honest one get through. A check that only ever says no is
# not a check.

set -u
cd "$(dirname "$0")"
REPO_ROOT="$(pwd)"
PY="${PYTHON:-python3}"
WORK="$(mktemp -d "${TMPDIR:-/tmp}witness-demo.XXXXXX" 2>/dev/null || mktemp -d /tmp/witness-demo.XXXXXX)"
trap 'rm -rf "$WORK"' EXIT

FILM=0
for arg in "$@"; do
  case "$arg" in
    --film|--quiet|-q) FILM=1 ;;
  esac
done
[ "${DEMO_QUIET:-}" = "1" ] && FILM=1

LIVE_HOLD="${WITNESS_LIVE_URL:-https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/}"
LIVE_RECORD="${WITNESS_RECORD_ID:-H-a6151a95ac}"

b() { printf '\n\033[1m%s\033[0m\n' "$*"; }
dim() { printf '\033[2m%s\033[0m\n' "$*"; }
rule() {
  if [ "$FILM" = "1" ]; then return; fi
  printf '\033[2m%s\033[0m\n' "──────────────────────────────────────────────────────────────────────────"
}

"$PY" - <<'PYCHK' || { echo "  This needs Python 3.9+. Found: $($PY -V 2>&1)"; exit 3; }
import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)
PYCHK

if [ "$FILM" = "1" ]; then
  b "THE AGENT WORK RECORD WITNESS · ./demo.sh --film"
  dim "  Probes decide · no network · same logic as the GitHub Action on PR #1"
else
  b "0 · A repository to be honest or dishonest about"
fi

git init -q "$WORK/shop" 2>/dev/null
cd "$WORK/shop"
git config user.email demo@example.com
git config user.name  "Demo Agent"
mkdir -p src docs
printf 'def validate(x):\n    return bool(x)\n' > src/validate.py
printf '# Auth\n\nHow auth works here.\n' > docs/auth.md
git add -A >/dev/null
git commit -qm "auth: add validator" >/dev/null
REAL_SHA="$(git rev-parse --short HEAD)"
if [ "$FILM" = "1" ]; then
  dim "  temp repo · 1 commit ${REAL_SHA}"
else
  dim "  $WORK/shop"
  dim "  1 commit $REAL_SHA · src/validate.py · docs/auth.md"
fi
cd "$REPO_ROOT"

# ---------------------------------------------------------------- honest ----
b "1 · An agent tells the truth"
HONEST="Fixed the auth check and shipped. Committed as ${REAL_SHA}. Wrote src/validate.py."
dim "  \"$HONEST\""
rule
GATE_REPO="$WORK/shop" "$PY" -m gate.outcome_gate "$HONEST"
HONEST_CODE=$?
rule
dim "  exit $HONEST_CODE  (0 PASS · 1 BLOCK · 2 HOLD — the exit code IS the verdict)"

# ------------------------------------------------------------------ false ----
b "2 · The same agent shape — two false claims"
if [ "$FILM" = "1" ]; then
  dim "  agent PR body: false commit + missing path (same pattern as live PR #1)"
else
  dim "  fixtures/agent-false-done-PR-BODY.md — every word around the false parts is plausible"
fi
rule
GATE_REPO="$WORK/shop" "$PY" -m gate.outcome_gate < fixtures/agent-false-done-PR-BODY.md
FALSE_CODE=$?
rule
dim "  exit $FALSE_CODE"

# ------------------------------------------------------------------- hold ----
b "3 · A claim it refuses to guess at"
TESTY="Fixed the auth check. Committed as ${REAL_SHA}. All 14 tests pass."
dim "  \"$TESTY\""
rule
GATE_REPO="$WORK/shop" "$PY" -m gate.outcome_gate "$TESTY"
HOLD_CODE=$?
rule
dim "  exit $HOLD_CODE"

# ------------------------------------------------------------------ result ---
b "4 · What just happened"
if [ "$HONEST_CODE" = "0" ] && [ "$FALSE_CODE" = "1" ] && [ "$HOLD_CODE" = "2" ]; then
  if [ "$FILM" = "1" ]; then
    cat <<TXT
  PASS (0) · BLOCK (1) · HOLD (2).

  Finding UNVERIFIABLE → gate HOLD. Nothing disproved, but we refuse to run a test
  command lifted from agent prose.

  Same probe the Action runs on agent PRs — posted to the live record:
      ${LIVE_HOLD}  →  row ${LIVE_RECORD}
TXT
  else
    cat <<'TXT'
  Honest report PASSED (0). False report BLOCKED (1). Test claim HELD (2).

  Finding-level verdicts: PASS · BLOCK · UNVERIFIABLE.
  Gate-level outcomes:    PASS · BLOCK · HOLD (HOLD means UNVERIFIABLE, nothing BLOCKed).

  Nothing read the agent's reasoning, its trace, or its diff. Each sentence was
  turned into a probe against the object and run:

      committed as deadbee    ->  git cat-file -t deadbee   ->  not a commit
      wrote docs/auth-...md   ->  stat docs/auth-...md      ->  no such path

  That is the whole wedge. Spend dashboards count tokens. Trace tools score
  reasoning. Diff review reads code. None of them checks the claim against the
  object, which is why "committed as deadbee" merges.

  And "all 14 tests pass" was refused as UNVERIFIABLE rather than guessed, even
  though every other claim in that same sentence checked out. Verifying it would
  mean executing a command lifted from agent prose. A tool that reports false
  claims does not get to make one about itself.
TXT
  fi
  STATUS=0
else
  printf '  UNEXPECTED: honest=%s (want 0), false=%s (want 1), test-claim=%s (want 2).\n' "$HONEST_CODE" "$FALSE_CODE" "$HOLD_CODE"
  printf '  That is itself a real result — this script does not pretend to pass.\n'
  STATUS=1
fi

if [ "$FILM" = "1" ]; then
  b "5 · Next"
  cat <<TXT
  Live record:  ${LIVE_HOLD}
  PR #1 chain:  https://github.com/Morkeeth/agent-work-record-witness-ata/pull/1
  In your repo: echo "Committed as deadbee." | $PY -m gate.outcome_gate
TXT
  exit $STATUS
fi

b "5 · What this demo did not touch"
cat <<TXT
  no network · no API key · no account · no pip install
  no transcript database, no ~/.trace, no file outside this clone
  the repository it probed was $WORK/shop, created and deleted by this script

  Next, in your own repo:      echo "Committed as deadbee." | $PY -m gate.outcome_gate
  As an advisory clearance check (until branch protection):  README.md § Install
  On your own transcripts:     $PY -m gate.corpus_scan --db <your.db> --code-root <dir>
TXT

b "6 · And the gate is not the product"
cat <<TXT
  What you just watched is the INTAKE. Every verdict above becomes a row in a
  record that outlives the pull request: who claimed what, whether the object
  agreed, who overrode a hold and the reason they typed, and the session behind
  each entry. That record is the product. The gate is how claims arrive in it.

      the console      ${LIVE_HOLD}
      the record       GET /audit          every claim and its verdict
      the artifact     GET /audit/export   the thing you hand a regulator

  Live instance and the full picture: README.md, and docs/ARCHITECTURE.md.
TXT

exit $STATUS
