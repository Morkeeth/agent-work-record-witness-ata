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
from contract.heldout import HELDOUT
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
    return scores


def main():
    print("DETERMINISTIC TASK-CLASS CLASSIFIER — offline lift proof")
    print("No Gemini key, no GCP, no network. Reproducible by any stranger.")

    c = show("IN-SAMPLE  ·  CONTROLS", CONTROLS)
    h = show("HELD-OUT   ·  HELDOUT (frozen before the classifier)", HELDOUT)

    base = "always-DIFFERENT (neg control)"
    det = "deterministic   (this build)  "
    print(f"\n{'='*70}\nVERDICT\n{'='*70}")
    print(f"  in-sample : deterministic {c[det]}/{len(CONTROLS)}  vs  "
          f"no-signal baseline {c[base]}/{len(CONTROLS)}")
    print(f"  held-out  : deterministic {h[det]}/{len(HELDOUT)}  vs  "
          f"no-signal baseline {h[base]}/{len(HELDOUT)}")
    in_lift = c[det] - c[base]
    out_lift = h[det] - h[base]
    print(f"  lift over no-signal baseline:  in-sample +{in_lift}   held-out +{out_lift}")
    if out_lift > 0:
        print("\n  HELD-OUT LIFT IS POSITIVE. The classifier carries signal on rows it")
        print("  never saw, not just the ones it was built against. The remaining misses")
        print("  are the zero-lexical-overlap SAME rows — the LLM's earned slot above")
        print("  this free floor.")
        rc = 0
    else:
        print("\n  HELD-OUT LIFT IS NOT POSITIVE. Reported honestly: this build did not")
        print("  generalise beyond the rows it was written against. An honest null.")
        rc = 1
    print("=" * 70)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
