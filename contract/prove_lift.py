#!/usr/bin/env python3
"""Prove the deterministic classifier carries signal the substring stub does not.

Runs entirely offline -- no Gemini key, no GCP, no network. Grades four implementations
on TWO sets:
  - CONTROLS   (contract/task_class.py)   the in-sample rows the classifier was built against
  - HELDOUT    (contract/heldout.py)      frozen BEFORE the classifier existed

and prints, for each, the score against the always-DIFFERENT and always-SAME negative
controls. The claim the pitch is allowed to make is exactly what this prints: a number,
reproducible by a stranger with nothing installed.
"""
from __future__ import annotations

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contract.task_class import (
    CONTROLS, classify_substring, classify_always_different, classify_always_same,
)
from contract.heldout import HELDOUT, HELDOUT2
from contract.deterministic import classify_deterministic


def grade(impl, rows) -> tuple[int, list[tuple]]:
    detail = []
    passed = 0
    for cid, a, b, expected, _why in rows:
        got = impl(a, b)
        ok = (got == expected)
        passed += ok
        detail.append((cid, expected, got, ok))
    return passed, detail


def show(name, rows):
    n = len(rows)
    print(f"\n{'='*70}\n{name}  ({n} rows)\n{'='*70}")
    impls = [
        ("always-DIFFERENT (neg control)", classify_always_different),
        ("always-SAME     (neg control)", classify_always_same),
        ("substring       (what ships)  ", classify_substring),
        ("deterministic   (this build)  ", classify_deterministic),
    ]
    scores = {}
    det_detail = None
    for label, impl in impls:
        p, detail = grade(impl, rows)
        scores[label] = p
        print(f"  {label}  {p}/{n}")
        if impl is classify_deterministic:
            det_detail = detail
    print("  " + "-" * 66)
    print("  deterministic per-row:")
    for cid, expected, got, ok in det_detail:
        mark = "PASS" if ok else "FAIL"
        print(f"    {mark}  {cid}  expected {expected:<11} got {got}")
    # SECONDARY metric: rows correct where always-DIFFERENT is WRONG (the SAME/UNDECIDABLE
    # rows). This is task_class.py's own definition of "carries signal", not a new goalpost.
    stub_wrong = [r for r in rows if classify_always_different(r[1], r[2]) != r[3]]
    det_right_where_stub_wrong = sum(
        1 for cid, e, g, ok in det_detail
        if ok and any(r[0] == cid for r in stub_wrong))
    scores["_unique_wins"] = det_right_where_stub_wrong
    scores["_stub_wrong"] = len(stub_wrong)
    print(f"  unique wins (deterministic right where always-DIFFERENT is wrong): "
          f"{det_right_where_stub_wrong}/{len(stub_wrong)}")
    return scores


def main():
    print("DETERMINISTIC TASK-CLASS CLASSIFIER — offline lift proof")
    print("No Gemini key, no GCP, no network. Reproducible by any stranger.")

    c = show("IN-SAMPLE   ·  CONTROLS", CONTROLS)
    h1 = show("HELD-OUT#1  ·  HELDOUT (dev set: seen; 2 bugs fixed after)", HELDOUT)
    h2 = show("HELD-OUT#2  ·  HELDOUT2 (test set: frozen before the fixed run)", HELDOUT2)

    base = "always-DIFFERENT (neg control)"
    det = "deterministic   (this build)  "
    print(f"\n{'='*70}\nVERDICT\n{'='*70}")
    print(f"  in-sample  (built against): deterministic {c[det]}/{len(CONTROLS)}  vs  "
          f"no-signal baseline {c[base]}/{len(CONTROLS)}   (+{c[det]-c[base]})")
    print(f"  held-out#1 (dev, post-fix): deterministic {h1[det]}/{len(HELDOUT)}  vs  "
          f"no-signal baseline {h1[base]}/{len(HELDOUT)}   (+{h1[det]-h1[base]})")
    print(f"  held-out#2 (clean test)   : deterministic {h2[det]}/{len(HELDOUT2)}  vs  "
          f"no-signal baseline {h2[base]}/{len(HELDOUT2)}   (+{h2[det]-h2[base]})")
    print(f"\n  secondary (unique wins, right where the stub is wrong):")
    print(f"    in-sample  {c['_unique_wins']}/{c['_stub_wrong']}   "
          f"held-out#2  {h2['_unique_wins']}/{h2['_stub_wrong']}")
    out_lift = h2[det] - h2[base]
    print()
    if out_lift > 0:
        print("  HELD-OUT#2 LIFT IS POSITIVE. The classifier carries signal on a clean test")
        print("  set it never saw. The remaining misses are the zero-lexical-overlap SAME")
        print("  rows (T2, T8) — the LLM's earned slot above this free, offline floor.")
        rc = 0
    else:
        print("  HELD-OUT#2 LIFT IS NOT POSITIVE. Reported honestly: an honest null — the")
        print("  product's own thesis. No third fix round; this is the result.")
        rc = 1
    print("=" * 70)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
