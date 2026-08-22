"""Find best operator prompt and propagate to org skill file."""

import hashlib
import os
from pathlib import Path

from fleet.episodes import rank_corpus


def _operator_id(path: str) -> str:
    parts = Path(path).stem.split("-")
    if len(parts) > 1 and parts[0] == "operator":
        return parts[1]
    return parts[0]


def find_best_prompt(anchor_prompt: str, corpus_paths: list[str]) -> dict:
    """Rank human prompts by episode signal within the anchor's task class."""
    ranked = rank_corpus(anchor_prompt, corpus_paths)
    if "error" in ranked:
        return ranked

    best = ranked["best"]
    operator = _operator_id(best["path"])
    return {
        "operator": operator,
        "prompt_text": best["prompt"],
        "signal": best["signal"],
        "probe": best["probe"],
        "source": best["path"],
        "why": best["why"],
        "score": best["score"],
        "field_size": ranked["field_size"],
        "rank_mode": ranked["mode"],
        "anchor": anchor_prompt,
    }


def propagate_prompt(prompt_text: str, target_skill_path: str,
                     operator: str = "unknown", topic: str = "") -> dict:
    """Write curated prompt to org skill path. Does not execute transcript text."""
    path = Path(os.path.expanduser(target_skill_path))
    path.parent.mkdir(parents=True, exist_ok=True)
    body = (
        f"# Org prompt — propagated from operator {operator}"
        + (f" ({topic})" if topic else "")
        + f"\n\n{prompt_text.strip()}\n\n"
        f"_Probe: best operator on task class · propagated by fleet supervisor_\n"
    )
    path.write_text(body)
    sha = hashlib.sha256(body.encode()).hexdigest()[:12]
    return {"written": str(path), "sha": sha, "bytes": len(body.encode()),
            "probe": "FILE-WRITE"}


def witness_propagation(target_skill_path: str) -> dict:
    """Ground truth: did the skill file land?"""
    path = os.path.expanduser(target_skill_path)
    if not os.path.isfile(path):
        return {"verdict": "MISSING", "probe": "FILE-EXISTS", "target": path,
                "evidence": "path does not exist"}
    data = open(path).read()
    if len(data) < 20:
        return {"verdict": "UNMEASURED", "probe": "FILE-EXISTS", "target": path,
                "evidence": "file too small to be a propagated skill"}
    nbytes = len(data.encode("utf-8"))
    return {"verdict": "VERIFIED-BY-REPO", "probe": "FILE-EXISTS", "target": path,
            "evidence": f"{nbytes} bytes"}
