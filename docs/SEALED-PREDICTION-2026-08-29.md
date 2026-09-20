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
> honest result · a judge runs `python3 contract/eligibility.py` on a bare clone (no
> `pip install google-adk`) and reads **0 of 3** as a broken claim about "1 of 3"
> (re-measured 2026-09-20 — bare cold is 0/3; the "1 of 3" figure assumes ADK installed).

---

## Scoring rubric self-call (pre-submit)

| Criterion | Weight | Our honest score | Why |
|-----------|--------|------------------|-----|
| Innovation & utility | 40% | 7/10 | four verdicts, the session join, and a corpus self-audit that found our own defect first; the niche is real and adoption is zero; eval accuracy loses to the always-silent null (45% vs 67.5%, re-run 2026-09-20) |
| Architecture | 30% | 8/10 | probe local, verdict-only over the network, diagram exported and read; live `/health` shows ADK constructed + Firestore (re-probed 2026-09-20); bare-clone eligibility is **0 of 3** without ADK — do not paste "1 of 3" without saying the ADK precondition |
| Demo readiness | 30% | 8/10 | `./demo.sh` exits 0 from a cold GitHub clone (re-run 2026-09-20), live `/hold/` + `/health` 200, anon mutating routes 401/403, PR #1 `verify-claims` + `witness-findings` both FAILURE; film cut is **3:48.3** (`demo-final-v2.mp4`), not the 3:27.6 pre-intro cut — corrected in this row 2026-09-20 after the reason still cited the dead length |

---

## Measured at the object · night wave 2026-09-20

Re-derived tonight. No number below was carried from an earlier doc.

| Object | Command / probe | Result |
|--------|-----------------|--------|
| Live `/health` | `curl -sS …/health` | HTTP 200 · `auth_required: true` · `demo_seed_enabled: false` · `store: firestore` · ADK `constructed: true` · `ever_invoked: true` |
| Live `/hold/` | `curl -sS …/hold/` | HTTP 200 · brand `THE AGENT WORK RECORD WITNESS` · Install tab advisory (ban on calling it required) |
| Live `/queue` | `curl -sS …/queue` | `count: 20` · `calm: false` |
| Live `/audit/export` | `curl -sS …/audit/export` | `events: 25` · hero `H-a6151a95ac` present · `gate: BLOCK` · `pr: 1` · `head_sha: c99589111f82ca4b8a074220cbb5a358b33f5941` · `traceable: true` · `agent_explanation.invoked: true` · model `gemini-3.5-flash-lite` · open holds 21 / closed 3 |
| Anon mutating | `POST /clearance` `/break-glass` `/prove` `/demo/seed-hold` | 401 · 401 · 401 · 403 |
| PR #1 | `gh pr view 1` · `gh pr checks 1` | OPEN · label `agent` · `verify-claims` FAILURE · `witness-findings` FAILURE · findings summary `**BLOCK** — 2 BLOCK · 0 UNVERIFIABLE · 0 PASS` |
| Cold `./demo.sh` | `git clone https://github.com/Morkeeth/agent-work-record-witness-ata && env -i PATH="$PATH" HOME="$HOME" ./demo.sh` | exit **0** · GATE PASS · GATE BLOCK · GATE HOLD · `no network · no API key · no account · no pip install` |
| `tests/test_demo.sh` | same | **PASS** (11 ok) |
| Bare eligibility | `python3 contract/eligibility.py` (no ADC, no google-adk) | **0 OF 3 MET**, exit 1 |
| ADC eligibility 3/3 | not re-run | **UNVERIFIED tonight** — no ADC on this runner |
| Film spine `film/` | `rg -i 'required check' film/voiceover.txt film/subtitles.srt` | clean |
| Shipped film `demo/` | `rg -n 'append only' demo/demo-final-v2.srt` | **2 hits** (cues at lines 131, 187) — known film defect; not fixable without Oscar re-cut |
| Film bytes | `md5sum` + `ffprobe` | `demo-final-v2.mp4` md5 `d327a995…` duration **228.35 s = 3:48.3** · `demo-final.mp4` md5 `3147f344…` duration **207.63 s = 3:27.6** |
| Eval baseline | `python3 eval/run_eval.py` | NULL 27/40 **67.5%** · A naive 9/40 **22.5%** · B headline 18/40 **45.0%** · McNemar A vs B p=0.0039 · **NULL beats both arms on accuracy** |
| Preflight | `./film/preflight.sh` | **PREFLIGHT PASS** |
| Live revision claimed on `/hold/` Stack tab | HTML string | `fleet-wedge-00014-q2g` (cannot confirm via gcloud on this runner) |

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
**Agent-updated 2026-09-20 (night wave):** measured-at-object table from live `/hold/` + PR #1;
demo-readiness reason corrected off the dead 3:27.6 length onto 3:48.3; bare-eligibility
0/3 falsifier added; eval NULL-beats-us row re-run; draft hash below.

### Draft hash (night wave)

Hash covers this file from the top through the **Agent-updated 2026-09-20** paragraph inclusive
(everything above this heading). Re-derive: `python3 -c "from pathlib import Path; import
hashlib; t=Path('docs/SEALED-PREDICTION-2026-08-29.md').read_text(); t=t.split('### Draft hash')[0];
print(hashlib.sha256(t.encode()).hexdigest())"`

```
sha256:PENDING
```
