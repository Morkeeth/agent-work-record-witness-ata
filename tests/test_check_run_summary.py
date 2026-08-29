#!/usr/bin/env python3
"""P3 check run summary builder. Run: PYTHONPATH=. python3 tests/test_check_run_summary.py"""
import os
import sys
import tempfile

from gate.check_run_summary import build_markdown, conclusion_for, load_findings

FAILED = []


def check(name, got, want):
    if got == want:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name}: got {got!r}, want {want!r}")
        FAILED.append(name)


SAMPLE = {
    "gate": "BLOCK",
    "exit_hint": 1,
    "findings": [
        {"assertion": "committed as deadbee", "verdict": "BLOCK",
         "probe": "git cat-file -t deadbee", "evidence": "NOT a commit in this repo"},
        {"assertion": "tests pass", "verdict": "UNVERIFIABLE",
         "probe": "no probe", "evidence": "refused"},
    ],
}

check("BLOCK conclusion", conclusion_for("BLOCK"), "failure")
check("HOLD conclusion", conclusion_for("HOLD"), "neutral")
check("PASS conclusion", conclusion_for("PASS"), "success")

title, summary, text = build_markdown(SAMPLE)
check("title has gate", "BLOCK" in title, True)
check("summary counts BLOCK", "1 BLOCK" in summary, True)
check("text has table", "| **BLOCK** |" in text, True)
check("text has honesty line", "no command from the report" in text, True)

with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
    import json
    json.dump(SAMPLE, f)
    path = f.name
check("load_findings", load_findings(path)["gate"], "BLOCK")
os.unlink(path)

print()
if FAILED:
    print(f"{len(FAILED)} FAILED: {', '.join(FAILED)}")
    sys.exit(1)
print("all green")
