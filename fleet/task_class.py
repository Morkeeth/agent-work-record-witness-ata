"""Task-class identity — delegates to contract.gemini_impl (read-only import).

NO MODEL, NO VERDICT.
---------------------
Until 2026-08-27 this module answered with a local substring heuristic whenever
no Gemini credential was present, and returned that answer as SAME/DIFFERENT with
nothing marking it as unmeasured. Two facts killed it:

1. The container ALWAYS took that path. `Dockerfile` does `COPY . .` and the key
   lives at ~/.config/keys/gemini.key, outside the repo, with no secret mount. So
   every verdict the deployed service ever produced came from the heuristic.
2. The heuristic was the negative control. Graded against `contract/task_class.py`
   CONTROLS it answered SAME on all 8 rows — row-for-row identical to
   `classify_always_same`, which that file defines as a control carrying ZERO
   information. It scored 4/8 and so appeared to BEAT the frozen substring
   baseline at 3/8, purely by defaulting.

A number that no model produced must not be reported as though one did. When no
model can be reached the answer is UNMEASURED, which `contract/task_class.run`
already treats as "could not be asked" rather than "got it wrong".
"""

import os

SAME, DIFFERENT, UNDECIDABLE = "SAME", "DIFFERENT", "UNDECIDABLE"
UNMEASURED = "UNMEASURED"

KEY_PATH = "~/.config/keys/gemini.key"

_CACHE: dict[tuple[str, str], str] = {}
_SOURCES: list[str] = []
_LAST_ERROR: list[str] = []


def _key(a: str, b: str) -> tuple[str, str]:
    return (a.strip(), b.strip()) if a.strip() <= b.strip() else (b.strip(), a.strip())


def key_file_present() -> bool:
    """Is the AI Studio key on disk? Cheap, no network call.

    NOT a gate. `contract.gemini_impl.classify_gemini` tries VERTEX/ADC first and
    only falls back to this key, so gating on the file would refuse to measure in
    exactly the environments that can (Cloud Run has ADC and no key file). The gate
    is the attempt itself: anything that does not come back as a verdict is
    UNMEASURED.
    """
    return os.path.isfile(os.path.expanduser(KEY_PATH))


def verdict_source() -> str:
    """What produced the verdicts in this process — for surfaces that must say so.

    Never let a caller render a count without being able to name its author.
    """
    if not _SOURCES:
        return "no-classification-run"
    if all(s == "unmeasured" for s in _SOURCES):
        return "unmeasured:no-model-credential"
    models = sorted({s for s in _SOURCES if s != "unmeasured"})
    if "unmeasured" in _SOURCES:
        return "mixed:" + ",".join(models) + ",unmeasured"
    return ",".join(models)


def classify(prompt_a: str, prompt_b: str) -> str:
    """SAME | DIFFERENT | UNDECIDABLE | UNMEASURED (no model reachable).

    UNMEASURED is a first-class answer, not an error, and it is NOT cached — an
    unreachable model is a transient condition of the environment, not a verdict
    about these two prompts. A credential can also appear mid-process.

    Every failure mode collapses to UNMEASURED on purpose: no ADC, no key file, a
    429, a safety filter, a socket error. None of them is evidence about the prompts,
    so none of them may be rendered as a verdict about the prompts.
    """
    ka = _key(prompt_a, prompt_b)
    if ka in _CACHE:
        return _CACHE[ka]

    try:
        from contract.gemini_impl import LAST_MODEL, classify_gemini
        out = classify_gemini(prompt_a, prompt_b)
    except Exception as e:
        # Missing key file included: gemini_impl._key() opens KEY_PATH unguarded.
        _SOURCES.append("unmeasured")
        _LAST_ERROR.append(f"{type(e).__name__}")
        return UNMEASURED

    if out not in (SAME, DIFFERENT, UNDECIDABLE):
        _SOURCES.append("unmeasured")
        _LAST_ERROR.append(str(out))
        return UNMEASURED

    _SOURCES.append("gemini:" + (LAST_MODEL[-1] if LAST_MODEL else "unknown"))
    _CACHE[ka] = out
    return out


def same_task_class(prompt_a: str, prompt_b: str) -> bool:
    """True only when a model actually answered SAME. UNMEASURED is not SAME."""
    return classify(prompt_a, prompt_b) == SAME
