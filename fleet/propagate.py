"""Find best operator prompt and propagate to org skill file."""

import hashlib
import os
from pathlib import Path

from fleet.signals import score_session


def find_best_prompt(topic: str, corpus_paths: list[str]) -> dict:
    """Rank human prompts on topic by score (landed > survive > abandon)."""
    ranked = []
    for path in corpus_paths:
        if not os.path.isfile(path):
            continue
        s = score_session(path, topic)
        if s["signal"] in ("survive", "landed"):
            ranked.append(s)
    if not ranked:
        return {"error": "no surviving prompt on topic",
                "probe": "GEMINI-TASK-CLASS+SURVIVE-VS-ABANDON", "topic": topic}
    best = max(ranked, key=lambda x: x["score"])
    parts = Path(best["path"]).stem.split("-")
    operator = parts[1] if len(parts) > 1 and parts[0] == "operator" else parts[0]
    return {"operator": operator, "prompt_text": best["prompt"],
            "signal": best["signal"], "probe": best["probe"],
            "source": best["path"], "why": best["why"], "score": best["score"]}


def propagate_prompt(prompt_text: str, target_skill_path: str,
                     operator: str = "unknown", topic: str = "") -> dict:
    """Write curated prompt to org skill path. Does not execute transcript text."""
    path = Path(os.path.expanduser(target_skill_path))
    path.parent.mkdir(parents=True, exist_ok=True)
    body = (
        f"# Org prompt — propagated from operator {operator}"
        + (f" ({topic})" if topic else "")
        + f"\n\n{prompt_text.strip()}\n\n"
        f"_Probe: best operator on task class {topic!r} · propagated by fleet supervisor_\n"
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
