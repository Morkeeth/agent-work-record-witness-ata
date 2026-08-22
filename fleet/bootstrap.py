"""Load Google surfaces on the path a judge actually runs.

Eligibility (`contract/eligibility.py`) checks `sys.modules` after the entry
path executes — seams that never import do not count. Call `ensure_google_stack()`
from the wedge entry so ADK + Firestore modules load without a flag.
"""

from __future__ import annotations


def ensure_google_stack() -> dict:
    """Import ADK + Firestore so they appear in sys.modules. Returns what loaded."""
    out = {"adk": None, "firestore": None}

    try:
        import google.adk.agents  # noqa: F401
        out["adk"] = "google.adk.agents"
    except Exception as e:
        out["adk"] = f"IMPORT-FAIL:{type(e).__name__}:{e}"

    try:
        from google.cloud import firestore  # noqa: F401
        out["firestore"] = "google.cloud.firestore"
    except Exception as e:
        out["firestore"] = f"IMPORT-FAIL:{type(e).__name__}:{e}"

    return out
