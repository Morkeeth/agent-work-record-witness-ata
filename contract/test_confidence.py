"""The deterministic floor knows when it doesn't know — the cascade boundary.

classify_deterministic answers every pair, and on the synonym tail ("fix auth" vs
"repair authentication") it guesses DIFFERENT and is wrong. classify_with_confidence
adds the one thing that makes a cheap tier safe to trust: it marks that guess
NOT-confident and defers it to the model. The claim this pins, measured on the frozen
CONTROLS + both held-out sets:

  1. when the floor is CONFIDENT, it is never wrong   (precision 1.0 on the kept set)
  2. every row the floor gets wrong is a row it DEFERRED  (its errors live in the tail)
  3. a cascade that escalates only the deferred tail recovers every row
  4. it stays cheap — it does not defer everything

That is the LLM-cascade result (escalate only the low-confidence tail; arXiv:2502.09054)
made deterministic: the model pays only for the tail, and every answer the floor keeps
is right.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from contract.deterministic import classify_with_confidence, classify_cascade
from contract.task_class import CONTROLS
from contract.heldout import HELDOUT, HELDOUT2

ROWS = list(CONTROLS) + list(HELDOUT) + list(HELDOUT2)


def _rows():
    for r in ROWS:
        yield r[0], r[1], r[2], r[3]  # id, a, b, gold


def test_confident_answers_are_never_wrong():
    wrong_confident = [
        rid for rid, a, b, gold in _rows()
        if (lambda vc: vc[1] and vc[0] != gold)(classify_with_confidence(a, b))
    ]
    assert wrong_confident == [], f"floor was confident AND wrong on {wrong_confident}"


def test_every_floor_error_is_deferred_not_asserted():
    # A row the floor gets wrong must be one it flagged NOT-confident (deferred), never
    # one it asserted. This is what makes the kept set safe.
    asserted_errors = []
    for rid, a, b, gold in _rows():
        verdict, confident = classify_with_confidence(a, b)
        if verdict != gold and confident:
            asserted_errors.append(rid)
    assert asserted_errors == [], f"floor asserted a wrong verdict on {asserted_errors}"


def test_cascade_recovers_every_row_when_the_tail_escalates():
    def oracle(a, b):
        return next(r[3] for r in ROWS if r[1] == a and r[2] == b)

    got = sum(1 for _rid, a, b, gold in _rows()
              if classify_cascade(a, b, escalate=oracle)[0] == gold)
    assert got == len(ROWS), f"cascade+oracle only got {got}/{len(ROWS)}"


def test_stays_cheap_confident_on_a_real_share():
    confident = sum(1 for _rid, a, b, _g in _rows()
                    if classify_with_confidence(a, b)[1])
    deferred = len(ROWS) - confident
    # not degenerate: it answers a real share on its own AND defers a real tail.
    assert confident >= len(ROWS) // 3, f"only {confident}/{len(ROWS)} confident — floor too timid"
    assert deferred >= 1, "floor deferred nothing — the tail is where the model earns its cost"


def test_no_escalate_still_returns_the_floor_guess_tagged():
    # A caller with no model still gets an answer, tagged so it can see it was unescalated.
    v, tier = classify_cascade("fix the auth module", "repair the authentication layer")
    assert tier == "floor" and v in ("SAME", "DIFFERENT", "UNDECIDABLE")


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
