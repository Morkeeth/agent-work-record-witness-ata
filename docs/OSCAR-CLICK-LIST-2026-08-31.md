# Oscar · the morning list · Mon 31 Aug 2026

**Devpost closes Mon 1 Sep 02:00 CEST (31 Aug 17:00 PDT).** You read this at 11:00. **~15 hours.**
Ordered by what blocks what. Every step carries its URL, its done-when as a **command**, and how
long it takes. There is **one** ruling for you in here, and it is 30 seconds.

---

## The one sentence

**Deploy is not polish. It is the difference between the product and the URL you hand a judge.**

If you submit without deploying, this is what a judge opens — measured this morning in a real
browser at real viewport widths (`document.documentElement.clientWidth` read inside the page, not
a cropped screenshot):

| `…/hold/?tab=queue` | live today (`sha 47f5c107`) | after deploy (`sha 12e0db09`) |
|---|---|---|
| Hold cards **fully readable** at 1440 | **1 of 7** | **7 of 7** |
| Hold cards **fully readable** at 390 | **0 of 7** | **7 of 7** |
| Cards **not rendered at all** | 5 at 1440 · 6 at 390 | 0 |
| A line saying seven exist | **absent** | `7 releases on hold, all shown below.` |
| Scroll affordance to reach the rest | **none** — `overflow-x: hidden`, `scrollWidth 3982` vs `clientWidth 910` | not needed |

Plus four things the live console gets wrong that the branch fixes:

1. It prints **a git commit sha as a Claude Code session id** and mints a dead `claude.ai` link
   from it, on 2 of the 7 holds.
2. It mints `https://github.com/Morkeeth/hack-fleet-ata/pull/phase-a` — **probed today: 404** —
   from a hold whose `pr` field says `phase-a`.
3. It says the record is **append-only and "nothing is edited in place."** `cloud/store.py:66`
   says the opposite in words, and `cloud/service.py:468` does the opposite in code.
4. It says `HOLD_API_TOKEN` is a **plaintext environment variable** and Secret Manager is
   **"enabled and unused."** Probed 02:44 UTC today: the live revision mounts it from
   `hold-api-token:latest`. That one is false in the direction nobody audits — it *under-claims*
   a real Google Cloud integration in a track scored 30% on architecture.

All three are the failure this product is named after, on this product's own console.

---

## 0 · Start the video upload (5 min of clicks, then it runs by itself)

Do this **first** and leave the tab open — it is the only thing with a queue in front of it.

- File: `~/Downloads/ATA-demo-final.mp4` — 3:27.6, 15.8 MB, 1920×1080, under the 4:00 cap.
- https://studio.youtube.com/ → Create → Upload videos → **Visibility: Unlisted**
- Title: `THE AGENT WORK RECORD WITNESS — All Things Agentic`
- Captions (optional): `demo/demo-final.srt`, 65 cues.

**Done when:** the watch URL plays in a private window. Step 8 pastes it.

---

## 1 · Merge the night branch (2 min) — this blocks the deploy

```
cd ~/CODE/hack-fleet-ata
git fetch origin
git log --oneline main..origin/nightrun/l1-shipprep
git merge --no-ff origin/nightrun/l1-shipprep && git push origin main
```

The `git log` line above prints the exact set — don't trust a count written the night before;
this note has already gone stale three times. Wave 4's substantive commits, newest first:

| | |
|---|---|
| *(adversarial pass)* | the Audit tab said **"Append-only clearance decisions"** — the same page's own Google-stack row says the opposite, 131 lines up. Fixed, plus the thesis's six-of-eleven. **This is why the target sha below is `12e0db09` and not `5d62eeb9`** |
| `f9cabc3` | the morning list leads with deploy, and the night's log carries every command |
| `779463c` | the console's own security posture was stale, and it under-claimed a Google service |
| `2161f19` | receipt for the repository count |
| `6bfdcf4` | "across 40 repositories" was never measured. It is 74 |
| `a5ec00c` | the record is not append-only, and the console said it was |

**Done when:**

```
git log --oneline -1 main            # the merge commit
shasum -a 256 surface/hold/index.html
# must print 12e0db0982ed91c53c0c0c9ae9e492482bb536b83bfde2f68939f5c032e99eec
```

---

## 2 · DEPLOY (10–15 min, most of it Cloud Build waiting)

```
cd ~/CODE/hack-fleet-ata
bash scripts/deploy_cloud_run.sh
```

Needs `HOLD_API_TOKEN` in the environment **or** `.hold_api_token` in the repo root (gitignored);
the script exits 1 with a named error if neither is there. Project `hack-fleet`, region
`us-central1`, service `fleet-wedge`. Cloud Build — no local Docker.

**Done when — this exact command returns this exact string:**

```
curl -s https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/ | shasum -a 256
```
```
12e0db0982ed91c53c0c0c9ae9e492482bb536b83bfde2f68939f5c032e99eec
```

**It returns `47f5c107918deeece6f5c5f62280918d2d34d751205187274c017befb3f1a49d` right now**
(read 02:42 UTC, and again at **03:10 UTC** by the adversarial pass — unchanged). If it still says `47f5c107…`, the deploy did not land and everything in
"The one sentence" above is still what a judge sees. Nothing else in this list depends on it, so
if the deploy fights you, **park it and keep going** — an undeployed submission is still a
submission, and a missed deadline is not.

Second check, because the deploy also re-provisions the secret:

```
curl -s https://fleet-wedge-33kamss2jq-uc.a.run.app/health | grep -o '"store": "[a-z]*"'
# "store": "firestore"
```

---

## 3 · Watch the film once, end to end (3:28) — and rule on it

Nobody has heard it with human ears. Machine transcription proved the words; it says nothing about
pace or level. **Three places to have an opinion, all timestamped:**

| Time | What | Cost of caring |
|---|---|---|
| **1:40** and **2:28** | The narration says **"append only"** twice (`demo/demo-final.srt` cues **33** and **47** — 65 cues in the file; 131/187 were the grep *line* numbers). Every *text* surface now says the true thing — *"a keyed store, not an append-only log"* — because closing a hold rewrites that clearance in place. The film cannot be edited without a re-cut. | Re-cut = deploy + re-capture + re-record ≈ 90 min, and it puts an unwatched revision in front of judges |
| **2:22–2:52** | Narration names the Google-stack tab, the queue and the 0%-cleared audit; the picture stays on the record detail. Cause was the `?record=` console loop, now fixed | Re-capture, same 90 min |
| **2:52** | The Policy panel is on screen ~1 s and its Mode box reads `report-only` while live `/policy` returns `"mode": "enforce"` and the narrator says "Enforce mode". The box had not finished loading | Same |

**Recommendation: ship as-is.** On the "append only" line specifically: a judge who hears it and
then reads the console — which now says *"Keyed store, not an append-only log … Said here rather
than found"* — sees a product correcting itself in public, which is the thesis. A judge who hears
it and reads nothing loses nothing. Neither outcome is worth 90 minutes and an unwatched cut
fifteen hours out.

**Done when:** you have said ship-as-is or re-cut.

---

## 4 · THE ONE RULING · writer-side session validation

**The question.** `make_clearance_record` (`cloud/hold_api.py:131`) accepts **any string** as a
session id. Do we tighten it now, or after the deadline?

**Evidence for tightening now.** It is how commit shas got into the session field: 2 of the 7 live
holds carry a 40-hex sha there, and `git cat-file -t` resolves both to real commits in this repo.
Untreated, the console printed `Claude Code session c2b1ad98…` and minted a dead claude.ai link
from it — one value labelled as two different objects, three lines apart.

**Evidence against tightening now.** Three tests **pin the permissiveness**, so the change is a
contract change, not a bug fix:

```
tests/test_partner_p1_p2.py:59   "explicit session-id wins over head_sha"  (session_id="TRANSCRIPT99")
tests/test_partner_p1_p2.py:66-68   make_clearance_record(session="abc123deadbeef",
                                                          head_sha="abc123deadbeef")
```

Line 66-68 constructs a record with **the identical value in both fields** — the fixture already
encodes the exact defect found in production and never asserts it is wrong. Tightening the writer
breaks all three, and what they encode ("any explicit session beats head_sha") is a decision, not
an accident.

**Recommendation: POST-DEADLINE. The renderer fix is sufficient for the submission**, for one
reason that a writer-side fix cannot match: **the seven bad records are already in Firestore.**
Only the renderer repairs what is already stored. A writer guard changes nothing a judge can see
today, and rewriting prod records is a write to prod. Verified this morning — all 7 live holds,
rendered at 1440 and 390:

| hold | `session` | what a judge reads |
|---|---|---|
| `H-a6151a95ac`, `H-57b130f397` | `01Lzbh4XPYTAgCKg1dciFS3Q` | real session, link live, sign-in wall named before **and** inside the link label |
| `H-ae0a3e064a`, `H-196e41b823` | 40-hex sha (`session == head_sha`, checked on both) | **no link** — "that is not a session id — it is this record's own commit sha, repeated into the wrong field" |
| `H-89d3746a0d` | `TESTP1RUN` | **no link** — shown, not followed. Test data, but rendered honestly |
| `H-d164970cb4`, `H-0664568267` | absent | "no session reference in the report. This claim cannot be opened back to what the agent actually did." |

`TESTP1RUN` is still test data sitting on a judge surface. Removing it is a **prod write** — your
click, and not worth it today: the console tells the truth about it.

**Cost of not deciding: zero before the deadline.** The renderer guards every case. This ruling
only decides what happens to the writer next week.

---

## 5 · Share the repo with the two graders (2 min)

- https://github.com/Morkeeth/agent-work-record-witness-ata/settings/access
- Add `testing@devpost.com` and `cloudhackathons@google.com` (read).

**Done when:** both show under "Manage access". The repo is already public, so this is the belt
and braces the rules ask for, not the access path.

---

## 6 · Re-probe the live service (90 seconds, after step 2)

```
B=https://fleet-wedge-33kamss2jq-uc.a.run.app
curl -s $B/health
curl -s $B/policy
for r in /clearance /break-glass /prove /wedge /policy; do
  echo -n "$r "; curl -s -o /dev/null -w '%{http_code}\n' -X POST -d '{}' $B$r; done
```

**Done when:** `/health` shows `auth_required: true`, `demo_seed_enabled: false`,
`store: firestore`, ADK class constructed; `/policy` shows `"mode": "enforce"`; **all five POSTs
return 401.** Read at 02:22 UTC today: exactly that, `/demo/seed-hold` 403, every read route 200,
`pct_cleared_without_hold` **0.0** over 36 events.

---

## 7 · Seal the prediction (3 min — before the submit button, not after)

`docs/SEALED-PREDICTION-2026-08-29.md`: replace `**OSCAR_ONLY** — timestamp before submit` in the
*Sealed at* row with the real local time, then commit.

**Done when:** `git log -1 -- docs/SEALED-PREDICTION-2026-08-29.md` predates your Devpost submit.

---

## 8 · Paste the Devpost form (20 min)

https://allthingsagentichackathon.devpost.com/ → Submit / Manage submission ·
Track: **Fortified Enterprise Fleet**

| Field | Paste from |
|---|---|
| Everything except the two below | **`SUBMISSION-PACK.md` §1**, field by field, top to bottom |
| Testing instructions | **`SUBMISSION-PACK.md` §5**, stopping at the *"end of the §5 paste"* line. Everything after it is an operator note |
| Built with | `SUBMISSION-PACK.md` §6 |
| Long description / "the story" | **`docs/THE-THESIS.md`**, whole. If the form has no such field, append it to "What it does" — never in place of §1's opening, which answers the track brief in the track's own words |
| Video URL | the unlisted YouTube link from step 0 |
| Architecture image | attach `docs/architecture.png` — 784×1247, 112,086 bytes, opened and read |

**Done when:** every required field is green and these four open in a private window:
`/hold/#finding`, `/hold/?tab=queue`, `/hold/#stack`, and the repo.

---

## 9 · Submit

Same page → **Submit**. **Done when:** Devpost shows **Submitted**, not draft, and the
confirmation email has arrived. Do this before 02:00 CEST, not at 01:55.

---

## Do not, at any point

- **Paste "3 of 3" eligibility without the cold "1 of 3" beside it.** Both re-measured this
  morning: **3 OF 3, exit 0** with ADC; **1 OF 3, exit 1** in a credential-stripped shell.
- Say "required check" — branch protection is off and `verify-claims` is advisory.
- Say the record is **append-only**. It is a keyed store: the API never deletes, but closing a
  hold rewrites that clearance in place. Every text surface now says so.
- Say the token is a **plaintext env var**. It is mounted from Secret Manager
  (`hold-api-token:latest`) on live revision `fleet-wedge-00014-q2g` — probed 02:44 UTC today.
  The console claimed the opposite until this morning.
- Shorten the product name, or call it "HOLD".
- Quote a live counter. `/audit` event counts move; `pct_cleared_without_hold` is 0.0 and that one
  is safe to say.

---

## What was open last night and is now closed

| | |
|---|---|
| `contract/eligibility.py` printed `NOT MET 1.` with a **blank reason** cold | Fixed. Now: *"no model answered — classify() returned UNMEASURED after FileNotFoundError"*. Both arms re-run and pasted in `NIGHTRUN-2026-08-31.md` |
| **"across 40 repositories"** — was a ruling for you | **Settled, not ruled.** The frozen corpus was reconstructed by timestamp and reproduces the artifact on three fields exactly; the answer is **74**. Receipt: `docs/CORPUS-REPO-COUNT-RECEIPT-2026-08-31.md`. Revert if you disagree: `git revert 6bfdcf4` |
| Secret Manager — "asserted in the pack, not probed" | Probed. The pack was right and the console was wrong |
| **Found by the adversarial pass, after the list above was written** | `surface/hold/index.html:509` still read *"Append-only clearance decisions."* on the **Audit tab** — while line 378 of the same file said *"Keyed store, not an append-only log"*. The **Do not** list above, claiming "every text surface now says so", was false when it was written. Fixed; it is true now. Re-verified: `grep -niI "append.only" surface/hold/index.html` returns two lines, both the correcting form |
| Same pass | `docs/THE-THESIS.md` (the Devpost long description) said *"Eleven more were shas inside shell commands, **six of them** our own test fixture"*. The only receipted six is **6 of the hand-labelled 40**, not a subset of the 11 — `gate/corpus_scan.py:16-17`, and `docs/ENTERPRISE-CASE-2026-08-27.md:48` keeps the hedge *"across the sample"* that the thesis had dropped. Rewritten to say the sample figure and name it as one |
| Same pass | Step 3's film row cited *"cues 131, 187"* of a file with **65 cues** — those were grep *line* numbers. Real cues are **33** and **47**; the timestamps 1:40 / 2:28 were correct |
