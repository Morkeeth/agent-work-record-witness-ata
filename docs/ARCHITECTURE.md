# Architecture — Transcripto fleet supervisor

**Required submission artifact.** Honest two-path: Firestore is live today; GEAP Memory Bank is optional stretch.

```mermaid
flowchart LR
  subgraph Corpus
    T[Claude Code transcripts<br/>opt-in org corpus]
    G[Authorship gate<br/>promptSource / isMeta]
  end

  subgraph Classify["Gemini 3.5+ Vertex"]
    C[Task-class classifier<br/>SAME / DIFFERENT / UNDECIDABLE]
  end

  subgraph Score
    E[Episode extract<br/>corrective turns · LANDED]
    R[Pairwise rank<br/>prompt ↔ prompt]
  end

  subgraph Agent["Google ADK"]
    A[fleet_supervisor<br/>find · propagate · witness]
  end

  subgraph Cloud["Google Cloud"]
    FS[(Firestore<br/>propagation log)]
    CR[Cloud Run<br/>POST /wedge · /prove]
  end

  subgraph Org
    S[Org skill file<br/>.cursor/rules]
    W[Witness<br/>VERIFIED-BY-REPO]
  end

  T --> G --> E
  E --> C --> R --> A
  A --> S --> W
  A --> FS
  CR --> A
```

## Mandatory stack (Devpost rules, verified 2026-08-22)

| Requirement | Implementation | Probe |
|---|---|---|
| Gemini 3.5+ via API or Vertex | `contract/gemini_impl.py` → Vertex (`gemini-3.5-flash-lite`) | `python3 contract/eligibility.py` MET 1 |
| Google Agent Framework | `cloud/agent.py` `build_agent()` → ADK `LlmAgent` | MET 2 |
| Google Cloud infrastructure | Firestore default store · Cloud Run `fleet-wedge` | MET 3 · `.cloud_run_url` |

**Smoke note:** use `GET /health` or `GET /` — GFE returns HTML 404 for `/healthz` on this service. Video must show the `*.run.app` URL.

## What is NOT claimed

- Pub/Sub fan-out of N analysts (EYES: KILL for Week 0)
- Population lift across an org on a single-builder corpus (Track B)
- Classifier 8/8 while C1 is red

## Run

```bash
python3 contract/eligibility.py
python3 fleet_cli.py prove
./scripts/deploy_cloud_run.sh   # writes .cloud_run_url
```
