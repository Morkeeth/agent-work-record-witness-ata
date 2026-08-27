#!/usr/bin/env python3
"""Point the gate at a real transcript corpus and report what it finds — honestly.

    python3 gate/corpus_scan.py --db ~/.trace/trace.db --code-root ~/CODE

WHY THIS EXISTS
---------------
The gate was built for a PR body: a short, first-person done-report. An enterprise
fleet does not produce PR bodies, it produces conversational transcripts. Running
the same probe over 144,306 real agent messages (docs/CORPUS-MEASUREMENT-2026-08-27)
produced "42% of agent commit claims are wrong", and that number was false twice
over:

  - 74 of 110 "wrong" SHAs were REAL COMMITS IN ANOTHER REPO on the same disk. An
    agent's cwd is where it was standing, not where it committed.
  - Of 40 randomly sampled extractions, only 13 were claims at all. 13 were
    citations, 8 were shas inside shell commands, and 6 were this repo's own test
    fixture appearing in transcripts about building this gate.

This script applies both corrections and prints the raw figure beside the
corrected one, because the gap between them IS the result. It never prints an
incidence rate: the hand-labelled n is 13, and a rate needs a denominator nobody
on this machine has.
"""
import argparse
import json
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gate.outcome_gate import check_report  # noqa: E402


def git_repos(code_root: str) -> list:
    root = os.path.expanduser(code_root)
    if not os.path.isdir(root):
        return []
    return [os.path.join(root, d) for d in sorted(os.listdir(root))
            if os.path.exists(os.path.join(root, d, ".git"))]


def scan(db_path: str, code_root: str, limit: int | None = None) -> dict:
    db = sqlite3.connect(f"file:{os.path.expanduser(db_path)}?mode=ro", uri=True)
    rows = db.execute(
        "select id, cwd, text from messages "
        "where role='assistant' and is_human=0 and text is not null "
        "and length(text) > 20" + (f" limit {int(limit)}" if limit else "")).fetchall()
    siblings = git_repos(code_root)

    raw_sha = raw_wrong = 0
    fixed_sha = fixed_wrong = elsewhere = 0
    skipped_machinery = 0
    seen_repo = {}

    for _mid, cwd, text in rows:
        if not cwd:
            continue
        if cwd not in seen_repo:
            seen_repo[cwd] = os.path.exists(os.path.join(cwd, ".git"))
        if not seen_repo[cwd]:
            continue

        # RAW: today's behaviour — whole message, cwd only.
        for f in check_report(text, cwd):
            if not f.assertion.startswith("committed as"):
                continue
            raw_sha += 1
            if f.verdict == "BLOCK":
                raw_wrong += 1

        # CORRECTED: machinery stripped, fixtures excluded, siblings consulted.
        for f in check_report(text, cwd, sibling_repos=siblings,
                              exclude_fixtures=True):
            if not f.assertion.startswith("committed as"):
                continue
            fixed_sha += 1
            if "not the reported cwd" in f.evidence or "unreachable" in f.evidence:
                elsewhere += 1
            if f.verdict == "BLOCK":
                fixed_wrong += 1

    skipped_machinery = raw_sha - fixed_sha
    return {
        "messages": len(rows),
        "repos_on_disk": len(siblings),
        "raw_sha_claims": raw_sha,
        "raw_disagree": raw_wrong,
        "corrected_sha_claims": fixed_sha,
        "corrected_disagree": fixed_wrong,
        "resolved_in_a_sibling_repo": elsewhere,
        "dropped_as_machinery_or_fixture": skipped_machinery,
    }


def render(r: dict) -> str:
    def pct(n, d):
        return f"{100*n/d:.1f}%" if d else "n/a"
    L = []
    L.append("\nWhat the gate finds in a real transcript corpus\n")
    L.append(f"  {r['messages']:,} assistant messages · {r['repos_on_disk']} repos on disk\n")
    L.append(f"  RAW        {r['raw_sha_claims']:>5} sha claims · "
             f"{r['raw_disagree']:>4} disagree · {pct(r['raw_disagree'], r['raw_sha_claims'])}")
    L.append(f"  CORRECTED  {r['corrected_sha_claims']:>5} sha claims · "
             f"{r['corrected_disagree']:>4} disagree · "
             f"{pct(r['corrected_disagree'], r['corrected_sha_claims'])}")
    L.append("")
    L.append(f"    {r['dropped_as_machinery_or_fixture']:>4} dropped — shell commands, fenced "
             f"output, and this repo's own test fixtures")
    L.append(f"    {r['resolved_in_a_sibling_repo']:>4} resolved in a SIBLING repo — the agent "
             f"was right, the probe was aimed at the wrong repo")
    L.append("")
    L.append("  The gap between those two lines is the result. Neither is an incidence")
    L.append("  rate: hand-labelling put extractor precision at 13/40 on prose, so most")
    L.append("  of what remains above is still citations rather than claims. n=13 is far")
    L.append("  too small to state a rate, and this tool will not print one.")
    L.append("")
    L.append("  Run it on yours:  python3 gate/corpus_scan.py --db <your.db> --code-root <dir>\n")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default="~/.trace/trace.db")
    ap.add_argument("--code-root", default="~/CODE")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    r = scan(a.db, a.code_root, a.limit)
    print(json.dumps(r, indent=2) if a.json else render(r))


if __name__ == "__main__":
    main()
