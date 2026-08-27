#!/usr/bin/env python3
"""The record: per-actor honesty and traceability over a window.

Pins the boundaries that stop this surface overstating: probe noise excluded, thin
denominators labelled, practice attached rather than merged, untraceable claims counted
rather than hidden. Run: PYTHONPATH=. python3 tests/test_record.py
"""
import sys
from datetime import datetime, timedelta, timezone

from fleet.record import build_record, is_noise, render

FAILED = []
NOW = datetime(2026, 8, 27, 12, 0, tzinfo=timezone.utc)


def check(name, got, want):
    if got == want:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name}: got {got!r}, want {want!r}")
        FAILED.append(name)


def clr(actor, decision, ago_h=1, session=None, rid=None, kind="clearance"):
    return {"id": rid or f"H-{actor}-{decision}-{ago_h}", "kind": kind, "actor": actor,
            "decision": decision, "session": session,
            "stored_at": (NOW - timedelta(hours=ago_h)).isoformat()}


# --- noise exclusion: the audit must not be computed over its own dry runs ---------
check("prove record is noise", is_noise({"kind": "prove"}), True)
check("phase-a actor is noise", is_noise({"kind": "clearance", "actor": "phase-a"}), True)
check("deadbee report is noise",
      is_noise({"kind": "clearance", "report_preview": "Committed as deadbee"}), True)
check("a real clearance is not noise",
      is_noise({"kind": "clearance", "actor": "agent-bot", "report_preview": "shipped"}), False)

recs = [
    clr("agent-bot", "CLEAR", 1, session="S1"),
    clr("agent-bot", "CLEAR", 2, session="S2"),
    clr("agent-bot", "HOLD", 3, session="S3", rid="H-held-1"),
    clr("agent-bot", "CLEAR", 4),            # no session: untraceable
    clr("agent-bot", "CLEAR", 5, session="S5"),
    clr("copilot", "HOLD", 6, session="S6"),
    clr("phase-a", "HOLD", 7, session="S7"),  # noise, must not count
    {"kind": "prove", "stored_at": (NOW - timedelta(hours=1)).isoformat()},  # noise
    clr("agent-bot", "CLEAR", 24 * 30, session="OLD"),  # outside the window
    {"id": "E-1", "kind": "exception", "clearance_id": "H-held-1", "reason": "shipped hotfix",
     "stored_at": (NOW - timedelta(hours=2)).isoformat()},
]

r = build_record(recs, days=7, now=NOW)

check("noise + old excluded from claims", r["claims"], 6)
check("held counted", r["held"], 2)
check("honesty rate", r["honesty_rate"], round(4 / 6, 3))
check("traceable counted", r["traceable"], 5)
check("noise tally reported", r["excluded_as_noise"], 2)
check("overrides counted", r["overrides"], 1)

bot = [a for a in r["actors"] if a["actor"] == "agent-bot"][0]
check("per-actor claims", bot["claims"], 5)
check("per-actor held", bot["held"], 1)
check("per-actor traceable (one had no session)", bot["traceable"], 4)
check("override attributed to the actor", bot["overridden"], 1)
check("healthy n is not thin", bot["thin"], False)

cop = [a for a in r["actors"] if a["actor"] == "copilot"][0]
check("thin denominator is flagged, not hidden", cop["thin"], True)
check("phase-a never appears as an actor",
      [a for a in r["actors"] if a["actor"] == "phase-a"], [])

# --- practice is attached, never merged ------------------------------------------
r2 = build_record(recs, days=7, now=NOW, coach_result={
    "operator": "oscar", "episodes": 1843, "durable_rate": 0.466,
    "human_pct": 4.9, "proxy": "survival is a proxy"})
check("practice attached", r2["practice"]["survival_rate"], 0.466)
check("practice states it is a different population",
      "NOT the fleet population" in r2["practice"]["scope"], True)
check("practice does not alter fleet honesty", r2["honesty_rate"], r["honesty_rate"])

# --- empty window is honest, not zero-filled -------------------------------------
r3 = build_record([{"kind": "prove"}], days=7, now=NOW)
check("no claims means no rate", r3["honesty_rate"], None)
check("empty window renders", "No agent claims" in render(r3), True)

check("render carries the proxy word", "probe result" in render(r), True)

print()
if FAILED:
    print(f"{len(FAILED)} FAILED: {', '.join(FAILED)}")
    sys.exit(1)
print("all green")
