# Sealed prediction · ATA · All Things Agentic

**Handbook #72:** write **before** the Devpost submit button. Do not edit after results.

---

## Metadata

| Field | Value |
|-------|--------|
| Event | All Things Agentic Hackathon · Fortified Enterprise Fleet |
| Repo | https://github.com/Morkeeth/agent-work-record-witness-ata |
| Video | **public** YouTube link, pasted at submit. **CORRECTED 2026-08-31 at seal time:** the film that shipped is `demo/demo-final-v2.mp4`, **3:48.3**, md5 `d327a995166b63ad3a64f248d5104397` — Oscar's 20.7s spoken intro joined ahead of the demo, subtitles re-timed. The row previously cited `demo-final.mp4`, 3:27.6, md5 `3147f344…`, which is the pre-intro cut and is no longer what was submitted. Row also said *unlisted* until 04:50 UTC; the rules require *"made publicly visible on YouTube or Vimeo"* |
| Sealed at | **Mon 31 Aug 2026 21:56 CEST** — stamped before the 02:00 CEST deadline, on Oscar's instruction. |
| Deadline | Mon 31 Aug 2026 · 17:00 PDT (Mon 1 Sep 02:00 CEST) |

---

## Prediction

**Placement:**

- [ ] Grand / category winner ($20K Fortified Enterprise Fleet)
- [ ] Architectural Design ($5K)
- [x] Honorable Mention ($2K)
- [ ] No prize · top quartile demo
- [ ] No prize · learning run

**Primary prediction (one sentence):**

> Top-five demo in Fortified Enterprise Fleet on honesty, live proof and a cold-clone
> `./demo.sh` that runs with no account and no network; not grand — zero non-author installs
> and a PR #1 that is red by design cap the ceiling.

**Confidence:** med

**What would falsify it:**

> A judge never clicks the live URL · a field full of GEAP-native fleet managers with richer
> Memory/Registry stories · another entry ships the same claim-vs-repo wedge with real adoption
> numbers · the console link puts a judge in a loop and they leave (measured and closed
> 2026-08-31 — see `docs/SHIP-VERIFICATION-2026-08-31.md` §A1; the link is now `?tab=queue`)
> · a judge reads "1 of 3" cold eligibility as a broken submission rather than as the designed
> honest result.

---

## Scoring rubric self-call (pre-submit)

| Criterion | Weight | Our honest score | Why |
|-----------|--------|------------------|-----|
| Innovation & utility | 40% | 7/10 | four verdicts, the session join, and a corpus self-audit that found our own defect first; the niche is real and adoption is zero |
| Architecture | 30% | 8/10 | probe local, verdict-only over the network, diagram exported and read, eligibility exercised rather than imported (3 of 3 with ADC exit 0, 1 of 3 cold exit 1, both re-measured 2026-08-31) |
| Demo readiness | 30% | 8/10 | `./demo.sh` exit 0 (re-probed 2026-09-02); `tests/test_demo.sh` 11/11; preflight 11/11; live `/hold/` + PR #1 checks at object (see below) |

---

## Live measurements (probed 2026-09-02 UTC)

**Commands run on this pass** — numbers re-derived at the object, not carried from docs.

| Probe | Command | Measured |
|-------|---------|----------|
| Cold demo | `env -i PATH="$PATH" HOME="$HOME" ./demo.sh` | exit **0** |
| Demo receipt | `./tests/test_demo.sh` | **11/11** ok |
| Preflight | `./film/preflight.sh` | **11/11** ok · PREFLIGHT PASS |
| Live health | `curl -sS …/health` | `auth_required=true` · `demo_seed_enabled=false` · `store=firestore` · `product=THE AGENT WORK RECORD WITNESS` |
| Hero record | `curl -sS …/audit/export` → `H-a6151a95ac` | **present** · `gate=BLOCK` · `head_sha=c99589111f82ca4b8a074220cbb5a358b33f5941` · `agent_explanation` populated |
| Export size | same | **25** events · **22** BLOCK · **0** CLEAR |
| PR #1 state | GitHub API `pulls/1` | **open** · title *HOLD demo: agent false-done (deadbee)* |
| PR #1 checks | `commits/c995891…/check-runs` | `verify-claims` → **failure** · `witness-findings` → **failure** (`**BLOCK** — 2 BLOCK · 0 UNVERIFIABLE · 0 PASS`) |
| Eligibility cold | `python3 contract/eligibility.py` (after `pip install -r requirements.txt`) | **1 of 3** MET (ADK `LlmAgent` only) · exit **1** |
| Anon mutating routes | `./tests/test_auth_gate.sh` | **5/5** → 401 |

**Film spine (repo, not live):** `film/voiceover.txt` 8 lines = `film/subtitles.srt` 8 cues · no
"required check" in either · corpus **78,618** · **41.7** raw · **8.1** corrected on `/hold/`.

---

## After results (do not fill before submit)

| Actual | Prediction hit? | Lesson # to distil |
|--------|-----------------|-------------------|
| | | |

---

**OSCAR_ONLY:** one cell — *Sealed at*. Put your local time in it and commit. Nothing else here
needs you before the submit button.
**Agent-filled 2026-08-29:** placement, primary prediction, confidence, falsifiers, rubric.
**Agent-updated 2026-08-31:** demo-readiness score and its reason, the video row (twice — the
second time at 04:50 UTC, correcting *unlisted* to *public* against the rules), and one
falsifier that was measured and closed overnight.
**Agent-updated 2026-09-02:** live-measurements table from `/hold/` + PR #1 + cold path re-run;
demo-readiness reason refreshed at object.

**Draft SHA-256:** `e87f137c05bb3f98e141f653b533f15111a62aa35c6850ddca4b0d8e126da7ea`
