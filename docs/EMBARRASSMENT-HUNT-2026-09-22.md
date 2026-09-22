# Embarrassment hunt · 22 Sep 2026 night wave

What could make us look worse than a clean demo. Measured at the object.

---

## Found and fixed in-repo

| Finding | Object | Fix |
|---------|--------|-----|
| Fixture header said "required check" | `fixtures/agent-false-done-PR-BODY.md` | Scrubbed → `verify-claims (advisory…)` |
| Demo printed that header | `./demo.sh` stdout via gate `report:` line | Cleared by fixture scrub; `tests/test_demo.sh` now bans `[Rr]equired [Cc]heck` |
| Pitch spine still said "required check fails" | `docs/PITCH-WHEN-YOU-ARE-BACK.md` | → `verify-claims` |
| Docs claimed only "1 of 3 cold" | README · SUBMISSION-PACK | Three-tier table: 0/3 pip-free · 1/3 ADK · 3/3 ADC |
| `| tee` hid eligibility exit | any piped run | `scripts/eligibility_truth_receipt.sh` asserts exit↔n |
| Probe read `HOLD_FINDINGS` same-step via `GITHUB_ENV` | `action.yml` | export + read `$FINDINGS`; summary takes env explicitly |
| Install tab put the banned phrase on the live console | `surface/hold/index.html` | Reworded without the words "required check" (**needs Cloud Run redeploy** to clear live HTML; source fixed tonight) |

## Found and still live (Oscar / token)

| Finding | Object | Why still red |
|---------|--------|---------------|
| Hero `report_preview` contains `"required check"` | `GET /audit/export` → `H-a6151a95ac` | Firestore row written from old fixture; rewrite needs `HOLD_API_TOKEN` / new clearance post |
| Spoken "one of three on a cold clone" | `film/voiceover.txt` line 7 | True only with ADK installed; pip-free is 0/3. Re-speak is Oscar |
| ADC **3 of 3** | `contract/eligibility.py` with ADC | Unmeasured on this VM (`gcloud` missing, no ADC file) |

## Ban-language survivors (intentional)

README, DEVPOST-CHECKLIST, OSCAR-FILM-CHECKLIST, SUBMISSION-PACK "Do not:" lines, helicon-ci advisory name — they **forbid** the phrase. Not theater.

## Control that went red (useful)

First eligibility measurement tonight used `python3 … \| tee …; echo EXIT:$?` and reported exit 0 while n&lt;3 — because `$?` was tee's. Same class of bug as `grep -qv` on empty input. Receipt script refuses that shape.

## Baseline arm (naive vs demo)

`git cat-file -t deadbee` and `test -f docs/auth-migration-2026.md` both fail without our gate. Naive ties us on SHA/path BLOCK. Demo's unique claim is UNVERIFIABLE→HOLD refusal + durable record. See `docs/STRANGER-PASS-2026-09-22.md`.
