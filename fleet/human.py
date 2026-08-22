"""Human-turn gate — same contract as transcripto.is_human_turn (read-only copy)."""

import json


def is_human_turn(record: dict) -> bool:
    if record.get("type") != "user":
        return False
    if record.get("promptSource") not in ("typed", "queued"):
        return False
    if record.get("isMeta") or record.get("isSidechain"):
        return False
    if record.get("toolUseResult") is not None:
        return False
    return True


def human_text(record: dict) -> str:
    msg = record.get("message") or {}
    parts = []
    for block in msg.get("content") or []:
        if isinstance(block, dict) and block.get("type") == "text":
            parts.append(block.get("text") or "")
    return "\n".join(p for p in parts if p)


def load_transcript(path: str) -> list[dict]:
    rows = []
    with open(path, errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows
