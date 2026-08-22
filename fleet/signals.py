"""Prompt performance signals — one probe for the wedge: survive vs abandon."""

from fleet.human import human_text, is_human_turn, load_transcript


def _topic_match(text: str, topic: str) -> bool:
    """Task-class overlap — any substantive topic term matches (demo heuristic).

    Probe: TASK-CLASS-OVERLAP-HEURISTIC
    "fix auth" and "refactor the auth module" both match topic "refactor auth".
    Gemini intent classification replaces this before submit (see docs/SIGNAL-SPEC.md).
    """
    terms = [t for t in topic.lower().split() if len(t) > 2]
    low = text.lower()
    if not terms:
        return True
    return any(t in low for t in terms)


def score_session(path: str, topic: str) -> dict:
    """Score one transcript for topic match.

    Probe: SURVIVE-VS-ABANDON-HEURISTIC
      survive  — last human turn on topic followed by assistant completion,
                 no abandon phrase in trailing human turns
      abandon  — explicit give-up ("never mind", "skip", "forget it") after topic prompt
    """
    rows = load_transcript(path)
    human_on_topic = []
    for i, row in enumerate(rows):
        if not is_human_turn(row):
            continue
        text = human_text(row)
        if _topic_match(text, topic):
            human_on_topic.append((i, text))

    if not human_on_topic:
        return {"signal": "NO_MATCH", "score": 0, "probe": "SURVIVE-VS-ABANDON-HEURISTIC",
                "path": path, "why": f"no human turn matches topic {topic!r}"}

    abandon_markers = ("never mind", "skip", "forget it", "ignore", "abandon")
    last_idx, last_text = human_on_topic[-1]
    tail_humans = [human_text(rows[j]).lower()
                   for j in range(last_idx, len(rows))
                   if j < len(rows) and is_human_turn(rows[j])]
    if any(any(m in t for m in abandon_markers) for t in tail_humans[1:]):
        return {"signal": "abandon", "score": 0, "probe": "SURVIVE-VS-ABANDON-HEURISTIC",
                "path": path, "prompt": last_text,
                "why": "trailing human turn contains abandon marker"}

    assistants_after = [r for r in rows[last_idx + 1:] if r.get("type") == "assistant"]
    if len(assistants_after) >= 2:
        return {"signal": "survive", "score": 1, "probe": "SURVIVE-VS-ABANDON-HEURISTIC",
                "path": path, "prompt": last_text,
                "why": f"{len(assistants_after)} assistant turns after topic prompt"}

    return {"signal": "UNMEASURED", "score": 0, "probe": "SURVIVE-VS-ABANDON-HEURISTIC",
            "path": path, "prompt": last_text,
            "why": "insufficient assistant follow-through to call survive"}
