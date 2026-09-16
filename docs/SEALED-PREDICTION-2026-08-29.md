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
>
> **Addendum 2026-09-16 (film morning):** the `?tab=queue` "first card = H-a6151a95ac" claim
> itself went false (hero at index 13). Deep link `?record=H-a6151a95ac` is restored in
> README / PACK; that is a judge-path fix, not a re-seal of placement.

---

## Scoring rubric self-call (pre-submit)

| Criterion | Weight | Our honest score | Why |
|-----------|--------|------------------|-----|
| Innovation & utility | 40% | 7/10 | four verdicts, the session join, and a corpus self-audit that found our own defect first; the niche is real and adoption is zero |
| Architecture | 30% | 8/10 | probe local, verdict-only over the network, diagram exported and read, eligibility exercised rather than imported (3 of 3 with ADC exit 0, 1 of 3 cold exit 1, both re-measured 2026-08-31) |
| Demo readiness | 30% | 8/10 | was 7 — raised one point: `./demo.sh` exits 0 from a cold clone, all four §5 links returned 200, all five mutating routes 401 anon, and the 3:27.6 film has been transcribed end to end and checked against the never-say list for the first time |

---

## Measured at the object · film-morning re-probe (2026-09-16)

**Not a re-seal.** Placement / primary prediction / sealed-at stay as sealed 31 Aug.
Numbers below were read tonight from the live service and PR #1 — not copied from an earlier receipt.

| Probe | Command | Result |
|-------|---------|--------|
| Live base | `cat .cloud_run_url` | `https://fleet-wedge-33kamss2jq-uc.a.run.app` |
| `/health` | `curl -sS $BASE/health` | `ok=true` · `auth_required=true` · `demo_seed_enabled=false` · `store=firestore` · ADK `constructed=true` · `ever_invoked=true` |
| `/queue` | `curl -sS $BASE/queue` | `count=20` · first card **`H-56f6e3a047`** (no session) · hero **`H-a6151a95ac` at index 13** |
| Hero row | same | `session=01Lzbh4XPYTAgCKg1dciFS3Q` · `traceable=true` · `head_sha=c99589111f82ca4b8a074220cbb5a358b33f5941` · `gate=BLOCK` · `decision=HOLD` · `pr=1` · `agent_explanation.invoked=true` · `model=gemini-3.5-flash-lite` · `open=true` |
| `/audit` | `curl -sS $BASE/audit` | `pct_cleared_without_hold=0.0` · `counts={clear:0, hold:22, exception:2, total_clearance:22}` |
| `/audit/export` | `curl -sS $BASE/audit/export` | 25 events · hero present |
| Anon writes | `curl -X POST $BASE/{clearance,break-glass,prove,demo/seed-hold}` | `401 · 401 · 401 · 403` |
| PR #1 | `gh pr view 1 --json state,statusCheckRollup` | OPEN · `verify-claims=FAILURE` · `witness-findings=FAILURE` |
| Cold eligibility (ADK installed, no ADC) | `python3 contract/eligibility.py` | **1 OF 3 MET** · exit **1** |
| Cold `./demo.sh` | `env -i PATH="$PATH" HOME="$HOME" ./demo.sh` | exit **0** |
| Deep link | Playwright → `$BASE/hold/?record=H-a6151a95ac` | detail opens with session + deadbee; stack tab still navigates (no loop) |
| First-card claim | Playwright → `$BASE/hold/?tab=queue` | first card `H-56f6e3a047` · hero index 13 · **claim was false** |

**3 of 3 with ADC** was not re-measured tonight — this environment has no `gcloud` / ADC. The 2026-08-31 seal row still carries that number from when it was exercised.

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
**Agent-updated 2026-09-16:** measured-at-object table from live `/hold/` + PR #1; first-card
falsifier addendum; draft hash below. Placement cells untouched.

---

### Draft hash (sha256 of everything above this heading · 2026-09-16 film-morning fill)

```
231a7ea24dc797bf09bc850ef9b5f6d5880f489e489143fecf2e504b03bcc0fc
```
