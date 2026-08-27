# THE AGENT WORK RECORD WITNESS

**The system of record for what your agent workforce actually did** — who claimed what, whether
the object agreed, whether the work survived, and the session behind every claim.

Built for **All Things Agentic** (Devpost · **Aug 31 2026, 5:00pm PT**) · Track: **Fortified Enterprise Fleet**.

> You can see how many agent seats you bought. You cannot see what those agents actually did,
> or how much of what they reported was true. Now you can.

**Console (Cloud Run):** https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/
**Gateway health:** https://fleet-wedge-33kamss2jq-uc.a.run.app/health

```bash
curl -s https://fleet-wedge-33kamss2jq-uc.a.run.app/health
curl -s https://fleet-wedge-33kamss2jq-uc.a.run.app/queue
open "https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/"
```

> **Naming.** The product is THE AGENT WORK RECORD WITNESS. **"Hold" is the name of the queue
> inside it** — the list of claims that did not survive their own probe. It is a route and a
> screen, not the product.

> **Deploy note:** the live URL serves the Gateway and the console. Re-deploy with
> `./scripts/deploy_cloud_run.sh` after local changes (needs `.hold_api_token`).

---

## The problem

Enterprises bought coding-agent seats. They see spend. They cannot govern whether agent work is
**true** — before it merges, and after. An agent reports *"Fixed the race. 214 tests pass.
Committed as `deadbee`. Deployed."* — and today the only way to know is to open the repo by hand.
With overnight fleets and auto-merge, that prose is an ungoverned production surface, and once it
scrolls past, nothing remembers it.

Four different people arrive at the same question from four directions — the regulator, the VP Eng
after an incident, the CFO at renewal, and your own customer's procurement. See
[`docs/WHY-THIS-MATTERS.md`](docs/WHY-THIS-MATTERS.md); each force is stated with its weakness.

## What it is

**A record, with a gate as its intake.**

| Surface | Job |
|---|---|
| **The record** Firestore | Every claim, its verdict, its break-glass reason. The thing that accumulates. |
| **The join** | A held claim opens back to the session that produced it. Nobody else holds the transcript. |
| **Console** `/hold/` | The Hold queue. Empty = calm. Break-glass + audit when not. |
| **Gateway** `POST /clearance` | Claim vs object (`git cat-file` / path). CLEAR or HOLD. |
| **Action** `.github/workflows/outcome-gate.yml` | Agent-scoped check → posts to the Gateway. |
| **Export** `GET /audit/export` | The compliance artifact an auditor asks for. |

Journey: [`docs/USER-JOURNEY.md`](docs/USER-JOURNEY.md) · Architecture: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) ·
Pitch: [`SUBMISSION-PACK.md`](SUBMISSION-PACK.md) · Product: [`hack.md`](hack.md) **(canonical)**

**The twist — not stageable:** the verification demo includes confident "done" claims **this fleet
made building it** — blocked against the real object. The tool catches its own makers.

```bash
python3 -m gate.tonight_cases   # the logged case series: agents confidently wrong, the object right
```

---

## Quickstart

### Prerequisites

Python 3.11+, then **one of two credential paths** — `wedge` and `prove` need a Gemini call and
will not run without either.

| Path | Set up | You also get |
|---|---|---|
| **A · Google Cloud (tried first)** | `gcloud auth application-default login` on a project with Vertex + Firestore | eligibility **3 of 3**. Nothing to place on disk. Billed, ~$0.0001 per classification. |
| **B · AI Studio key (free fallback)** | Free key from [aistudio.google.com/apikey](https://aistudio.google.com/apikey) → save it alone into `~/.config/keys/gemini.key` | eligibility stays **1 of 3**. Free tier is 20 requests/day/model. |

`contract/gemini_impl.py` tries Vertex first and drops to the key file only if that fails, so
path A alone is enough and the key file is never required when ADC is present.

⚠️ **With neither, `fleet_cli.py wedge` exits 1 with `{"error": "no rankable prompt in corpus"}`.**
Measured on a cold clone 2026-08-27. The corpus is fine — the message is misleading: nothing was
rankable because no Gemini call could be made. Set up A or B first.

```bash
git clone https://github.com/Morkeeth/hack-fleet-ata
cd hack-fleet-ata
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# path A (preferred):
gcloud auth application-default login
# ...or path B:
mkdir -p ~/.config/keys && printf '%s' "YOUR_AI_STUDIO_KEY" > ~/.config/keys/gemini.key

python3 fleet_cli.py wedge                      # field of 2 · operator a · VERIFIED-BY-REPO
python3 fleet_cli.py prove && open surface/org-proof.html
```

### Google eligibility — read the two numbers

`contract/eligibility.py` **calls** all three services on the path a judge runs. Import is not
call, and credentials you do not have do not count, so it reports two different honest answers:

| You run it | It prints | Exit |
|---|---|---|
| With ADC on a project with Firestore + Vertex | **3 OF 3 MET** | 0 |
| Cold clone, no GCP credentials | **1 OF 3 MET** (ADK only) | **1** |

Both were run on 2026-08-27. **A judge who clones this cold and runs it will see 1 of 3 and a
non-zero exit — that is the designed, honest result, not a broken build.** The same
object-over-claim rule this product enforces is applied to its own eligibility check.

**Two of the three are verifiable with no credentials at all**, against the running deployment —
Firestore as the live store, and the ADK agent constructed:

```bash
curl -s https://fleet-wedge-33kamss2jq-uc.a.run.app/health
# {"ok":true,"store":"firestore","agent":"google.adk.agents.llm_agent.LlmAgent", ...}
```

`/health` does **not** evidence the Gemini requirement — no Gemini call happens on that path, and
today none happens inside the container at all. Requirement 1 is exercised by
`contract/eligibility.py`, which calls Vertex directly. Do not read a `/health` 200 as 3 of 3.

```bash
# To see 3 of 3 locally:
gcloud auth application-default login
gcloud config set project hack-fleet
python3 contract/eligibility.py
```

## Architecture

[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) (mermaid source) · `docs/architecture.png` (submission
export) · journey [`docs/USER-JOURNEY.md`](docs/USER-JOURNEY.md) · company thesis
[`docs/COMPANY.md`](docs/COMPANY.md) · build plan [`hack.md`](hack.md).

Internal process logs (collab protocol, phase tracker, patent memos) are preserved under
[`docs/internal/`](docs/internal/).

## Pre-existing code (disclosure)

| Source | Role |
|---|---|
| [transcripto](https://github.com/Morkeeth/transcripto) | corpus spine / authorship gating |
| agent-claims-inbox (local) | Cloud Run + ADK shell patterns |

Product logic (episodes, pairwise rank, propagate, org-proof, the claim gate, the join) is **new in
this repo**.

## Honest state, measured 2026-08-27

These are probes run today, not numbers quoted from a note.

- **The record holds no real agent claims.** 4 clearances, **all four staged by us**
  (`demo-seed` ×2, `api`, `eyes-probe`). `GET /audit` reports `clear: 0` — **nothing has ever
  passed the gate, because nothing real has ever gone through it.**
- **The check has never fired on a real pull request.**
- **`GET /audit` reports 30 events; `GET /audit/export` returns 6.** Two judge-facing endpoints
  disagree about how many events exist. Open defect.
- **The deployed revision is behind the repo on one route.** Anonymous `POST /prove` returns
  **201** against the live service; it is gated in `cloud/service.py`. `tests/test_auth_gate.sh`
  is green — against a local server. A green local test is not a statement about production.
- **The ADK agent is constructed, not invoked.** It is visible in `/health`; the Gemini call does
  not happen inside the container on the request path today.
- Demo field size is **2** fixtures — enough for the mechanism; org-population claims need **n≥3**
  (`org_claim: UNMEASURED_FOR_ORG_CLAIM`).
- Classifier C1 can stay red — do not seal "8/8" (`scripts/variance_appendix.py`).
- v1 verifies **checkable code claims** (commit exists, test ran, file changed, deploy serves).
  Claims with no artifact witness (*"I analyzed the logs"*) return `UNVERIFIABLE` rather than fake
  a verdict.
- **A cold clone with no credentials blames the wrong thing.** `python3 fleet_cli.py wedge`
  with neither ADC nor a key file exits 1 saying `no rankable prompt in corpus`. The corpus is
  intact; the real cause is that no Gemini call was possible. Separately,
  `contract/gemini_impl.py` calls `_key()` outside its try block, so the key path can raise an
  uncaught `FileNotFoundError`. Both open.
- **Installs by a person who is not the author: zero.**

## License

TBD.
