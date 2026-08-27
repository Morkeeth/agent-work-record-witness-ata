# WITNESS

**The trust layer that verifies what agent fleets claim against the object — the repo, the deploy, the test.**

Built for **All Things Agentic** (Devpost · **Aug 31 2026, 5:00pm PT**) · Track: **Fortified Enterprise Fleet**.

> **GEAP governs the agents. Witness governs whether their work is true.**

**Live demo (Cloud Run · verified HTTP 200):** https://fleet-wedge-33kamss2jq-uc.a.run.app

```bash
curl -s https://fleet-wedge-33kamss2jq-uc.a.run.app/health
```

---

## The problem

Enterprises bought coding-agent seats. They see spend. They cannot govern whether agent work is
**true** before it merges, deploys, or acts. An agent reports *"Fixed the race. 214 tests pass.
Committed as `deadbee`. Deployed."* — four claims — and today the only way to know is to open the
repo, the CI, and the URL by hand. With one agent that is annoying; with a fleet running async in
the background it is impossible. You either trust blindly (and ship a hallucination) or re-check by
hand (and lose the point of delegating).

That gap is not observability (trace theater). It is **assurance** — closer to Datadog-for-agentic-
outcomes than a chat-search tool. Witness stands between an agent's "done" and your trust in it.

## What Witness does

Two surfaces, one trust layer:

| Surface | What it governs | Verdict |
|---|---|---|
| **Verify the work they did** | Each claim an agent makes vs the real artifact (git / deploy / test). | `CONTRADICTED-BY-REPO`, `VERIFIED-BY-REPO`, or `UNVERIFIABLE` — never "looks done." |
| **Govern the prompts they never see** | Which operator practice actually survives on a task class. | Ranks by corrective-turn count and **propagates the literal winning prompt** into the org skill file — witnessed on disk / Firestore. No LLM rewrite. |

**The twist — not stageable:** the verification demo is the four confident "done" claims **this fleet
made building it**. 3 of 4 were blocked against the real object. The tool catches its own makers.

```bash
python3 -m gate.tonight_cases   # the logged case series: agents confidently wrong, the object right
```

## Google eligibility (3 of 3 mandatory)

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

## Quickstart (stranger, no GCP required)

```bash
git clone https://github.com/Morkeeth/hack-fleet-ata
cd hack-fleet-ata
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Wedge runs on fixtures (Gemini via AI Studio key at ~/.config/keys/gemini.key):
python3 fleet_cli.py wedge
python3 fleet_cli.py prove && open surface/org-proof.html

# Full 3/3 (ADC + a project with Firestore + Vertex):
gcloud auth application-default login
gcloud config set project hack-fleet
python3 contract/eligibility.py
```

## Architecture

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) (mermaid) · journey [`docs/USER-JOURNEY.md`](docs/USER-JOURNEY.md) · company thesis [`docs/COMPANY.md`](docs/COMPANY.md) · moonshot tiers [`docs/MOONSHOT-PLAN.md`](docs/MOONSHOT-PLAN.md).

Internal process logs (collab protocol, phase tracker, patent memos, submission pack) are preserved
under [`docs/internal/`](docs/internal/).

## Pre-existing code (disclosure)

| Source | Role |
|---|---|
| [transcripto](https://github.com/Morkeeth/transcripto) | corpus spine / authorship gating |
| agent-claims-inbox (local) | Cloud Run + ADK shell patterns |

Product logic (episodes, pairwise rank, propagate, org-proof, the claim gate) is **new in this repo**.

## Honest limits (v1 scope)

- Demo field size is **2** fixtures — enough for the mechanism; org-population claims need **n≥3**
  (`org_claim: UNMEASURED_FOR_ORG_CLAIM`).
- Classifier C1 can stay red — do not seal "8/8" (`scripts/variance_appendix.py`).
- Population lift across engineers is **day-two customer data**, not a single-builder corpus.
- v1 verifies **checkable code claims** (commit exists, test ran, file changed, deploy serves). Claims
  with no artifact witness (*"I analyzed the logs"*) return `UNVERIFIABLE` rather than fake a verdict.

## License

TBD.
