# OSCAR SUBMIT PACK — All Things Agentic
_Probed live 2026-08-26 evening. **Company brand: Witness.** Shell repo: this one only. `agent-claims-inbox` is engine + disclosure, not a second Devpost project._

**Company one-pager:** `~/CODE/fleet-ops/gtm/WITNESS-COMPANY.md`  
**Film beats:** `~/CODE/fleet-ops/gtm/WITNESS-ATA-BEAT-SHEET.md`  
**Orchestrator:** `~/CODE/fleet-ops/gtm/CLAUDE-HANDOVER-WITNESS-2026-08-26.md`

**Deadline:** Aug 31 2026 · **17:00 PDT**  
**Devpost:** https://allthingsagentichackathon.devpost.com/  
**Repo (private):** https://github.com/Morkeeth/hack-fleet-ata  
**Cloud Run:** `https://fleet-wedge-33kamss2jq-uc.a.run.app` (also in `.cloud_run_url`)

---

## Live receipt (do not re-litigate)

| Probe | Result | When |
|---|---|---|
| `python3 contract/eligibility.py` | **3 OF 3 MET** (Vertex Gemini · ADK constructed · Firestore round-trip) | 2026-08-26 |
| `GET /health` | `ok:true` · store=`firestore` · agent=`LlmAgent` · HTTP 200 | 2026-08-26 |
| `POST /prove` | winner **a** · 0 corrective · loser **b** · 2 · `VERIFIED-BY-REPO` · HTTP 201 | 2026-08-26 |
| First `/health` curl | can **time out** on cold start — wait / retry; video must show a successful JSON | same |

**Mandatory video path is `/health` not `/healthz`** (GFE HTML 404).

---

## Do not paste these into Devpost

| File | Why |
|---|---|
| `PITCH.md` | Drifted into Gate / verification-gate story; not the fleet product on camera |
| `CLOSE.md` | Stale "INELIGIBLE" banner + "no remote" — remote exists; eligibility is 3/3 |
| Population-lift / "hundreds of seats" | Field size **2** · `org_claim: UNMEASURED_FOR_ORG_CLAIM` |
| Classifier "8/8" | C1 red — variance appendix forbids seal |

**Paste sources:** this file · `README.md` · `docs/ARCHITECTURE.md` · live prove JSON · `surface/org-proof.html` / `org-lift-live.html`.

---

## Oscar click list (order)

1. **Share private repo** with `testing@devpost.com` **and** `cloudhackathons@google.com` (GitHub → Settings → Collaborators, or org invite).
2. **Warm Cloud Run** before film: `curl -s "$(cat .cloud_run_url)/health"` until JSON (not hang).
3. **One-take ≤4 min** — run `python3 scripts/video_beat_sheet.py` and follow beats below.
4. Upload to **YouTube or Vimeo** · public (or unlisted-but-link-works logged out) · English.
5. Open Devpost submission · paste fields below · attach architecture (mermaid export or screenshot of `docs/ARCHITECTURE.md`) · video URL · repo URL.
6. **Submit before 17:00 PDT Aug 31.** Paste Devpost project URL + video URL into a receipt note when done.

Optional Gate 1 direction pick is **not** on the critical path for eligibility.

---

## Film beats (≤4:00, unedited)

| Time | Beat | On camera |
|---|---|---|
| 0:00–0:20 | Problem | GEAP governs agents; nothing governs prompts. Seats ≠ practice. |
| 0:20–0:50 | Eligibility | Terminal: `python3 contract/eligibility.py` → **3 OF 3 MET**. |
| 0:50–1:20 | Google Cloud proof | Console: Cloud Run service **fleet-wedge** · browser `*.run.app/health` JSON · say the URL aloud. |
| 1:20–2:10 | M3 delta | `POST /prove` or `python3 fleet_cli.py prove` · A=0 vs B=2 · `VERIFIED-BY-REPO`. |
| 2:10–2:40 | Literal | Skill/witness text = winner opener bytes (no LLM rewrite). Field of 2 · no org population claim. |
| 2:40–3:20 | Architecture | Mermaid from `docs/ARCHITECTURE.md` · ADK · Firestore · Cloud Run · Gemini. |
| 3:20–3:50 | Honest limit | Day-two customer corpus for population lift; no 8/8 seal. |
| 3:50–4:00 | Close | Repo + README spin-up. |

### Pre-roll smoke (terminal, before record)

```bash
cd ~/CODE/hack-fleet-ata
export PATH="$HOME/google-cloud-sdk/bin:$PATH"
URL=$(cat .cloud_run_url)
curl -sS -m 30 "$URL/health"
curl -sS -m 45 -X POST "$URL/prove" -H 'Content-Type: application/json' -d '{}'
open "surface/org-lift-live.html?api=$URL"
python3 contract/eligibility.py
```

---

## Devpost paste pack

### Project title
**Witness** — outcome truth for agentic fleets

### Tagline (one line)
GEAP governs the agents. Witness governs whether their work is true.

### Track
Fortified Enterprise Fleet (institutional agents / outcome assurance)

### Hosted project URL
```
https://fleet-wedge-33kamss2jq-uc.a.run.app
```
(Health: `/health` · Proof: `POST /prove` with `{}` · UI: open local `surface/org-lift-live.html?api=<that-url>`)

### Repo URL
```
https://github.com/Morkeeth/hack-fleet-ata
```
Private — shared with `testing@devpost.com` and `cloudhackathons@google.com`.

### Architecture diagram
Source of truth: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) (mermaid). Export PNG/SVG or screenshot for the form.

### Text description (paste)

**Problem.** Enterprises run coding-agent fleets and can see seats and spend, not whether agent work is **true** before it merges — “done” is prose; git and the claim often disagree.

**What we built.** **Witness** is the assurance layer: an authorship-gated transcript spine (Transcripto) feeds an outcome record. Y1 surface = claim-vs-repo gate (`CONTRADICTED-BY-REPO`). Module C on this entry = rank surviving operator practice and **propagate the literal winning prompt** into the org skill file, witnessed on disk / Firestore — no LLM rewrite.

**Demo proof.** Scene A: fabricated “committed as `deadbee`” → contradicted by repo (read-only probe). Scene B: fixture field of 2 — operator **a** = 0 corrective turns, **b** = 2 — `VERIFIED-BY-REPO`, with honest `UNMEASURED_FOR_ORG_CLAIM` (no org-population lift claimed).

**Eligibility (exercised, not imported).** Gemini 3.5+ via Vertex · Google ADK `LlmAgent` constructed on the service path · Google Cloud via Firestore default store + Cloud Run `fleet-wedge`. Probe: `python3 contract/eligibility.py` → 3 OF 3 MET.

**Technologies.** Gemini 3.5 (Vertex) · Google ADK · Cloud Run · Firestore · Python CLI · HTML proof surface · authorship-gated corpus spine.

**Data.** Demo uses in-repo fixtures. Org corpus path is opt-in Claude Code transcripts (Transcripto); population lift is day-two customer data, not claimed on submit.

**Pre-existing code (disclosure).** [transcripto](https://github.com/Morkeeth/transcripto) = corpus spine / authorship gating. Local `agent-claims-inbox` = claim/repo witness patterns + Cloud Run/ADK shell inheritance. Helicon = roadmap memory-truth module (not required for this demo). Product composition in this repo is the submitted wedge.

**Findings.** Mechanism proof on field size 2. Org-population claims stay unmeasured until n≥3. Classifier C1 can flake — do not seal 8/8. The company story is outcome truth, not chat search.

### Spin-up
Already in `README.md` — judges get clone → venv → `fleet_cli.py prove` (no GCP) or ADC + `eligibility.py` for 3/3.

---

## Kill list (say out loud if tempted)

- Second Devpost entry from `agent-claims-inbox`
- Claiming live org lift / hundreds of seats
- `/healthz` in the video
- Sealing classifier accuracy
- Pub/Sub fan-out before this video ships
- Using `PITCH.md` / stale `CLOSE.md` as the write-up

---

## After submit (paste here)

| Field | Value |
|---|---|
| Devpost project URL | |
| YouTube/Vimeo URL | |
| Submitted at (local) | |
| Repo shared with both Google addresses | ☐ |
