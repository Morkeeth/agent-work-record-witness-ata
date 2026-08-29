# Devpost checklist · ATA · Mon 31 Aug 17:00 PDT

**Paste source:** `SUBMISSION-PACK.md` §1 only. Do not mix `docs/SUBMISSION.md` §8 tagline.

---

## Before paste

- [ ] `./film/preflight.sh` green
- [ ] `curl -sS https://fleet-wedge-33kamss2jq-uc.a.run.app/health` — auth, firestore, ADK constructed
- [ ] `python3 contract/eligibility.py` — say **3/3 with ADC** and **1/3 cold** on form or video
- [ ] Repo shared: `testing@devpost.com` + `cloudhackathons@google.com`
- [x] **`architecture.png`** attached (exported 2026-08-29)

---

## Devpost fields

| Field | Value |
|-------|--------|
| Name | THE AGENT WORK RECORD WITNESS |
| Tagline | Run your agents. Check the math. |
| Track | Fortified Enterprise Fleet |
| Live URL | https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/ |
| Repo | https://github.com/Morkeeth/agent-work-record-witness-ata |
| Built with | Python · Google Cloud Run · Firestore · GitHub Actions · Vertex Gemini · ADK |

**What it does / How we built it:** copy from `SUBMISSION-PACK.md` §1 + partner block from
`docs/PARTNER-INTEGRATION-DEEP-DIVE-2026-08-29.md` §8.

---

## Honest bullets (include at least one)

- PR #1 red by design · record `H-a6151a95ac` · `clear: 0`
- Zero non-author installs
- Branch protection off — `verify-claims` is advisory until you require it
- Cold eligibility 1/3 without GCP credentials

---

## Never on Devpost or film

- "Required check" while branch protection off
- "HOLD" as the product name (queue name only)
- Unqualified "3 of 3" eligibility
- GEAP Memory Bank / Registry as shipped

---

## Video ≤4:00

Spine: `SUBMISSION-PACK.md` §2 · voiceover `film/voiceover-vo.txt` · subtitles `film/subtitles.srt`
