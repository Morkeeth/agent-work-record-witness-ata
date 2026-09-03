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
> 2026-08-31 — latch deployed; link is `?record=H-a6151a95ac`, re-probed 2026-09-03)
> · a judge reads "1 of 3" cold eligibility as a broken submission rather than as the designed
> honest result.

---

## Live measurements (re-derived 2026-09-03 · night wave)

Probed at the object — not quoted from earlier docs.

| Probe | Command | Measured |
|-------|---------|----------|
| Live `/health` | `curl -sS https://fleet-wedge-33kamss2jq-uc.a.run.app/health` | `auth_required: true` · `demo_seed_enabled: false` · `store: firestore` · `product: THE AGENT WORK RECORD WITNESS` |
| Hero record | `curl -sS …/audit/export \| jq … H-a6151a95ac` | present · `gate: BLOCK` · `session: 01Lzbh4XPYTAgCKg1dciFS3Q` · `head_sha: c99589111f82` |
| Clear count | `curl -sS …/audit` | `pct_cleared_without_hold: 0.0` · 49 total events |
| Export count | `curl -sS …/audit/export` | 25 events · `clear: 0` |
| Queue position | `curl -sS …/queue` | 20 holds · `H-a6151a95ac` at **position 14** (not first row — `?record=` deep link is honest) |
| PR #1 checks | `gh pr view 1 --json statusCheckRollup` | OPEN · `verify-claims` **failure** · `witness-findings` **failure** · head `c99589111f82…` |
| Stranger path | `env -i PATH="$PATH" HOME="$HOME" ./demo.sh` | exit **0** |
| Stranger test | `tests/test_demo.sh` | **PASS** (11 assertions) |
| Preflight | `./film/preflight.sh` | **11/11 PASS** |
| Eligibility cold | `CLOUDSDK_CONFIG=/nonexistent GOOGLE_APPLICATION_CREDENTIALS= python3 contract/eligibility.py` (after `pip install -r requirements.txt`) | **1 OF 3 MET**, exit **1** (ADK constructed; Gemini + Firestore not reachable without credentials) |

Deployed HTML contains `recordOpened` latch — `?record=H-a6151a95ac` is the judge deep link.

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

**OSCAR_ONLY:** one cell — *Sealed at*. Put your local time in it and commit. Nothing else here
needs you before the submit button.
**Agent-filled 2026-08-29:** placement, primary prediction, confidence, falsifiers, rubric.
**Agent-updated 2026-09-03:** live measurement table (night wave) · falsifier link corrected to `?record=` · draft hash below.

---

**Draft integrity (SHA-256 of this file excluding this footer block):**

```
PLACEHOLDER
```
