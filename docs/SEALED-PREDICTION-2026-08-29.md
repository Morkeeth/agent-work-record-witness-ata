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
| Night-wave re-measure | **2026-09-18T00:09:59Z** — numbers below from live `/hold/` + PR #1; placement cells above are **not** re-opened |

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
| Architecture | 30% | 8/10 | probe local, verdict-only over the network, diagram exported and read, eligibility exercised rather than imported (3 of 3 with ADC exit 0, 1 of 3 cold exit 1 with `pip install -r requirements.txt`, both shapes re-measured 2026-09-18) |
| Demo readiness | 30% | 8/10 | was 7 — raised one point: `./demo.sh` exits 0 from a cold clone, mutating routes 401/403 anon, and the film on disk is `demo-final-v2.mp4` **228.35s (3:48.3)** md5 `d327a995166b63ad3a64f248d5104397` (re-probed 2026-09-18; the earlier 3:27.6 cite was the pre-intro cut) |

---

## Night-wave object measures · 2026-09-18 (do not substitute for seal cells)

Commands run; figures re-derived at the object — not carried from an earlier doc.

### Live `/health` · `curl -sS https://fleet-wedge-33kamss2jq-uc.a.run.app/health`

| Field | Measured |
|-------|----------|
| `ok` | `true` |
| `product` | `THE AGENT WORK RECORD WITNESS` |
| `auth_required` | `true` |
| `demo_seed_enabled` | `false` |
| `store` | `firestore` |
| `agent.constructed` | `true` (`google.adk.agents.llm_agent.LlmAgent`) |
| `agent.ever_invoked` | `true` |

### Live `/queue` · hero `H-a6151a95ac`

| Field | Measured |
|-------|----------|
| `queue.count` | `20` |
| `decision` / `gate` | `HOLD` / `BLOCK` |
| `pr` | `1` |
| `repo` | `Morkeeth/agent-work-record-witness-ata` |
| `session` | `01Lzbh4XPYTAgCKg1dciFS3Q` |
| `head_sha` | `c99589111f82ca4b8a074220cbb5a358b33f5941` |
| `agent_invoked` | `true` |
| `agent_explanation.model` | `gemini-3.5-flash-lite` |
| findings | 2× BLOCK — `deadbee` not a commit; `docs/auth-migration-2026.md` no such path |
| `open` | `true` |
| `stored_at` | `2026-08-29T12:15:09+00:00` |

### PR #1 · `gh pr checks 1` + Checks API

| Check | Conclusion | Object |
|-------|------------|--------|
| `verify-claims` | `failure` | run `33252027654` / job `99099237081` |
| `witness-findings` (P3) | `failure` | check-run `99099248806` · title `Witness gate: BLOCK` · summary `**BLOCK** — 2 BLOCK · 0 UNVERIFIABLE · 0 PASS` |

### Anon mutating routes · `curl -X POST`

| Route | HTTP |
|-------|------|
| `/clearance` | `401` |
| `/break-glass` | `401` |
| `/prove` | `401` |
| `/demo/seed-hold` | `403` |

### Eligibility · `python3 contract/eligibility.py`

| Arm | Result | Exit |
|-----|--------|------|
| This cloud image **before** `pip install -r requirements.txt` | **0 OF 3 MET** | `1` |
| After `pip install -r requirements.txt`, ADC stripped by script | **1 OF 3 MET** (ADK only) | `1` |

Both arms are true. Docs that say "1 of 3 cold" mean the deps-installed stranger path (`requirements.txt`), not a bare `python3` with no ADK package.

### Film bytes · `ffprobe` + `md5sum demo/demo-final-v2.mp4`

| Field | Measured |
|-------|----------|
| duration | `228.349870` s → **3:48.3** |
| md5 | `d327a995166b63ad3a64f248d5104397` |

### Audit · `GET /audit/export`

| Field | Measured |
|-------|----------|
| `exported_at` | `2026-09-18T00:06:38+00:00` |
| events | `25` |
| `CLEAR` decisions | `0` |

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
**Agent night-wave 2026-09-18:** object appendix above; demo-readiness reason corrected to the
v2 film duration measured tonight; placement cells untouched. **Devpost not submitted.**

---

---

## Draft hash (night-wave)

Hash of this file **above this section** (bytes before the `---` rule under Draft hash),
computed 2026-09-18 after the object appendix was filled. Placement cells were not reopened.

```
sha256 (pre-footer body): 84e2e5b0a658ce1a182de59a6ea92e38206cfc3db66583db000315629555332b
```

Recompute: `python3 -c "from pathlib import Path; t=Path('docs/SEALED-PREDICTION-2026-08-29.md').read_text(); print(__import__('hashlib').sha256(t.split('\n---\n\n## Draft hash')[0].rstrip().encode()+b'\n').hexdigest())"`

**Devpost submit: not done (Oscar only).**
