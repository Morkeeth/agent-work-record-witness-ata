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


def test_KNOWN_SCOPE_GAP_only_the_denominator_shape_is_caught():
    """Honest limit of the folded feature, pinned so a future fix flips this red.

    The pitch says "every fact true, the composition false" — a whole class. The engine
    as folded implements ONE member of it: DENOMINATOR-EXCLUDES-ITS-FAILURES. Two sibling
    shapes it does NOT yet catch:
      - count-vs-its-own-list  ("54 repos" above 60 rows)
      - percent-then-contradiction ("90% coverage" above "2 files had zero tests")
    This test asserts the gap is REAL, so 'ADJACENT-FALSE is covered' can never be
    claimed while these return nothing. When the engine grows to catch one, delete its
    line here — the failure is the signal to update the pitch.
    """
    count_vs_list = "PROJECT PULSE · 54 repos\n" + "\n".join(f"repo{i}" for i in range(60))
    pct_then_contra = "90% coverage (18 of 20)\n2 files had zero tests"
    assert not find_adjacency(count_vs_list), "count-vs-list now caught — update the pitch + this test"
    assert not find_adjacency(pct_then_contra), "pct-then-contradiction now caught — update the pitch + this test"


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
