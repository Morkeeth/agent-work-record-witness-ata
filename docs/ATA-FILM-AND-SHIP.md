# ATA film + ship — THE AGENT WORK RECORD WITNESS (Oscar checklist)

**Product name on camera: THE AGENT WORK RECORD WITNESS, said in full, at least twice.**
"Hold" is the name of the queue inside it. Never say "HOLD" as the product.

**Do not film Seed.** Seed is disabled on Cloud Run (`HOLD_DEMO_MODE=0`).

## 0 · Push + secrets (blocks judges + Action)

```bash
cd ~/CODE/hack-fleet-ata
git status
git push -u origin HEAD   # Oscar click — includes the console + auth

# GitHub repo settings:
# Variables:  HOLD_POLICY_URL = https://fleet-wedge-33kamss2jq-uc.a.run.app/clearance
# Secrets:    HOLD_API_TOKEN  = (same value as local .hold_api_token / Cloud Run env)
```

Local token (gitignored): `.hold_api_token` — paste into console "Operator token" for break-glass.

## 1 · Real false-done PR (the beat that fills the record)

```bash
cd ~/CODE/hack-fleet-ata
./scripts/open_agent_hold_pr.sh
# or manually:
# 1. Branch from main
# 2. Open PR, label `agent`
# 3. PR body = fixtures/agent-false-done-PR-BODY.md
# 4. Branch protection: require check name verify-claims
```

Expected: check **fails** (BLOCK on `deadbee` / missing path). The Hold queue shows the row after
the Action POSTs (needs secrets).

**This is the ten minutes that turns the demo into a product.** Until it runs, the record holds
four staged clearances and `clear: 0` — nothing real has ever gone through the gate.

## 2 · Pre-roll smoke

```bash
URL=$(cat .cloud_run_url)
curl -sS "$URL/health"          # auth_required true, demo_seed false, firestore, ADK agent
curl -sS "$URL/config"
curl -sS -o /dev/null -w "%{http_code}\n" "$URL/hold/"
python3 contract/eligibility.py # 3 OF 3 MET here — cold with no GCP creds it is 1 OF 3, exit 1
open "$URL/hold/"
```

**Open defects to re-check before rolling** (both found 2026-08-27, both may still be live):

```bash
curl -s -o /dev/null -w "prove anon: %{http_code}\n" -X POST -H 'Content-Type: application/json' -d '{}' "$URL/prove"
# want 401. It returned 201 — the deployed revision is behind cloud/service.py on this one route.

curl -s "$URL/audit"        | python3 -c 'import sys,json;print("audit events:",json.load(sys.stdin)["events"])'
curl -s "$URL/audit/export" | python3 -c 'import sys,json;print("export events:",len(json.load(sys.stdin)["events"]))'
# these two disagreed: 30 vs 6. The export films at beat 5.
```

## 3 · Film spine (≤4:00) — **open on the record, not the check**

1. **Problem** — you can see the seats and the spend; you cannot see what the agents did
2. **The record** — `/hold/`: a held claim, opened, resolving to the session that produced it
3. **How it fills** — the gate: agent PR → probe vs object → HOLD
4. **Real PR** — red `verify-claims` + the Hold row + the probe output
5. **Break-glass + Audit** (+ Export JSON)
6. **GCP** — Cloud Run + `/health`, say the `*.run.app` URL · `eligibility.py` 3/3, **and say cold is 1/3**
7. **Honest state** — zero real claims before today · `clear: 0` · never fired on a real PR
8. **Close** — *Run your agents. Check the math.*

**Banned on camera:** the Seed button · `/healthz` · org lift at n=2 · the words "required check"
while requiredness is unresolved · the names HOLD / Witness / Claims Inbox / hack-fleet-ata as the
product · the old line "GEAP governs the agents."

## 4 · Devpost

Paste from `SUBMISSION-PACK.md`. Share private repo with `testing@devpost.com` +
`cloudhackathons@google.com`.

**Before pasting:** re-export `docs/architecture.png` from `docs/ARCHITECTURE.md`. The committed PNG
predates the RECORD ruling — it leads with the gate, says "required check", and shows a Gemini
invocation that does not happen in the container.

## 5 · After submit

Paste Devpost URL + video URL into a receipt note in this repo (Oscar).
