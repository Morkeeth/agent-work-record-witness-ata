# Lane 1 receipt — ATA demo stack, 2026-08-28

Everything below was probed, not carried forward. Head `6042d28`, pushed, public.

## Ship condition — MET

Fresh clone from public GitHub, `env -i`, `HOME=/nonexistent`, `PATH=/usr/bin:/bin`, no `PYTHON`
override, no `~/.trace`:

```
./demo.sh            exit 0    PASS(0) / BLOCK(1) / HOLD(2), all three shown
./tests/test_demo.sh exit 0    8 of 8
git status --short   empty     clone == origin/main
```

A judge clones, runs one command, and watches a false claim get caught. No account, no key, no
network, no file read outside the clone. Nothing on the judge path touches `~/.trace/trace.db`.

## What was broken, by class

**The judge could not run it at all.** `str | None` in annotation position is a runtime TypeError
before 3.10, so `cloud/service.py` died at **import** on stock macOS `python3` (3.9.6) — every
endpoint, not just `/health`. The Dockerfile pins 3.12, which is why nothing caught it. Seven
modules got `from __future__ import annotations`; `requires-python >=3.9`; suite green on 3.9.6.

**The repo contradicted itself about its own security posture.** The closed `/prove` defect was
still open in three docs — SUBMISSION-PACK, `docs/ARCHITECTURE.md:154`, `docs/GEAP-GAP:60`, the
last calling it "currently broken live". Re-probed anonymously: `/prove` `/clearance`
`/break-glass` `/agent/run` all **401**, `/seed` **404**. Closed in all three.

**Correct source, wrong artifact.** `docs/ARCHITECTURE.md` was fixed; the committed
`docs/architecture.png` — the file `ATA-FILM-AND-SHIP` §4 says to paste into Devpost — was the old
render with **no Cloud Run anywhere in it**, against a rubric that hard-requires a Google Cloud
infrastructure service. Regenerated and looked at. First attempt put Cloud Run in the subgraph
title; mermaid does not wrap those and it rendered clipped. Caught by rendering twice.

**The repo made a claim the submission disclaims.** `surface/org-proof.html` and
`org-lift-live.html` present "ORG LIFT PROOF" from n=2 while SUBMISSION-PACK §3 records the same
thing as `UNMEASURED_FOR_ORG_CLAIM` and both `hack.md` and `ATA-FILM-AND-SHIP` ban it on camera.
The ban was enforced on the video and not on the artifact. Both now carry the n=2 line.

**A dead page wearing the inviting filename.** `surface/fleet-report.html` sat at `loading…`
forever — it is the template, `fleet-report-page.html` is the render. Linked from nothing, so
nobody had opened it. It now names itself and links to the real report.

**Also:** `8.4%` → `8.1%` (19/236), none left in any `.md` · the `/audit`-vs-export row was never a
defect, it is the prove-only filter · `docs/internal` said the repo was private and to invite the
judges, it is PUBLIC · workflow `uses:` still pointed at the pre-rename repo · film docs carried a
resolved blocker as live and a Shot 0 whose pasted output no longer matched the terminal.

## Rules this day produced

- **Correct source is not a correct artifact.** The fix existed; the thing a stranger receives did
  not have it. Adopted fleet-wide.
- **A stale warning is worse than no warning.** `ATA-FILM-AND-SHIP` warned the PNG said "required
  check" — it does not — while the real defect, the missing Cloud Run, sat beside it unmentioned.
  A warning pointing at the wrong defect aims the next reader away from the real one.
- **The filter is the fact; the count is a reading.** `/audit` 31→32 and export 7→8 within one
  hour. No live counter on a slate, in a film, or in a submission doc.
- **`clear: 0` is the product working.** The one real claim that arrived was false and was held.

## Judge-POV evaluation, run against `docs/SPEC-EXTRACT.md`

Hard requirements all met — 3 of 3 Google boxes **exercised**, public repo, runnable setup,
diagram, disclosure. **Open gap:** Devpost requires a text description covering *features,
technologies, data sources, learnings*. §1 is headed "What it does / How we built it / Challenges /
What's next / Architecture" — the content is there, none of the four required words is. Relabelling,
not writing.

**Filming optic:** run `python3 -V` first. `eligibility.py` prints **3 OF 3** on 3.12 and **1 OF 3**
on stock `/usr/bin/python3`. Both honest; only one survives a judge who does not read footnotes.
Now a pre-roll check in both film docs.

## Market probe — closes an "informed negative" in hack.md

`hack.md` §WHITE SPACE flags its own competitive claim as *"a Fable market scan, an informed
negative, NOT web-verified."* Partially closed:

- **Zenity $125M Series C, 3 Aug 2026**, Norwest-led, revenue tripling annually, Gartner frontrunner
  in agent governance. Multi-source. The category is funded.
- The one vendor taxonomy found (Critique's own listicle — **single source, weight accordingly**)
  names `agentwatch` for claim-versus-recorded-**actions**, and states outright that observation
  "is not the same as reproducing semantic correctness." That is claim-vs-**trace**. Ours is
  claim-vs-**repo**, and `--no-repo-witness` is that A/B as a runnable switch.

## Read this — Oscar's ruling, not mine

`docs/internal/CURSOR-LOG.md` carried a GCP account email, project number and **billing account ID**
in a repo that has been public. Redacted; history still has them on `origin/main`. An identifier,
not a credential — nobody can spend against it. Scrub / rotate / accept is his call. Not acted on.

## Still Oscar's

The film — **and he ruled 2026-08-28 that filming waits until the demo clears a named bar**, not
before. The cold-open choice (Shot 0 has 0a and 0b, both verified). Break-glass live, once, with a
real reason. The Devpost submit.
