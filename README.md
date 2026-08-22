# hack-fleet-ata

Org fleet prompt management for **All Things Agentic** (Devpost · **Aug 31 2026, 5:00pm PT**).

**Track:** Fortified Enterprise Fleet — institutional agents; we govern the **prompts** they never see.

> **GEAP governs the agents. Nothing governs the prompts.**

## What it does

Companies see seats and spend. They cannot see **practice**. This repo finds the operator
prompt that landed with the fewest corrective turns on a task class and **propagates the
literal text** into the org skill file — witnessed on disk / Firestore. No LLM rewrite.

## Judge path (3 of 3 mandatory)

| Requirement | Status | Probe |
|---|---|---|
| Gemini 3.5+ (API or Vertex) | MET | `python3 contract/eligibility.py` |
| Google Agent Framework (ADK) | MET | agent **constructed** on `/wedge` |
| Google Cloud infra | MET | Firestore default store · Cloud Run |

```bash
python3 contract/eligibility.py    # exits 0 only at 3/3 — services CALLED, not imported
python3 fleet_cli.py wedge         # field of 2 · operator a · VERIFIED-BY-REPO
python3 fleet_cli.py prove         # A 0 vs B 2 corrective turns → surface/org-proof.html
```

## Spin-up (stranger)

```bash
git clone https://github.com/Morkeeth/hack-fleet-ata
cd hack-fleet-ata
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# No GCP: wedge still runs on fixtures (Gemini via AI Studio key at ~/.config/keys/gemini.key)
python3 fleet_cli.py wedge
python3 fleet_cli.py prove && open surface/org-proof.html

# Full 3/3 (ADC + project hack-fleet or your own with Firestore + Vertex):
gcloud auth application-default login
gcloud config set project hack-fleet
python3 contract/eligibility.py
```

## Cloud Run

```bash
export PATH="$HOME/google-cloud-sdk/bin:$PATH"
./scripts/deploy_cloud_run.sh
# then:
curl -s "$(cat .cloud_run_url)/health"
curl -s -X POST "$(cat .cloud_run_url)/prove" -H 'Content-Type: application/json' -d '{}'
open "surface/org-lift-live.html?api=$(cat .cloud_run_url)"
```

## Architecture

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) (mermaid diagram).  
Journey: [`docs/USER-JOURNEY.md`](docs/USER-JOURNEY.md) · Moonshot tiers: [`docs/MOONSHOT-PLAN.md`](docs/MOONSHOT-PLAN.md).

## Pre-existing code (disclosure)

| Source | Role |
|---|---|
| [transcripto](https://github.com/Morkeeth/transcripto) | corpus spine / authorship gating |
| agent-claims-inbox (local) | Cloud Run + ADK shell patterns |

Product logic (episodes, pairwise rank, propagate, org-proof) is **new in this repo**.

## Honest limits

- Demo field size is **2** fixtures — enough for the mechanism; org-population claims need **n≥3** (`org_claim: UNMEASURED_FOR_ORG_CLAIM`).
- Classifier C1 can stay red — do not seal "8/8" (`scripts/variance_appendix.py`).
- Population lift across engineers is **day-two customer data**, not a single-builder corpus.

## License

TBD.
