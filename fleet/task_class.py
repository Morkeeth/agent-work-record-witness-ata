"""Task-class identity — delegates to contract.gemini_impl (read-only import)."""

import os

SAME, DIFFERENT, UNDECIDABLE = "SAME", "DIFFERENT", "UNDECIDABLE"
UNMEASURED = "UNMEASURED"

_CACHE: dict[tuple[str, str], str] = {}


def _key(a: str, b: str) -> tuple[str, str]:
    return (a.strip(), b.strip()) if a.strip() <= b.strip() else (b.strip(), a.strip())


def classify(prompt_a: str, prompt_b: str) -> str:
    """SAME | DIFFERENT | UNDECIDABLE | UNMEASURED (API unreachable)."""
    ka = _key(prompt_a, prompt_b)
    if ka in _CACHE:
        return _CACHE[ka]
    key_path = os.path.expanduser("~/.config/keys/gemini.key")
    if not os.path.isfile(key_path):
        terms = [t for t in prompt_a.lower().split() if len(t) > 2] + \
                [t for t in prompt_b.lower().split() if len(t) > 2]
        low_a, low_b = prompt_a.lower(), prompt_b.lower()
        out = SAME if any(t in low_a for t in terms) and any(t in low_b for t in terms) else DIFFERENT
        _CACHE[ka] = out
        return out
    from contract.gemini_impl import classify_gemini
    out = classify_gemini(prompt_a, prompt_b)
    if str(out).startswith(("API-ERROR", "NO-CANDIDATE")):
        _CACHE[ka] = UNMEASURED
        return UNMEASURED
    _CACHE[ka] = out
    return out


def same_task_class(prompt_a: str, prompt_b: str) -> bool:
    """True when Gemini (or legacy fallback) says SAME."""
    return classify(prompt_a, prompt_b) == SAME
