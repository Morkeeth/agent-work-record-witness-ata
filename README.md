# hack-fleet-ata

Org-level fleet and prompt management for **All Things Agentic** (Devpost · Aug 31 2026).

**Track:** Fortified Enterprise Fleet — *a scalable network of institutional agents.*

## What it does

Companies see seats and spend. They cannot see **practice** — what engineers actually prompt,
which prompts work, who is good at it. This tool builds on the [transcripto](https://github.com/Morkeeth/transcripto)
corpus and closes the loop: the ADK fleet supervisor finds a high-survival prompt from your
org's best operator and **propagates it** into the team skill file without a human opening a
coaching UI.

Read `CONTEXT.md` for product scope · `docs/WEDGE.md` for the demo loop · `PHASE-0.md` for gates.

## Pre-existing code (disclosure)

| Source | Repo | Role |
|---|---|---|
| transcripto | Morkeeth/transcripto | corpus spine, `is_human` / `promptSource` gating |
| agent-claims-inbox | local (~1,345 LOC) | ingest discovery, witness probes, Cloud Run + ADK shell |

Product surfaces (prompt performance, propagation, people view) are **new in this repo**.

## Setup

**Status:** Phase 1 — wedge loop runs on fixtures. Cloud Run / ADK pending GCP (Aug 26 gate).

```bash
git clone <this-repo>
cd hack-fleet-ata
python3 fleet_cli.py wedge --topic "refactor auth"
```

Expected: operator-a's prompt propagated to `fixtures/org-repo/.cursor/rules/propagated-skill.md`,
witness `VERIFIED-BY-REPO`.

**Requirements (submission):** Gemini 3.5+ · Google ADK · Cloud Run or Firestore · see
`docs/SPEC-EXTRACT.md`.

## Trust model

Opt-in team corpus: Claude Code session transcripts the org chooses to index. Nothing extracted
from a transcript is ever executed. Every verdict names the probe that produced it.

## License

TBD.
