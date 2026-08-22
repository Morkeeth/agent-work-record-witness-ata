#!/usr/bin/env bash
# Stranger wedge — one command, minimal env. Phase 5 exhibit prep.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export GEMINI_MODEL="${GEMINI_MODEL:-gemini-3.5-flash-lite}"
export GEMINI_PACE_SECONDS="${GEMINI_PACE_SECONDS:-1}"
TARGET="${TMPDIR:-/tmp}/fleet-stranger-skill.md"
rm -f "$TARGET"
python3 fleet_cli.py wedge --target "$TARGET"
test -f "$TARGET"
echo "STRANGER OK: witness target exists at $TARGET"
