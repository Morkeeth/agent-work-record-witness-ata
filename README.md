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

## Collaboration — two local builders + one cloud lane

| Lane | Where | Owns |
|---|---|---|
| Claude Code (local) | terminal | `docs/**` · `surface/**` · vision docs |
| Cursor (local) | this session | `fleet/**` · `fixtures/**` · `fleet_cli.py` |
| Cursor Cloud | paste `CLOUD-HANDOFF.md` | audit · gap tracking · `CURSOR-LOG.md` appends |

Protocol: `COLLAB-PROTOCOL.md` · Phase gates: `PHASE-TRACKER.md` · Shared log: `CURSOR-LOG.md`.

**Cloud agent requires a git remote first** — Oscar pushes, then open Cloud Agent on the repo.

## Setup

### 1. Run it with no accounts (stranger path)

```bash
git clone <this-repo>
cd hack-fleet-ata
python3 fleet_cli.py wedge --topic "refactor auth"
```

Expected: operator-a's prompt propagated to `fixtures/org-repo/.cursor/rules/propagated-skill.md`,
witness `VERIFIED-BY-REPO`. This path uses a local jsonl store and the free AI-Studio classifier —
**no GCP required, and it satisfies 1 of the 3 required Google technologies (Gemini).**

### 2. The full Google-stack path (required for 3 of 3)

The submission requires Gemini 3.5+, a Google Agent Framework, and a Google Cloud service. The
first is met above; the other two need a GCP project:

```bash
pip install google-adk google-cloud-firestore
gcloud auth application-default login          # provides ADC — no key file
gcloud config set project <YOUR_PROJECT_ID>    # a project with Firestore + Vertex AI enabled
```

### 3. Verify eligibility — exercised, not asserted

```bash
python3 contract/eligibility.py                # exits 0 only at 3 OF 3
```

It strips the environment, **calls** each service (does not merely import it), and prints the
answering path per requirement:

```
MET  1. Gemini    vertex:gemini-3.5-flash -> <verdict>
MET  2. ADK       google.adk.agents.LlmAgent  (agent constructed)
MET  3. Cloud     round-trip hit FirestoreStore
3 OF 3 MET — exercised on the path a judge runs.
```

**Without step 2, the app runs at 1 of 3** (local store, no ADK) — the setup is required for the
full Google-stack path, and it degrades gracefully rather than crashing. See
`docs/SPEC-EXTRACT.md` for the verbatim requirement text.

## Trust model

Opt-in team corpus: Claude Code session transcripts the org chooses to index. Nothing extracted
from a transcript is ever executed. Every verdict names the probe that produced it.

## License

TBD.
