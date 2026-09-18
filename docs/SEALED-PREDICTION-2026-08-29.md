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

## Night-wave object measurements · 2026-09-18 (do not rewrite sealed cells above)

Re-derived at the live objects — not carried from earlier docs.

| Object | Command | Measured |
|--------|---------|----------|
| `/health` | `curl -sS https://fleet-wedge-33kamss2jq-uc.a.run.app/health` | `ok=true` · `product=THE AGENT WORK RECORD WITNESS` · `auth_required=true` · `demo_seed_enabled=false` · `store=firestore` · ADK `constructed=true` · `ever_invoked=true` |
| `/hold/` | `curl -sS -o /dev/null -w '%{http_code}' …/hold/` | **200** · 49255 bytes · brand in `<title>` + `.brand` |
| `/audit/export` | `curl -sS …/audit/export` | `events=25` · decisions HOLD **22** / EXCEPTION **2** / unset **1** · `open=true` **21** · cleared-PASS **0** |
| Hero `H-a6151a95ac` | same export | `gate=BLOCK` · `decision=HOLD` · `open=true` · `pr=1` · `head_sha=c99589111f82ca4b8a074220cbb5a358b33f5941` · `session=01Lzbh4XPYTAgCKg1dciFS3Q` · **2** BLOCK probes (`deadbee`, missing path) · `agent_invoked=true` |
| Mutating routes | anon POST | `/clearance` **401** · `/break-glass` **401** · `/prove` **401** · `/demo/seed-hold` **403** |
| PR #1 | `gh pr view 1` + `gh pr checks 1` | **OPEN** · `verify-claims` **failure** · `witness-findings` **failure** (id `99099248806`, title `Witness gate: BLOCK`, summary `2 BLOCK · 0 UNVERIFIABLE · 0 PASS`) |
| Cold `./demo.sh` | `env -i PATH="$PATH" HOME="$HOME" ./demo.sh` | exit **0** · GATE PASS / BLOCK / HOLD |
| Cold eligibility (this VM) | `python3 contract/eligibility.py` | **0 OF 3 MET**, exit **1** (no ADC, no `google-adk` here). Docs' "1 of 3 cold" assumes ADK installable — say which environment you measured. |

**Embarrassment still on the sealed live path:** hero `report_preview` and PR #1 body still contain the old fixture phrase `required check` (repo fixture scrubbed this run; Oscar must edit PR body + re-clearance to rewrite the store). See `docs/EMBARRASSMENT-HUNT-2026-09-18.md`.

**Sealed-doc internal drift (not rewritten — sealed cells stay):** Video metadata row says film `demo-final-v2.mp4` **3:48.3** md5 `d327a995166b63ad3a64f248d5104397` — **re-derived at file:** `md5sum` match · `ffprobe` duration **228.35s** (= 3:48.3). Demo readiness reason still cites **3:27.6** (pre-intro cut). Leave sealed; noted here.

**Live scrub control (must be able to go red):** `./tests/test_live_preview_scrub.sh` — expects FAIL until Oscar rewrite.

---

**OSCAR_ONLY:** one cell — *Sealed at*. Put your local time in it and commit. Nothing else here
needs you before the submit button.
**Agent-filled 2026-08-29:** placement, primary prediction, confidence, falsifiers, rubric.
**Agent-updated 2026-08-31:** demo-readiness score and its reason, the video row (twice — the
second time at 04:50 UTC, correcting *unlisted* to *public* against the rules), and one
falsifier that was measured and closed overnight.
**Agent night-wave 2026-09-18:** measured table above only — sealed placement/scores untouched.

### Draft hash (prediction + rubric + metadata through seal row; night-wave table excluded)

```
sha256:775e836a214a48631819f623c41959e7803a577d4a202c3a4de39ae0d643de80
```

```bash
# re-derive:
python3 -c "import hashlib,pathlib; t=pathlib.Path('docs/SEALED-PREDICTION-2026-08-29.md').read_text(); c=t[:t.find('## After results')]; print(hashlib.sha256(c.encode()).hexdigest())"
```
