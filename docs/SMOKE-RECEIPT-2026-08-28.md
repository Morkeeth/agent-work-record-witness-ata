# ATA smoke receipt · 28 Aug 2026 (~13:45 CET)

**Runner:** Cursor (autonomous while Oscar away)  
**URL:** `https://fleet-wedge-33kamss2jq-uc.a.run.app`

## Results

| Check | Result | Notes |
|-------|--------|-------|
| `GET /health` | **200** | `auth_required: true`, `demo_seed_enabled: false`, Firestore store, ADK constructed |
| `POST /prove` (no auth) | **401** | Anon route closed — good |
| `GET /hold/` | **200** | Console loads |
| `python3 contract/eligibility.py` | **3 OF 3 MET** | Vertex + ADK + Firestore round-trip |

## Film-ready verdict

**Code path: green.** Push is not the blocker (`dc1591c`+ on `origin/main`).

**Still human-only before film:**
1. GitHub secrets — `HOLD_API_TOKEN`, `HOLD_POLICY_URL` variable
2. Real false-done PR through `verify-claims` check (`./scripts/open_agent_hold_pr.sh`)
3. Oscar films per `FILM-SHOT-LIST-2026-08-28.md` — say the **Aug 26 corpus window** out loud

## GCP note

`/health` first attempt timed out at 10s; succeeded at 25s. Cold start or network — re-check before rolling camera.
