# Ship verification · 2026-08-31, 23:50 → 01:40 CEST

Everything below was measured tonight against the object — the live service, the public repo
cloned cold, and the bytes of `~/Downloads/ATA-demo-final.mp4`. Nothing here is quoted from
another document in this repo. Where a number appears it carries the command that produced it,
the population it came from, and when it was read.

Reader: a **judge** cloning the repo cold and clicking the four Devpost links, on the clock.

---

# A · Cold stranger pass

Fresh `git clone https://github.com/Morkeeth/agent-work-record-witness-ata` into a scratch dir,
no branch flag, no local config, docs followed literally.

```
BRANCH: main  HEAD: 45b346f
files:      259
git log --all --oneline -- .hold_api_token   ->  (empty, never committed)
git ls-files | grep -iE 'token|secret|key|\.env'  ->  film/numbers.env  (on-camera numbers, no secret)
curl -sI https://github.com/Morkeeth/agent-work-record-witness-ata  ->  HTTP/2 200 (public, unauthenticated)
```

### A1 · BLOCKER — the console link in the README and in Devpost §5 puts the judge in a loop

**Promised** (README "Judge path (60 seconds)", and Devpost testing instruction 2):
open `https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/?record=H-a6151a95ac`.

**Happened.** Headless Chromium against the **live** service, 2026-08-31 00:20 CEST:

```
--- plain console, no ?record ---
  visible section after 6s : ['tab-finding']
  GET counts at end        : {'config': 1}

--- the Devpost testing-instruction link ---
  visible section after 6s : ['tab-queue']
  clicked                  : Google stack
  visible +0.5s after click: ['tab-queue']
  visible +4.5s after click: ['tab-queue']
  GET /queue at 6s         : 21
  GET /queue at 10.5s      : 41
```

Locally, against the identical file with no network latency in the way
(`md5 surface/hold/index.html` == `md5` of the deployed `/hold/` — `ba279717248a51550d540b1bee255fba`,
so this IS the deployed code):

```
=== UNPATCHED main  (port 8795) ===
  GET /queue in first 6s : 5262
  GET /queue after 10.5s : 8352
  visible tab 4s later   : ['tab-queue']   <-- want ['tab-stack']

=== PATCHED worktree (port 8796) ===
  GET /queue in first 6s : 1
  GET /queue after 10.5s : 1
  visible tab 4s later   : ['tab-stack']
```

**Cause**, read in `surface/hold/index.html`: `loadQueue()` re-reads `params.get("record")` on
every call and calls `openClearance()`; `openClearance()` calls `tab("queue")`; `tab("queue")`
calls `loadQueue()`. Unbounded. A judge cannot leave the queue, and Cloud Run takes traffic for
as long as the tab is open.

**Fix, two of them, and they are independent.**
1. *Shipped on this branch, needs no deploy:* the judge-facing links in `README.md` and
   `SUBMISSION-PACK.md` §5 now use `?tab=queue`. Measured live: **1** `GET /queue`, the
   `H-a6151a95ac` card is the **first** card, one click opens the record with
   `Trace · Claude Code session 01Lzbh4XPYTAgCKg1dciFS3Q`, and "Google stack", "Audit",
   "Install" and "Policy" all navigate afterwards.
2. *Shipped on this branch, needs a deploy to reach judges:* a `recordOpened` latch in
   `loadQueue()`, set before the first `await` so a re-entrant call cannot re-fire.

### A2 · COSMETIC — `./demo.sh` prints a verdict legend that reads as a count

`./demo.sh` from the cold clone: **exit 0**, 98 lines, all three gate outcomes real. But under
step 1, which passed every claim, it prints:

```
  exit 0  (0 PASS · 1 BLOCK · 2 HOLD — the exit code IS the verdict)
```

That is the exit-code legend. Read at speed, next to a report that just passed, it looks like
"0 passed, 1 blocked, 2 held". **Fix:** write it as `exit codes: 0=PASS 1=BLOCK 2=HOLD`.

### A3 · COSMETIC — `FLEET_STORE=memory` makes `GET /queue` return 500

`tests/test_auth_gate.sh` runs the gateway with `FLEET_STORE=memory` and never reads the queue,
so nothing catches it. Reproduced locally: `POST /clearance` → 201, then `GET /queue` → **500**.
With `FLEET_STORE=jsonl` the same sequence returns 200 and the hold. No judge path touches
`memory`, so this is not a blocker — but a test store that half-works is the shape this product
exists to catch. **Fix:** either make `memory` a real store or delete the value.

### A5 · BLOCKER for anyone who runs the tests — the security gate can grade the wrong process

`tests/test_auth_gate.sh` is the regression gate for the 2026-08-27 finding that `/wedge` and
`/prove` were unauthenticated. It hard-codes `PORT=8791`. Tonight it printed:

```
  FAIL  anon POST /clearance -> 201 (expected 401)
  FAIL  anon POST /break-glass -> 400 (expected 401)
  FAIL  anon POST /policy -> 200 (expected 401)
  FAIL  anon POST /wedge -> 500 (expected 401)
  FAIL  anon POST /prove -> 500 (expected 401)
```

The code is fine. An orphaned gateway from an earlier session (PID 12395, `auth_required: false`,
`store: jsonl`) was already listening on 8791. The test's own server never bound —
`/tmp/hold_test.log` ends `OSError: [Errno 48] Address already in use` — and the script went on
to probe the orphan and grade it. **The product's own security test reported the product
insecure, about a process that is not the product.** A judge with anything on 8791 sees the same
five FAILs.

**Fixed on this branch.** The script now scans 8791–8830 for a free port, aborts loudly if its
server died, and refuses to continue unless `/health` on that port reports `auth_required: true`
— proof the responses come from its own process. Re-run with the orphan still squatting:

```
  (test gateway pid 11648 on :8792, auth on)
  PASS  anon POST /clearance -> 401      PASS  anon POST /wedge  -> 401
  PASS  anon POST /break-glass -> 401    PASS  anon POST /prove  -> 401
  PASS  anon POST /policy -> 401         PASS  GET /health still 200
  PASS  no file written by an anonymous caller          TEST EXIT=0
```

The orphan on 8791 was **left running deliberately** — it may belong to another live session.
Nothing was killed.

### A6 · Suite state

`python3 -m pytest tests -q` → **25 passed** on `main`, and **25 passed** on this branch's
content unpacked into a plain directory (`git ls-files | tar`, fresh `git init`), together with
`./demo.sh` exit 0 and the hardened auth gate green. Run from inside a git *worktree*,
`tests/test_hard_wedge.py::test_a_sha_in_a_sibling_repo_is_not_a_false_claim` fails, because it
takes the repo's parent directory as a stand-in for "another repo" and a worktree's parent is
`.worktrees`. Cosmetic, and only visible to someone working in a worktree.

### A4 · Stale pointer — `docs/DEVPOST-CHECKLIST.md` names the wrong narration file

It says the video spine is `film/voiceover-vo.txt` and `film/subtitles.srt`. Those are the
**3:15 cut's** eight-line script. The shipped 3:27.6 film speaks `demo/voiceover.txt` — a
different, longer script. Anyone rehearsing from the checklist rehearses the wrong film.

---

# B · The film — first end-to-end check anyone has run on it

`~/Downloads/ATA-demo-final.mp4` is **byte-identical** to `demo/demo-final.mp4`
(`cmp` clean, md5 `3147f34484886a83161f585d5084da44`). 207.63 s = **3:27.6**, 1920×1080 h264,
audio 205.1 s aac, 15,797,684 bytes. Under the 4:00 cap with 32 seconds to spare.

## B1 · There IS a local speech-to-text path, and it was used

`which whisper` fails, which is why nobody found it. But `whisper-cli` (whisper.cpp, Metal) is on
`PATH` from Homebrew, and Recall already downloaded the weights:
`~/CODE/recall/.cache/models/ggml-small.bin`, 487 MB, present since 2026-07-15.
The film's audio was decoded to 16 kHz mono and transcribed **locally, offline, free**, in 24.8 s:

```
ffmpeg -i ~/Downloads/ATA-demo-final.mp4 -ar 16000 -ac 1 film.wav
whisper-cli -m ~/CODE/recall/.cache/models/ggml-small.bin -f film.wav -otxt -ovtt --language en
```

The transcript matches `demo/voiceover.txt` sentence for sentence. Every divergence is an ASR
mishearing of a correct script (`deadby`←deadbee, `UIL`←URL, `FOSS mode`←enforce mode,
`red access`←read access, `a center one`←us-central-one, `GitCat file`←git cat-file). No
sentence in the audio is absent from the script and no script sentence is missing from the audio.

## B2 · Never-say list — clean, in the audio and on the screen

| Rule | Result |
|---|---|
| `42%` anywhere | **absent from the audio.** The spoken pair is "forty one point seven percent" at **1:58** and "eight point one percent" at **2:04–2:11** — six seconds apart, one paragraph, cause stated in between ("that number was wrong, and the error was ours"). |
| `42%` on screen | **absent.** The finding tab at **2:02** shows `RAW 247 sha claims 103 disagree 41.7%` directly above `CORRECTED 236 sha claims 19 disagree 8.1%`. The two numbers are never apart. |
| Short form of the product name | **absent.** Said in full twice: "This is the Agent Work Record Witness" at **1:46**, "The Agent Work Record Witness" at **3:21**. No "Witness" alone, no "ATA", no "hack-fleet-ata". |
| "HOLD" as the product | **absent.** "held", "the queue", "it is held, not guessed" — the verdict and the queue, never the name. |

## B3 · Every checkable spoken claim, checked against the object

| Spoken, at | Claim | Probed | Verdict |
|---|---|---|---|
| 1:16 | "with credentials it prints three of three and exits zero" | `python3 contract/eligibility.py` with ADC | **TRUE** — `3 OF 3 MET`, `EXIT=0`, req 3 proof `round-trip hit FirestoreStore, 61 records` |
| 1:20 | "cold, with no credentials, it prints one of three and exits one" | fresh clone, new venv, `pip install -r requirements.txt`, `HOME` without `~/.config/keys/gemini.key`, `CLOUDSDK_CONFIG=/nonexistent` | **TRUE** — `1 OF 3 MET` (ADK only), `EXIT=1` |
| 2:53 | "enforce mode, scoped to pull requests an agent actually opened" | `curl -s $B/policy` | **TRUE** — `{"mode":"enforce","agent_only":true,"label":"agent","break_glass_role":"break-glass"}` |
| 2:33 | "zero percent cleared" | `curl -s $B/audit` | **TRUE** — `pct_cleared_without_hold: 0.0` over 36 events (24 prove, 9 clearance/HOLD, 2 exception, 1 agent_run) |
| 3:01 | "one real agent pull request went through the gate… it is held" | `/audit` and PR #1 | **TRUE** — clearance `H-a6151a95ac`, `source=github-action`, session `01Lzbh4XPYTAgCKg1dciFS3Q` |
| 2:04 | "seventy three of a hundred and three were real commits in a sibling repository" | the finding tab renders `73 resolved in a SIBLING repo` | **TRUE on screen** |

> Care taken, and worth repeating: the first cold eligibility run on this machine printed
> **2 of 3**, which would have made the film wrong. It was contamination —
> `contract/gemini_impl.py` falls back to `~/.config/keys/gemini.key`, which exists on Oscar's
> disk and on no judge's. Stripping it produced the 1 of 3 the film claims. A finding written
> from the first run would itself have been the error this product exists to catch.

## B4 · Picture against words — the claim in commit `d7a6e11` re-derived, not inherited

Frames pulled at 1 fps by sequential decode (`-vf fps=1`, frame *N* = second *N*; keyframe
seeking with `-ss` was checked and rejected as it snaps and lies). Every frame looked at.

Verified in sync: 0:00 title slide · 0:10 "Seats and spend are visible" · 0:20 "Nothing checks
the sentence" with `deadbee` in blue · 0:30 terminal BLOCK on deadbee · 1:37 Cloud Run console,
`fleet-wedge`, us-central1, live request graph · 1:53–2:11 the finding tab with 41.7 and 8.1
together · 2:11 the record with `Trace · Claude Code session …` · 3:00–3:16 GitHub PR #1 and the
red `verify-claims` run · 3:17 the closing slide.

**Out of sync, one window: 2:22 → 2:52.** The narration names the Google-stack tab, then the
queue, then the exportable append-only record at 0% cleared, then the install path. The picture
shows the record detail throughout, with the queue appearing at **2:23** and **2:51** for about a
second each, and the Policy panel for about a second at **2:52**.

**This is not a cue error and not a narration error.** `film/browser.py` drives the console
through `?record=H-a6151a95ac` — finding A1. Every tab it clicked was undone within a second by
the loop. The cue table in `film/lay_voice.py` is right about where each beat *should* land; the
page would not stay put. Deploy the A1 fix and re-run `film/browser.py` and the picture becomes
what the narration already describes.

**One more thing to know at 2:52:** the Policy panel's Mode box reads `report-only` in the frame
that survives. `<option value="report-only">` is the first option and `loadPolicy()` overwrites
it from `GET /policy` a moment later — the panel vanished before it finished. The live policy is
`enforce`, so the narrator is right and the box is stale.

**Verdict: no re-render.** The standing rule is to re-cut only for a real defect. Every spoken
claim holds against the object and the never-say list is clean. The picture window is a symptom
of A1 and closes when A1 is deployed — which is a judgement call about putting an unwatched
revision in front of judges 14 hours before the deadline, not a defect in the audio.
`~/Downloads/ATA-demo-final.mp4` is untouched; nothing was overwritten.

## B5 · `film/build.sh` does not rebuild the shipped film

It concatenates `seg-terminal + seg-console + seg-browser` and writes no intro or outro.
The shipped 207.63 s cut is:

| Segment | Duration | Starts at |
|---|---|---|
| `demo/seg-intro.mp4` (slides 1–3) | 25.00 s | 0:00 |
| `demo/seg-terminal.mp4` | 62.32 s | 0:25 |
| `demo/seg-console-trim.mp4` | 26.07 s | 1:27 |
| `demo/seg-browser.mp4` | 84.17 s | 1:53 |
| `demo/seg-outro.mp4` (slide 4) | 10.00 s | 3:17 |
| | **207.56 s** | (file: 207.63 s) |

Derived, not read from a note: 25 + 62.32 = 87.32 s, and `lay_voice.py`'s cue 8 comment says the
Cloud Run console lands at 87.3 s. `demo/segments.txt` names only two of the five. Anyone who
runs `./film/build.sh` today gets a different, shorter film with no slides.

## B6 · Subtitles now exist for the cut that shipped

`film/make_srt.py` → `demo/demo-final.srt`, 65 cues, last ends 3:25.1. Text comes from
`demo/voiceover.txt` and timing from `film/lay_voice.py`'s cue table plus the measured duration
of each `demo/.vo-parts/pNN.mp3` — one cue table, no second copy. Spot-checked against the
whisper transcript: cue 1 at 0.8 s "Run your agents." against ASR 0:00–0:04, cue 3 at 5.0 s
"Every company running AI agents can see two things." against ASR 0:04–0:07.

---

# C · Submission pack, field by field

## C1 · §Live probe receipt — every row re-probed 2026-08-31 00:37 CEST

| Probe | Pack says | Measured | |
|---|---|---|---|
| `GET /health` | auth_required true · demo_seed false · firestore · ADK | exactly that, plus `ever_invoked: true` | ✅ |
| `GET /hold/` | 200 | 200, 41,516 bytes | ✅ |
| `GET /audit/export` | JSON download | 200 `application/json`, 21,345 bytes | ✅ |
| anon `POST /clearance` | 401 | 401 | ✅ |
| anon `POST /break-glass` | 401 | 401 | ✅ |
| anon `POST /prove` | 401 | 401 | ✅ |
| `POST /demo/seed-hold` | 403 | 403 | ✅ |
| eligibility with ADC | 3 OF 3, exit 0 | 3 OF 3, exit 0 | ✅ |
| eligibility cold | 1 OF 3, exit 1 | 1 OF 3, exit 1 (venv, no key, no ADC) | ✅ |

The pack lists three mutating routes. There are **five**: `/wedge` and `/policy` are also
POST-mutating and both also returned **401**. The claim "every mutating route 401 anon" is true
at **5 of 5**, not 3 of 3, and it is stronger than the pack states.

Reads all open as designed: `/health` `/policy` `/audit` `/audit/export` `/queue` `/hold/`
`/config` → 200, 7 of 7.

## C2 · §1 Devpost paste

- Project name, tagline, track, hosted URL, repo URL: all present, no placeholder.
  `grep -nE 'TODO|FIXME|XXX|TBD|<[A-Z_]{3,}>|PLACEHOLDER|YOUR_'` over `SUBMISSION-PACK.md`,
  `README.md` and `docs/SEALED-PREDICTION-2026-08-29.md` → **no matches. Nothing to warn about.**
- "78,618 … 144,306 sit in the corpus" — both numbers travel together in the paste, and the
  console renders the same pair. ✅
- "41.7% … Corrected: 8.1% (19/236)" — the console's finding tab renders
  `RAW 247 sha claims 103 disagree 41.7%` and `CORRECTED 236 sha claims 19 disagree 8.1%`.
  19/236 ✅.
- "the repo is public" ✅ (`curl -sI` unauthenticated → 200).
- **Missing field, and it is required:** the pack has no **video URL** row and
  `docs/DEVPOST-CHECKLIST.md` has none either. Devpost will ask for a hosted link; the film is a
  local mp4. That upload is step 1 of the click list because it is the long pole.

## C3 · §5 Testing instructions

Four links, all 200 today. Link 2 changed from `?record=H-a6151a95ac` to `?tab=queue` — see A1.
Links 1 and 3 use hash routing and were confirmed to boot on the right tab with **one** request.
An operator note now sits after an explicit "end of the §5 paste" line so the loop explanation
cannot be pasted into a judge-facing field by accident.

## C4 · §6 Built with

`google-cloud-run` `firestore` `vertex-ai` `gemini-3.5-flash-lite` `google-adk` `secret-manager`
`github-actions` `python`. Each one is exercised on a path checked above, except **secret-manager**,
which is asserted in prose ("held in Secret Manager and mounted to the service") and is the one
row here with no probe in this document. Everything else has a command beside it.

## C5 · `docs/architecture.png`

Present, 112 KB, PNG 784×1247 RGBA, exported 2026-08-29. **Opened and read tonight**, not just
stat'd: it renders the record-first story — agent PR → verify-claims (labelled *advisory today ·
'required' is roadmap*) → `outcome_gate.py` → survives? → `POST /clearance` → the yellow
**THE RECORD · this is the product** box holding Cloud Run, Firestore, the console, the export,
break-glass and the join back to the session; Transcripto is drawn outside it and labelled
*ROADMAP — not in this submission*. Legible at full size. Nothing in it is a claim the rest of
this document contradicts.

---

# D · What is NOT verified

- **Nobody has listened to the film with human ears.** Machine transcription proves the words;
  it says nothing about pace, level, or whether the two long silences (6.2 s at 1:22, 5.0 s at
  2:35, both deliberate per the cue comments) feel like dead air. That is step 2 of the click list.
- **Secret Manager** — asserted in the pack, not probed here.
- **The deployed revision as a whole.** `surface/hold/index.html` was confirmed byte-identical to
  `main`; the Python behind it was exercised through its HTTP surface only.
- **A judge's actual browser.** All console measurements used headless Chromium.
