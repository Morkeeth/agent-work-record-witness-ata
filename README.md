# HOLD

**Outcome clearance for agentic production** — agent work is not production-real until its claims survive the object.

Built for **All Things Agentic** (Devpost · **Aug 31 2026, 5:00pm PT**) · Track: **Fortified Enterprise Fleet**.

> **GEAP governs the agents. HOLD governs the release.**

**Enterprise console (Cloud Run):** https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/  
**Gateway health:** https://fleet-wedge-33kamss2jq-uc.a.run.app/health

```bash
curl -s https://fleet-wedge-33kamss2jq-uc.a.run.app/health
curl -s https://fleet-wedge-33kamss2jq-uc.a.run.app/queue
open "https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/"
```

> **Deploy note:** Live URL is HOLD Gateway + console. Re-deploy with `./scripts/deploy_cloud_run.sh` after local changes (needs `.hold_api_token`).

---

## The problem

Enterprises bought coding-agent seats. They see spend. They cannot govern whether agent work is
**true** before it merges, deploys, or acts. An agent reports *"Fixed the race. 214 tests pass.
Committed as `deadbee`. Deployed."* — and today the only way to know is to open the repo by hand.
With overnight fleets and auto-merge, that prose is an ungoverned production surface.

HOLD is **release control**: fail closed when the claim and the object disagree. Not observability.
Not code review. Not a chat inbox.

## What HOLD does

| Surface | Job |
|---|---|
| **Gateway** `POST /clearance` | Claim vs object (`git cat-file` / path). CLEAR or HOLD. |
| **Console** `/hold/` | Empty Hold Queue = calm. Break-glass + audit when not. |
| **Action** `.github/workflows/outcome-gate.yml` | Required check on agent PRs → posts to Gateway. |
| **Registry** `POST /prove` | Literal surviving practice → org skill (`UNMEASURED` on n=2). |

Pitch: [`SUBMISSION-PACK.md`](SUBMISSION-PACK.md) · Film: [`docs/ATA-FILM-AND-SHIP.md`](docs/ATA-FILM-AND-SHIP.md) · Product: [`hack.md`](hack.md) **(canonical)**

**The twist — not stageable:** the verification demo includes confident "done" claims **this fleet
made building it** — blocked against the real object. The tool catches its own makers.

```bash
python3 -m gate.tonight_cases   # the logged case series: agents confidently wrong, the object right
```

## Google eligibility (3 of 3 mandatory)

**3/3 is verified against the live deployment.** Curl the running Cloud Run URL — it reports the
Firestore store and the constructed ADK agent live, on the project that fills all three slots:

```bash
curl -s https://fleet-wedge-33kamss2jq-uc.a.run.app/health
# {"ok":true,"store":"firestore","agent":"google.adk.agents.llm_agent.LlmAgent"}
```

| Requirement | Verified where | Probe |
|---|---|---|
| Gemini 3.5+ (API or Vertex) | live deploy / with creds | Gemini classify verdict returned |
| Google Agent Framework (ADK) | live deploy / with creds | ADK agent **constructed** on `/wedge` |
| Google Cloud infra | live deploy / with creds | Firestore default store · Cloud Run |

`contract/eligibility.py` exercises all three on the path a judge runs. **It shows 3/3 only with ADC +
the `hack-fleet` project (Firestore + Vertex reachable); a cold local run with no GCP creds shows 1/3
— only ADK — by design.** That is not a bug: the same object-over-claim honesty this tool exists to
enforce is applied to its own eligibility check. Import is not call, and creds you don't have don't
count.

```bash
# With ADC + Firestore + Vertex on the hack-fleet project → 3/3, exit 0:
python3 contract/eligibility.py    # services CALLED, not imported; 1/3 cold (ADK only), by design

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

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) (mermaid) · journey [`docs/USER-JOURNEY.md`](docs/USER-JOURNEY.md) · company thesis [`docs/COMPANY.md`](docs/COMPANY.md) · build plan [`hack.md`](hack.md).

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
