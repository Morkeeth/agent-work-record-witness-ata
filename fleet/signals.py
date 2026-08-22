"""Prompt performance signals — Gemini task-class + episode scoring."""

from fleet.episodes import score_session_episodes
from fleet.human import human_text, is_human_turn, load_transcript
from fleet.task_class import UNMEASURED, classify


def _topic_match(prompt_a: str, prompt_b: str) -> bool:
    """Live classifier binding for contract/task_class.py classify_substring."""
    verdict = classify(prompt_a, prompt_b)
    if verdict == UNMEASURED:
        return False
    return verdict == "SAME"


def _tool_use_names(record: dict) -> list[str]:
    if record.get("type") != "assistant":
        return []
    msg = record.get("message") or {}
    content = msg.get("content")
    if not isinstance(content, list):
        return []
    return [b.get("name") for b in content
            if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name")]


def _landed_at_row(record: dict) -> bool:
    """Probe: LANDED-FROM-TOOL-RECORD — Write/Edit/Bash on this row."""
    durable = {"Write", "Edit", "Bash"}
    return any(n in durable for n in _tool_use_names(record))


def _landed_after(rows: list[dict], human_idx: int) -> bool:
    for r in rows[human_idx + 1:]:
        if is_human_turn(r):
            break
        if _landed_at_row(r):
            return True
    return False


def score_session(path: str, topic: str) -> dict:
    """Score one transcript via episode extraction (SIGNAL-SPEC unit)."""
    return score_session_episodes(path, topic)


def compare_prompts(a: str, b: str) -> str:
    """Expose classify for tests — SAME | DIFFERENT | UNDECIDABLE | UNMEASURED."""
    return classify(a, b)
