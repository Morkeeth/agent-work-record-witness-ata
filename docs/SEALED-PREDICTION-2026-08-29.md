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

## Measured objects (night wave · 2026-08-31 UTC)

Every row probed tonight at the object — not copied from another doc.

| Object | Command | Measured |
|--------|---------|----------|
| Live `/health` | `curl -sS https://fleet-wedge-33kamss2jq-uc.a.run.app/health` | `ok: true` · `auth_required: true` · `demo_seed_enabled: false` · `store: firestore` · `product: THE AGENT WORK RECORD WITNESS` |
| Read routes (anon) | `for r in /health /hold/ /audit/export /policy /queue; do curl -sS -o /dev/null -w "%{http_code} $r\n" …; done` | **5/5 → 200** |
| Mutating routes (anon) | `for r in /clearance /break-glass /prove /wedge /policy; do curl -sS -o /dev/null -w "%{http_code} POST $r\n" -X POST …; done` | **5/5 → 401** |
| Audit cleared | `curl -sS …/audit \| python3 -c "…pct_cleared_without_hold…"` | **0.0%** cleared without hold · **49** events in `/audit` · **25** in `/audit/export` |
| Hero record | `curl -sS …/audit/export \| jq '.events[] \| select(.id=="H-a6151a95ac")'` | `gate: BLOCK` · `decision: HOLD` · `session: 01Lzbh4XPYTAgCKg1dciFS3Q` · `head_sha: c99589111f82ca4b8a074220cbb5a358b33f5941` · `agent_invoked: true` · **2** BLOCK findings (`deadbee`, `docs/auth-migration-2026.md`) · `stored_at: 2026-08-29T12:15:09+00:00` |
| PR #1 checks | `gh api repos/Morkeeth/agent-work-record-witness-ata/commits/c995891…/check-runs` | `verify-claims` → **failure** · `witness-findings` → **failure** (P3) · PR **open** · head `c99589111f82ca4b8a074220cbb5a358b33f5941` |
| Stranger path | `env -i PATH="$PATH" HOME="$HOME" ./demo.sh` | **exit 0** · `tests/test_demo.sh` **11/11 PASS** (incl. never-say *required check*) |
| Film preflight | `./film/preflight.sh` | **PASS** · 8 voiceover lines = 8 subtitle cues · hero record present · PR #1 red-by-design |
| Eligibility (this VM) | `python3 contract/eligibility.py` | **1 OF 3 MET**, exit **1** — ADK only; no ADC/Gemini/Firestore round-trip in this stripped pod. **Not re-claimed as 3/3 here.** Prior 3/3+1/3 pair is in `docs/SHIP-VERIFICATION-2026-08-31.md` §A from a credentialed run. |

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
**Night wave 2026-08-31:** measured-objects table filled from live `/hold/` + PR #1 + stranger
path; draft hash in footer below.

**Draft sha256:** `b64a22c013d80c5abb039525c7f3239f1d70a25593fe855c43f5a22a6e4e4bda` — computed over this file excluding this line.
