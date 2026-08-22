"""Episode extraction — one human intent opened and closed (SIGNAL-SPEC unit)."""

from fleet.human import human_text, is_human_turn, load_transcript
from fleet.task_class import UNMEASURED, classify

ABANDON_MARKERS = ("never mind", "skip", "forget it", "ignore", "abandon")
_DURABLE_TOOLS = {"Write", "Edit", "Bash"}


def _tool_use_names(record: dict) -> list[str]:
    if record.get("type") != "assistant":
        return []
    content = (record.get("message") or {}).get("content")
    if not isinstance(content, list):
        return []
    return [b.get("name") for b in content
            if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name")]


def _landed_at_row(record: dict) -> bool:
    return any(n in _DURABLE_TOOLS for n in _tool_use_names(record))


def extract_episodes(rows: list[dict]) -> list[dict]:
    """Split transcript into episodes. Each names its probes."""
    episodes = []
    i = 0
    n = len(rows)
    while i < n:
        if not is_human_turn(rows[i]):
            i += 1
            continue
        opener = human_text(rows[i]).strip()
        if not opener:
            i += 1
            continue
        start_idx = i
        corrective = 0
        abandoned = False
        landed = False
        j = i + 1
        while j < n:
            row = rows[j]
            if is_human_turn(row):
                ht = human_text(row).strip()
                if not ht:
                    j += 1
                    continue
                if any(m in ht.lower() for m in ABANDON_MARKERS):
                    abandoned = True
                    j += 1
                    break
                verdict = classify(opener, ht)
                if verdict == UNMEASURED:
                    episodes.append({
                        "opener": opener, "start": start_idx, "end": j,
                        "signal": "UNMEASURED", "probe": "GEMINI-TASK-CLASS",
                        "why": "could not classify corrective vs new intent",
                        "corrective_turns": corrective,
                        "landed": False, "abandoned": False,
                    })
                    i = j
                    j = -1
                    break
                if verdict == "SAME":
                    corrective += 1
                    j += 1
                    continue
                break
            if _landed_at_row(row):
                landed = True
                j += 1
                break
            j += 1

        if j == -1:
            continue

        if abandoned:
            ep = {"signal": "abandon", "probe": "ABANDON-MARKER",
                  "why": "explicit abandon marker in episode"}
        elif landed and corrective == 0:
            ep = {"signal": "landed", "probe": "LANDED-FROM-TOOL-RECORD",
                  "why": "durable tool_use with 0 corrective turns"}
        elif landed:
            ep = {"signal": "landed_corrected", "probe": "LANDED-FROM-TOOL-RECORD",
                  "why": f"landed after {corrective} corrective turn(s)"}
        elif j >= n and not landed:
            ep = {"signal": "abandon", "probe": "ABANDON-NO-ARTIFACT",
                  "why": "session ended with no durable tool record"}
        else:
            assistants = [r for r in rows[start_idx + 1:j] if r.get("type") == "assistant"]
            if len(assistants) >= 2:
                ep = {"signal": "survive", "probe": "SURVIVE-VS-ABANDON-HEURISTIC",
                      "why": f"{len(assistants)} assistant turns, no durable tool record"}
            else:
                ep = {"signal": "UNMEASURED", "probe": "EPISODE-INCOMPLETE",
                      "why": "insufficient follow-through"}

        ep.update({
            "opener": opener, "start": start_idx, "end": j,
            "corrective_turns": corrective, "landed": landed, "abandoned": abandoned,
        })
        episodes.append(ep)
        i = j if j > start_idx else start_idx + 1
    return episodes


def score_episodes_for_topic(episodes: list[dict], topic: str) -> dict:
    """Pick best episode matching task class of topic."""
    matched = []
    for ep in episodes:
        if ep["signal"] == "UNMEASURED" and ep.get("probe") == "GEMINI-TASK-CLASS":
            continue
        v = classify(ep["opener"], topic)
        if v == UNMEASURED:
            return {"signal": "UNMEASURED", "score": 0, "probe": "GEMINI-TASK-CLASS",
                    "why": "classifier unreachable for topic match"}
        if v == "SAME":
            matched.append(ep)
    if not matched:
        return {"signal": "NO_MATCH", "score": 0, "probe": "GEMINI-TASK-CLASS",
                "why": "no episode same task class as topic"}

    score_map = {
        "landed": 4, "landed_corrected": 3, "survive": 1, "abandon": 0, "UNMEASURED": 0,
    }
    best = max(matched, key=lambda e: score_map.get(e["signal"], 0))
    return {
        "signal": best["signal"],
        "score": score_map.get(best["signal"], 0),
        "probe": best["probe"],
        "prompt": best["opener"],
        "why": best["why"],
        "corrective_turns": best["corrective_turns"],
        "episodes_matched": len(matched),
        "episodes_total": len(episodes),
    }


def score_session_episodes(path: str, topic: str) -> dict:
    rows = load_transcript(path)
    eps = extract_episodes(rows)
    out = score_episodes_for_topic(eps, topic)
    out["path"] = path
    return out
