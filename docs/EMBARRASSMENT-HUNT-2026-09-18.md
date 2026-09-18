# Embarrassment hunt · 18 Sep 2026 night wave

**Rule:** open the object. A nearer proxy is how four Qwen-loss diagnoses failed.

---

## Baseline arm (naive · ~2 min)

```bash
grep -Rni 'required check' film/voiceover.txt film/subtitles.srt film/voiceover-vo.txt
# → 0 hits. Scrub looks done.
```

## Object arm (what a judge actually sees)

| Object | Command | Measured |
|--------|---------|----------|
| `./demo.sh` stdout | `env -i PATH="$PATH" HOME="$HOME" ./demo.sh \| grep -ni 'required check'` | **HIT** before fix — fixture comment truncated into the report preview |
| Live export hero | `curl -sS …/audit/export` → `H-a6151a95ac.report_preview` | **HIT** — stored preview still starts with the old fixture comment |
| PR #1 body | `gh pr view 1 --json body -q .body` | **HIT** — same fixture text live on GitHub |
| `/hold/` detail UI (browser) | open card `H-a6151a95ac` | **no** literal `required check` in rendered detail (Gemini explain + evidence table); contamination is in export/PR body, not the painted card |
| `tests/test_demo.sh` | patterns `'As a required PR check'` / `'As an required'` | **FALSE GREEN** — PASS while demo stdout contained `required check` |
| `/hold/` Install tab | curl HTML | advisory only: *"do not call it a required check"* (allowed) |
| Film voiceover/SRT | grep | clean (0 hits) |
| `/health` product | curl | `THE AGENT WORK RECORD WITNESS` — not `HOLD` |
| IAM wording on `/hold/` | HTML | *"public at the IAM layer by design"* · *"application token gate (not IAM)"* — matches PACK |

### Baseline vs object

Naive film grep: **clean**. Object path (demo + PR body + export): **contaminated**. The control that graded the stranger path was itself the defect.

**Watchable red control (this run):** `./tests/test_live_preview_scrub.sh` → exit **1** (hero preview RED · PR #1 body RED). A control that has not been watched going red is not a control.

---

## Fixes landed this run (repo)

- [x] `fixtures/agent-false-done-PR-BODY.md` — removed affirmative "required check"
- [x] `tests/test_demo.sh` — substring `required check` (case-insensitive); proved green after fix
- [x] `.github/workflows/outcome-gate.yml` header comment
- [x] `scripts/open_agent_hold_pr.sh` commit template
- [x] Judge-facing pitch docs: `PITCH-WHEN-YOU-ARE-BACK`, `THE-PITCH-RULING`, `HOLD-AMBITIOUS-GOAL` (also corrected stale `product=HOLD`)

## Still live until Oscar clicks (not claimed fixed)

- PR #1 **body** on GitHub still carries the old comment (gh write blocked for this agent).
- Firestore **report_preview** on `H-a6151a95ac` still carries the old comment until a fresh clearance rewrite.
- Historical commit message on PR #1: `demo: agent false-done PR marker for HOLD required check`.

**Oscar path to close:** edit PR #1 body to match the scrubbed fixture → synchronize → confirm new export preview.

---

## Eligibility re-derived this VM (not carried)

```bash
python3 contract/eligibility.py; echo exit:$?
# → 0 OF 3 MET, exit 1
# Gemini UNMEASURED · ADK missing (pip install google-adk) · JsonlStore default
```

Docs' "1 of 3 cold" assumes ADK constructible. This cold clone without `google-adk` measures **0 of 3**. Both true for different environments; say which one you ran.

---

_Probed 2026-09-18T12:22Z · live base `https://fleet-wedge-33kamss2jq-uc.a.run.app`_
