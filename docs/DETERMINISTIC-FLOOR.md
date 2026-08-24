# The deterministic floor — an offline classifier that carries signal

_Runnable proof: `python3 contract/prove_lift.py` (no Gemini key, no GCP, no network)._

## The problem this closes

Two classifiers ship in this repo and **neither carries signal**:

| Implementation | CONTROLS score | What it really is |
|---|---|---|
| `classify_substring` (`fleet/signals._topic_match`, frozen in `contract/task_class.py`) | **3/8** | identical to `always-DIFFERENT` — passes only the three DIFFERENT rows by defaulting to DIFFERENT |
| `fleet/task_class.classify` no-key-file fallback | zero-signal | returns **SAME for "refactor the auth module" vs "add a dark mode toggle"** (probed 2026-08-23) — an `always-SAME` stub |

So a stranger who clones the repo with no GCP project and no Gemini key runs a
classifier that carries **no information** — and the two stubs fail in *opposite*
directions, so neither the substring nor the fallback is a safe default.

## The feature

`contract/deterministic.py` — a rule-based classifier from two general features, **no
network and no domain synonym table**:

1. **Intent bucket** = the *head verb* (earliest intent token in reading order):
   `CHANGE` / `DESCRIBE` / `REVERT` / `TEST`. Same object + incompatible bucket →
   `DIFFERENT`. This is what cracks the false-positive traps a substring test cannot:
   *refactor* vs *document* (change vs describe), *write a migration* vs *roll back the
   migration* (opposite direction).
2. **Object overlap** = the normalized nouns the work touches. No placeable object (only
   a pronoun: "fix it", "make it faster") → `UNDECIDABLE`, never a guess. Disjoint
   objects → `DIFFERENT`. Shared object + compatible intent → `SAME`.

## The numbers (measured, not claimed)

| Set | deterministic | no-signal baseline | lift |
|---|---|---|---|
| in-sample (`CONTROLS`, built against) | **6/8** | 3/8 | **+3** |
| held-out#1 (`HELDOUT`, dev set — seen, then 2 bugs fixed) | 4/8 | 3/8 | +1 |
| **held-out#2 (`HELDOUT2`, clean test — frozen before the run)** | **5/8** | 3/8 | **+2** |

Secondary metric (task_class.py's own definition of signal — right where the stub is
wrong): **held-out#2 2/5**.

The held-out#2 wins are all **on-mechanism**, not accidents of defaulting: the two
false-positive/opposite-direction traps (T5, T6), the undecidable row (T7), the
unrelated row (T4), and a head-verb row with a trailing side-constraint (T1). The three
misses (T2, T3, T8) are all **zero-lexical-overlap synonym pairs** — the rows that
require semantic knowledge and are the **LLM's earned slot** above this free floor.

## Why the held-out discipline is itself the finding

Held-out#1 was frozen *before* the classifier existed and the first classifier **tied
the no-signal stub on it (3/8)**. That blind tie is what exposed two general bugs
(head-verb intent; generic verbs mis-read as objects). Fixing only those two, then
re-validating on a *fresh* set frozen in git before the run (`b8de685`), produced the
+2. A control-set that can catch its own author is the product's whole thesis in
miniature.

## Complementarity with Gemini (reported, not wired)

`docs/VARIANCE-APPENDIX.md` records Gemini's **C1 ok-rate at 0%**. The deterministic
floor gets **C1 green** (auth ↔ auth, both CHANGE). The floor covers Gemini's known-red
row; Gemini covers the floor's zero-overlap rows (C2/C8, T2/T3/T8). This is a measured
complementarity — **it is not wired into an "8/8" hybrid**: the seal-forbidden rule
(`scripts/variance_appendix.py`, C1 red) stands, and the live path is Cursor's column.

## The open decision (Oscar)

Whether Cursor wires `classify_deterministic` in as the **offline fallback** in
`fleet/task_class.classify`, replacing the always-SAME no-key-file branch. That would
give the stranger path a classifier that carries signal for free, with Gemini layered on
top when a key/ADC is present. `fleet/` is Cursor's column — this is a routing decision,
not a Claude edit.
