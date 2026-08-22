#!/usr/bin/env python3
"""The claim gate — nothing an agent says is 'done' passes until the OBJECT confirms it.

WHY THIS IS THE PRODUCT, not prompt-propagation.
------------------------------------------------
Every real failure this fleet caught in one night had the same shape: a confident "done" /
"3 of 3" / "7/8" / "it's running" that the object contradicted. The propagation demo is one
small autonomous act; THIS is the one an org cannot ship agents to production without.

Observability tools score the TRACE (what the agent did). This gates the CLAIM (whether what
it SAID is true), across four claim types that a single repo-vs-trace check does not cover —
because tonight proved the false claim is usually not a fabricated SHA. It is:
  - an import mistaken for a call,
  - one sample quoted as a measurement,
  - a kernel run mistaken for a scored submission,
  - a default path mistaken for the configured one.

Each verdict names the probe that produced it and refuses (UNMEASURED) rather than guessing.
"""
import math, os, subprocess, sys
from dataclasses import dataclass

PASS, BLOCK, UNMEASURED = "PASS", "BLOCK", "UNMEASURED"


@dataclass
class Verdict:
    claim: str
    verdict: str
    probe: str
    evidence: str


# ---- probe 1: REPO — a claimed SHA / path exists in the repo (the ci_gate primitive) ----
def probe_repo(claim, *, sha=None, path=None, repo="."):
    if sha:
        r = subprocess.run(["git", "-C", repo, "cat-file", "-t", sha],
                           capture_output=True, text=True)
        ok = r.stdout.strip() == "commit"
        return Verdict(claim, PASS if ok else BLOCK, f"git cat-file -t {sha}",
                       r.stdout.strip() or r.stderr.strip()[:60])
    if path:
        ok = os.path.exists(os.path.join(repo, path))
        return Verdict(claim, PASS if ok else BLOCK, f"stat {path}",
                       "exists" if ok else "no such path in repo")
    return Verdict(claim, UNMEASURED, "repo", "no SHA or path to probe")


# ---- probe 2: POWER — a rate quoted as a result must survive a re-run at its own n ----
def probe_power(claim, *, k, n, min_n=30, ci_halfwidth_max=0.10):
    if n < min_n:
        return Verdict(claim, UNMEASURED, f"power n={n}",
                       f"n={n} < {min_n}: one sample, not a measurement")
    p = k / n
    half = 1.96 * math.sqrt(p * (1 - p) / n)
    ok = half <= ci_halfwidth_max
    return Verdict(claim, PASS if ok else UNMEASURED, f"95% CI on n={n}",
                   f"{p:.1%} +/- {half:.1%}" + ("" if ok else "  (too wide to quote)"))


# ---- probe 3: EXERCISE — a service must be CALLED, not merely imported ----
def probe_exercise(claim, *, call, want):
    """`call` is a zero-arg thunk that returns the thing actually used; `want` is a predicate."""
    try:
        got = call()
    except Exception as e:
        return Verdict(claim, BLOCK, "exercise", f"raised {type(e).__name__}: {e}")
    ok = want(got)
    return Verdict(claim, PASS if ok else BLOCK, "exercise (called, not imported)",
                   f"got {got!r}" + ("" if ok else "  — import is not call"))


# ---- probe 4: RIGHT-OBJECT — the claim must be checked against the object it is about ----
def probe_right_object(claim, *, observed, expected_kind, actual_kind):
    """Guards the kernel-vs-submission / default-vs-configured class: same-looking, wrong thing."""
    ok = expected_kind == actual_kind
    return Verdict(claim, PASS if ok else BLOCK, f"object kind == {expected_kind}",
                   f"observed on a {actual_kind}, claim is about a {expected_kind}"
                   if not ok else f"confirmed on the {expected_kind}: {observed}")


def report(verdicts):
    blocks = [v for v in verdicts if v.verdict == BLOCK]
    unmeas = [v for v in verdicts if v.verdict == UNMEASURED]
    print("=" * 74)
    print("  CLAIM GATE — an agent said done; the object was asked")
    print("=" * 74)
    for v in verdicts:
        print(f"  {v.verdict:<10} {v.claim}")
        print(f"             probe: {v.probe}   ->   {v.evidence}")
    print("-" * 74)
    if blocks:
        print(f"  GATE: BLOCK — {len(blocks)} claim(s) the object disproves. Do not ship.")
        code = 1
    elif unmeas:
        print(f"  GATE: HOLD — {len(unmeas)} claim(s) unmeasured. Unmeasured is not clean.")
        code = 2
    else:
        print("  GATE: PASS — every claim confirmed against its object.")
        code = 0
    print("=" * 74)
    return code


if __name__ == "__main__":
    sys.exit(report(__import__("gate.tonight_cases", fromlist=["CASES"]).CASES()))
