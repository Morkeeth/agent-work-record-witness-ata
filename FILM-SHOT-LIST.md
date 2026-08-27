# Film shot list — eight shots, every output pasted from a real run

**Rule for this document: nothing illustrative.** Every block below was executed and its output
pasted. Where a shot could not be verified, it says so in bold instead of showing a plausible line.

**Verified by T3 on 2026-08-27.** Commands run from a **cold clone of the public repo**
(`git clone https://github.com/Morkeeth/agent-work-record-witness-ata`) into a clean venv, not from
the working tree, unless a shot says otherwise.

---

## Before you press record — four checks, two minutes

| Check | Command | Must show |
|---|---|---|
| The clone a judge gets is current | `git ls-remote origin HEAD` | matches your local `main` |
| The page opens from disk | `open surface/fleet-report-page.html` | claims rows render, not a blank list |
| The service is up | `curl -s $URL/health` | `auth_required: true` |
| The gate is installed | `witness --help` | usage, not `command not found` |

> **⚠ Two things that are true right now and will be visible on camera.**
> 1. **The deployed service still returns `"product": "HOLD"`.** The rename to
>    THE AGENT WORK RECORD WITNESS is committed in `cloud/service.py` and **not deployed**.
>    Either redeploy before filming, or do not linger on the `/health` body in shot 5.
> 2. **The public clone is behind local `main`.** A judge cloning today gets `dd9800b`.
>    The push is the coordinator's, and it must land before this is filmed.
> 3. **`surface/fleet-report-page.html` in the repo is the PRE-REWIRE build.** The template
>    `fleet-report.html` now reads `witness-corpus`'s fields and shows RAW beside CORRECTED; the
>    openable page was generated before that and still shows the old single number (hero reads
>    `53`, not `8.1%`). **It renders — 43 rows, receipts work — it is just the wrong version.**
>    Regenerating it is one command once the scan finishes:
>    `witness-corpus --db ~/.trace/trace.db --code-root ~/CODE --json > surface/witness-corpus.json`
>    then re-inline into the template. **Do not film shot 3 off the committed page until this is done.**

---

## Shot 1 · Week zero — measure before you install anything

**Say:** *"Before it changes anything, it tells you what your fleet already claimed."*

```bash
pip install .            # or: python3 -m gate.corpus_scan
witness-corpus --db ~/.trace/trace.db --code-root ~/CODE
```

**⚠ NOT VERIFIED IN THIS PASS.** The full run takes longer than the window I had; it was still
executing when this list was written. **Run it once end to end before filming and paste the real
block here.** The two numbers that must appear on screen are the examined count *and* the corpus
total, because quoting only the larger one is the defect this tool reports in others.

---

## Shot 2 · The gap — RAW beside CORRECTED

**Say:** *"Our first number said agents are wrong 41.7% of the time. That was our probe, not them."*

The same `witness-corpus` output carries both lines. **Both stay on screen together.** The point
is not the corrected number; it is that the entire gap was ours — a probe aimed at the wrong
repository, machinery counted as prose, and our own fixtures scored as claims.

**⚠ Depends on shot 1. Paste the real RAW/CORRECTED lines here after the run.**

---

## Shot 3 · The receipt — the one thing nobody else does

**Say:** *"Every number on this page opens to the command that produced it."*

```bash
open surface/fleet-report-page.html
```

Click one row. It opens to three lines:

```
BLOCK   wrote PITCH.md                                    Datahubhack-jt
        $ stat PITCH.md
        → NO SUCH PATH in the repo
```

**That is the whole argument.** Observability products show a score you have to trust. This shows
the probe. **Do not narrate over it — let it sit.**

The page is self-contained: data is inlined at generation, so it opens from disk with no server.
*(An earlier draft fetched its JSON and rendered blank from `file://` — caught by rendering it.)*

**⚠ The committed page is the pre-rewire build — see warning 3 at the top.** It renders correctly
(43 rows, receipts open) but shows the old hero number instead of RAW beside CORRECTED. Regenerate
before filming.

**Verified: renders at 1440 with 43 rows.** **390px is UNVERIFIED** — headless Chrome clamps its
layout viewport to 500px, so a true phone render was never produced. At 500px `scrollWidth ==
innerWidth`, so there is no overflow. **If you film a phone, check it first.**

---

## Shot 4 · The gate — no GitHub, no account, no credentials

**Say:** *"Three states, not two. It refuses rather than guesses."*

All three run from the cold clone. **Output below is verbatim.**

**4a — a false claim blocks.**
```
$ printf 'Fixed the race. Committed as deadbee. Wrote docs/auth.md.' | witness

  BLOCK         committed as deadbee
                probe: git cat-file -t deadbee  ->  NOT a commit in this repo
  BLOCK         wrote docs/auth.md
                probe: stat docs/auth.md  ->  NO SUCH PATH in the repo
--------------------------------------------------------------------------
  GATE: BLOCK — 2 claim(s) the repo disproves. Do not auto-merge.
exit 1
```

**4b — a true claim passes.**
```
$ printf 'Wrote README.md.' | witness

  PASS          wrote README.md
                probe: stat README.md  ->  exists
  GATE: PASS — every claim confirmed against the repo.
exit 0
```

**4c — a test claim is refused, not guessed.** *This is the beat that separates it from a linter.*
```
$ printf 'All 214 tests pass.' | witness

  UNVERIFIABLE  tests pass
                probe: no probe  ->  a test claim needs the suite RUN; this gate never
                executes a command lifted from a report — verify via the CI outcome,
                not the word
  GATE: HOLD — nothing disproved, but a claim is unverifiable.
exit 2
```

**Exit codes are the verdict, not an error channel: 0 PASS · 1 BLOCK · 2 HOLD.** Verified.

---

## Shot 5 · The record and the export

**Say:** *"The gate is a moment. The record is the product."*

**5a — the service is live and gated.** Verified 2026-08-27:
```
$ curl -s $URL/health
  auth_required   : true
  demo_seed_enabled: false
  store           : firestore
  agent           : {"class": "...LlmAgent", "constructed": true,
                     "invoked": false, "last_run": "never invoked in this process"}
```
> **Say `constructed`, not `invoked`.** A fresh container honestly reports `invoked: false` until
> something calls `POST /agent/run`. **A receipt that says "never invoked" is the point** — do not
> claim a run that has not happened in that process.
> **And see the warning at the top: this body still says `"product": "HOLD"` until redeployed.**

**5b — the queue.** Verified: `calm: false · count: 2`.
**5c — the export.** Verified: `GET /audit/export` → **7 events**, `exported_at` stamped.
**5d — writes are gated.** Verified: anonymous `POST /break-glass` → **HTTP 401**.
**5e — the console.** Verified: `GET /hold/` → **HTTP 200**.

**⚠ THE BREAK-GLASS WRITE IS NOT PRE-RUN, DELIBERATELY.** Performing it now would put a fake
override with a fake reason into the production record that shot 5c exports on camera. **Oscar
performs it live, once, with a real reason.** The token comes from `.hold_api_token`.

---

## Shot 6 · The four self-catches — the closing shot, not a footnote

**Say:** *"Every one of these was caught by this tool, on us, this week."*

Each is a real commit. `git show <sha>` on camera if you want the receipt.

| # | Catch | Commit |
|---|---|---|
| 1 | **The probe was aimed at the wrong repository.** "42% of agent commit claims are wrong" was two artifacts, not a finding. | `638bae7` |
| 2 | **Our own headline quoted the wrong denominator**, in a tool about denominators. | `4590f57` |
| 3 | **Our own seed text was being reported as a caught claim**, plus 7 rows that were never checkable. | `bd2bc65` |
| 4 | **The gateway that blocks false "done" was itself a false "done"** — it ran on Cloud Run out of a working tree that existed in no repository. | `8b7b0aa` |

**Close on this:** *"We could not show these skills help. We could not show they hurt. What the
controls let us say is exactly what we measured, and nothing else."*

---

## Shots 7 and 8 — only if the run is going well

**7 · Install in a foreign repo.** `examples/customer-workflow.yml`, twelve lines, `uses:` resolves
because the repo is public. **Verified that the file and the action exist; a live install into a
third-party repo was not performed in this pass.**

**8 · The honest-state section of the README.** Zero non-author installs. The record holds no real
agent claims. **This is a strength on camera, not an apology** — it is the only page in the
submission that a judge cannot catch out.

---

## What I could not verify, stated plainly

1. **Shots 1, 2 and 3 all wait on one thing: the full `witness-corpus` run.** It was still
   executing after twenty minutes when this was written — it probes every message twice and shells
   out to `git` each time. Commands are correct and the template is wired. **One run unblocks all
   three shots**, and until it lands shot 3 must be filmed from a regenerated page, not the
   committed one.
2. **390px rendering** — tooling clamps to a 500px viewport. No overflow at 500. Unchecked at 390.
3. **The break-glass write** — deliberately not pre-run, so the record stays clean for shot 5c.
4. **A live third-party install** — the workflow and action are verified to exist; the install was not run.
5. **`wrote _jed.py` and `wrote needs.ts`** on the report page survive the not-checkable filter and
   **have not been probed against their repositories.** Plausible, not confirmed. If a judge clicks
   one, that is the row I would least want to be wrong.
