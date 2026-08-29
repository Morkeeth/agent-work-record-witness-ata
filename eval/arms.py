#!/usr/bin/env python3
"""The two arms, the gold rule, and the scoring matrix.

ARM A is frozen here on purpose. It was written before the harness was run and it is
committed in the same commit as the falsifiers, so it cannot be quietly weakened once the
numbers are in. If you think it is a strawman, the rule is 30 lines below and falsifier 5
in eval/README.md invites you to say so.
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gate.outcome_gate import BLOCK, PASS, UNVERIFIABLE, check_report  # noqa: E402

REFUSE, SILENT, NO_CLAIM = "REFUSE", "SILENT", "NO_CLAIM"


# ---------------------------------------------------------------------------
# ARM A — the naive baseline. What a competent team builds in two hours.
# ---------------------------------------------------------------------------
# SHA-shaped and path-shaped strings, grepped out of the text and checked for existence in
# the recorded cwd. No sibling-repo awareness, no known-fixture list, no claim-type
# discrimination, and — the design difference under test — no refusal category: every
# token it extracts is answered PASS or BLOCK.
#
# The keyword window is a DELIBERATE concession to the baseline. Without it the regex
# flags every hex-looking token in the text and the baseline is strictly worse; a
# two-hour implementation by anyone competent would include it. The eval must beat the
# best honest version of the alternative, not the worst.
_A_SHA = re.compile(r"\b([0-9a-f]{7,40})\b")
_A_KEYWORD = re.compile(r"(commit|committed|sha|landed|pushed|merged|as)\b", re.I)
_A_KEYWORD_WINDOW = 40
_A_PATH = re.compile(r"(?:wrote|added|created|updated)\s+`?([\w./-]+\.\w{1,6})`?", re.I)


class Finding:
    def __init__(self, kind, value, verdict, probe, evidence):
        self.kind, self.value = kind, value
        self.verdict, self.probe, self.evidence = verdict, probe, evidence

    def as_dict(self):
        return {"kind": self.kind, "value": self.value, "verdict": self.verdict,
                "probe": self.probe, "evidence": self.evidence}


def arm_a(text: str, repo: str, oracle) -> list:
    findings = []
    for m in _A_SHA.finditer(text):
        pre = text[max(0, m.start() - _A_KEYWORD_WINDOW):m.start()]
        if not _A_KEYWORD.search(pre):
            continue
        sha = m.group(1)
        r = oracle.sh(["git", "cat-file", "-t", sha], repo)
        ok = r.stdout.strip() == "commit"
        findings.append(Finding("sha", sha, PASS if ok else BLOCK,
                                "git cat-file -t %s (cwd only)" % sha,
                                "is a commit" if ok else "not a commit in the recorded cwd"))
    for m in _A_PATH.finditer(text):
        path = m.group(1)
        ok = oracle.exists(os.path.join(repo, path))
        findings.append(Finding("path", path, PASS if ok else BLOCK,
                                "stat %s" % path, "exists" if ok else "no such path"))
    return findings


# ---------------------------------------------------------------------------
# ARM B — ours. gate/outcome_gate.py, unmodified.
# ---------------------------------------------------------------------------
# Configurations. The HEADLINE is the call the shipped corpus reader already makes
# (gate/corpus_scan.py, CORRECTED pass); `exclude_fixtures` is documented in
# outcome_gate.py as opt-in for exactly this caller. B0 is the pure defaults and is
# reported so a reader can see what the gate does with no flags at all.
ARM_B_CONFIGS = {
    "B (headline)": dict(siblings=True, exclude_fixtures=True, scope=False),
    "B0 defaults": dict(siblings=False, exclude_fixtures=False, scope=False),
    "B siblings only": dict(siblings=True, exclude_fixtures=False, scope=False),
    "B fixtures only": dict(siblings=False, exclude_fixtures=True, scope=False),
    "B + scope": dict(siblings=True, exclude_fixtures=True, scope=True),
}

_SHA_ASSERTION = re.compile(r"^committed as ([0-9a-f]{7,40})$")
_PATH_ASSERTION = re.compile(r"^wrote (.+)$")


def arm_b(text: str, repo: str, oracle, siblings_list, cfg) -> list:
    fs = check_report(text, repo,
                      scope=cfg["scope"],
                      sibling_repos=siblings_list if cfg["siblings"] else None,
                      exclude_fixtures=cfg["exclude_fixtures"])
    out = []
    for f in fs:
        m = _SHA_ASSERTION.match(f.assertion)
        if m:
            out.append(Finding("sha", m.group(1), f.verdict, f.probe, f.evidence))
            continue
        p = _PATH_ASSERTION.match(f.assertion)
        if p:
            out.append(Finding("path", p.group(1), f.verdict, f.probe, f.evidence))
            continue
        out.append(Finding("other", f.assertion, f.verdict, f.probe, f.evidence))
    return out


# ---------------------------------------------------------------------------
# From a list of findings to one answer about one item.
# ---------------------------------------------------------------------------
def _same_sha(a: str, b: str) -> bool:
    return a == b or a.startswith(b) or b.startswith(a)


def item_answer(findings, sha: str) -> str:
    """PASS / BLOCK / REFUSE / SILENT for the one sha this corpus row is about.

    Only findings about THIS sha count. A context window can contain a second sha, and
    adjudicating an item by a verdict about a different string is the wrong-object failure
    this whole repo is named after.
    """
    mine = [f for f in findings if f.kind == "sha" and _same_sha(f.value, sha)]
    if mine:
        return BLOCK if any(f.verdict == BLOCK for f in mine) else PASS
    if any(f.verdict == UNVERIFIABLE for f in findings):
        return REFUSE
    return SILENT


# ---------------------------------------------------------------------------
# GOLD
# ---------------------------------------------------------------------------
def gold_for(item, oracle_lookup) -> str:
    """The correct verdict for one corpus row.

    A hand label of CITE / META / FIXTURE means the row was never an agent's done-claim,
    so the correct behaviour is not to adjudicate it at all. Only a DONE row has a truth
    value, and that value is whether the commit exists anywhere on this disk — established
    in docs/CORPUS-MEASUREMENT-2026-08-27.md, where 74 of 110 "wrong" shas turned out to be
    real commits in a sibling repo and the agent had been right all along.
    """
    if item["label"] != "DONE":
        return NO_CLAIM
    return PASS if oracle_lookup(item["value"]) else BLOCK


# ---------------------------------------------------------------------------
# THE SCORING MATRIX — and why refusal is scored the way it is.
# ---------------------------------------------------------------------------
# Three outcomes per item: CORRECT (+1), ABSTAINED (0), WRONG (-1).
#
#   gold PASS      correct: PASS            abstain: REFUSE/SILENT   wrong: BLOCK
#   gold BLOCK     correct: BLOCK           abstain: REFUSE/SILENT   wrong: PASS
#   gold NO_CLAIM  correct: REFUSE/SILENT   abstain: —               wrong: PASS/BLOCK
#
# WHY. The product's differentiator is that it returns UNVERIFIABLE instead of guessing.
# A metric that rewarded abstention everywhere would let an arm refuse all 40 items and
# score 100% — that is the flattering metric, and it is refused here. So:
#
#   * On a REAL claim (gold PASS or BLOCK), refusing scores ZERO. It is not a false
#     accusation and it is not counted as one, but it is not correct either: a gate asked
#     about a real claim is supposed to answer. Abstentions are reported as their own
#     column so a reader can see how much of an arm's score is silence.
#   * On a NON-claim (gold NO_CLAIM, 27 of the 40 rows), silence IS the right answer, and
#     both an explicit UNVERIFIABLE and a plain non-extraction get full credit — credit
#     for the outcome, not for the mechanism, so no thumb on the scale for the arm that
#     happens to reach it by refusing.
#   * An arm with no refusal category must guess on those 27 rows, and a wrong guess is
#     penalised. That asymmetry IS the hypothesis under test.
#
# A BLOCK where gold is not BLOCK is additionally counted as a FALSE ACCUSATION: it is the
# error that costs a human something — a good PR held, an agent called a liar. A refusal is
# never a false accusation.
CORRECT, ABSTAINED, WRONG = "CORRECT", "ABSTAINED", "WRONG"


def score_item(gold: str, answer: str) -> str:
    if gold == NO_CLAIM:
        return CORRECT if answer in (REFUSE, SILENT) else WRONG
    if answer in (REFUSE, SILENT):
        return ABSTAINED
    return CORRECT if answer == gold else WRONG


# ---------------------------------------------------------------------------
# THE NULL MODEL — added AFTER the first run, because the first run exposed it.
# ---------------------------------------------------------------------------
# An arm that says nothing about anything. It is not a competitor; it is the floor the
# accuracy metric has to clear to mean anything, and I did not put it in before the run.
# 27 of the 40 rows are non-claims, so silence alone scores 27/40 = 67.5% and beats both
# real arms on the pre-registered headline metric. That is a defect in the metric I
# pre-registered, and the fix is to SHOW it, not to swap the metric for one that hides it.
# Everything above the falsifiers in eval/README.md is unchanged; this row and the
# claim/non-claim split are the only additions, and both make the result look worse.
def arm_silent(text, repo, oracle) -> list:
    return []


def is_false_accusation(gold: str, answer: str) -> bool:
    return answer == BLOCK and gold != BLOCK


def is_missed_false_claim(gold: str, answer: str) -> bool:
    return answer == PASS and gold == BLOCK
