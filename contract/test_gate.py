"""The verification gate blocks a report that lies by composition, passes one that holds.

This is the merged product's single call, tested at both poles + the CI exit-code seam.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from contract.gate import verify_report, gate_report, PASS, BLOCK


def test_blocks_a_report_that_lies_by_composition():
    # every number true; 96% excludes the two cases named beneath it.
    r = verify_report("22 of 23 projects have a phase on disk (96%)\n21 no repo · 1 unknown")
    assert r.verdict == BLOCK and not r.ok
    assert r.exit_code() == 1
    assert r.findings and "true" in r.why.lower()


def test_passes_an_honestly_composed_report():
    r = verify_report("12 of 12 tests pass (100%)\nall green, nothing skipped")
    assert r.verdict == PASS and r.ok
    assert r.exit_code() == 0
    assert not r.findings


def test_catches_all_three_composition_shapes():
    for text in (
        "22 of 23 (96%)\n21 no repo · 1 unknown",                              # denominator
        "PROJECT PULSE · 54 repos\n" + "\n".join(f"repo{i}" for i in range(60)),  # count-vs-list
        "90% coverage (18 of 20)\n2 files had zero tests",                     # percent-contra
    ):
        assert verify_report(text).verdict == BLOCK, text


def test_task_axis_is_reported_but_not_gated():
    # a prompt pair adds the task/authorship axis; it never flips a PASS to BLOCK.
    r = verify_report(
        "12 of 12 tests pass (100%)\nall green",
        prompt_pair=("fix the auth module", "add a dark mode toggle"),
    )
    assert r.verdict == PASS            # composition holds -> still PASS
    assert r.task is not None and r.task["verdict"] in ("SAME", "DIFFERENT", "UNDECIDABLE")


def test_gate_report_is_human_readable():
    out = gate_report("22 of 23 (96%)\n21 no repo · 1 unknown")
    assert out.startswith("[BLOCK]") and "✗" in out


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
