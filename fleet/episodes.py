"""Episode extraction — one human intent opened and closed (SIGNAL-SPEC unit)."""

from fleet.human import human_text, is_human_turn, load_transcript
from fleet.task_class import DIFFERENT, UNMEASURED, UNDECIDABLE, classify

ABANDON_MARKERS = ("never mind", "skip", "forget it", "ignore", "abandon")
# Clarifications are corrective turns — do NOT ask Gemini (it flakes DIFFERENT on
# "no, I meant X" and splits one episode into a fake cold land).
CORRECTIVE_MARKERS = (
    "no,", "no ", "no.", "not that", "not this", "not the", "i meant", "i mean",
    "actually", "wait,", "wrong ", "other file", "other one",
)
_DURABLE_TOOLS = {"Write", "Edit", "Bash"}
SCORE_MAP = {
    "landed": 4, "landed_corrected": 3, "survive": 1, "abandon": 0, "UNMEASURED": 0,
}
RANKABLE = frozenset({"survive", "landed", "landed_corrected"})


def _looks_corrective(text: str) -> bool:
    low = text.lower().strip()
    return any(low.startswith(m) or f" {m}" in f" {low}" for m in CORRECTIVE_MARKERS)


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
                # Linguistic corrective markers beat Gemini — measured flake otherwise.
                if _looks_corrective(ht):
                    corrective += 1
                    j += 1
                    continue
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
                if verdict == DIFFERENT:
                    break
                if verdict in ("SAME", UNDECIDABLE):
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


def _episode_score(ep: dict) -> int:
    return SCORE_MAP.get(ep["signal"], 0)


def _best_rankable_episode(episodes: list[dict]) -> dict | None:
    ranked = [e for e in episodes if e["signal"] in RANKABLE]
    if not ranked:
        return None
    return max(ranked, key=_episode_score)


def score_episodes_for_anchor(episodes: list[dict], anchor_prompt: str) -> dict:
    """Pick best episode in SAME task class as anchor — prompt-vs-prompt only."""
    matched = []
    for ep in episodes:
        if ep["signal"] == "UNMEASURED" and ep.get("probe") == "GEMINI-TASK-CLASS":
            continue
        v = classify(ep["opener"], anchor_prompt)
        if v == UNMEASURED:
            return {"signal": "UNMEASURED", "score": 0, "probe": "GEMINI-TASK-CLASS",
                    "why": "classifier unreachable for anchor match"}
        if v == "SAME":
            matched.append(ep)
    if not matched:
        return {"signal": "NO_MATCH", "score": 0, "probe": "GEMINI-TASK-CLASS",
                "why": "no episode same task class as anchor prompt"}

    best = max(matched, key=_episode_score)
    return {
        "signal": best["signal"],
        "score": _episode_score(best),
        "probe": best["probe"],
        "prompt": best["opener"],
        "why": best["why"],
        "corrective_turns": best["corrective_turns"],
        "episodes_matched": len(matched),
        "episodes_total": len(episodes),
    }


def rank_sessions_pairwise(corpus_paths: list[str]) -> list[dict]:
    """Best rankable episode per path, filtered to largest SAME cluster (no anchor)."""
    bests = []
    for path in corpus_paths:
        eps = extract_episodes(load_transcript(path))
        best_ep = _best_rankable_episode(eps)
        if not best_ep:
            continue
        bests.append({
            "signal": best_ep["signal"],
            "score": _episode_score(best_ep),
            "probe": best_ep["probe"],
            "prompt": best_ep["opener"],
            "why": best_ep["why"],
            "corrective_turns": best_ep["corrective_turns"],
            "episodes_matched": 1,
            "episodes_total": len(eps),
            "path": path,
        })

    if len(bests) < 2:
        return bests

    # Largest connected component under pairwise SAME
    clusters: list[list[dict]] = [[bests[0]]]
    for item in bests[1:]:
        placed = False
        for cluster in clusters:
            if classify(item["prompt"], cluster[0]["prompt"]) == "SAME":
                cluster.append(item)
                placed = True
                break
        if not placed:
            clusters.append([item])
    return max(clusters, key=len)


def score_session_episodes(path: str, anchor_prompt: str) -> dict:
    rows = load_transcript(path)
    eps = extract_episodes(rows)
    out = score_episodes_for_anchor(eps, anchor_prompt)
    out["path"] = path
    return out


def rank_corpus(anchor_prompt: str, corpus_paths: list[str]) -> dict:
    """Rank operators: pairwise cluster first, anchor narrows when it helps."""
    cluster = rank_sessions_pairwise(corpus_paths)
    if len(cluster) >= 2:
        ranked = cluster
        mode = "pairwise-cluster"
    else:
        anchor_hits = []
        for path in corpus_paths:
            s = score_session_episodes(path, anchor_prompt)
            if s["signal"] in RANKABLE:
                anchor_hits.append(s)
        ranked = anchor_hits
        mode = "anchor-cluster" if len(anchor_hits) >= 2 else "anchor-single"

    if not ranked:
        return {
            "error": "no rankable prompt in corpus",
            "probe": "GEMINI-TASK-CLASS+EPISODE-SIGNAL",
            "anchor": anchor_prompt,
            "mode": "none",
        }

    best = max(ranked, key=lambda x: x["score"])
    return {
        "best": best,
        "mode": mode,
        "field_size": len(ranked),
        "operators": [b["path"] for b in ranked],
    }
