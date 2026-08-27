#!/usr/bin/env python3
"""Outcome gate — an agent's done-report, checked against the object, before merge.

THE VALIDATED WEDGE (market-checked 2026-08-22, sources in gate/MARKET.md):
  - Code-review tools (Qodo $70M, CodeRabbit, Augment) review the CODE ARTIFACT: is the diff good?
  - Observability tools score the TRACE: what did the agent do?
  - NEITHER checks the agent's SELF-REPORT against the outcome. The 2026 failures are exactly there:
    "reported deployed while prod served the old revision", "self-reports advance to Done even when
    git, deployment and production disagree", "a clean 200 and a confident lie".

This gate does outcome-based verification: it extracts the falsifiable assertions from a done-report
and probes each against the real repo — and REFUSES (UNVERIFIABLE) rather than guessing, and never
executes a command lifted from the report (that would be an RCE hole wearing a feature costume).
"""
import os, re, subprocess, sys
from dataclasses import dataclass

BLOCK, PASS, UNVERIFIABLE = "BLOCK", "PASS", "UNVERIFIABLE"


@dataclass
class Finding:
    assertion: str
    verdict: str
    probe: str
    evidence: str


def _sh(args, repo):
    try:
        return subprocess.run(args, cwd=repo, capture_output=True, text=True)
    except FileNotFoundError as e:
        # Cloud Run image may lack git — CI Action always has it and posts findings.
        class _R:
            stdout = ""
            stderr = f"probe binary missing: {e.filename or args[0]}"
            returncode = 127
        return _R()


def check_report(report: str, repo: str = "."):
    findings = []

    # 1. Claimed commit SHAs — "committed as abc1234", "as `deadbee`", bare 7-40 hex tokens in context
    for m in re.finditer(r'\b(?:commit(?:ted)?\s+(?:as\s+)?`?|as\s+`)?([0-9a-f]{7,40})`?\b', report):
        sha = m.group(1)
        if not re.search(r'(commit|sha|as)\b', report[max(0, m.start()-24):m.start()], re.I):
            continue
        r = _sh(["git", "cat-file", "-t", sha], repo)
        if r.returncode == 127:
            findings.append(Finding(f"committed as {sha}", BLOCK,
                                    f"git cat-file -t {sha}",
                                    "NOT verifiable here (git missing in runtime) — treat as HOLD/BLOCK for safety"))
            continue
        ok = r.stdout.strip() == "commit"
        findings.append(Finding(f"committed as {sha}", PASS if ok else BLOCK,
                                f"git cat-file -t {sha}",
                                "is a commit" if ok else "NOT a commit in this repo"))

    # 2. Claimed file paths — "wrote/added/created/updated <path.ext>" or a backticked path
    for m in re.finditer(r'(?:wrote|added|created|updated|added the file|notes? (?:at|to))\s+`?([\w./-]+\.\w{1,6})`?', report, re.I):
        path = m.group(1)
        ok = os.path.exists(os.path.join(repo, path))
        findings.append(Finding(f"wrote {path}", PASS if ok else BLOCK,
                                f"stat {path}", "exists" if ok else "NO SUCH PATH in the repo"))

    # 3. Claimed test results — REFUSED, not run. Executing a command from a report is an RCE hole.
    if re.search(r'\b(tests?\s+pass|suite\s+green|all\s+green|\d+\s+tests?\s+pass)', report, re.I):
        findings.append(Finding("tests pass", UNVERIFIABLE, "no probe",
                                "a test claim needs the suite RUN; this gate never executes a "
                                "command lifted from a report — verify via the CI outcome, not the word"))

    # 4. Claimed done/merged/deployed with no durable artifact asserted alongside it
    if re.search(r'\b(done|merged|deployed|shipped|complete)\b', report, re.I) and not findings:
        findings.append(Finding("done/merged/deployed", UNVERIFIABLE, "no checkable referent",
                                "a completion claim with no SHA, path, or outcome to probe is not "
                                "clean — it is unmeasured. Ask what durable artifact proves it."))

    if not findings:
        findings.append(Finding("(no falsifiable assertion found)", UNVERIFIABLE, "parser",
                                "the report contains nothing this gate can check against the object"))
    return findings


def gate(report, repo=".", *, as_json: bool = False):
    fs = check_report(report, repo)
    blocks = [f for f in fs if f.verdict == BLOCK]
    payload = {
        "findings": [
            {
                "assertion": f.assertion,
                "verdict": f.verdict,
                "probe": f.probe,
                "evidence": f.evidence,
            }
            for f in fs
        ],
        "blocks": len(blocks),
        "report_preview": report.strip()[:240],
    }
    if blocks:
        payload["gate"] = "BLOCK"
        code = 1
    elif any(f.verdict == UNVERIFIABLE for f in fs):
        payload["gate"] = "HOLD"
        code = 2
    else:
        payload["gate"] = "PASS"
        code = 0
    payload["exit_hint"] = code

    if as_json:
        import json
        print(json.dumps(payload, indent=2))
        return code

    print("=" * 74)
    print("  OUTCOME GATE — the agent's report, checked against the repo")
    print("=" * 74)
    print(f"  report: {report.strip()[:120]}{'...' if len(report.strip())>120 else ''}\n")
    for f in fs:
        print(f"  {f.verdict:<13} {f.assertion}")
        print(f"                probe: {f.probe}  ->  {f.evidence}")
    print("-" * 74)
    if blocks:
        print(f"  GATE: BLOCK — {len(blocks)} claim(s) the repo disproves. Do not auto-merge.")
        return 1
    if any(f.verdict == UNVERIFIABLE for f in fs):
        print("  GATE: HOLD — nothing disproved, but a claim is unverifiable. Needs a human/CI outcome.")
        return 2
    print("  GATE: PASS — every claim confirmed against the repo.")
    return 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--json"]
    as_json = "--json" in sys.argv[1:] or os.environ.get("OUTCOME_GATE_JSON") == "1"
    report = sys.stdin.read() if not args else " ".join(args)
    sys.exit(gate(report, os.environ.get("GATE_REPO", "."), as_json=as_json))
