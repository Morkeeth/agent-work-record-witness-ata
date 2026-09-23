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

**OSCAR_ONLY:** one cell — *Sealed at*. Put your local time in it and commit. Nothing else here
needs you before the submit button.
**Agent-filled 2026-08-29:** placement, primary prediction, confidence, falsifiers, rubric.
**Agent-updated 2026-08-31:** demo-readiness score and its reason, the video row (twice — the
second time at 04:50 UTC, correcting *unlisted* to *public* against the rules), and one
falsifier that was measured and closed overnight.

---

## Measured appendix · 2026-09-23 night wave (re-derived at objects)

Numbers below were **run**, not carried forward from earlier seals. Commands are the done-when.

| Object | Command | Result |
|--------|---------|--------|
| `/health` | `curl -sS $BASE/health` | `ok:true` · `auth_required:true` · `demo_seed_enabled:false` · `store:firestore` · ADK `LlmAgent` constructed |
| `/hold/` | `curl -sS -o /dev/null -w '%{http_code}' $BASE/hold/` | **200** |
| `/hold/?tab=queue` | same | **200** |
| `/audit/export` | `curl -sS $BASE/audit/export` | `exported_at=2026-09-23T00:12:01+00:00` · **25** events · hero `H-a6151a95ac` present |
| Hero row | python over export JSON | `gate=BLOCK` · `decision=HOLD` · `open=true` · `head_sha=c9958911…` · `session=01Lzbh4XPYTAgCKg1dciFS3Q` · `agent_explanation.invoked=True` · model `gemini-3.5-flash-lite` |
| Clear-like in export | count over events | **0** |
| Anon mutating | `POST /clearance` `/break-glass` `/prove` | **401** / **401** / **401** |
| Seed | `POST /demo/seed-hold` | **403** |
| PR #1 | `gh pr view 1 --json statusCheckRollup` | `verify-claims=FAILURE` · `witness-findings=FAILURE` · state OPEN · label `agent` |
| Preflight | `./film/preflight.sh` | **PREFLIGHT PASS** (11 ok) |
| Stranger demo | cold clone + `env -i … ./demo.sh` | exit **0** · `tests/test_demo.sh` PASS |
| Eligibility bare | stock python, no pip | **0 OF 3**, exit **1** |
| Eligibility deps / no ADC | `pip install -r requirements.txt`, empty HOME | **1 OF 3** (ADK), exit **1** |
| Eval (baseline arm) | `PYTHONPATH=. python3 eval/run_eval.py` | B 18/40 (45%) beats A 9/40 (22.5%); **NULL always-silent 27/40 (67.5%) beats both on accuracy** — metric defect disclosed, not swapped |
| Film scrub | `rg 'required check' film/voiceover.txt film/voiceover-vo.txt film/subtitles.srt` | **no matches** |

`$BASE` = `https://fleet-wedge-33kamss2jq-uc.a.run.app` (from `.cloud_run_url`).

**Do not submit Devpost from this appendix.** Outward submit is Oscar's click.

---

## Draft hash (content above this line)

```
sha256:371d44c9d4104a8623096504dedd063bffc0a3901f29d29b438cefb0f8055611
```

UTF-8 sha256 of every byte **above** the `## Draft hash` heading. Re-derive:

```bash
python3 -c "from pathlib import Path; import hashlib; t=Path('docs/SEALED-PREDICTION-2026-08-29.md').read_text(); print(hashlib.sha256(t.split('## Draft hash')[0].encode()).hexdigest())"
```

Do not trust a carried hash — run that command at the object.
