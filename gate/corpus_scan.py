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
import re
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gate.outcome_gate import check_report  # noqa: E402


# A claim whose target was never inside a repository is not a finding: the probe is
# correct and the claim was never checkable. Proposed by another lane, verified here
# against the real rows before wiring -- 7 drops of 33, every one read by hand.
# Dropped rows are COUNTED WITH THEIR REASON and never silently deleted. A filter
# that quietly shrinks the finding list is the flattering version, and the refusal
# is the product.
_HOST = re.compile(r"^[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.(com|org|net|io|dev|ai|co|sh|app)(/|$)")
_ABS = ("/tmp", "/var", "/private", "/Users", "/home", "~")
# A dotted token with no path separator and an extension nobody ships is an
# identifier -- a db column `task_runs.run_id`, an attribute `oracle.signing.digest`,
# a method call `_INDEX_OK.pop`. Kept narrow on purpose: over-filtering hides real
# findings, which is the worse failure.
_CODEISH = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)+$")
_REAL_EXT = {"md", "py", "ts", "js", "tsx", "json", "yml", "yaml", "sql", "txt",
             "html", "css", "sh", "toml", "cfg", "ini", "lock", "rs", "go", "java",
             "rb", "xml", "csv", "jsonl"}


def not_checkable(target: str):
    """A reason string when this path claim can never be checked, else None."""
    t = (target or "").strip().strip("`\"'")
    if "://" in t or t.startswith("www."):
        return "a URL, not a repository path"
    if _HOST.match(t):
        return "a hostname, not a repository path"
    if t.startswith(_ABS) or os.path.isabs(t):
        return "an absolute path outside the repository"
    if "/" not in t and _CODEISH.match(t):
        if t.rsplit(".", 1)[-1].lower() not in _REAL_EXT:
            return "a code identifier, not a file"
    return None


def git_repos(code_root: str) -> list:
    root = os.path.expanduser(code_root)
    if not os.path.isdir(root):
        return []
    return [os.path.join(root, d) for d in sorted(os.listdir(root))
            if os.path.exists(os.path.join(root, d, ".git"))]


def scan(db_path: str, code_root: str, limit: int | None = None) -> dict:
    db = sqlite3.connect(f"file:{os.path.expanduser(db_path)}?mode=ro", uri=True)
    # THE DENOMINATOR IS COMPUTED, NOT ASSERTED. The corpus total and the examined
    # subset are two different numbers and a tool about unchecked denominators does
    # not get to print only the flattering one. Found by another lane 2026-08-27:
    # our own writeup was headed with the corpus total while the scan examined 54%
    # of it.
    FILTER = "role='assistant' and is_human=0 and text is not null and length(text) > 20"
    corpus_total = db.execute("select count(*) from messages").fetchone()[0]
    examined_total = db.execute(f"select count(*) from messages where {FILTER}").fetchone()[0]
    rows = db.execute(
        f"select id, cwd, text from messages where {FILTER}"
        + (f" limit {int(limit)}" if limit else "")).fetchall()
    siblings = git_repos(code_root)

    raw_sha = raw_wrong = 0
    fixed_sha = fixed_wrong = elsewhere = 0
    skipped_machinery = 0
    seen_repo = {}
    messages_with_a_repo = 0
    # Receipts, not just counts. Every Finding already carries the probe that was
    # run and what it returned; dropping them meant no surface could show a single
    # one, and the receipt is the whole point -- a number you can click into
    # `git cat-file -t deadbee -> NOT a commit in this repo`.
    claims = []
    not_checkable_counts = {}

    for _mid, cwd, text in rows:
        if not cwd:
            continue
        if cwd not in seen_repo:
            seen_repo[cwd] = os.path.exists(os.path.join(cwd, ".git"))
        if not seen_repo[cwd]:
            continue
        messages_with_a_repo += 1

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
            if f.assertion.startswith("wrote ") and f.verdict == "BLOCK":
                reason = not_checkable(f.assertion[len("wrote "):])
                if reason:
                    not_checkable_counts[reason] = not_checkable_counts.get(reason, 0) + 1
                    continue
                claims.append({
                    "message_id": _mid,
                    "repo": os.path.basename(cwd.rstrip("/")),
                    "assertion": f.assertion,
                    "verdict": f.verdict,
                    "probe": f.probe,
                    "evidence": f.evidence,
                    "pass": "corrected",
                })
            if not f.assertion.startswith("committed as"):
                continue
            fixed_sha += 1
            if "not the reported cwd" in f.evidence or "unreachable" in f.evidence:
                elsewhere += 1
            if f.verdict == "BLOCK":
                fixed_wrong += 1
                claims.append({
                    "message_id": _mid,
                    "repo": os.path.basename(cwd.rstrip("/")),
                    "assertion": f.assertion,
                    "verdict": f.verdict,
                    "probe": f.probe,
                    "evidence": f.evidence,
                    # Which pass produced this row. RAW is the uncorrected number and
                    # it is louder; nothing downstream may ship one without knowing
                    # which it has.
                    "pass": "corrected",
                })

    skipped_machinery = raw_sha - fixed_sha
    return {
        # Three populations, all printed, none inferred from another.
        "corpus_total_messages": corpus_total,
        "examined_messages": examined_total if limit is None else len(rows),
        "examined_filter": FILTER,
        "messages_in_a_live_repo": messages_with_a_repo,
        "messages": len(rows),
        "repos_on_disk": len(siblings),
        "raw_sha_claims": raw_sha,
        "raw_disagree": raw_wrong,
        "corrected_sha_claims": fixed_sha,
        "corrected_disagree": fixed_wrong,
        "resolved_in_a_sibling_repo": elsewhere,
        "dropped_as_machinery_or_fixture": skipped_machinery,
        "claims_pass": "corrected",
        "claims_listed": len(claims),
        "path_claims_not_checkable": sum(not_checkable_counts.values()),
        "path_claims_not_checkable_by_reason": not_checkable_counts,
        "claims_not_listed": max(0, fixed_wrong - len([c for c in claims
                                                       if c["assertion"].startswith("committed as")])),
        "claims_listing_rule": ("BLOCK rows from the CORRECTED pass only; PASS rows "
                                "and every RAW-pass row are counted but not listed"),
        "claims": claims,
    }


def render(r: dict) -> str:
    def pct(n, d):
        return f"{100*n/d:.1f}%" if d else "n/a"
    L = []
    L.append("\nWhat the gate finds in a real transcript corpus\n")
    L.append(f"  {r['examined_messages']:,} messages examined, of {r['corpus_total_messages']:,} "
             f"in the corpus · {r['repos_on_disk']} repos on disk")
    L.append(f"  filter: {r['examined_filter']}")
    L.append(f"  {r['messages_in_a_live_repo']:,} of those were written in a directory that is "
             f"still a git repo today\n")
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
    for reason, n in sorted(r.get("path_claims_not_checkable_by_reason", {}).items()):
        L.append(f"    {n:>4} path claims dropped — {reason}")
    L.append("")
    L.append("  The gap between those two lines is the result. Neither is an incidence")
    L.append("  rate: hand-labelling put extractor precision at 13/40 on prose, so most")
    L.append("  of what remains above is still citations rather than claims. n=13 is far")
    L.append("  too small to state a rate, and this tool will not print one.")
    L.append("")
    L.append("  Run it on yours:  witness-corpus --db <your.db> --code-root <dir>\n")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default="~/.trace/trace.db")
    ap.add_argument("--code-root", default="~/CODE")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    # The README sends a stranger here first, and the default --db is a file that
    # exists on one machine. Without this, their first command is a raw
    # sqlite3.OperationalError traceback. A product about checking claims does not
    # get to hand a stranger a stack trace on the way in.
    db = os.path.expanduser(a.db)
    if not os.path.exists(db):
        sys.stderr.write(
            "\n  No transcript database at " + db + "\n\n"
            "  This command reads a corpus of agent transcripts you already have.\n"
            "  If you do not have one, nothing is wrong: it is the second thing to\n"
            "  run, not the first.\n\n"
            "  Start here instead, it needs no database and no account:\n\n"
            '      echo "Fixed the race. Committed as deadbee." | witness\n\n'
            "  Point this at your own corpus when you have one:\n\n"
            "      witness-corpus --db <your.db> --code-root <dir>\n\n"
        )
        return 2

    r = scan(a.db, a.code_root, a.limit)
    print(json.dumps(r, indent=2) if a.json else render(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
