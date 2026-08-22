"""Prompt performance signals — Gemini task-class + LANDED from tool records."""

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


def _landed_after(rows: list[dict], human_idx: int) -> bool:
    """Probe: LANDED-FROM-TOOL-RECORD — Write/Edit/Bash after the opener."""
    durable = {"Write", "Edit", "Bash"}
    for r in rows[human_idx + 1:]:
        if is_human_turn(r):
            break
        for name in _tool_use_names(r):
            if name in durable:
                return True
    return False


def score_session(path: str, topic: str) -> dict:
    """Score one transcript for topic match + outcome.

    Probes (named on every return):
      GEMINI-TASK-CLASS — topic ↔ human prompt (contract/gemini_impl)
      LANDED-FROM-TOOL-RECORD — durable tool_use after opener
      SURVIVE-VS-ABANDON-HEURISTIC — abandon markers / assistant follow-through
    """
    rows = load_transcript(path)
    human_on_topic = []
    for i, row in enumerate(rows):
        if not is_human_turn(row):
            continue
        text = human_text(row)
        if not text.strip():
            continue
        match = classify(text, topic)
        if match is UNMEASURED:
            return {"signal": "UNMEASURED", "score": 0,
                    "probe": "GEMINI-TASK-CLASS", "path": path,
                    "why": "classifier unreachable — not scored as failure"}
        if match == "SAME":
            human_on_topic.append((i, text))

    if not human_on_topic:
        return {"signal": "NO_MATCH", "score": 0, "probe": "GEMINI-TASK-CLASS",
                "path": path, "why": f"no human turn same task class as {topic!r}"}

    abandon_markers = ("never mind", "skip", "forget it", "ignore", "abandon")
    last_idx, last_text = human_on_topic[-1]
    tail_humans = [human_text(rows[j]).lower()
                   for j in range(last_idx, len(rows))
                   if j < len(rows) and is_human_turn(rows[j])]
    if any(any(m in t for m in abandon_markers) for t in tail_humans[1:]):
        return {"signal": "abandon", "score": 0, "probe": "SURVIVE-VS-ABANDON-HEURISTIC",
                "path": path, "prompt": last_text,
                "why": "trailing human turn contains abandon marker"}

    if _landed_after(rows, last_idx):
        return {"signal": "landed", "score": 3, "probe": "LANDED-FROM-TOOL-RECORD",
                "path": path, "prompt": last_text,
                "why": "durable tool_use (Write/Edit/Bash) after topic prompt"}

    assistants_after = [r for r in rows[last_idx + 1:] if r.get("type") == "assistant"]
    if len(assistants_after) >= 2:
        return {"signal": "survive", "score": 1, "probe": "SURVIVE-VS-ABANDON-HEURISTIC",
                "path": path, "prompt": last_text,
                "why": f"{len(assistants_after)} assistant turns, no durable tool record"}

    return {"signal": "UNMEASURED", "score": 0, "probe": "SURVIVE-VS-ABANDON-HEURISTIC",
            "path": path, "prompt": last_text,
            "why": "insufficient follow-through to call survive or landed"}


def compare_prompts(a: str, b: str) -> str:
    """Expose classify for tests — SAME | DIFFERENT | UNDECIDABLE | UNMEASURED."""
    return classify(a, b)
