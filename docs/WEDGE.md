> ⛔ **SUPERSEDED 2026-08-27 — do not read as current.** The canonical doc is `hack.md` at the repo root.
> This file is kept for history only. It described a narrower product than the one being built.

# WEDGE — the one loop the video must show

Phase 3 vision lock. Overrides code's current state (there is none yet). Written post-EYES
2026-08-22.

## The press-release line

> A rollout owner asks *"who on my team prompts well, and can we spread that?"* — the fleet
> supervisor finds a high-survival prompt from operator A, writes it into the org skill file,
> and operator B's next session uses it **without anyone opening a coaching UI.**

## Why this is Surface 5 (not a dashboard feature)

Innovation 40% asks: *"How much real-world friction does the agent remove **on its own**?"*

Reporting surfaces 1–4 answer *"what happened."* Surface 5 is the agent **acting**:

1. **Discover** — corpus query: human turns (`is_human=1`) on topic X, ranked by outcome signal.
2. **Select** — best operator's prompt (highest survive / lowest abandon on matched tasks).
3. **Propagate** — ADK supervisor writes prompt into org `.cursor/rules` or team skill file
   (deterministic path on fixture repo — never executes transcript text blindly).
4. **Prove** — `repo_witness` confirms the skill file landed; next fixture session references it.

The VP Eng sees the *result* in a summary view. The **video shows the agent doing steps 1–4
live**, unedited.

## Demo fixture (deterministic, stranger-safe)

| Fixture | Role |
|---|---|
| `fixtures/operators/` | Two synthetic transcript JSONL files (operator-a high-survive, operator-b low-survive on same task class). **operator-a was rebuilt 2026-08-30 and is now genuinely synthetic.** The previous file was labelled synthetic and was not: it was a real session dump carrying `~/.claude` paths and a written-up live database finding, public since `f812bea`. A fixture described as synthetic must be synthetic, or the label is the vulnerability. |
| `fixtures/org-repo/` | Minimal git repo with empty `.cursor/rules/` |
| `fixtures/expected/` | Golden: propagated skill content + witness verdict |

Stranger clones into empty `HOME`, runs one command, sees propagation + proof. No Oscar machine
data required for the gate; real corpus is the stretch demo after fixtures pass.

## Submission-critical vs stretch

| Slice | Video-critical? | Notes |
|---|---|---|
| Ingest + `is_human` gate | yes | transcripto spine read-only |
| One performance signal (survive vs abandon) | yes | heuristic OK if probe named |
| Agent propagation (ADK + 3 tools) | **yes — the wedge** | reuses `cloud/agent.py` pattern |
| People leaderboard | stretch | thin table OK if time |
| Full org multi-seat ingest | post-hackathon | trust model in README |
| Cloud Run + Firestore | yes | visual proof in video |
| Diagram · stranger · video | yes | starts Aug 28 earliest |

## ADK tools (plain functions first, ADK wraps second)

```
find_best_prompt(topic, corpus_root) -> {operator, prompt_text, signal, probe}
propagate_prompt(prompt_text, target_skill_path) -> {written, sha}
witness_propagation(target_skill_path) -> {verdict, probe, evidence}
```

Same split as `agent-claims-inbox/cloud/agent.py`: tools verified without ADK; wrapper UNVERIFIED
until GCP live.

## The line for judges

> **GEAP governs the agents. Nothing governs the prompts.** We close the loop: your org's best
> prompt, found in yesterday's transcript, applied tomorrow — by the supervisor, not by a memo.
