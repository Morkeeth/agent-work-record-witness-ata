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


# Regions of a message that are MACHINERY, not a report. Measured on 144,306 real
# agent messages (docs/CORPUS-MEASUREMENT-2026-08-27.md): of 40 randomly sampled
# extractions, 8 were a sha inside a shell command the agent was running and 6 were
# TEST FIXTURES -- including this repo's own `deadbee`, found in transcripts about
# building this gate. Two thirds of what the extractor flagged were not claims.
_FENCE = re.compile(r"```.*?```|~~~.*?~~~", re.S)
_SHELL_LINE = re.compile(r"^\s*(?:\$|#|>)?\s*(?:git|echo|cd|cat|ls|grep|sed|awk|"
                         r"python3?|curl|gh|npm|pytest)\b.*$", re.M)
# Fixtures this repo ships. A tool that counts its own test data as an agent's
# claim is the joke that writes itself, and it happened.
_OWN_FIXTURES = {"deadbee", "deadbee1", "deadbeef", "abc1234"}

# Path literals this repo itself stages as false done-claims. Same circularity as
# `deadbee`: they reach a corpus because real messages discuss the demo while it is
# being built, and the tool then reports its own seed text as a caught claim. A
# judge who greps the repo finds the string in cloud/service.py and
# fixtures/agent-false-done-PR-BODY.md.
_OWN_PATH_FIXTURES = {"docs/auth-migration-2026.md"}

# A report region, when the message declares one. An agent's done-report is a
# section, not a whole conversational turn -- scoping to it is the cheap half of
# the precision fix, and it needs no model.
_REPORT_REGION = re.compile(
    r"^\s{0,3}#{1,4}\s*(?:✅\s*)?(?:done|summary|what i did|final report|result|"
    r"changes|shipped)\b(.*?)(?=^\s{0,3}#{1,4}\s|\Z)", re.I | re.M | re.S)


def strip_machinery(report: str) -> str:
    """Blank out fenced blocks and shell lines, preserving offsets is unnecessary.

    Replaced with spaces rather than deleted so a claim never accidentally joins
    two unrelated sentences into a new one.
    """
    out = _FENCE.sub(lambda m: " " * len(m.group(0)), report or "")
    out = _SHELL_LINE.sub(lambda m: " " * len(m.group(0)), out)
    return out


def claim_region(report: str, scope: bool = False) -> str:
    """The part of a message that is a done-report.

    `scope=False` (default) keeps today's behaviour: the whole message, minus
    machinery. `scope=True` narrows to a declared report section when the message
    has one, and is what a caller reading conversational transcripts should use.
    A message with no such section yields nothing under scope -- refusing to guess
    is the same rule the rest of this gate runs on.
    """
    text = strip_machinery(report)
    if not scope:
        return text
    hits = _REPORT_REGION.findall(text)
    return "\n".join(hits) if hits else ""


def check_report(report: str, repo: str = ".", *, scope: bool = False,
                 sibling_repos: list | None = None, exclude_fixtures: bool = False):
    report = claim_region(report, scope=scope)
    findings = []

    # 1. Claimed commit SHAs — "committed as abc1234", "as `deadbee`", bare 7-40 hex tokens in context
    for m in re.finditer(r'\b(?:commit(?:ted)?\s+(?:as\s+)?`?|as\s+`)?([0-9a-f]{7,40})`?\b', report):
        sha = m.group(1)
        if not re.search(r'(commit|sha|as)\b', report[max(0, m.start()-24):m.start()], re.I):
            continue
        if exclude_fixtures and sha in _OWN_FIXTURES:
            # Opt-in, and never on by default: `deadbee` MUST still block in the
            # product's own demo, where it is a deliberately false claim. It is
            # skipped only when a caller says it is reading a corpus, because
            # there the same string is this repo's test data appearing in
            # transcripts about building this gate -- 6 of 40 sampled hits.
            continue
        r = _sh(["git", "cat-file", "-t", sha], repo)
        if r.returncode == 127:
            # The primary probe could not run at all — git missing, or the recorded
            # cwd no longer exists, which is ordinary in a corpus. Siblings are
            # still worth asking before calling an agent a liar; only if none of
            # them can answer either is this genuinely unverifiable.
            elsewhere = ""
            for alt in (sibling_repos or []):
                if _sh(["git", "cat-file", "-t", sha], alt).stdout.strip() == "commit":
                    elsewhere = alt
                    break
            if elsewhere:
                findings.append(Finding(f"committed as {sha}", PASS,
                                        f"git cat-file -t {sha}",
                                        f"is a commit, in {elsewhere} (the reported cwd was unreachable)"))
                continue
            findings.append(Finding(f"committed as {sha}", BLOCK,
                                    f"git cat-file -t {sha}",
                                    "NOT verifiable here (git missing in runtime) — treat as HOLD/BLOCK for safety"))
            continue
        ok = r.stdout.strip() == "commit"
        where = repo
        if not ok and sibling_repos:
            # THE REPO-RESOLUTION FIX. Measured on the corpus: 74 of 110 "wrong"
            # SHAs were real commits in ANOTHER repo on the same disk. An agent's
            # cwd is where it was standing, not where it committed. Probing only
            # cwd reports the agent as lying when the check was aimed at the wrong
            # object -- which is the failure this product is named after.
            for alt in sibling_repos:
                if alt == repo:
                    continue
                if _sh(["git", "cat-file", "-t", sha], alt).stdout.strip() == "commit":
                    ok, where = True, alt
                    break
        if ok and where != repo:
            findings.append(Finding(f"committed as {sha}", PASS,
                                    f"git cat-file -t {sha}",
                                    f"is a commit, in {where} (not the reported cwd)"))
        else:
            findings.append(Finding(f"committed as {sha}", PASS if ok else BLOCK,
                                    f"git cat-file -t {sha}",
                                    "is a commit" if ok else
                                    ("NOT a commit in this repo, nor in any of the "
                                     f"{len(sibling_repos)} sibling repos checked"
                                     if sibling_repos else
                                     "NOT a commit in this repo (no sibling repos were checked)")))

    # 2. Claimed file paths — "wrote/added/created/updated <path.ext>", including the
    #    natural-English forms an agent actually writes: "added the case to tests/x.py".
    #
    #    THE PERVERSE INCENTIVE THIS CLOSES. The pattern used to require the path to
    #    follow the verb immediately, so "wrote foo.py" was probed and "added the case
    #    to foo.py" was not. An agent whose report was loosely worded therefore got
    #    FEWER probes than one that was precise — the gate rewarded vagueness. Found on
    #    the Northwind end-to-end run 2026-08-27, where a true claim went unprobed.
    #
    #    The filler is a closed whitelist, not \w+, so the match cannot leap across a
    #    sentence and attribute an unrelated path to this verb. A wrongly-probed path
    #    is a false BLOCK on someone's good PR, which costs more than a missed probe.
    _FILLER = (r"(?:(?:the|a|an|new|another|case|cases|test|tests|file|files|line|lines|"
               r"note|notes|entry|section|coverage|it|to|in|into|at|for|of|and)\s+){0,4}")
    for m in re.finditer(r'(?:wrote|added|created|updated|extended)\s+' + _FILLER +
                         r'`?([\w./-]+\.\w{1,6})`?', report, re.I):
        path = m.group(1)
        if exclude_fixtures and path in _OWN_PATH_FIXTURES:
            continue
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


HELP = """witness — check an agent's done-report against the repository object.

  witness "Done. Committed as a41c9f2. Wrote src/cache.py."
  echo "$PR_BODY" | witness
  witness --json < report.md

  GATE_REPO=<path>   probe against that repo instead of the working directory

Exit code IS the verdict, not an error channel:
  0  PASS   every falsifiable claim checks out
  1  BLOCK  the repo disproves a claim
  2  HOLD   nothing disproved, but something is unverifiable

It never runs a command lifted from a report. A test claim is refused, not guessed.

Measure before you install anything:  witness-corpus --db <your-transcripts.db>
"""


def main(argv: list[str] | None = None) -> int:
    """Console entry point. Reads a done-report from argv or stdin, returns the exit code.

    Exit codes are the verdict, not an error channel: 0 PASS, 1 BLOCK, 2 HOLD. A crash
    is a different thing from a claim being false, which is the rule this tool exists
    to enforce, so it is enforced here too.
    """
    argv = sys.argv[1:] if argv is None else argv
    if any(a in ("-h", "--help") for a in argv):
        # A stranger's first keystroke. Treating it as a done-report and grading it
        # HOLD is technically consistent and practically a slammed door.
        print(HELP)
        return 0
    args = [a for a in argv if a != "--json"]
    as_json = "--json" in argv or os.environ.get("OUTCOME_GATE_JSON") == "1"
    report = sys.stdin.read() if not args else " ".join(args)
    return gate(report, os.environ.get("GATE_REPO", "."), as_json=as_json)


if __name__ == "__main__":
    sys.exit(main())
