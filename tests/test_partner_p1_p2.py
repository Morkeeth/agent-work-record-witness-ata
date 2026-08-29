#!/usr/bin/env python3
"""P1 ADK explain-on-HOLD + P2 Action payload metadata.

Run: PYTHONPATH=. python3 tests/test_partner_p1_p2.py
"""
import os
import sys
import unittest.mock as mock

from cloud.hold_api import attach_agent_explanation, make_clearance_record, default_policy
from gate.post_clearance import build_payload

FAILED = []


def check(name, got, want):
    if got == want:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name}: got {got!r}, want {want!r}")
        FAILED.append(name)


HOLD_EV = {
    "decision": "HOLD",
    "gate": "BLOCK",
    "exit_hint": 1,
    "findings": [{"assertion": "deadbee", "verdict": "BLOCK", "probe": "git", "evidence": "missing"}],
    "blocks": [],
    "report_preview": "Committed as deadbee",
}
CLEAR_EV = {"decision": "CLEAR", "gate": "PASS", "exit_hint": 0, "findings": [], "blocks": []}
POL = default_policy()

# --- P2: action posts actor, head_sha, session fallback -------------------------
p = build_payload(
    {"findings": HOLD_EV["findings"]},
    report="done",
    pr="42",
    repo="acme/app",
    actor="coding-agent[bot]",
    session_id="",
    head_sha="abc123deadbeef",
)
check("payload actor is PR author", p["actor"], "coding-agent[bot]")
check("payload head_sha", p["head_sha"], "abc123deadbeef")
check("session falls back to head_sha", p["session"], "abc123deadbeef")
check("source is github-action", p["source"], "github-action")

p2 = build_payload(
    {"findings": []},
    report="done",
    pr="1",
    repo="r/r",
    actor="human",
    session_id="TRANSCRIPT99",
    head_sha="abc123deadbeef",
)
check("explicit session-id wins over head_sha", p2["session"], "TRANSCRIPT99")

rec = make_clearance_record(
    evaluation=HOLD_EV,
    policy=POL,
    pr="1",
    repo="acme/app",
    actor="coding-agent[bot]",
    session="abc123deadbeef",
    head_sha="abc123deadbeef",
    source="github-action",
)
check("record carries head_sha", rec["head_sha"], "abc123deadbeef")
check("record actor not workflow literal", rec["actor"], "coding-agent[bot]")

# --- P1: explain on HOLD only; skipped when disabled ---------------------------
rec_clear = make_clearance_record(evaluation=CLEAR_EV, policy=POL, report="all good")
attach_agent_explanation(rec_clear, CLEAR_EV)
check("CLEAR does not invoke agent", rec_clear.get("agent_invoked"), False)
check("CLEAR has no explanation", "agent_explanation" in rec_clear, False)

rec_hold = make_clearance_record(evaluation=HOLD_EV, policy=POL, report="Committed as deadbee")
os.environ["HOLD_AGENT_EXPLAIN"] = "0"
attach_agent_explanation(rec_hold, HOLD_EV)
check("HOLD skipped when disabled", rec_hold.get("agent_explain_skipped"), True)
check("HOLD skipped means not invoked", rec_hold.get("agent_invoked"), False)

os.environ["HOLD_AGENT_EXPLAIN"] = "1"
fake_receipt = {
    "invoked": True,
    "text": "The commit hash deadbee is not in this repository.",
    "agent_class": "google.adk.agents.Agent",
    "model": "gemini-3.5-flash-lite",
}
with mock.patch("cloud.agent.run_agent", return_value=fake_receipt):
    rec_hold2 = make_clearance_record(evaluation=HOLD_EV, policy=POL, report="Committed as deadbee")
    attach_agent_explanation(rec_hold2, HOLD_EV, session_id="H-test123")
check("HOLD with mock run sets invoked", rec_hold2.get("agent_invoked"), True)
check("HOLD stores explanation receipt",
      rec_hold2["agent_explanation"]["text"].startswith("The commit hash deadbee"), True)

print()
if FAILED:
    print(f"{len(FAILED)} FAILED: {', '.join(FAILED)}")
    sys.exit(1)
print("all green")
