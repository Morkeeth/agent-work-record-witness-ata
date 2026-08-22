"""Org-lift proof — the VC/judge artifact the fixtures exist to demonstrate.

Same task. Same land. Different corrective-turn cost.
The cheaper prompt is propagated literally.

Episode scores are deterministic (tool records). Gemini pairwise membership is
reported per row — it must not blank the corrective-turn contrast when it flakes.
Population lift across an org is day-two customer data (Track B).
"""

from __future__ import annotations

import glob
import html
import json
from pathlib import Path

from fleet.episodes import extract_episodes
from fleet.human import load_transcript
from fleet.propagate import find_best_prompt, propagate_prompt, witness_propagation
from fleet.task_class import classify

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS = str(ROOT / "fixtures/operators/*.jsonl")
DEFAULT_TARGET = str(ROOT / "fixtures/org-repo/.cursor/rules/propagated-skill.md")
DEFAULT_ANCHOR = (
    "Refactor the auth module: extract validate_token into auth/validate.py, "
    "keep tests green, show me the diff before applying."
)
SCORE = {"landed": 4, "landed_corrected": 3, "survive": 1, "abandon": 0}


def _score_operator(path: str) -> dict:
    eps = extract_episodes(load_transcript(path))
    parts = Path(path).stem.split("-")
    op = parts[1] if len(parts) > 1 and parts[0] == "operator" else parts[0]
    if not eps:
        return {"path": path, "operator": op, "opener": "", "signal": "EMPTY",
                "corrective_turns": None, "score": 0}
    best = max(eps, key=lambda e: SCORE.get(e["signal"], 0))
    return {
        "path": path,
        "operator": op,
        "opener": best["opener"],
        "signal": best["signal"],
        "corrective_turns": best.get("corrective_turns", 0),
        "score": SCORE.get(best["signal"], 0),
        "probe": best.get("probe"),
        "why": best.get("why"),
    }


def build_proof(anchor: str = DEFAULT_ANCHOR,
                corpus_glob: str = DEFAULT_CORPUS,
                target: str = DEFAULT_TARGET) -> dict:
    paths = sorted(glob.glob(corpus_glob))
    scanned = [_score_operator(p) for p in paths]
    scored = [o for o in scanned if o["opener"] and o["signal"] != "EMPTY"]

    find = find_best_prompt(anchor, paths)
    prop = wit = None
    if "error" not in find:
        prop = propagate_prompt(find["prompt_text"], target,
                                operator=find["operator"], topic=anchor)
        wit = witness_propagation(target)

    winner_opener = (find.get("prompt_text") if isinstance(find, dict) else "") or ""
    field = []
    for op in scored:
        v = classify(op["opener"], winner_opener) if winner_opener else "UNMEASURED"
        field.append(dict(op, vs_winner=v))

    durable = [o for o in scored if o["signal"] in ("landed", "landed_corrected", "survive")]
    ranked = sorted(durable, key=lambda o: (-o["score"], o["corrective_turns"] or 99))

    delta = {}
    vc = "Need ≥2 operators with durable episode signals to state the lift."
    if len(ranked) >= 2:
        win, lose = ranked[0], ranked[1]
        gap = (lose["corrective_turns"] or 0) - (win["corrective_turns"] or 0)
        gemini_same = sum(1 for o in field if o.get("vs_winner") == "SAME")
        delta = {
            "winner": win["operator"],
            "loser": lose["operator"],
            "winner_turns": win["corrective_turns"],
            "loser_turns": lose["corrective_turns"],
            "corrective_turn_delta": gap,
            "winner_opener": win["opener"],
            "loser_opener": lose["opener"],
            "winner_signal": win["signal"],
            "loser_signal": lose["signal"],
            "gemini_same_count": gemini_same,
            "rank_field_size": find.get("field_size") if isinstance(find, dict) else None,
        }
        vc = (
            f"Operator {win['operator']} lands cold ({win['signal']}, "
            f"{win['corrective_turns']} corrective turns). "
            f"Operator {lose['operator']} needs {lose['corrective_turns']} "
            f"({lose['signal']}) — {gap} more. "
            f"We propagate {win['operator']}'s literal prompt — not an LLM rewrite."
        )

    return {
        "thesis": (
            "GEAP governs agents. Nothing governs prompts. "
            "Same task, same land — cheaper corrective-turn cost wins; "
            "the literal winner is written to the org skill file."
        ),
        "anchor": anchor,
        "field": field,
        "operators_scanned": scanned,
        "delta": delta,
        "find": find,
        "propagate": prop,
        "witness": wit,
        "vc_one_liner": vc,
        "honest_limit": (
            "This proves the mechanism on a two-operator fixture. "
            "Population lift across an org's engineers is day-two customer data — "
            "a single-builder corpus cannot produce it (Track B). "
            "Gemini pairwise membership is shown per row; the corrective-turn "
            "contrast comes from tool records and does not vanish when the classifier flakes."
        ),
    }


def write_surface(proof: dict, out_path: str | None = None) -> str:
    out_path = out_path or str(ROOT / "surface/org-proof.html")
    d = proof.get("delta") or {}
    wit = proof.get("witness") or {}
    find = proof.get("find") or {}
    e = html.escape

    rows = []
    for o in proof.get("field") or []:
        rows.append(
            "<tr>"
            f"<td>{e(str(o['operator']))}</td>"
            f"<td>{e(str(o['signal']))}</td>"
            f"<td>{e(str(o['corrective_turns']))}</td>"
            f"<td>{e(str(o.get('vs_winner', '')))}</td>"
            f"<td class='prompt'>{e(o['opener'])}</td>"
            "</tr>"
        )

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Org lift — mechanism proof</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560;9..144,650&family=IBM+Plex+Sans:wght@400;600;700&family=IBM+Plex+Mono:wght@500;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --ink:#14171a; --paper:#f3efe6; --quiet:#5a5e59; --land:#0d6a4f; --refuse:#b83314;
    --rule:#d2cec4; --mono:"IBM Plex Mono", ui-monospace, monospace;
    --sans:"IBM Plex Sans", system-ui, sans-serif; --display:"Fraunces", Georgia, serif;
  }}
  * {{ box-sizing:border-box; }}
  body {{
    margin:0; color:var(--ink); font:16px/1.5 var(--sans);
    background:
      radial-gradient(1100px 520px at 8% -8%, #e4ede6 0%, transparent 55%),
      radial-gradient(900px 480px at 100% 0%, #ebe2d4 0%, transparent 50%),
      var(--paper);
  }}
  main {{ max-width:940px; margin:0 auto; padding:52px 28px 88px; }}
  .brand {{ font:700 12px/1 var(--mono); letter-spacing:.16em; text-transform:uppercase; color:var(--quiet); }}
  h1 {{
    font-family:var(--display); font-weight:650; font-size:clamp(2.1rem, 5vw, 3.35rem);
    line-height:1.02; letter-spacing:-.03em; margin:14px 0 12px; max-width:16ch;
  }}
  .lede {{ font-size:1.12rem; color:var(--quiet); max-width:54ch; margin:0 0 40px; }}
  .delta {{ display:grid; grid-template-columns:1fr auto 1fr; gap:18px; margin:0 0 40px; }}
  .card {{ padding:24px 22px; border-top:3px solid var(--ink); background:rgba(255,255,255,.62); }}
  .card.win {{ border-color:var(--land); }}
  .card.lose {{ border-color:var(--refuse); }}
  .who {{ font:700 11px/1 var(--mono); letter-spacing:.14em; text-transform:uppercase; color:var(--quiet); }}
  .num {{ font-family:var(--display); font-size:4.2rem; line-height:1; letter-spacing:-.04em; margin:12px 0 6px; }}
  .card.win .num {{ color:var(--land); }}
  .card.lose .num {{ color:var(--refuse); }}
  .vs {{ align-self:center; font:700 11px/1 var(--mono); letter-spacing:.18em; color:var(--quiet); }}
  .prompt {{ font-family:var(--display); font-size:1.05rem; line-height:1.35; margin-top:14px; }}
  table {{ width:100%; border-collapse:collapse; font-size:14px; margin:8px 0 28px; }}
  th, td {{ text-align:left; padding:11px 8px; border-bottom:1px solid var(--rule); vertical-align:top; }}
  th {{ font:700 11px/1 var(--mono); letter-spacing:.1em; text-transform:uppercase; color:var(--quiet); }}
  td.prompt {{ font-family:var(--display); font-size:15px; }}
  .witness {{ padding:20px 22px; border:1px solid var(--rule); background:#fff; }}
  .tag {{ font:700 11px/1 var(--mono); letter-spacing:.1em; }}
  .ok {{ color:var(--land); margin-top:10px; font:600 13px/1.4 var(--mono); }}
  .limit {{ margin-top:28px; font-size:13px; color:var(--quiet); max-width:64ch; }}
  code {{ font-family:var(--mono); font-size:12px; }}
  @media (max-width:720px) {{
    .delta {{ grid-template-columns:1fr; }}
    .vs {{ display:none; }}
  }}
</style>
</head>
<body>
<main>
  <div class="brand">Transcripto · org lift proof</div>
  <h1>Same work. Different cost. Propagate the cheaper prompt.</h1>
  <p class="lede">{e(proof.get("vc_one_liner", ""))}</p>

  <div class="delta">
    <div class="card win">
      <div class="who">Operator {e(str(d.get("winner", "?")))} · winner</div>
      <div class="num">{e(str(d.get("winner_turns", "—")))}</div>
      <div class="who">corrective turns · {e(str(d.get("winner_signal", "")))}</div>
      <p class="prompt">{e(d.get("winner_opener", ""))}</p>
    </div>
    <div class="vs">VS</div>
    <div class="card lose">
      <div class="who">Operator {e(str(d.get("loser", "?")))} · same class</div>
      <div class="num">{e(str(d.get("loser_turns", "—")))}</div>
      <div class="who">corrective turns · {e(str(d.get("loser_signal", "")))}</div>
      <p class="prompt">{e(d.get("loser_opener", ""))}</p>
    </div>
  </div>

  <table>
    <thead><tr><th>Op</th><th>Signal</th><th>Corrective</th><th>vs winner</th><th>Opener</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>

  <div class="witness">
    <div class="tag">PROPAGATED · operator <code>{e(str(find.get("operator", "?")))}</code>
      · score {e(str(find.get("score", "?")))}</div>
    <p class="prompt">{e(find.get("prompt_text", ""))}</p>
    <div class="ok">Witness {e(str(wit.get("verdict", "PENDING")))}
      · {e(str(wit.get("evidence", "")))}
      · {e(str(wit.get("target", "")))}</div>
  </div>

  <p class="limit"><strong>Honest limit.</strong> {e(proof.get("honest_limit", ""))}</p>
  <p class="limit">Reproduce: <code>python3 fleet_cli.py prove</code> · open <code>surface/org-proof.html</code></p>
</main>
</body>
</html>
"""
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(page)
    return out_path


def emit_json(proof: dict) -> str:
    return json.dumps(proof, indent=2)
