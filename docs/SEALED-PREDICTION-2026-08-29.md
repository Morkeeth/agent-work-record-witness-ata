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

## Re-measured at objects · 2026-09-16 (night wave · do not treat as re-seal)

Oscar's **Sealed at** cell above stays. Numbers below were read tonight from the live
service and PR #1 — not carried from an earlier note.

| Object | Measured |
|--------|----------|
| `GET /health` | ok=True · product='THE AGENT WORK RECORD WITNESS' · auth_required=True · demo_seed_enabled=False · store=firestore · ADK constructed=True · ever_invoked=True |
| `GET /queue` | count=20 · hero `H-a6151a95ac` gate=BLOCK decision=HOLD pr=1 head_sha=`c99589111f82…` session=`01Lzbh4XPYTAgCKg1dciFS3Q` agent_invoked=True traceable=True |
| Hero embarrassment | Firestore `report_preview` still contains **"required check"** on **4/20** holds — UI scrub shipped in `surface/hold/index.html`, Cloud Run deploy pending |
| PR #1 | state=OPEN · verify-claims=FAILURE · witness-findings=FAILURE |
| Eligibility (ADK installed, no ADC) | 1 OF 3 MET — exercised on the path a judge runs. · exit 1 |
| Mutating routes anon | `/clearance` `/break-glass` `/prove` → 401 · `/demo/seed-hold` → 403 |
| `./demo.sh` cold | exit 0 — see `docs/STRANGER-PASS-2026-09-16.md` |
| Film md5 (object) | `demo/demo-final-v2.mp4` md5 `d327a995166b63ad3a64f248d5104397` · duration 228.35s |

**Commands:**

```
curl -sS "$(cat .cloud_run_url)/health"
curl -sS "$(cat .cloud_run_url)/queue"
gh pr view 1 --repo Morkeeth/agent-work-record-witness-ata --json state,statusCheckRollup
python3 contract/eligibility.py
env -i PATH="$PATH" HOME="$HOME" ./demo.sh
./film/preflight.sh
md5sum demo/demo-final-v2.mp4
```


## Draft hash

`sha256:775e836a214a48631819f623c41959e7803a577d4a202c3a4de39ae0d643de80`

SHA-256 of the sealed body: bytes from the start of this file through the end of the
Scoring rubric section (everything **before** `## After results`). Re-derive:

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib
doc = Path('docs/SEALED-PREDICTION-2026-08-29.md').read_text()
# Drop night-wave appendix if present, then take pre-After-results body:
if '## Re-measured at objects' in doc:
    doc = doc.split('## Re-measured at objects')[0]
body = doc.split('## After results')[0]
print(hashlib.sha256(body.encode()).hexdigest())
PY
```
