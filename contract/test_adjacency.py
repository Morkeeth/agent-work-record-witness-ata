"""ADJACENT-FALSE, folded in from agent-claims-inbox — the composition check.

The authorship + task-class work answers "who wrote this, and is it the same task."
This answers the other half a fleet needs before it trusts a report: is the report's
COMPOSITION honest, even when every individual number is true? A denominator that
quietly excludes the failures printed right under it shows 96% where the truth is 50% —
every figure correct, the pair a lie. No per-claim attestation catches it.

This is the merge: the ADJACENT-FALSE detector now lives inside the admissible shell, so
one submission carries both the corpus (whose prompt worked) and the check (whether the
work it reports is honestly composed).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from contract.adjacency import find_adjacency


def test_denominator_that_excludes_its_own_failures_is_flagged():
    # every number true; the 96% excludes the two cases named directly beneath it.
    text = "22 of 23 projects have a phase on disk (96%)\n21 no repo · 1 unknown"
    found = find_adjacency(text)
    assert found, "the composed-false report was not flagged"
    assert found[0]["kind"] == "DENOMINATOR-EXCLUDES-ITS-FAILURES"
    # the finding must carry both lines — the point is the RELATIONSHIP, not one line
    assert "22 of 23" in found[0]["a"] and "21 no repo" in found[0]["b"]


def test_an_honestly_composed_report_is_quiet():
    # consistent numbers -> no finding. A checker that fires on everything is the
    # always-DIFFERENT stub of this class; it must stay silent when the pair holds.
    for good in (
        "12 of 12 tests pass (100%)\nall green, nothing skipped",
        "shipped 3 files across 3 deliveries\neach delivery named and hashed",
        "just prose with no numeric claims at all",
    ):
        assert not find_adjacency(good), f"false positive on: {good!r}"


def test_denominator_defect_fires_on_any_subject_not_a_keyword():
    # the class is the NUMBER relationship, not the word "projects": a different subject
    # with the same denominator-excludes shape still fires.
    text = "40 of 42 items cleared (95%)\n38 blocked · 2 pending"
    assert find_adjacency(text), "missed the same denominator defect on a different subject"


def test_count_that_disagrees_with_its_own_list_is_flagged():
    """The second member: a headline count above a list of a different length.

    Both the markdown path ("MCP Server (14 tools)" over a 12-row table) and the
    bare-row path ("54 repos" over 60 plain lines) belong to one kind. The kind is
    asserted explicitly so a different detector firing cannot fake the pass.
    """
    # bare rows — no bullet, no pipe — is the shape the folded engine used to miss.
    count_vs_list = "PROJECT PULSE · 54 repos\n" + "\n".join(f"repo{i}" for i in range(60))
    found = find_adjacency(count_vs_list)
    assert found, "count-vs-bare-list not flagged"
    assert found[0]["kind"] == "COUNT-DISAGREES-WITH-ITS-LIST"

    # markdown table: a parenthesised count over 12 data rows.
    table = "MCP Server (14 tools)\n| tool | note |\n|---|---|\n" + "\n".join(
        f"| t{i} | ok |" for i in range(12)
    )
    tfound = find_adjacency(table)
    assert tfound and tfound[0]["kind"] == "COUNT-DISAGREES-WITH-ITS-LIST", (
        "count-over-table not flagged"
    )


def test_count_vs_list_stays_quiet_on_honest_shapes():
    # A count is not its list only when the lengths differ AND a list truly follows.
    for good in (
        # a count followed by PROSE, not a list — sentences, not rows.
        "Deployed 54 repos\nProduction is stable now.\nMonitoring looks clean.",
        # the count matches the list it heads.
        "3 files changed\nalpha\nbeta\ngamma",
        # a bare-row block under three rows never counts (signature/fragment guard).
        "shipped 9 repos\nalpha\nbeta",
    ):
        assert not find_adjacency(good), f"count-vs-list false positive on: {good!r}"


def test_percent_contradicted_by_a_categorical_zero_below_is_flagged():
    # 18 of 20 is CONSISTENT with "2 zero-test files" (2 = 20-18); the flag is not
    # arithmetic. A success percentage above a positive count of items holding ZERO
    # of the measured thing is the contradiction.
    text = "90% coverage (18 of 20)\n2 files had zero tests"
    found = find_adjacency(text)
    assert found, "percent-then-categorical-zero not flagged"
    assert found[0]["kind"] == "PERCENT-CONTRADICTED-BELOW"
    assert "90% coverage" in found[0]["a"] and "zero tests" in found[0]["b"]


def test_percent_contradiction_stays_quiet_on_honest_shapes():
    # The dangerous false positive of this whole class is firing on honest
    # elaboration. Each of these must stay silent.
    for good in (
        # elaboration: names the gap, but with no zero-word — a gradient, not a hole.
        "90% coverage (18 of 20)\n2 files still need review",
        # zero applied to a BAD thing is good news, and the count is 0 besides.
        "100% pass (20 of 20)\n0 failures",
        # the existing all-green report, restated for this detector.
        "12 of 12 tests pass (100%)\nall green, nothing skipped",
        # a LOW percentage already implies failures exist — not a contradiction.
        "10% coverage (2 of 20)\n18 files had zero tests",
        # the zero-word rides a failure verb: "zero tests failed" is honest.
        "95% pass (19 of 20)\n5 suites ran; zero tests failed",
    ):
        assert not find_adjacency(good), f"percent-contradiction false positive on: {good!r}"


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in fns:
        try:
            fn(); print(f"PASS  {fn.__name__}")
        except AssertionError as e:
            failed += 1; print(f"FAIL  {fn.__name__}: {e}")
    print(f"\n{len(fns) - failed}/{len(fns)} passed")
    sys.exit(1 if failed else 0)
