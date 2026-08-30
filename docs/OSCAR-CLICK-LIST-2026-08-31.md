# Oscar · click list · Sun 31 Aug 2026

**Submit closes Mon 1 Sep 02:00 CEST (31 Aug 17:00 PDT).** You wake at 11:00 CEST. 15 hours.
Steps are ordered so the slowest thing (video upload) is running while you do the rest.
Every step names its URL and its done-when. Nothing else is in this file.
Evidence for every claim below: [`docs/SHIP-VERIFICATION-2026-08-31.md`](SHIP-VERIFICATION-2026-08-31.md).

---

## 0 · Merge the night branch (2 min)

```
cd ~/CODE/hack-fleet-ata
git fetch origin && git log --oneline main..origin/nightrun/l1-shipprep
git merge --no-ff origin/nightrun/l1-shipprep && git push origin main
```
**Done when:** `git log --oneline -1 main` is the merge commit and
`curl -sI https://raw.githubusercontent.com/Morkeeth/agent-work-record-witness-ata/main/README.md`
returns 200. The branch changes the judge-facing console link in `README.md` and
`SUBMISSION-PACK.md` §5 from `?record=` to `?tab=queue`, adds subtitles, and fixes the
console loop in `surface/hold/index.html`. **Nothing on the branch requires a deploy.**

---

## 1 · Upload the video, unlisted (start this first, it takes longest)

- File: `~/Downloads/ATA-demo-final.mp4` — 3:27.6, 15.8 MB, 1920×1080, under the 4:00 cap.
- URL: https://studio.youtube.com/ → Create → Upload videos → **Visibility: Unlisted**
- Title: `THE AGENT WORK RECORD WITNESS — All Things Agentic`
- Optional captions: `demo/demo-final.srt` (65 cues, built from the spoken script, not by ear).

**Done when:** you can open the watch URL in a private window and it plays. Copy that URL —
step 6 pastes it. Leave the tab open; processing to 1080p can lag the link going live.

---

## 2 · Watch the film end to end, once (3:28)

Nobody has. Two places to have an opinion, both listed with timestamps in
[`docs/SHIP-VERIFICATION-2026-08-31.md`](SHIP-VERIFICATION-2026-08-31.md) §B:

- **2:22–2:55** — the narration names the Google-stack tab, the queue and the 0%-cleared audit;
  the picture stays on the record detail. It is not a narration error and not a cue error: the
  capture ran through `?record=`, so the console kept yanking itself back to the queue. Same bug
  as step 0's fix.
- **2:52** — the Policy panel is on screen for about one second and its Mode box reads
  `report-only`, while the live `/policy` returns `"mode": "enforce"` and the narrator says
  "Enforce mode". The box had not finished loading.

**Done when:** you have said ship-as-is or re-cut. Re-cutting costs a deploy plus a re-capture
(`python3 film/console.py --login` needs your hands) — the honest estimate is 90 minutes and it
puts a fresh, unwatched revision in front of judges. Shipping as-is costs two soft seconds.
**Recommendation: ship as-is.** Every spoken claim was checked against the object and holds.

---

## 3 · Share the repo with the two graders (2 min)

- URL: https://github.com/Morkeeth/agent-work-record-witness-ata/settings/access
- Add `testing@devpost.com` and `cloudhackathons@google.com` as collaborators (read).

**Done when:** both appear under "Manage access" as pending or accepted invitations.
The repo is already public (unauthenticated `curl -sI` → HTTP 200), so this is belt and braces
the rules ask for, not the access path.

---

## 4 · Re-probe the live service (90 seconds, do it after step 0)

```
B=https://fleet-wedge-33kamss2jq-uc.a.run.app
curl -s $B/health | head -20
curl -s $B/policy
for r in /clearance /break-glass /prove /wedge /policy; do
  echo -n "$r "; curl -s -o /dev/null -w '%{http_code}\n' -X POST -d '{}' $B$r; done
```
**Done when:** `/health` shows `auth_required: true`, `store: firestore`, ADK constructed;
`/policy` shows `"mode": "enforce"`; all five POSTs return `401`.
Measured 00:37 CEST today: 5 of 5 were 401, `/demo/seed-hold` was 403, and every read route
returned 200. If any of that has changed overnight, stop and read
[`docs/SHIP-VERIFICATION-2026-08-31.md`](SHIP-VERIFICATION-2026-08-31.md) §C before pasting.

---

## 5 · Seal the prediction (3 min, before the submit button, not after)

- File: `docs/SEALED-PREDICTION-2026-08-29.md`
- Everything is pre-filled except one line. Replace `**OSCAR_ONLY** — timestamp before submit`
  in the *Sealed at* row with the real local time, then commit.

**Done when:** the file has a timestamp and `git log -1 -- docs/SEALED-PREDICTION-2026-08-29.md`
predates your Devpost submit.

---

## 6 · Paste the Devpost form

- URL: https://allthingsagentichackathon.devpost.com/ → Submit / Manage submission
- Paste source: **`SUBMISSION-PACK.md` §1 only.** Field by field, top to bottom.
  Track: **Fortified Enterprise Fleet**.
- Testing instructions field: **`SUBMISSION-PACK.md` §5, stopping at the
  "end of the §5 paste" line.** Everything after that line is an operator note — do not paste it.
- Built with: `SUBMISSION-PACK.md` §6.
- **Long description / "the story" field, if the form has one beyond "What it does":**
  [`docs/THE-THESIS.md`](THE-THESIS.md), whole, top to bottom. One page, written tonight, every
  claim in it carries the evidence it was checked against. It exists so a judge reading one entry
  can see the layer the entry is the first instrument of. If the form has no such field, paste it
  as the last block of "What it does" — never in place of §1's opening, which answers the track
  brief in the track's own words.
- Video URL: the unlisted YouTube link from step 1.
- Architecture image: attach `docs/architecture.png` (784×1247, opened and read today, legible).

**Done when:** every required field is green and the four §5 links open in a private window:
`/hold/#finding`, `/hold/?tab=queue`, `/hold/#stack`, and the repo. All four returned 200 today.

---

## 7 · Submit

- URL: the same Devpost submission page → **Submit**.

**Done when:** Devpost shows the submission as **Submitted** (not draft) and the confirmation
email is in the inbox. Do this before 02:00 CEST, not at 01:55.

---

## Optional, only if steps 0–7 are done and there is an hour left

**Deploy the console fix** so the `?record=` link also behaves.
Runbook: [`docs/REDEPLOY-RUNBOOK-2026-08-29.md`](REDEPLOY-RUNBOOK-2026-08-29.md).
**Done when:** `python3` + headless Chromium on `/hold/?record=H-a6151a95ac` counts **1**
`GET /queue` instead of 41, and a click on "Google stack" leaves `tab-stack` visible.
**Do not start this after 00:00 CEST.** The submission does not need it — step 0 already
removed the loop from every link a judge is given.

---

## Do not, at any point

- Paste "3 of 3" eligibility without the cold "1 of 3" beside it. Both were re-measured today
  and both are true: **3 of 3, exit 0** with ADC; **1 of 3, exit 1** on a fresh clone in a venv
  with `requirements.txt` and no credentials.
- Say "required check" — branch protection is off and `verify-claims` is advisory.
- Shorten the product name, or call it "HOLD".
- Quote a live counter (`/audit` event counts move; `pct_cleared_without_hold` is 0.0 and that
  one is safe to say).
