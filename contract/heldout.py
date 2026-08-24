#!/usr/bin/env python3
"""HELD-OUT control set — frozen BEFORE the deterministic classifier was written.

WHY THIS FILE EXISTS
--------------------
`contract/deterministic.py` is a rule-based classifier authored while looking at the
eight rows of `task_class.CONTROLS`. A rule set tuned against the rows it will be graded
on has learned the answer key, not the task. That is the exact failure Oscar's memory
bank names ("control rows need every call-site shape", "a baseline must be frozen").

So these eight rows were written and committed FIRST, span the SAME trap categories as
CONTROLS with entirely different surface content, and the classifier was NOT allowed to
be edited after its held-out score was seen. The held-out number is the honest one. A
lower held-out score reported plainly is the product's thesis, not a defect.

Categories mirrored from CONTROLS:
  - SAME with low / zero shared vocabulary       (CONTROLS C1, C2)
  - SAME with synonymous verbs, partial overlap  (CONTROLS C3)
  - DIFFERENT, plainly unrelated area            (CONTROLS C4)
  - DIFFERENT, false-positive vocab overlap       (CONTROLS C5)  -- change vs describe
  - DIFFERENT, opposite direction, shared tokens  (CONTROLS C6)  -- do vs undo
  - UNDECIDABLE, no referent                      (CONTROLS C7)
  - SAME stated at two levels of abstraction      (CONTROLS C8)
"""
SAME, DIFFERENT, UNDECIDABLE = "SAME", "DIFFERENT", "UNDECIDABLE"

# Every row: (id, prompt_a, prompt_b, expected, why this row exists)
HELDOUT = [
    ("H1", "the search box returns nothing",
     "debug why query_index yields an empty result set for two-word queries",
     SAME,
     "SAME, low shared vocabulary. Both debug the search path. Mirrors C2."),

    ("H2", "add coverage for the serializer",
     "write unit tests for the encode_payload edge cases",
     SAME,
     "SAME class, synonymous verbs, partial overlap on 'serializ/encode'. Mirrors C3."),

    ("H3", "speed up the checkout page",
     "translate the checkout page into French",
     DIFFERENT,
     "DIFFERENT job on the SAME object. Optimising is not localising. A pure "
     "object-overlap test says SAME here and is wrong."),

    ("H4", "optimize the cache layer",
     "benchmark the cache layer under load",
     DIFFERENT,
     "TRAP - FALSE POSITIVE. Near-identical vocabulary, change vs measure. Mirrors C5."),

    ("H5", "deploy the new release to production",
     "roll back the production release",
     DIFFERENT,
     "TRAP - opposite direction, shared tokens. Ship vs revert. Mirrors C6."),

    ("H6", "make it faster",
     "profile the request handler",
     UNDECIDABLE,
     "No referent in prompt A. 'it' names no object that can be placed. Mirrors C7."),

    ("H7", "harden the login flow",
     "add rate limiting and lockout to the authentication endpoint",
     SAME,
     "SAME class, two levels of abstraction, minimal literal overlap "
     "('login'/'authentication'). Mirrors C8 + C1."),

    ("H8", "tidy up the imports in utils.py",
     "run the formatter over the whole repository",
     SAME,
     "SAME class (code hygiene) stated narrow vs broad. Mirrors C8."),
]
