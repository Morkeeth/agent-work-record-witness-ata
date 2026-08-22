# NEXT STEPS — read this first, every session
_Kept current 2026-08-22 late evening. If this disagrees with a chat message, open the object._

**PRODUCT:** Org fleet prompt management on transcript corpus — GEAP governs agents; nothing governs prompts. Propagate the *literal* best operator prompt. **All Things Agentic · Aug 31 17:00 PDT.**

## State (measured)

| Probe | Result |
|---|---|
| `python3 contract/eligibility.py` | **3 OF 3 MET** (Gemini Vertex · ADK constructed · Firestore round-trip) |
| `python3 fleet_cli.py wedge` | field of **2** · operator **a** · `VERIFIED-BY-REPO` · `org_claim: UNMEASURED_FOR_ORG_CLAIM` |
| `python3 fleet_cli.py prove` | A **0** vs B **2** corrective · HTML |
| Cloud Run | `https://fleet-wedge-33kamss2jq-uc.a.run.app` · smoke **`/health`** (not `/healthz` — GFE 404) · `POST /prove` · `POST /wedge` |
| Variance | N=5 · **7/8** every run · C1 0% · seal forbidden (`docs/VARIANCE-APPENDIX.md`) |
| Remote | https://github.com/Morkeeth/hack-fleet-ata |

## Column ownership — do not cross
- **Cursor:** `fleet/**` · `fleet_cli.py` · `fixtures/**` · `cloud/**` · `scripts/**` · `tests/**` · `README.md`
- **Claude:** `docs/**` · `surface/**` · `contract/**` · phase files · `PITCH.md` · `CLOSE.md`
- Shared append-only: `CURSOR-LOG.md` · never `git add -A`

## Next (ranked)

1. **Oscar — Gate 1 direction pick** + design owner + hours one-liner
2. **Oscar — one-take video** — `python3 scripts/video_beat_sheet.py` · show Cloud Run console + `/health` + prove delta
3. **Oscar — Devpost submit** — repo (share with testing@devpost.com) · architecture · video · README spin-up
4. **Claude polish** — PITCH/CLOSE against measured state; optional Gate 1 surface after pick
5. **Week 1** — corpus ≥3 operators (org claim gate) per `docs/THIRTY-DAY-PLAN.md`

## Do not
- Re-open Gate 1 directions while Oscar holds the pick
- Seal classifier "8/8" while C1 red
- Ship Pub/Sub fan-out before video (EYES: KILL M2)
- Local Docker / Colima (disk)
- Claim population lift on field of 2
