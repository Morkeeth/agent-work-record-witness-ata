#!/usr/bin/env python3
"""The task-class contract, and the control set any implementation must pass.

WHY THIS FILE EXISTS
--------------------
`docs/COMPLIANCE-AUDIT.md`: today's artifact satisfies 0 of 3 mandatory requirements,
and the fix for requirement 1 (Gemini 3.5) is the same fix as the wedge's worst defect.
`fleet/signals.py` decides whether two prompts are about the same work with
`all(t in low for t in terms)` -- a substring test, where the real relation is
TASK-CLASS IDENTITY.

This file does NOT implement the classifier. It states the interface, and it states the
control set that ANY implementation must satisfy -- written BEFORE the model exists, so
the requirement is pinned before anything can be tuned to whatever the model happens to do.

The current substring implementation is registered here as ONE implementation, not as the
product. It is expected to go RED. A failing control committed today is worth more than a
passing one written afterwards.

COLUMN NOTE: `contract/` is Claude's. `fleet/` is Cursor's. This file IMPORTS from fleet
read-only and never writes to it.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SAME, DIFFERENT, UNDECIDABLE = "SAME", "DIFFERENT", "UNDECIDABLE"


# ---------------------------------------------------------------- the interface
def classify(prompt_a: str, prompt_b: str) -> str:
    """Do these two prompts open the same class of work?

    Returns SAME | DIFFERENT | UNDECIDABLE.

    UNDECIDABLE is a first-class answer, not an error. A prompt with no referent
    ("fix it") cannot be placed, and an implementation that guesses rather than
    saying so fails the same law the rest of this product runs on.
    """
    raise NotImplementedError


# ------------------------------------------------- implementation 1: the substring test
def classify_substring(prompt_a: str, prompt_b: str) -> str:
    """What ships today, lifted from fleet/signals.py._topic_match.

    `_topic_match(text, topic)` asks: does every term of `topic` appear in `text`?
    Used as a same-class test that means: is one prompt's whole vocabulary inside
    the other's. Registered so the control set measures the REAL current behaviour.

    IMPORTED, NOT COPIED -- deliberately. The first version of this file reimplemented
    the substring test inline, which meant the control set graded a FROZEN COPY of
    Cursor's logic. The moment `fleet/signals.py` changed, the controls would have kept
    reporting on code that no longer ships, while staying the same colour. A control
    set that does not bind to the live object is a claim about the past.
    """
    from fleet.signals import _topic_match as match   # the LIVE function, not a copy
    if match(prompt_a, prompt_b) or match(prompt_b, prompt_a):
        return SAME
    return DIFFERENT          # note: it can never return UNDECIDABLE


# --------------------------------------------- the NEGATIVE CONTROL (a check that
# passes is not a check that ran)
def classify_always_different(prompt_a: str, prompt_b: str) -> str:
    """Returns DIFFERENT unconditionally. Carries zero information.

    If the shipping implementation scores the same as this, it is not classifying --
    it is defaulting, and its passing rows are accidents.
    """
    return DIFFERENT


# ---------------------------------------------------------------- the control set
# Every row: (id, prompt_a, prompt_b, expected, why this row exists)
CONTROLS = [
    ("C1", "fix auth",
     "Refactor the auth module: extract validate_token into auth/validate.py, "
     "keep tests green, show me the diff before applying.",
     SAME,
     "THE ROW THAT MATTERS. The real fixture pair. Both open work on auth. "
     "A human says same; a substring test cannot. Without SAME here the demo has "
     "no comparison and the field of candidates is one."),

    ("C2", "the login is broken",
     "Debug why validate_token returns None for expired sessions",
     SAME,
     "Same work, zero shared vocabulary. Defeats any keyword-overlap implementation."),

    ("C3", "add tests for the parser",
     "write unit tests covering parse_header edge cases",
     SAME,
     "Same class, synonymous verbs, partial overlap."),

    ("C4", "Refactor the auth module: extract validate_token into auth/validate.py",
     "add a dark mode toggle to the settings page",
     DIFFERENT,
     "Plainly unrelated. A classifier that says SAME here is worthless."),

    ("C5", "refactor the auth module",
     "document the auth module",
     DIFFERENT,
     "TRAP - FALSE POSITIVE. Near-identical vocabulary, different intent. "
     "This is the failure a substring test makes in the OTHER direction, and the "
     "one a lazily-prompted model makes too."),

    ("C6", "write a migration for the users table",
     "roll back the users table migration",
     DIFFERENT,
     "TRAP - FALSE POSITIVE, inverted intent. Almost every token is shared and the "
     "work is opposite."),

    ("C7", "fix it",
     "fix auth",
     UNDECIDABLE,
     "No referent. An implementation that returns SAME or DIFFERENT here is guessing, "
     "and guessing is the thing this product exists to refuse."),

    ("C8", "bump the dependency",
     "update package.json to the new lockfile",
     SAME,
     "Same class stated at two levels of abstraction."),
]


def run(impl, name):
    rows, passed = [], 0
    for cid, a, b, expected, why in CONTROLS:
        try:
            got = impl(a, b)
        except NotImplementedError:
            got = "NOT-IMPLEMENTED"
        ok = got == expected
        passed += ok
        rows.append((cid, ok, expected, got, why))
    print(f"\nCONTROL SET · implementation: {name}")
    print("=" * 78)
    for cid, ok, expected, got, why in rows:
        print(f"  {'PASS' if ok else 'FAIL'}  {cid}  expected {expected:<11} got {got}")
        if not ok:
            print(f"        why this row exists: {why}")
    print("-" * 78)
    print(f"  {passed}/{len(CONTROLS)} pass")
    return passed, len(CONTROLS)


if __name__ == "__main__":
    p1, t = run(classify_substring, "classify_substring (what ships today)")
    p0, _ = run(classify_always_different, "classify_always_different (NEGATIVE CONTROL)")
    print("\n" + "=" * 78)
    if p1 <= p0:
        print(f"  VERDICT: the shipping implementation scores {p1}/{t}.")
        print(f"           a function that always answers DIFFERENT scores {p0}/{t}.")
        print(f"           IT CARRIES NO SIGNAL ON THIS CONTROL SET. Its passing rows")
        print(f"           are accidents of always saying no, not classifications.")
    else:
        print(f"  the shipping implementation beats the negative control {p1} to {p0}.")
    print("=" * 78)
    print("\nThe interface is unimplemented by design — the model lands behind it.")
    print("This control set is RED today, and red is the point: the requirement is")
    print("pinned before anything can be tuned to whatever the model happens to do.")
    sys.exit(0 if p1 == t else 1)
