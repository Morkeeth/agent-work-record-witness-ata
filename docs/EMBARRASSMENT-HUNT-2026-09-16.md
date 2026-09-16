# Embarrassment hunt · 16 Sep 2026

Opened the objects judges open — not titles, not checklists.

---

## Finding 1 · live hero `report_preview` still says "required check"

**Object:** `GET /queue` → hold `H-a6151a95ac` → `report_preview`.

**Measured:**

```
HERO_PREVIEW_HAS_REQUIRED_CHECK True
PREVIEW_FIRST_200: # Agent false-done report ...
# Used to prove HOLD as a required check without /demo/seed-hold.
holds_with_required_check_in_preview 4 of 20
```

**Why it matters:** Install tab says do not call it a required check. Branch protection is off.
The stored PR-body comment contradicts the product on the same console.

**Mitigation shipped this run (needs Cloud Run redeploy to reach judges):**

- `surface/hold/index.html` → `judgeSafeText()` strips banned lines + `#` comments before render
- `fixtures/agent-false-done-PR-BODY.md` scrubbed for any future re-post
- Oscar film spine `docs/PITCH-WHEN-YOU-ARE-BACK.md` scrubbed
- `.github/workflows/outcome-gate.yml` header scrubbed
- `film/preflight.sh` now fails if film scripts affirm "required check"

**Still live until Oscar acts:**

- Firestore documents retain the old `report_preview` bytes (API never deletes)
- PR #1 body on GitHub still has the old comment (agent cannot `gh` write)
- Deployed `/hold/` HTML is the previous revision until redeploy

## Finding 2 · "1 of 3 cold" without naming pip

**Object:** `python3 contract/eligibility.py` under two cold shapes.

| Shape | Measured |
|-------|----------|
| No `google-adk` installed | **0 OF 3**, exit 1 |
| After `pip install -r requirements.txt`, no ADC | **1 OF 3** (ADK), exit 1 |

README and PACK said "1 of 3 cold" as if bare clone matched. A judge who runs eligibility
before pip sees **0 of 3** and may call the submission broken. README now names both paths.

## Finding 3 · P3 was live on PR #1 but invisible in README

**Object:** PR #1 check runs + `action.yml` step `check_run_summary.py`.

`witness-findings` conclusion=`failure` on PR #1. Local test green. README had **zero**
mentions of P3 / `check_run_summary` / `witness-findings`. Documented this run.

## What would still embarrass us on camera tomorrow

1. Oscar says "required check" (film spine was wrong until this scrub)
2. Judge opens PR #1 body and reads the old fixture comment
3. Judge runs eligibility bare and gets 0/3 while Devpost paste says 1/3
4. Deployed console without `judgeSafeText` still risks audit fallback text

---

_Commands: curl live `/queue` `/health` · `gh pr view 1` · eligibility two ways · `rg` judge surfaces._
