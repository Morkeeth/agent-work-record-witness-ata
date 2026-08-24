#!/usr/bin/env python3
"""A deterministic, offline task-class classifier — the free floor under the LLM.

WHAT THIS IS, AND WHY IT EARNS A SLOT
-------------------------------------
`contract/task_class.py` proves the shipping substring test scores 3/8 on the control
set -- identical to a stub that always answers DIFFERENT. No signal. And the no-key-file
fallback in `fleet/task_class.py` is worse: it answers SAME for plainly unrelated prompts
(auth-refactor vs dark-mode-toggle) -- an always-SAME stub, the OTHER zero-signal default.
So a stranger who clones the repo with no GCP project and no Gemini key runs a classifier
that carries no information at all.

This module is the fix that needs no network: a rule-based classifier built from two
features that separate software-work prompts WITHOUT a synonym table and WITHOUT peeking
at anything beyond the general shape of the task:

  1. INTENT BUCKET  -- what KIND of act the prompt opens (change / describe / revert /
     test). Two prompts on the same object but in incompatible buckets are DIFFERENT.
     This is what cracks the false-positive traps a substring test cannot: "refactor the
     auth module" vs "document the auth module" share every noun and are still different
     work (change vs describe); "write a migration" vs "roll back the migration" are
     opposite direction.
  2. OBJECT OVERLAP -- the normalized nouns the work touches. No object at all (only a
     pronoun: "fix it", "make it faster") -> UNDECIDABLE, never a guess. Disjoint objects
     -> DIFFERENT. Shared object + compatible bucket -> SAME.

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
It carries NO domain synonym map. It does not know that `login` is `validate_token`, or
that `package.json` is a `dependency`. Those rows (CONTROLS C2, C8) have zero lexical
overlap and require semantic knowledge -- they are exactly the rows an LLM must earn its
slot on. Leaving them red is the honest boundary: this floor is free and reproducible;
the model covers the semantic gap above it. Encoding those synonyms here would be copying
the answer key, not classifying.

Registered BESIDE classify_substring and classify_gemini and graded on the same control
set plus a FROZEN held-out set (`contract/heldout.py`). In-sample and held-out scores are
reported separately; the held-out number is the honest measure of whether this learned the
task or the rows.
"""
from __future__ import annotations

import re

SAME, DIFFERENT, UNDECIDABLE = "SAME", "DIFFERENT", "UNDECIDABLE"

# ------------------------------------------------------------------ intent buckets
# Multi-word phrases are checked first (see _intent) so "roll back" beats "back".
# CHANGE and its neighbours (fix/debug/refactor) are one compatible family: all of them
# alter or repair the same code. DESCRIBE is read-only. REVERT is the opposite direction.
# TEST is its own family. Only same-family (or CHANGE-internal) pairs can be SAME.
_INTENT_PHRASES = {
    "roll back": "REVERT", "rolling back": "REVERT",
}
_INTENT_WORDS = {
    # CHANGE family (create / modify / repair). Generic light verbs (make/let/get/do/
    # have) live here too: their only job is to be STRIPPED from the object set so
    # "make it faster" is seen as referent-less, not as an object called "make".
    "make": "CHANGE", "let": "CHANGE", "get": "CHANGE", "do": "CHANGE", "have": "CHANGE",
    "fix": "CHANGE", "refactor": "CHANGE", "extract": "CHANGE", "add": "CHANGE",
    "implement": "CHANGE", "build": "CHANGE", "create": "CHANGE", "write": "CHANGE",
    "update": "CHANGE", "bump": "CHANGE", "upgrade": "CHANGE", "change": "CHANGE",
    "edit": "CHANGE", "modify": "CHANGE", "wrap": "CHANGE", "optimize": "CHANGE",
    "optimise": "CHANGE", "improve": "CHANGE", "speed": "CHANGE", "harden": "CHANGE",
    "rename": "CHANGE", "move": "CHANGE", "migrate": "CHANGE", "tidy": "CHANGE",
    "clean": "CHANGE", "cleanup": "CHANGE", "format": "CHANGE", "debug": "CHANGE",
    "diagnose": "CHANGE", "trace": "CHANGE", "reproduce": "CHANGE", "broken": "CHANGE",
    "crash": "CHANGE", "crashes": "CHANGE", "failing": "CHANGE", "handle": "CHANGE",
    # DESCRIBE family (read-only)
    "document": "DESCRIBE", "describe": "DESCRIBE", "explain": "DESCRIBE",
    "summarize": "DESCRIBE", "summarise": "DESCRIBE", "comment": "DESCRIBE",
    "review": "DESCRIBE", "audit": "DESCRIBE", "benchmark": "DESCRIBE",
    "measure": "DESCRIBE", "profile": "DESCRIBE", "analyze": "DESCRIBE",
    "analyse": "DESCRIBE", "translate": "DESCRIBE", "localize": "DESCRIBE",
    "localise": "DESCRIBE",
    # REVERT family (opposite direction)
    "revert": "REVERT", "rollback": "REVERT", "undo": "REVERT", "remove": "REVERT",
    "delete": "REVERT", "downgrade": "REVERT", "disable": "REVERT", "deprecate": "REVERT",
    # TEST family
    "test": "TEST", "tests": "TEST", "coverage": "TEST", "cover": "TEST",
    "assert": "TEST", "spec": "TEST",
    # DEPLOY reads as CHANGE-forward, but its opposite (roll back) is REVERT -> the pair
    # is caught as incompatible.
    "deploy": "CHANGE", "ship": "CHANGE", "release": "CHANGE", "publish": "CHANGE",
}

# Intent is the HEAD verb: the earliest recognised intent token/phrase in reading order.
# A prompt's real job is named by its leading verb; later verbs ("...keep tests green",
# "...before applying") are side constraints, not the intent. Taking a max over all verbs
# let "keep tests green" turn a refactor into a TEST task -- the bug this replaced.

# Pronouns / fillers that name no object. A prompt whose only "object" is one of these
# cannot be placed -> UNDECIDABLE.
_NON_OBJECTS = {
    "it", "this", "that", "them", "these", "those", "everything", "anything",
    "stuff", "things", "thing", "something", "better", "faster", "cleaner",
    "nicer", "here", "there",
}

# Structural words that are neither intent nor object. Kept deliberately small: over-long
# stoplists start deleting real objects.
_STOP = {
    "the", "a", "an", "to", "of", "in", "into", "on", "for", "and", "or", "but",
    "with", "from", "by", "at", "as", "is", "are", "be", "been", "was", "were",
    "why", "how", "what", "when", "which", "who", "whose", "returns", "return",
    "yields", "yield", "keep", "green", "show", "me", "my", "our", "your", "new",
    "old", "up", "down", "out", "over", "under", "whole", "two", "word", "words",
    "page", "flow", "layer", "module", "so", "if", "then", "before", "after",
    "please", "can", "you", "do", "does", "not", "no", "all", "some", "any",
    "edge", "case", "cases", "set", "result", "nothing", "empty", "load", "box",
}

_TOKEN_RE = re.compile(r"[A-Za-z0-9_.]+")


def _tokens(text: str) -> list[str]:
    return [t.lower() for t in _TOKEN_RE.findall(text)]


def _intent(text: str) -> str | None:
    """The HEAD intent: the earliest intent token/phrase in reading order, or None."""
    low = text.lower()
    toks = _tokens(text)
    hits: list[tuple[float, str]] = []
    for i, tok in enumerate(toks):
        b = _INTENT_WORDS.get(tok)
        if b:
            hits.append((float(i), b))
    for phrase, bucket in _INTENT_PHRASES.items():
        if phrase in low:
            first = phrase.split()[0]
            if first in toks:
                # a phrase sits just before its head word so it wins ties at that position
                hits.append((toks.index(first) - 0.5, bucket))
    if not hits:
        return None
    hits.sort(key=lambda x: x[0])
    return hits[0][1]


def _compatible(bucket_a: str | None, bucket_b: str | None) -> bool:
    """Same bucket only. Unknown intent (None) is treated as CHANGE-compatible, so a
    prompt with a plain object and no recognised verb still clusters by object."""
    a = bucket_a or "CHANGE"
    b = bucket_b or "CHANGE"
    return a == b


def _norm(tok: str) -> list[str]:
    """Split snake_case / dotted paths, drop tiny fragments, strip a trailing plural s."""
    parts = re.split(r"[_.]", tok)
    out = []
    for p in parts:
        if len(p) < 2:
            continue
        if len(p) > 3 and p.endswith("s"):
            p = p[:-1]
        out.append(p)
    return out


def _objects(text: str) -> set[str]:
    objs: set[str] = set()
    for tok in _tokens(text):
        if tok in _STOP or tok in _NON_OBJECTS:
            continue
        if tok in _INTENT_WORDS:
            continue
        for n in _norm(tok):
            if n in _STOP or n in _INTENT_WORDS:
                continue
            objs.add(n)
    return objs


def _overlap(a: set[str], b: set[str]) -> bool:
    if a & b:
        return True
    # prefix-4 match for morphological variants (parser / parse, serializer / serialize)
    for x in a:
        if len(x) < 5:
            continue
        for y in b:
            if len(y) < 5:
                continue
            if x[:4] == y[:4]:
                return True
    return False


def classify_deterministic(prompt_a: str, prompt_b: str) -> str:
    """SAME | DIFFERENT | UNDECIDABLE — no network, no synonym table, no answer key.

    1. Either prompt has no placeable object -> UNDECIDABLE.
    2. Objects disjoint -> DIFFERENT.
    3. Objects overlap, intents incompatible -> DIFFERENT (the false-positive traps).
    4. Objects overlap, intents compatible -> SAME.
    """
    obj_a, obj_b = _objects(prompt_a), _objects(prompt_b)
    if not obj_a or not obj_b:
        return UNDECIDABLE
    if not _overlap(obj_a, obj_b):
        return DIFFERENT
    if not _compatible(_intent(prompt_a), _intent(prompt_b)):
        return DIFFERENT
    return SAME
