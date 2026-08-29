#!/usr/bin/env python3
"""P3 — publish gate findings to GitHub: job summary, annotations, optional Checks API.

Lifted from the partner deep dive: richer red check UI on the PR. Safe to skip when
GITHUB_TOKEN or HEAD_SHA are unset (local / dry runs).
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

CHECK_NAME = "witness-findings"


def load_findings(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def conclusion_for(gate: str) -> str:
    g = (gate or "").upper()
    if g == "BLOCK":
        return "failure"
    if g == "HOLD":
        return "neutral"
    return "success"


def build_markdown(findings: dict) -> tuple[str, str, str]:
    """Return title, summary (short), text (full markdown)."""
    gate = findings.get("gate") or "UNKNOWN"
    rows = findings.get("findings") or []
    title = f"Witness gate: {gate}"
    blocks = [r for r in rows if r.get("verdict") == "BLOCK"]
    summary = (
        f"**{gate}** — {len(blocks)} BLOCK · "
        f"{sum(1 for r in rows if r.get('verdict') == 'UNVERIFIABLE')} UNVERIFIABLE · "
        f"{sum(1 for r in rows if r.get('verdict') == 'PASS')} PASS"
    )
    lines = [
        "# Agent Work Record Witness",
        "",
        f"**Gate:** `{gate}` · probes decide; the model never overrules.",
        "",
        "| Verdict | Claim | Evidence |",
        "|---------|-------|----------|",
    ]
    for r in rows:
        v = r.get("verdict") or "?"
        a = (r.get("assertion") or "").replace("|", "\\|")
        e = (r.get("evidence") or r.get("probe") or "").replace("|", "\\|")[:120]
        lines.append(f"| **{v}** | {a} | {e} |")
    lines.extend(["", "*Deterministic probes only — no command from the report is executed.*"])
    return title, summary, "\n".join(lines)


def emit_annotations(rows: list[dict]) -> None:
    """GitHub workflow commands — visible on the check's Annotations tab."""
    for r in rows:
        v = (r.get("verdict") or "").upper()
        assertion = (r.get("assertion") or "claim").replace("%", "").replace("\n", " ")[:80]
        evidence = (r.get("evidence") or "").replace("%", "").replace("\n", " ")[:200]
        if v == "BLOCK":
            print(f"::error title={assertion}::{evidence}")
        elif v == "UNVERIFIABLE":
            print(f"::warning title={assertion}::{evidence}")


def write_step_summary(text: str) -> None:
    path = os.environ.get("GITHUB_STEP_SUMMARY", "").strip()
    if not path:
        return
    with open(path, "a") as f:
        f.write(text)
        if not text.endswith("\n"):
            f.write("\n")


def post_check_run(
    token: str,
    repo: str,
    head_sha: str,
    *,
    conclusion: str,
    title: str,
    summary: str,
    text: str,
) -> dict | None:
    owner, name = repo.split("/", 1)
    url = f"https://api.github.com/repos/{owner}/{name}/check-runs"
    body = {
        "name": CHECK_NAME,
        "head_sha": head_sha,
        "status": "completed",
        "conclusion": conclusion,
        "output": {"title": title, "summary": summary, "text": text},
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def main() -> int:
    findings_path = os.environ.get("HOLD_FINDINGS", "/tmp/hold-findings.json")
    if not os.path.isfile(findings_path):
        print(f"check_run_summary: no findings at {findings_path} — skip")
        return 0

    findings = load_findings(findings_path)
    title, summary, text = build_markdown(findings)
    gate = findings.get("gate") or "UNKNOWN"

    print(f"witness summary: {gate}")
    write_step_summary(text + "\n")
    emit_annotations(findings.get("findings") or [])

    token = (os.environ.get("GITHUB_TOKEN") or "").strip()
    repo = (os.environ.get("REPO") or os.environ.get("GITHUB_REPOSITORY") or "").strip()
    sha = (os.environ.get("HEAD_SHA") or os.environ.get("GITHUB_SHA") or "").strip()

    if not (token and repo and sha):
        print("check_run_summary: GITHUB_TOKEN/REPO/HEAD_SHA incomplete — step summary only")
        return 0

    try:
        out = post_check_run(
            token, repo, sha,
            conclusion=conclusion_for(gate),
            title=title,
            summary=summary,
            text=text,
        )
        print(f"check_run_summary: posted {CHECK_NAME} id={out.get('id') if out else '?'}")
    except urllib.error.HTTPError as e:
        print(f"check_run_summary: Checks API HTTP {e.code} — {e.read()[:300]!r}")
        return 0  # summary + annotations still landed
    except OSError as e:
        print(f"check_run_summary: Checks API {type(e).__name__}: {e}")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
