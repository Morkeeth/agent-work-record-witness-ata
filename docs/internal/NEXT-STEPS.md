# NEXT STEPS — read this first, every session
_Kept current 2026-08-26 evening. If this disagrees with a chat message, open the object._

**PRODUCT:** Org fleet prompt management on transcript corpus — GEAP governs agents; nothing governs prompts. Propagate the *literal* best operator prompt. **All Things Agentic · Aug 31 17:00 PDT.**

**Company brand:** Witness — `~/CODE/fleet-ops/gtm/WITNESS-COMPANY.md`  
**Submit path (Oscar):** [`OSCAR-SUBMIT.md`](OSCAR-SUBMIT.md) + `~/CODE/fleet-ops/gtm/WITNESS-ATA-BEAT-SHEET.md`. Do not paste stale `PITCH.md` / `CLOSE.md`.  
**Orchestrator:** `~/CODE/fleet-ops/gtm/CLAUDE-HANDOVER-WITNESS-2026-08-26.md`

## State (measured)

| Probe | Result |
|---|---|
| `python3 contract/eligibility.py` | **3 OF 3 MET** (Gemini Vertex · ADK constructed · Firestore round-trip) · re-probed **2026-08-26** |
| `python3 fleet_cli.py wedge` | field of **2** · operator **a** · `VERIFIED-BY-REPO` · `org_claim: UNMEASURED_FOR_ORG_CLAIM` |
| `python3 fleet_cli.py prove` / `POST /prove` | A **0** vs B **2** corrective · `VERIFIED-BY-REPO` · HTTP 201 on Cloud Run **2026-08-26** |
| `python3 contract/prove_lift.py` | offline deterministic floor **beats no-signal baseline**: clean held-out#2 **5/8** vs always-DIFFERENT 3/8 (+2) / always-SAME 4/8 (+1) · exit 0 · `docs/DETERMINISTIC-FLOOR.md` |
| Cloud Run | `https://fleet-wedge-33kamss2jq-uc.a.run.app` · smoke **`/health`** (not `/healthz` — GFE 404) · cold start can time out once — retry · `POST /prove` · `POST /wedge` |
| Variance | N=5 · **7/8** every run · C1 0% · seal forbidden (`docs/VARIANCE-APPENDIX.md`) |
| Remote | https://github.com/Morkeeth/hack-fleet-ata · **private** — share with `testing@devpost.com` + `cloudhackathons@google.com` before submit |

## Column ownership — do not cross
- **Cursor:** `fleet/**` · `fleet_cli.py` · `fixtures/**` · `cloud/**` · `scripts/**` · `tests/**` · `README.md` · `OSCAR-SUBMIT.md`
- **Claude:** `docs/**` · `surface/**` · `contract/**` · phase files · `PITCH.md` · `CLOSE.md`
- Shared append-only: `CURSOR-LOG.md` · never `git add -A`

## Next (ranked)

0. **Oscar — one-take video + Devpost** — follow [`OSCAR-SUBMIT.md`](OSCAR-SUBMIT.md) (beats · paste · share repo). Critical path to Aug 31.
1. **Oscar — Gate 1 direction pick** + design owner + hours one-liner (not required for eligibility)
2. **Oscar/Cursor — wire the offline floor** (post-submit OK). `fleet/task_class.classify` no-key fallback is always-SAME stub; `contract/classify_deterministic` should replace it when Gemini absent.
3. **Claude polish** — rewrite PITCH/CLOSE against measured 3/3 + remote (kill stale INELIGIBLE banners)
4. **Week 1** — corpus ≥3 operators (org claim gate) per `docs/THIRTY-DAY-PLAN.md`

## Do not
- Re-open Gate 1 directions while Oscar holds the pick
- Seal classifier "8/8" while C1 red
- Ship Pub/Sub fan-out before video (EYES: KILL M2)
- Local Docker / Colima (disk)
- Claim population lift on field of 2
