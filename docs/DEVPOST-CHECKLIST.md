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

**Shipped cut:** `demo/demo-final.mp4` = `~/Downloads/ATA-demo-final.mp4` (byte-identical,
md5 `3147f34484886a83161f585d5084da44`), **3:27.6**, 1920×1080, 15.8 MB.
Spoken script: **`demo/voiceover.txt`** · subtitles: **`demo/demo-final.srt`** (65 cues).

`film/voiceover-vo.txt` and `film/subtitles.srt` belong to the **older 3:15 cut** and are not
what this film says. Do not rehearse from them.

- [ ] **Upload to YouTube, PUBLIC (not unlisted), and paste the watch URL into the Devpost video field.**
      **Corrected 2026-08-31 04:50 UTC.** This line said *unlisted*. The rules say the submission
      *"must be uploaded to and made publicly visible on YouTube or Vimeo"*, and the same page writes
      *"must be public (not unlisted)"* elsewhere. Unlisted is a Stage-One eligibility risk.
      Devpost wants a hosted link, not a file. This is the long pole — start it first.
