> ⛔ **SUPERSEDED 2026-08-27 — do not read as current.** The canonical doc is `hack.md` at the repo root.
> This file is kept for history only. It described a narrower product than the one being built.

# HOLD — Ambitious ATA goal (this repo only)

**Hackathon:** All Things Agentic · Fortified Enterprise Fleet · **Aug 31 2026 17:00 PDT**  
**Product home:** this repo (`hack-fleet-ata`) — not fleet-ops.  
**Live:** https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/

## Ambition (one sentence)

Ship **outcome clearance for agentic production** — a Gateway enterprises would recognize — so judges feel “they understand enterprises,” not “nice CI script.”

## Done when (evidence)

| # | Requirement | Evidence |
|---|-------------|----------|
| 1 | HOLD console + Gateway live on Cloud Run | `/hold/`, `/health` product=HOLD, auth_required |
| 2 | Writes locked; Seed off for film | `/config` demo_seed_enabled=false; anon POST /clearance → 401 |
| 3 | Real agent-PR path (no Seed) | `agent` label + `fixtures/agent-false-done-PR-BODY.md` → required check red |
| 4 | Break-glass + audit export | Console + `/audit/export` |
| 5 | Registry footnote honest | `/prove` + UNMEASURED on n=2 |
| 6 | Eligibility 3/3 | `python3 contract/eligibility.py` |
| 7 | Devpost pack under HOLD | `SUBMISSION-PACK.md` + film sheet |
| 8 | origin shows HOLD (not old Hack Fleet README) | `git push` of this tree |

## CUT (do not burn calendar)

SSO/SAML theater · fake tenant switcher · Helicon live · Claims Inbox brand · five products · filming Seed.

## Phases

**A — ATA week (now):** anti-demo + real PR + film + submit.  
**B — 30d:** GitHub App, Check Runs, packaged Action, external repo.  
**C — 90d:** SSO/RBAC, deploy witnesses, Transcripto provenance, Helicon probe pack.

## Oscar clicks still required

1. `git push`  
2. Secrets: `HOLD_API_TOKEN` · var `HOLD_POLICY_URL`  
3. Branch protection: require `verify-claims`  
4. Open labeled PR · film · Devpost  

See `docs/ATA-FILM-AND-SHIP.md`.
