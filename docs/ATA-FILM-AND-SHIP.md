# ATA film + ship — HOLD (Oscar checklist)

**Do not film Seed.** Seed is disabled on Cloud Run (`HOLD_DEMO_MODE=0`).

## 0 · Push + secrets (blocks judges + Action)

```bash
cd ~/CODE/hack-fleet-ata
git status
git push -u origin HEAD   # Oscar click — includes HOLD console + auth

# GitHub repo settings:
# Variables:  HOLD_POLICY_URL = https://fleet-wedge-33kamss2jq-uc.a.run.app/clearance
# Secrets:    HOLD_API_TOKEN  = (same value as local .hold_api_token / Cloud Run env)
```

Local token (gitignored): `.hold_api_token` — paste into console “Operator token” for break-glass.

## 1 · Real false-done PR (the ambitious camera beat)

```bash
cd ~/CODE/hack-fleet-ata
./scripts/open_agent_hold_pr.sh
# or manually:
# 1. Branch from main
# 2. Open PR, label `agent`
# 3. PR body = fixtures/agent-false-done-PR-BODY.md
# 4. Branch protection: require check name verify-claims
```

Expected: check **fails** (BLOCK on `deadbee` / missing path). Console Hold Queue shows the row after Action POSTs (needs secrets).

## 2 · Pre-roll smoke

```bash
URL=$(cat .cloud_run_url)
curl -sS "$URL/health"          # product HOLD, auth_required true, demo_seed false
curl -sS "$URL/config"
curl -sS -o /dev/null -w "%{http_code}\n" "$URL/hold/"
python3 contract/eligibility.py # 3 OF 3 MET
open "$URL/hold/"
```

## 3 · Film spine (≤4:00)

1. Problem — overnight fleets / false done  
2. Install tab — Action + policy URL + progressive enforce story  
3. GCP — Cloud Run console + `/health`  
4. **Real PR** — red `verify-claims` + Hold Strip + probe  
5. Break-glass + Audit (+ Export JSON)  
6. Registry `/prove` footnote + UNMEASURED  
7. Close — *GEAP governs the agents. HOLD governs the release.*

## 4 · Devpost

Paste from `SUBMISSION-PACK.md`. Share private repo with `testing@devpost.com` + `cloudhackathons@google.com`.

## 5 · After submit

Paste Devpost URL + video URL into a receipt note in this repo (Oscar).
