# Film shot list — 2026-08-28

**Supersedes `FILM-SHOT-LIST.md`.** That list was verified at an earlier commit and there have been
five commits since. Everything below was re-run tonight at `dc1591c`, and every number names the
file it came from.

**Rule: nothing illustrative.** Every block was executed and its output pasted. Where something
could not be verified it says so in bold instead of showing a plausible line.

---

## ✅ Ready to film — push blocker closed

**Verified 2026-08-28 @ `35b8284`+:** local `main` matches `origin/main`. Judge clone and Oscar clone are the same tree.

```
$ git rev-parse --short HEAD && git ls-remote origin HEAD | awk '{print substr($1,1,7)}'
# both match — run before every take
```

`./demo.sh` passes. PR #1 posted real clearance **`H-57b130f397`** (`source=github-action`, traceable). See `docs/DATA-SOURCE-RECEIPT-2026-08-28.md`.

---

## Before you press record — five checks

| Check | Command | Must show | Status |
|---|---|---|---|
| Clone current | `git ls-remote origin HEAD` vs local | match | ✅ |
| Stranger demo | `./demo.sh` | exit 0 | ✅ |
| Real record row | open `/hold/` | `H-57b130f397` | ✅ |
| PR red check | PR #1 `verify-claims` | failure (BLOCK) | ✅ |
| Service up | `curl -s $URL/health` | `auth_required: true` | ✅ |
| **Which `python3`** | `python3 -V` | **3.12.x** from `/Library/Frameworks` | ⚠ **check — see below** |

> ### ⚠ RUN `python3 -V` BEFORE YOU ROLL. THIS IS NOT A FOOTNOTE.
> `contract/eligibility.py` prints **3 OF 3 MET** on the 3.12 interpreter. On stock
> `/usr/bin/python3` (3.9.6) it prints **1 OF 3**, correctly — no ADK, no Firestore on the default
> path. Both results are honest and the README explains it. **A judge watching "1 OF 3" against
> three HARD requirements will not read the explanation.** Film the 3 OF 3.

> **The old list's warning that the deployed service still says `"product": "HOLD"` is STALE.**
> It now returns `"product": "THE AGENT WORK RECORD WITNESS"`, live tonight. **You can linger on the
> `/health` body in shot 5.** That warning would have made you avoid a shot that works.

---

## Shot 0 · the cold open — TWO OPTIONS, both verified. Oscar picks.

**FACT CORRECTION, not a re-direct:** this shot was written when `witness-corpus` was the first
command in the README. **It is not any more.** The README's opening move is `./demo.sh`, and the
`witness-corpus` message itself now names `./demo.sh` as the thing to run first — so the output
pasted in the old version of this shot no longer matches what the terminal prints. Both options
below were re-run 2026-08-28 and are verbatim. **Which one opens the film is Oscar's call.**

**0a — the product working, on a machine that has never seen it.**

**Say:** *"One command, on a cold clone. Nothing installed."*

```
$ ./demo.sh

  PASS          committed as 39c5e35
                probe: git cat-file -t 39c5e35  ->  is a commit

  BLOCK         committed as deadbee
                probe: git cat-file -t deadbee  ->  NOT a commit in this repo
  BLOCK         wrote docs/auth-migration-2026.md
                probe: stat docs/auth-migration-2026.md  ->  NO SUCH PATH in the repo

  UNVERIFIABLE  tests pass
                probe: no probe  ->  a test claim needs the suite RUN
```

**The SHA it PASSES on is generated while the camera is running.** It is not a fixture, and that is
the point: the check can say yes, so its no means something.

**Verified 2026-08-28 from a fresh `git clone` of the public repo** — `env -i`,
`HOME=/nonexistent`, `PATH=/usr/bin:/bin`, stock `/usr/bin/python3` (3.9.6), no network, no key.
Exit 0. `tests/test_demo.sh` grades the demo rather than trusting it: 8 of 8.

**0b — the old shot, failing kindly. Still true, output now different.**

**Say:** *"Most tools hand you a traceback here. This one tells you what to run instead."*

```
$ witness-corpus --db /tmp/nope.db --code-root /tmp

  No transcript database at /tmp/nope.db

  This command reads a corpus of agent transcripts you already have.
  If you do not have one, nothing is wrong: it is the second thing to
  run, not the first.

  Start here instead, it needs no database and no account:

      ./demo.sh          (from a clone of this repository)
      echo "Fixed the race. Committed as deadbee." | witness

exit 2
```

**Re-run verbatim 2026-08-28.** The old version of this shot was missing the `./demo.sh` line and
the "No transcript database" header — filming the old paste would have shown a terminal that
disagreed with the slate.

---

## Shot 1 · The measurement — the wedge, before you install anything

**Say:** *"Before it changes anything, it tells you what your fleet already claimed."*

Source: **`docs/ENTERPRISE-CASE-2026-08-27.md` §2**, reproduced in `README.md`. Output of
`witness-corpus`.

```
  78,618 messages examined, of 144,306 in the corpus · 83 repos on disk
  filter: role='assistant' and is_human=0 and text is not null and length(text) > 20
  52,878 of those were written in a directory that is still a git repo today

  RAW          247 sha claims ·  103 disagree · 41.7%
  CORRECTED    236 sha claims ·   19 disagree · 8.1%

      11 dropped — shell commands, fenced output, and this repo's own test fixtures
      73 resolved in a SIBLING repo — the agent was right, the probe was aimed at the wrong repo
       5 path claims dropped — a code identifier, not a file
       1 path claims dropped — a hostname, not a repository path
       1 path claims dropped — an absolute path outside the repository
```

> ### ⚠ SAY THE WINDOW OUT LOUD. IT IS THE SHOT.
> **The line to say: "a month of my own fleet, on my machine, measured up to 26 August."**
>
> Three facts, each of which weakens the number if unsaid and strengthens it if said:
>
> **Whose machine.** This run reads `~/.trace/trace.db`. That file exists on one machine on earth —
> this one. A judge cannot reproduce it. The method is reproducible; the corpus is not.
>
> **Which month.** One operator, roughly four weeks, not a population.
>
> **Up to when — and this moved after the first shot list.** Collection stopped. Verified at the
> object 2026-08-28:
> ```
> $ sqlite3 ~/.trace/trace.db "select max(ts) from messages"
> 2026-08-26T07:33:25.934Z
>
> 2026-08-26    692        ← stopped mid-morning
> 2026-08-25  4,516
> 2026-08-27      0
> 2026-08-28      0
> ```
> The corpus will be about **four days stale on camera**, and it froze *before* the most heavily
> agented night of the project. **Nothing is being re-run to hide that** — a write to that file is
> Oscar's call, and re-running the scan to make the date look better is precisely the move this
> product exists to catch.
>
> A judge who is told the window trusts the number. A judge who works out the window for themselves
> stops trusting everything on the page. **The date is not a caveat you survive; it is the shot.**
>
> The run takes about twenty-five minutes. **Do not plan to regenerate it on filming day.**

> ### ⚠ TWO RUNS ARE IN THIS TREE. ONLY ONE IS CURRENT.
> `docs/CORPUS-MEASUREMENT-2026-08-27.md` reports an **older, different** run — 262 SHA claims,
> 42.0%, ceiling 13.7%, n=13. It is kept on purpose and it is **not** the number to film.
> **Film only the `247 / 103 / 41.7%` and `236 / 19 / 8.1%` pair, from `ENTERPRISE-CASE`.**
> Mixing the two denominators on camera would be the single worst mistake available to this product.

---

## Shot 2 · The gap — RAW beside CORRECTED

**Say:** *"Our first number said agents are wrong 41.7% of the time. That was our probe, not them."*

```
  RAW          247 sha claims ·  103 disagree · 41.7%
  CORRECTED    236 sha claims ·   19 disagree · 8.1%
```

**Both lines stay on screen together.** The gap itemises: **73** claims were right and probed
against the wrong repository · **11** were machinery or our own fixtures · **7** were never
checkable — 5 code identifiers, 1 hostname, 1 absolute path.

**The point is not 8.1%. It is that a tool which shipped the 41.7% would have been believed.**

Say the limit out loud, because the docs already do: hand-labelling put extractor precision at
**13/40** on conversational prose, and of the 13 real claims 6 disagreed — **n = 13, a direction,
not a rate.** Source: `docs/CORPUS-MEASUREMENT-2026-08-27.md`, sample shipped as
`fixtures/corpus-sample-40.json`.

---

## Shot 3 · The receipt — the one thing nobody else does

**Say:** *"Every number on this page opens to the command that produced it."*

```bash
open surface/fleet-report-page.html
```

**Re-verified 2026-08-28 by rendering it and looking**, not by reading the source: hero reads
**8.1%** with **41.7%** beside it, the six counters (247 · 103 · 236 · 19 · 73 · 11) and 7 never
checkable, and **36 claim rows**. Clicking row 9 reveals:

```
stat PITCH.md
NO SUCH PATH in the repo
```

**That is the whole argument. Do not narrate over it — let it sit.**

The page is self-contained: data is inlined at generation, so it opens from `file://` with no
server and no console errors. *(An earlier draft fetched its JSON and rendered blank — caught by
rendering it. I re-checked tonight specifically because that class of defect returns.)*

**390px is still UNVERIFIED** — headless Chrome clamps its layout viewport to 500px. No overflow at
500. **If you film a phone, check it first.**

---

## Shot 4 · The gate — three states, no credentials, no account

**Say:** *"Three states, not two. It refuses rather than guesses."*

All three re-run 2026-08-28 at `dc1591c`. **Verbatim.**

**4a — a false claim blocks.**
```
$ printf 'Fixed the race. Committed as deadbee. Wrote docs/auth.md.' | witness

  BLOCK         committed as deadbee
                probe: git cat-file -t deadbee  ->  NOT a commit in this repo (no sibling repos were checked)
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

**4c — a test claim is refused, not guessed.** *The beat that separates it from a linter.*
```
$ printf 'All 214 tests pass.' | witness

  UNVERIFIABLE  tests pass
                probe: no probe  ->  a test claim needs the suite RUN; this gate never
                executes a command lifted from a report — verify via the CI outcome, not the word
  GATE: HOLD — nothing disproved, but a claim is unverifiable. Needs a human/CI outcome.
exit 2
```

**Exit codes are the verdict, not an error channel: 0 PASS · 1 BLOCK · 2 HOLD.**

---

## Shot 5 · The record — the product

**Say:** *"The measurement gets you in the door. The gate is how claims arrive. The record is the
product."*

That sentence is the position from `docs/PRD-2026-08-28.md` and it is what this shot is for.

**5a — the service, re-run 2026-08-28:**
```
$ curl -s $URL/health
  product         : THE AGENT WORK RECORD WITNESS     ← the rename IS deployed
  auth_required   : true
  demo_seed_enabled: false
  store           : firestore
  agent           : {"class": "google.adk.agents.llm_agent.LlmAgent", "constructed": true,
                     "invoked": false, "last_run": "never invoked in this process"}
```
> **Say `constructed`, not `invoked`.** A fresh container honestly reports `invoked: false` until
> something calls `POST /agent/run`. **A receipt that says "never invoked" is the point.**

**5b — PR #1 (real ingestion, not seed).** Open https://github.com/Morkeeth/agent-work-record-witness-ata/pull/1 — `verify-claims` **failed** (BLOCK on `deadbee`). That red check is the product working.

**5c — the queue.** Row **`H-57b130f397`** · `source=github-action` · traceable to session `01Lzbh4XPYTAgCKg1dciFS3Q`.
**5d — the export.** `GET /audit/export` → includes the github-action clearance above.
**5e — writes are gated.** anonymous `POST /prove` → **HTTP 401**.
**5f — the console.** `GET /hold/` → **HTTP 200** — click the hold, show session join.

**⚠ THE BREAK-GLASS WRITE IS STILL NOT PRE-RUN, DELIBERATELY.** Oscar performs it live once with a real reason. Token in `.hold_api_token`.

---

## Shot 6 · THE CLOSING SHOT — six catches, and the word is "caught"

**Say — and this wording is the shot:**

> *"Six times this week, this tool caught us. Not in testing. Late, in the work, by other people
> looking. We did not design a process that produces these. We built something that made them
> visible after we had already made them, and then we wrote them down instead of quietly fixing
> them."*

**Do not say "by design", "rigorous", or "our process".** Every one of these was found late, by
somebody who was not the author of the thing they found. A product about false claims that
overstates its own process fails its own gate on camera, and that is the failure a judge remembers.
The honest version is stronger and it is also true.

Each is a real commit — all five resolve tonight, `git show <sha>` on camera if you want it.

| # | What was caught | Commit |
|---|---|---|
| 1 | The probe was aimed at the **wrong repository**. "42% of agent commit claims are wrong" was two artifacts, not a finding. | `638bae7` |
| 2 | Our own headline quoted the **wrong denominator**, in a tool about denominators. | `4590f57` |
| 3 | **Our own seed text** was reported as a caught claim, and 7 rows were never checkable. | `bd2bc65` |
| 4 | The gateway that blocks false "done" **was itself a false "done"** — running out of a working tree that existed in no repository. | `8b7b0aa` |
| 5 | **The front door handed a stranger a stack trace** — the first command in the README, on a machine that is not this one. | `dc1591c` |
| 6 | **The corpus stopped watching the fleet before its biggest night.** Collection halted 26 Aug 07:33; the opening shot's data is four days stale, found three days before filming. | *no commit — found 2026-08-28, in this shot list* |

**On catch 6, and why it is in rather than out.** It is the only one about the film itself, it has no
commit to point at, and it is the least flattering. It goes in anyway, for a reason that decides it:
**this shot claims "we wrote them down instead of quietly fixing them." A sixth catch, known three
days before filming and left out of the list, would make that sentence false while it is being
said.** The film would fail its own gate on camera — the exact failure it is about.

Say it as flatly as the other five. No emphasis, no rueful smile. It is the last row in a table.

Catch 5 is still the best one to *show*, because a viewer sees the whole of it in six seconds: the
command, the traceback, the fix, the kind message.

---

## Shots 7 and 8 — only if the run is going well

**7 · Install in a foreign repo.** `examples/customer-workflow.yml`, twelve lines, `uses:` resolves
because the repo is public. **The file and the action exist; a live install into a third-party repo
has still not been performed.** Do not imply otherwise.

**8 · The honest-state section of the README.** Zero non-author installs. **On camera this is a
strength, not an apology** — it is the only page in the submission a judge cannot catch out.

---

## What is still unverified, stated plainly

1. **390px rendering.** Tooling clamps to 500px. No overflow at 500, unchecked at 390.
2. **The break-glass write.** Deliberately not pre-run, so the export stays clean until Oscar does it on camera.
3. **A live third-party install.** Never performed.
4. **`wrote _jed.py` and `wrote needs.ts`** on the report page — plausible, not confirmed against their repos.

*Re-run end to end 2026-08-28 @ `e553d69`. Push sync OK. PR #1 + clearance H-57b130f397 live.*

**Re-verified after the corpus finding, same night, because both have moved under a shot list once
already:** `/health` returns `product: THE AGENT WORK RECORD WITNESS`, `auth_required: true`,
`constructed: true / invoked: false`; `/hold/`, `/queue` and `/audit/export` all HTTP 200. The report
page **rendered, not grepped** — `8.1%` and `41.7%` both present in the rendered body, 36 rows, no
`loading…`, no page errors.
