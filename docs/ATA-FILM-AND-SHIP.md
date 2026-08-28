# ATA film + ship — THE AGENT WORK RECORD WITNESS (Oscar checklist)

**Product name on camera: THE AGENT WORK RECORD WITNESS, said in full, at least twice.**
"Hold" is the name of the queue inside it. Never say "HOLD" as the product.

**Do not film Seed.** Seed is disabled on Cloud Run (`HOLD_DEMO_MODE=0`).

## 0 · Push + secrets — ✅ DONE 2026-08-28, nothing blocks here

`origin/main` matches local and the repo is **PUBLIC** (`gh repo view` → `visibility: PUBLIC`).
Secrets and variables are set. **A judge clones the same files you have on screen** — re-check
with one command before rolling, and only act if it disagrees:

```bash
cd ~/CODE/hack-fleet-ata
[ "$(git ls-remote origin HEAD | cut -c1-7)" = "$(git rev-parse --short HEAD)" ] \
  && echo "clone == screen" || echo "PUSH BEFORE FILMING"

# GitHub repo settings:
# Variables:  HOLD_POLICY_URL = https://fleet-wedge-33kamss2jq-uc.a.run.app/clearance
# Secrets:    HOLD_API_TOKEN  = (same value as local .hold_api_token / Cloud Run env)
```

Local token (gitignored): `.hold_api_token` — paste into console "Operator token" for break-glass.

## 1 · Real false-done PR — ✅ RAN 2026-08-28. This beat is no longer blocked.

`GET /audit` carries a **`github-action`** clearance against the real public repo — the first
genuine claim the gate has ever seen. Commit `35b8284`. Re-run below only if you want a second one
on camera.


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

**`clear: 0` is still 0, and that is the product working, not a gap.** The one real claim that
arrived was false, and it was held. Say that rather than apologising for it: the record has never
cleared anything because nothing honest has been submitted to it yet.

**Do not read a live counter onto camera.** `/audit` and `/audit/export` moved twice in one hour
today. The filter is the fact; the count is a reading. Show the rows, not the totals.

## 2 · Pre-roll smoke

```bash
URL=$(cat .cloud_run_url)
curl -sS "$URL/health"          # auth_required true, demo_seed false, firestore, ADK agent
curl -sS "$URL/config"
curl -sS -o /dev/null -w "%{http_code}\n" "$URL/hold/"
python3 contract/eligibility.py # MUST print 3 OF 3 — see the pre-roll check below
open "$URL/hold/"
```

### ⚠ WHICH `python3` — check this before you roll, it is not a footnote

```bash
python3 -V     # want 3.12.x from /Library/Frameworks. /usr/bin/python3 is 3.9.6 and has no ADK.
```

On the 3.12 interpreter `eligibility.py` prints **3 OF 3 MET**. On stock `/usr/bin/python3` it
prints **1 OF 3**, correctly — no ADK, no Firestore on the default path. Both results are honest
and the README says so, **but a judge watching "1 OF 3" against three HARD requirements will not
read the footnote.** Film the 3 OF 3.

### Both 2026-08-27 open defects are CLOSED — verified 2026-08-28, do not re-warn on camera

```bash
curl -s -o /dev/null -w "prove anon: %{http_code}\n" -X POST -H 'Content-Type: application/json' -d '{}' "$URL/prove"
# 401. Was 201. Every mutating route now rejects an anonymous caller:
# /prove /clearance /break-glass /agent/run all 401 · /seed 404 (disabled)
```

The `/audit` vs `/audit/export` gap was **never a defect**: the export drops prove-only rows by
design, and `?include_prove=1` makes the two agree exactly. Explain the filter if it comes up;
never quote the counts.

## 3 · Film spine (≤4:00) — **open on the record, not the check**

1. **Problem** — you can see the seats and the spend; you cannot see what the agents did
2. **The record** — `/hold/`: a held claim, opened, resolving to the session that produced it
3. **How it fills** — the gate: agent PR → probe vs object → HOLD
4. **Real PR** — red `verify-claims` + the Hold row + the probe output
5. **Break-glass + Audit** (+ Export JSON)
6. **GCP** — Cloud Run + `/health`, say the `*.run.app` URL · `eligibility.py` 3/3, **and say cold is 1/3**
7. **Honest state** — `clear: 0` · the one real claim that arrived was false and was held ·
   zero installs by anyone who is not the author
8. **Close** — *Run your agents. Check the math.*

**Banned on camera:** the Seed button · `/healthz` · org lift at n=2 · the words "required check"
while requiredness is unresolved · the names HOLD / Witness / Claims Inbox / hack-fleet-ata as the
product · the old line "GEAP governs the agents."

## 4 · Devpost

Paste from `SUBMISSION-PACK.md`. **No repo sharing step — the repo is PUBLIC.**

`docs/architecture.png` was **re-exported 2026-08-28 from `docs/ARCHITECTURE.md` and looked at**,
not just regenerated. The previous PNG had **no Cloud Run anywhere in it**, against a rubric that
hard-requires a Google Cloud infrastructure service and scores Cloud Deployment Proof. Cloud Run is
now a node on the request path, so Cloud Run, Firestore and ADK/Vertex Gemini are all in one frame.
The Transcripto lane is labelled ROADMAP — it needs a corpus a judge cannot verify.

Regenerate with:
```bash
npx -y @mermaid-js/mermaid-cli@11 -i <mermaid-block> -o docs/architecture.png -w 1400 -b white
```
**Then open it and look.** A clipped subgraph title got through the first render today.

## 5 · After submit

Paste Devpost URL + video URL into a receipt note in this repo (Oscar).
