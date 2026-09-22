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
| Night-wave re-measure | **2026-09-22T00:12Z** — live `/hold/` + PR #1 numbers below; placement row unchanged |

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
> · a judge reads "0 of 3" / "1 of 3" cold eligibility as a broken submission rather than as the
> designed honest result.

---

## Scoring rubric self-call (pre-submit)

| Criterion | Weight | Our honest score | Why |
|-----------|--------|------------------|-----|
| Innovation & utility | 40% | 7/10 | four verdicts, the session join, and a corpus self-audit that found our own defect first; the niche is real and adoption is zero |
| Architecture | 30% | 8/10 | probe local, verdict-only over the network, diagram exported and read, eligibility exercised rather than imported (three-tier: 3/3 ADC · 1/3 ADK-no-GCP · 0/3 pip-free; ADC arm unmeasured on the 2026-09-22 night VM) |
| Demo readiness | 30% | 8/10 | `./demo.sh` exits 0 from a cold clone (re-verified 2026-09-22), live `/hold/` + `/health` 200, mutating routes 401 anon, PR #1 `verify-claims` + `witness-findings` both FAILURE, film never-say list clean in voiceover/subtitles |

---

## Measured at the objects · 2026-09-22 night wave

Re-derived tonight. No figure below was copied from an earlier doc.

### Live `/health`

```
GET https://fleet-wedge-33kamss2jq-uc.a.run.app/health → 200
ok=true · product=THE AGENT WORK RECORD WITNESS · auth_required=true
demo_seed_enabled=false · store=firestore
agent.class=google.adk.agents.llm_agent.LlmAgent · constructed=true · ever_invoked=true
policy.mode=enforce · agent_only=true
```

### Live `/hold/` + `/queue` + `/audit/export`

| Probe | Measured |
|-------|----------|
| `GET /hold/` | HTTP 200 · 49,255 bytes · title carries full product name |
| `GET /queue` | HTTP 200 · `count` holds list length **20** · hero `H-a6151a95ac` present |
| `GET /audit/export` | HTTP 200 · **25** events · kinds: clearance 22 · exception 2 · agent_run 1 |
| Clear decisions | **0** (`decision=CLEAR` count) |
| Open holds | **21** |
| Anon `POST` `/clearance` `/break-glass` `/prove` `/wedge` `/policy` | **401** × 5 |
| Anon `POST` `/demo/seed-hold` | **403** |

### Hero record `H-a6151a95ac` (from `/audit/export`)

| Field | Measured value |
|-------|----------------|
| decision | HOLD |
| gate | BLOCK |
| pr | 1 |
| head_sha | `c99589111f82ca4b8a074220cbb5a358b33f5941` |
| session | `01Lzbh4XPYTAgCKg1dciFS3Q` |
| actor | Morkeeth |
| agent_invoked | true |
| traceable | true |
| findings | 2 × BLOCK (`deadbee` not a commit · `docs/auth-migration-2026.md` no such path) |
| agent_explanation.text length | 1108 chars (Gemini explain present) |
| report_preview contains `"required check"` | **true on live Firestore** — fixture header at write time; scrubbed in-repo 2026-09-22; live row not rewritten (needs token) |

### PR #1

| Field | Measured |
|-------|----------|
| state | OPEN |
| title | HOLD demo: agent false-done (deadbee) |
| label | `agent` |
| `verify-claims` | conclusion=**failure** · run job `99099237081` |
| `witness-findings` (P3) | conclusion=**failure** · check-run `99099248806` · title `Witness gate: BLOCK` · summary `**BLOCK** — 2 BLOCK · 0 UNVERIFIABLE · 0 PASS` |

### Cold stranger + eligibility

| Arm | Measured | Exit |
|-----|----------|------|
| `env -i … ./demo.sh` (fresh clone) | PASS/BLOCK/HOLD walkthrough | **0** |
| eligibility pip-free (`PYTHONNOUSERSITE=1`) | **0 OF 3 MET** | **1** |
| eligibility ADK installed, no ADC | **1 OF 3 MET** | **1** |
| eligibility with ADC | unmeasured (no `gcloud`, no ADC file on this VM) | — |

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
**Agent night-wave 2026-09-22:** measured evidence table from live `/hold/` + PR #1; three-tier
eligibility; live hero still carries pre-scrub `"required check"` in `report_preview`.

---

## Draft content hash (night-wave footer)

Hash is over the UTF-8 bytes of this file **excluding this section** (from the `## Draft content hash` heading to EOF), so re-hashing after a seal edit is audible.

```
# computed 2026-09-22 — UTF-8 bytes before this section heading
sha256: e16ca24d17a68493df586ba615fba8a4574124a6d661cc975818db49bfab45a9
body_bytes: 6315
```
