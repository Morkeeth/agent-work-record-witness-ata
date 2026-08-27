#!/usr/bin/env python3
"""The join: a clearance record carries the session that produced the claim.

Why this matters (2026-08-27): Zenity governs agent actions, Norm Ai does content
compliance, Qodo reviews the diff, Langfuse scores the trace. None of them holds the
agent's transcript, so none can open a blocked claim back to what actually happened.
That link is the product claim, so it gets a test.

Run: PYTHONPATH=. python3 tests/test_session_join.py
"""
import sys

from cloud.hold_api import extract_session_ref, make_clearance_record, default_policy

FAILED = []


def check(name, got, want):
    if got == want:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name}: got {got!r}, want {want!r}")
        FAILED.append(name)


SID = "01Lzbh4XPYTAgCKg1dciFS3Q"

# --- extraction: the shapes a real agent actually leaves behind -------------------
check("claude.ai session URL",
      extract_session_ref(f"done.\nClaude-Session: https://claude.ai/code/session_{SID}\n"), SID)
check("Session: trailer",
      extract_session_ref(f"Committed as abc1234\nSession: {SID}\n"), SID)
check("session_id inline",
      extract_session_ref(f'ran it. session_id="{SID}" and it passed'), SID)
check("no reference stays absent",
      extract_session_ref("done. tests pass. committed as abc1234."), None)
check("empty report", extract_session_ref(""), None)
check("None report", extract_session_ref(None), None)
# It must not accept junk that merely looks adjacent to the word.
check("bare word is not an id", extract_session_ref("this session was long"), None)

# --- the record carries it, and says so ------------------------------------------
ev = {"decision": "HOLD", "gate": "BLOCK", "exit_hint": 1, "findings": [],
      "blocks": ["deadbee not in repo"], "report_preview": "Committed as deadbee"}
pol = default_policy()

rec = make_clearance_record(evaluation=ev, policy=pol,
                            report=f"Committed as deadbee\nSession: {SID}")
check("record.session recovered from report", rec["session"], SID)
check("record.traceable true", rec["traceable"], True)

rec2 = make_clearance_record(evaluation=ev, policy=pol, report="Committed as deadbee")
check("untraceable claim is honest about it", rec2["session"], None)
check("record.traceable false", rec2["traceable"], False)

# An explicit session beats one scraped out of prose.
rec3 = make_clearance_record(evaluation=ev, policy=pol, session="EXPLICIT123",
                             report=f"Session: {SID}")
check("explicit session wins", rec3["session"], "EXPLICIT123")

# The join must not disturb the verdict.
check("decision untouched", rec["decision"], "HOLD")
check("open still set by decision", rec["open"], True)

print()
if FAILED:
    print(f"{len(FAILED)} FAILED: {', '.join(FAILED)}")
    sys.exit(1)
print("all green")
