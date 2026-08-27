#!/usr/bin/env python3
"""HOLD Gateway — outcome clearance against the object.

Deterministic probes decide CLEAR / HOLD / UNVERIFIABLE.
Gemini/ADK may extract claims elsewhere; they are never the release authority.
"""

from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from typing import Any

from gate.outcome_gate import BLOCK, PASS, UNVERIFIABLE, check_report

CLEAR, HOLD, EXCEPTION = "CLEAR", "HOLD", "EXCEPTION"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def findings_to_dict(findings) -> list[dict]:
    return [
        {
            "assertion": f.assertion,
            "verdict": f.verdict,
            "probe": f.probe,
            "evidence": f.evidence,
        }
        for f in findings
    ]


def evaluate_report(report: str, repo: str = ".") -> dict[str, Any]:
    """Run read-only object probes on a done-report."""
    findings = check_report(report, repo)
    blocks = [f for f in findings if f.verdict == BLOCK]
    unmeas = [f for f in findings if f.verdict == UNVERIFIABLE]
    if blocks:
        decision = HOLD
        gate = "BLOCK"
        exit_hint = 1
    elif unmeas:
        decision = HOLD
        gate = "HOLD"
        exit_hint = 2
    else:
        decision = CLEAR
        gate = "PASS"
        exit_hint = 0
    return {
        "decision": decision,
        "gate": gate,
        "exit_hint": exit_hint,
        "findings": findings_to_dict(findings),
        "blocks": findings_to_dict(blocks),
        "report_preview": (report or "").strip()[:240],
    }


def evaluate_precomputed(findings: list[dict], report: str = "") -> dict[str, Any]:
    """Accept findings already probed in CI (Action has the checkout)."""
    norm = []
    for f in findings:
        norm.append(
            {
                "assertion": f.get("assertion") or f.get("claim") or "",
                "verdict": (f.get("verdict") or UNVERIFIABLE).upper(),
                "probe": f.get("probe") or "",
                "evidence": f.get("evidence") or "",
            }
        )
    blocks = [f for f in norm if f["verdict"] == BLOCK]
    unmeas = [f for f in norm if f["verdict"] == UNVERIFIABLE]
    if blocks:
        decision, gate, exit_hint = HOLD, "BLOCK", 1
    elif unmeas:
        decision, gate, exit_hint = HOLD, "HOLD", 2
    else:
        decision, gate, exit_hint = CLEAR, "PASS", 0
    return {
        "decision": decision,
        "gate": gate,
        "exit_hint": exit_hint,
        "findings": norm,
        "blocks": blocks,
        "report_preview": (report or "").strip()[:240],
    }


def default_policy() -> dict[str, Any]:
    return {
        "mode": os.environ.get("HOLD_MODE", "enforce"),  # report-only | enforce
        "agent_only": True,
        "label": os.environ.get("HOLD_AGENT_LABEL", "agent"),
        "break_glass_role": "break-glass",
    }


def make_clearance_record(
    *,
    evaluation: dict,
    policy: dict,
    pr: str | None = None,
    repo: str | None = None,
    actor: str | None = None,
    source: str = "api",
) -> dict[str, Any]:
    rid = f"H-{uuid.uuid4().hex[:10]}"
    return {
        "id": rid,
        "kind": "clearance",
        "product": "HOLD",
        "stored_at": _now(),
        "decision": evaluation["decision"],
        "gate": evaluation["gate"],
        "exit_hint": evaluation["exit_hint"],
        "findings": evaluation["findings"],
        "blocks": evaluation.get("blocks") or [],
        "report_preview": evaluation.get("report_preview") or "",
        "policy_mode": policy.get("mode"),
        "pr": pr,
        "repo": repo,
        "actor": actor or "agent",
        "source": source,
        "open": evaluation["decision"] == HOLD,
    }


def make_exception_record(
    *,
    clearance_id: str,
    reason: str,
    actor: str,
    pr: str | None = None,
    repo: str | None = None,
) -> dict[str, Any]:
    return {
        "id": f"E-{uuid.uuid4().hex[:10]}",
        "kind": "exception",
        "product": "HOLD",
        "stored_at": _now(),
        "clearance_id": clearance_id,
        "reason": reason.strip(),
        "actor": actor.strip() or "break-glass",
        "pr": pr,
        "repo": repo,
        "decision": EXCEPTION,
        "open": False,
    }


def filter_queue(records: list[dict]) -> list[dict]:
    """Open holds: clearance HOLD not yet closed by exception on that id."""
    excepted = {
        r.get("clearance_id")
        for r in records
        if r.get("kind") == "exception" and r.get("clearance_id")
    }
    out = []
    for r in records:
        if r.get("kind") != "clearance":
            continue
        if r.get("decision") != HOLD:
            continue
        if r.get("id") in excepted:
            continue
        if r.get("open") is False:
            continue
        out.append(r)
    # newest first
    out.sort(key=lambda x: x.get("stored_at") or "", reverse=True)
    return out


def filter_audit(records: list[dict]) -> list[dict]:
    kinds = {"clearance", "exception", "prove", "policy"}
    out = [r for r in records if r.get("kind") in kinds or r.get("product") == "HOLD"]
    out.sort(key=lambda x: x.get("stored_at") or "", reverse=True)
    return out
