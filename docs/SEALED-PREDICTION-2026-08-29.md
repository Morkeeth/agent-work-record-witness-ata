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
| Demo readiness | 30% | 8/10 | was 7 — raised one point: `./demo.sh` exits 0 from a cold clone, all four §5 links returned 200, all five mutating routes 401 anon, and the 3:27.6 film has been transcribed end to end and checked against the never-say list for the first time |

---

## After results (do not fill before submit)

| Actual | Prediction hit? | Lesson # to distil |
|--------|-----------------|-------------------|
| | | |

---

## Measured at draft seal · 2026-09-01 UTC

Re-derived at the object tonight — not carried from any prior doc.

| Probe | Command | Result |
|-------|---------|--------|
| Repo HEAD | `git rev-parse HEAD` on `main` | `4a45551297c6d878257a516c90baf2f2fb103eb2` |
| Live `/health` | `curl -sS …/health` | `auth_required: true` · `demo_seed_enabled: false` · `store: firestore` · ADK `constructed: true` |
| Anon mutating routes | `curl -X POST …/{clearance,break-glass,prove}` | **401** each |
| Read surfaces | `curl …/{health,hold,audit,audit/export}` | **200** each |
| Audit export population | `curl …/audit/export \| jq '.events \| length'` | **25** events |
| Hero record `H-a6151a95ac` | same export, filter by id | `gate: BLOCK` · `decision: HOLD` · `open: true` · `pr: 1` · `session: 01Lzbh4XPYTAgCKg1dciFS3Q` · `head_sha: c99589111f82ca4b8a074220cbb5a358b33f5941` · `blocks: 2` · `source: github-action` |
| PR #1 state | `gh pr view 1 --json state` | **OPEN** |
| PR #1 `verify-claims` | `gh api …/check-runs --jq …verify-claims` | conclusion **`failure`** (2026-08-29T12:15:18Z) |
| PR #1 `witness-findings` (P3) | same API, name `witness-findings` | conclusion **`failure`** (2026-08-29T12:15:06Z) |
| Stranger cold path | `git clone … && env -i PATH="$PATH" HOME="$HOME" ./demo.sh` | **exit 0** · PASS · BLOCK · HOLD |
| `./film/preflight.sh` | tail | **PREFLIGHT PASS** (11/11) |
| Eligibility bare clone | `python3 contract/eligibility.py` after cold clone, no pip | **0 of 3**, exit 1 |
| Eligibility cold + ADK | same after `pip install google-adk`, no GCP creds | **1 of 3** (ADK constructed only), exit 1 |

**Architecture score note:** live service proves Firestore + ADK on `/health`; cold `eligibility.py` without `pip install google-adk` reads **0/3**, not the headline **1/3** — the honest cold clone path is `./demo.sh` (no pip), and eligibility **1/3** only after installing ADK locally.

---

**OSCAR_ONLY:** one cell — *Sealed at*. Put your local time in it and commit. Nothing else here
needs you before the submit button.
**Agent-filled 2026-08-29:** placement, primary prediction, confidence, falsifiers, rubric.
**Agent-updated 2026-08-31:** demo-readiness score and its reason, the video row (twice — the
second time at 04:50 UTC, correcting *unlisted* to *public* against the rules), and one
falsifier that was measured and closed overnight.
**Agent-updated 2026-09-01:** measured-at-draft-seal table (live `/hold/` + PR #1 + stranger path);
fixture scrub removed "required check" from `./demo.sh` output; draft hash below.

**Draft SHA256:** `3bf619bc0fdbb898635a172fc20faf24e465a863f0038f606e143056a770b9a9`
