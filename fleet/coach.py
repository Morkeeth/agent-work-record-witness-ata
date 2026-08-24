"""fleet/coach.py — the prompting coach (PRD-2026-08 §6, Slice 1).

Point the authorship gate + the survival proxy at ONE operator's OWN Claude Code
transcripts and rank their prompt PATTERNS by whether the work survived. This is the
single-seat wedge: it needs no org, runs on the operator's own `~/.claude` logs, and
emits a shareable "your top-5 / bottom-5 prompt patterns" summary (the growth loop).

WHY THIS IS ITS OWN MODULE (and does NOT call fleet/episodes.py)
---------------------------------------------------------------
`fleet/episodes.py` is the fleet ranker, but it decides episode boundaries with
`fleet.task_class.classify`, which makes a **Gemini network call per prompt pair**.
Against one operator's real history that is hundreds of network hops — it times out on a
laptop and cannot run offline. The coach is a single-seat, no-key surface, so it reuses
only the FREE, deterministic machinery:

  - `fleet.human.is_human_turn`  — THE MOAT. Keeps only genuinely typed/queued human
    prompts; drops agent echoes, tool results, sidechains, meta, and SDK/judge-run turns
    (`promptSource=="sdk"`). On this machine that gate drops 860 cvfit-judge files to zero
    kept turns — the separator the whole category is built on.
  - `contract.deterministic.classify_deterministic` — the offline task-class floor, used
    for episode boundaries (no network, no key, no synonym table).
  - The landed-tool proxy — the same durable signal `episodes.py` uses (Write/Edit/Bash),
    tightened here into ranked tiers (see below).

THE SURVIVAL PROXY — A PROXY, NOT TRUTH. Read the limits.
---------------------------------------------------------
"Did the work survive?" cannot be measured perfectly from a transcript. We approximate it
with a deterministic, tiered read of what durable act followed the human prompt inside the
same episode:

  Tier 2  COMMIT-WITNESSED  — a `git commit` ran in a Bash tool_use after the prompt, and
                             no `git revert` / `git reset --hard` undid it later in the
                             same session. Strongest durable signal.
  Tier 1  ARTIFACT-WITNESSED — a Write or Edit tool_use landed a file change.
  Tier 0  NOT-DURABLE        — only read-only Bash (ls/grep/cat/git-status) ran, or no tool
                             ran at all: the prompt produced nothing that survived. This is
                             the "looped / abandoned" bucket.

An episode "SURVIVED" iff it reached Tier 1 or Tier 2. Its patterns are ranked by that rate.

HONEST LIMITS (do not oversell — this is exactly the kind of claim the product exists to
keep honest):
  - A commit is not proof the code was correct, merged, or kept beyond this session; we
    only detect a revert if it happened in the SAME transcript. Cross-session reverts are
    invisible.
  - A Write/Edit is a durable *keystroke*, not a durable *outcome* — the file may have been
    thrown away in a later session we did not read.
  - "Not-durable" can misjudge a prompt whose real work happened in a later session, or
    whose payoff was a decision/answer rather than an edit.
  - Episode boundaries use a lexical offline classifier; a topic shift it cannot see splits
    or merges episodes. It never calls a model, so it never hallucinates a boundary either.
So: this ranks PATTERNS by a survival PROXY. It is a coaching signal, not a verdict.
"""
from __future__ import annotations

import glob
import os
import re

from contract.deterministic import SAME, _intent, _objects, classify_deterministic
from fleet.human import human_text, is_human_turn, load_transcript

# --- episode segmentation markers (offline, deterministic) -----------------------------
_ABANDON_MARKERS = ("never mind", "forget it", "abandon", "scrap this", "drop it")
_CORRECTIVE_MARKERS = (
    "no,", "no ", "no.", "not that", "not this", "not the", "i meant", "i mean",
    "actually", "wait,", "wrong ", "other file", "other one",
)
_WRITE_TOOLS = {"Write", "Edit", "NotebookEdit"}
_COMMIT_RE = re.compile(r"\bgit\s+commit\b")
_REVERT_RE = re.compile(r"\bgit\s+(revert|reset\s+--hard)\b")
# A path or filename mentioned in a prompt: foo.py, src/app.ts, a/b/c.md, Makefile-ish.
_FILE_RE = re.compile(r"\b[\w./-]+\.[A-Za-z]{1,5}\b|\b[\w-]+/[\w./-]+\b")
_CHECK_RE = re.compile(
    r"\b(test|tests|verify|verif|prove|proof|done[- ]?when|make sure|ensure|"
    r"confirm|check that|assert|so that|screenshot|render)\b"
)

# survival tiers
TIER_COMMIT, TIER_ARTIFACT, TIER_NONE, TIER_REVERTED = "commit", "artifact", "none", "reverted"
_DURABLE_TIERS = frozenset({TIER_COMMIT, TIER_ARTIFACT})
_TIER_SCORE = {TIER_COMMIT: 2, TIER_ARTIFACT: 1, TIER_REVERTED: 0, TIER_NONE: 0}
_TIER_PROBE = {
    TIER_COMMIT: "COMMIT-WITNESSED",
    TIER_ARTIFACT: "ARTIFACT-WITNESSED",
    TIER_REVERTED: "COMMIT-THEN-REVERTED",
    TIER_NONE: "NO-DURABLE-RECORD",
}

MIN_PATTERN_N = 3  # a pattern is only rankable with at least this many episodes


def _looks_corrective(text: str) -> bool:
    low = " " + text.lower().strip()
    return any(low.startswith(" " + m) or f" {m}" in low for m in _CORRECTIVE_MARKERS)


def _tool_uses(record: dict) -> list[dict]:
    if record.get("type") != "assistant":
        return []
    content = (record.get("message") or {}).get("content")
    if not isinstance(content, list):
        return []
    return [b for b in content if isinstance(b, dict) and b.get("type") == "tool_use"]


def _bash_command(block: dict) -> str:
    if block.get("name") != "Bash":
        return ""
    return (block.get("input") or {}).get("command", "") or ""


# --------------------------------------------------------------------------- episodes
def extract_episodes(rows: list[dict], source: str = "") -> list[dict]:
    """Deterministic, offline episode split. One human intent, opened and closed.

    Boundaries: a later human turn ends the episode unless it is a linguistic correction
    ("no, I meant…") or same-task-class under the offline floor. Never calls a network.
    """
    episodes: list[dict] = []
    n = len(rows)
    i = 0
    while i < n:
        if not (is_human_turn(rows[i]) and human_text(rows[i]).strip()):
            i += 1
            continue
        opener = human_text(rows[i]).strip()
        start = i
        corrective = 0
        assistants = 0
        abandoned = False
        wrote = committed = reverted = read_only_bash = False
        witness = ""  # human-readable durable evidence
        j = i + 1
        while j < n:
            row = rows[j]
            if is_human_turn(row) and human_text(row).strip():
                nxt = human_text(row).strip()
                low = nxt.lower()
                if any(m in low for m in _ABANDON_MARKERS):
                    abandoned = True
                    break
                if _looks_corrective(nxt):
                    corrective += 1
                    j += 1
                    continue
                if classify_deterministic(opener, nxt) != SAME:
                    break  # a genuinely new intent — this episode is over
                corrective += 1  # same task class = continuation of the same intent
                j += 1
                continue
            if row.get("type") == "assistant":
                assistants += 1
            for b in _tool_uses(row):
                name = b.get("name")
                if name in _WRITE_TOOLS:
                    wrote = True
                    if not witness:
                        tgt = (b.get("input") or {}).get("file_path") or \
                              (b.get("input") or {}).get("notebook_path") or "?"
                        witness = f"{name} {os.path.basename(tgt)} @ {row.get('timestamp', '?')}"
                elif name == "Bash":
                    cmd = _bash_command(b)
                    if _COMMIT_RE.search(cmd):
                        committed = True
                        witness = f"git commit @ {row.get('timestamp', '?')}"
                    elif _REVERT_RE.search(cmd):
                        reverted = True
                    else:
                        read_only_bash = True
            j += 1

        if committed and reverted:
            tier = TIER_REVERTED
        elif committed:
            tier = TIER_COMMIT
        elif wrote:
            tier = TIER_ARTIFACT
        else:
            tier = TIER_NONE
            witness = ("read-only Bash only, no file change" if read_only_bash
                       else "no tool ran after the prompt")

        episodes.append({
            "opener": opener,
            "source": os.path.basename(source),
            "start": start,
            "end": j,
            "tier": tier,
            "probe": _TIER_PROBE[tier],
            "score": _TIER_SCORE[tier],
            "survived": tier in _DURABLE_TIERS,
            "corrective_turns": corrective,
            "assistant_turns": assistants,
            "abandoned": abandoned,
            "witness": witness,
        })
        i = j if j > start else start + 1
    return episodes


# --------------------------------------------------------------------------- patterns
def prompt_patterns(text: str) -> list[str]:
    """Deterministic, observable pattern tags for one prompt. No fabrication: every tag is
    a mechanical feature of the text, not an inferred 'style'."""
    tags: list[str] = []
    words = text.split()
    wc = len(words)

    intent = _intent(text)
    tags.append(f"intent:{intent}" if intent else "intent:none")

    tags.append("names-a-concrete-object" if _objects(text) else "no-object (pronoun/vague)")

    if wc < 8:
        tags.append("terse (<8 words)")
    elif wc <= 40:
        tags.append("medium (8-40 words)")
    else:
        tags.append("detailed (>40 words)")

    if _FILE_RE.search(text):
        tags.append("cites-a-file-or-path")
    if _CHECK_RE.search(text.lower()):
        tags.append("states-a-check-or-done-condition")
    return tags


def rank_patterns(episodes: list[dict]) -> list[dict]:
    """Aggregate episodes by pattern tag; survival_rate = durable / n. Rankable at n>=MIN."""
    from collections import defaultdict
    buckets: dict[str, list[dict]] = defaultdict(list)
    for ep in episodes:
        for tag in prompt_patterns(ep["opener"]):
            buckets[tag].append(ep)
    out = []
    for tag, eps in buckets.items():
        n = len(eps)
        durable = sum(1 for e in eps if e["survived"])
        out.append({
            "pattern": tag,
            "n": n,
            "survived": durable,
            "survival_rate": durable / n if n else 0.0,
            "rankable": n >= MIN_PATTERN_N,
        })
    # highest survival first; ties broken by larger sample
    out.sort(key=lambda p: (p["survival_rate"], p["n"]), reverse=True)
    return out


def _best_landed(episodes: list[dict]) -> dict | None:
    """The single most convincing landed prompt: highest tier, fewest corrections, and a
    substantive (not one-word) opener."""
    cand = [e for e in episodes if e["survived"] and len(e["opener"]) >= 25]
    if not cand:
        cand = [e for e in episodes if e["survived"]]
    if not cand:
        return None
    return max(cand, key=lambda e: (e["score"], -e["corrective_turns"], e["assistant_turns"]))


def _worst_looped(episodes: list[dict]) -> dict | None:
    """The most convincing 'looped then died': not durable, most back-and-forth."""
    cand = [e for e in episodes if not e["survived"] and len(e["opener"]) >= 25]
    if not cand:
        cand = [e for e in episodes if not e["survived"]]
    if not cand:
        return None
    return max(cand, key=lambda e: (e["corrective_turns"], e["assistant_turns"]))


# ------------------------------------------------------------------------------- coach
def _corpus_paths(transcript_dir: str) -> list[str]:
    d = os.path.expanduser(transcript_dir)
    if os.path.isfile(d):
        return [d]
    here = sorted(glob.glob(os.path.join(d, "*.jsonl")))
    return here if here else sorted(glob.glob(os.path.join(d, "**", "*.jsonl"), recursive=True))


def coach(transcript_dir: str, operator: str = "operator") -> dict:
    """Rank an operator's own prompt patterns by a survival proxy. Offline, deterministic."""
    paths = _corpus_paths(transcript_dir)
    episodes: list[dict] = []
    total_records = 0
    human_turns = 0
    for p in paths:
        rows = load_transcript(p)
        total_records += len(rows)
        human_turns += sum(1 for r in rows if is_human_turn(r) and human_text(r).strip())
        episodes.extend(extract_episodes(rows, source=p))

    patterns = rank_patterns(episodes)
    rankable = [p for p in patterns if p["rankable"]]
    durable = sum(1 for e in episodes if e["survived"])
    tiers = {t: sum(1 for e in episodes if e["tier"] == t)
             for t in (TIER_COMMIT, TIER_ARTIFACT, TIER_REVERTED, TIER_NONE)}

    return {
        "operator": operator,
        "files": len(paths),
        "total_records": total_records,
        "human_turns": human_turns,
        "human_pct": round(100 * human_turns / total_records, 2) if total_records else 0.0,
        "episodes": len(episodes),
        "durable": durable,
        "durable_rate": round(durable / len(episodes), 3) if episodes else 0.0,
        "tiers": tiers,
        "top_patterns": [p for p in rankable[:5]],
        "bottom_patterns": [p for p in rankable[-5:][::-1]] if len(rankable) > 5
        else [p for p in rankable[::-1]][:5],
        "best_prompt": _best_landed(episodes),
        "worst_prompt": _worst_looped(episodes),
        "sparse": len(rankable) < 5,
        "proxy": "survival = reached a durable Write/Edit or an un-reverted git commit "
                 "in-episode (a PROXY, not proof of shipped/correct work).",
    }


# ------------------------------------------------------------------------------- render
def _fmt_prompt(text: str, width: int = 100) -> str:
    one = " ".join(text.split())
    return one if len(one) <= width else one[: width - 1] + "…"


def render(result: dict) -> str:
    r = result
    L = []
    L.append("=" * 74)
    L.append(f"  PROMPTING COACH — {r['operator']}   (transcripto, single-seat wedge)")
    L.append("=" * 74)
    L.append(f"  corpus : {r['files']} transcript(s), {r['total_records']:,} records")
    L.append(f"  moat   : {r['human_turns']} genuine human prompts kept "
             f"({r['human_pct']}% of records) — is_human_turn dropped the rest")
    L.append(f"  ranked : {r['episodes']} prompt episodes; "
             f"{r['durable']} survived ({int(round(r['durable_rate'] * 100))}%)")
    t = r["tiers"]
    L.append(f"  tiers  : commit {t[TIER_COMMIT]} | write/edit {t[TIER_ARTIFACT]} | "
             f"reverted {t[TIER_REVERTED]} | not-durable {t[TIER_NONE]}")
    L.append("")
    L.append("  SURVIVAL is a PROXY: " + r["proxy"])
    L.append("")

    if r["sparse"]:
        L.append("  (few patterns cleared the min-sample bar — reporting what is rankable)")
    L.append("  TOP prompt patterns  (highest survival rate) — do more of these:")
    for p in r["top_patterns"]:
        L.append(f"    {int(round(p['survival_rate']*100)):3d}%  "
                 f"({p['survived']}/{p['n']})  {p['pattern']}")
    L.append("")
    L.append("  BOTTOM prompt patterns  (lowest survival rate) — these tend to loop:")
    for p in r["bottom_patterns"]:
        L.append(f"    {int(round(p['survival_rate']*100)):3d}%  "
                 f"({p['survived']}/{p['n']})  {p['pattern']}")
    L.append("")

    b = r["best_prompt"]
    if b:
        L.append("  ✓ BEST landed prompt (a real one, with its witness):")
        L.append(f"      “{_fmt_prompt(b['opener'])}”")
        L.append(f"      survived → {b['probe']}: {b['witness']}")
        L.append(f"      corrections: {b['corrective_turns']} | source: {b['source']}")
    w = r["worst_prompt"]
    if w:
        L.append("")
        L.append("  ✗ WORST looped prompt (a real one, with its witness):")
        L.append(f"      “{_fmt_prompt(w['opener'])}”")
        L.append(f"      no durable work → {w['probe']}: {w['witness']}")
        L.append(f"      corrections: {w['corrective_turns']} | "
                 f"assistant turns: {w['assistant_turns']} | source: {w['source']}")
    L.append("=" * 74)
    return "\n".join(L)


if __name__ == "__main__":
    import sys
    _dir = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(
        "~/.claude/projects/-Users-morkeeth")
    _op = sys.argv[2] if len(sys.argv) > 2 else "oscar"
    print(render(coach(_dir, _op)))
