# Embarrassment hunt · night wave 2026-09-20

Things that would make us look worse if a judge found them first. Found by opening the
object, not by reading the pitch.

| # | Object | Finding | Fix / status |
|---|--------|---------|--------------|
| 1 | `fixtures/agent-false-done-PR-BODY.md` fed to `./demo.sh` | Cold `main` clone prints `# Used to prove HOLD as a required check` in the BLOCK report preview | Scrubbed on this branch; `tests/test_demo.sh` bans the substring |
| 2 | Prior sealed draft | `sha256:PENDING` — a seal that was never hashed | Hash stamped this run (see `SEALED-PREDICTION` footer) |
| 3 | Prior sealed draft `/audit/export` row | Claimed “open holds 21 / closed 3” on export; those counts are on `/audit` (49 events). Export: 25 events, 21 open clearances, 1 closed clearance | Corrected in measured table |
| 4 | `docs/PARTNER-INTEGRATION…` §8 paste block | Said “IAM-gated APIs” while `/hold/` Stack tab says Cloud Run is public at IAM (`allUsers`) and the 401 is the app token | Reworded to application-token-gated |
| 5 | Partner theater table | Affirmative `"Required check"` as the theater cell | Relabeled as theater to avoid |
| 6 | `.github/workflows/outcome-gate.yml` header | “Required check for agent-authored PRs” while protection is off | Advisory wording |
| 7 | Pitch docs (`THE-PITCH-RULING`, `PITCH-WHEN-YOU-ARE-BACK`, `HOLD-AMBITIOUS-GOAL`) | Affirmative “required check” | → `verify-claims` / advisory |
| 8 | `demo/demo-final-v2.srt` | Says “append only” twice; product truth is keyed store | **Oscar re-cut** — agent must not rewrite the MP4 |
| 9 | `eval/run_eval.py` | Always-silent NULL beats headline arm on accuracy (67.5% vs 45.0%) | Disclosed in sealed prediction + `EVAL-NIGHT-RECEIPT` — do not hide |
| 10 | Bare `contract/eligibility.py` | **0 of 3** without ADK; older copy said cold is 1/3 without saying the ADK precondition | Documented in PACK + sealed falsifiers |

## Grep still allowed (meta / ban lists)

Judge-facing ban lists that *forbid* the phrase are fine. Affirmative product claims are not.

```bash
rg -n -i 'required check' --glob '!docs/EMBARRASSMENT*' --glob '!hack.md' .
```

## Commands that proved the rows

```bash
# 1 — leak on main clone
git clone --depth 1 https://github.com/Morkeeth/agent-work-record-witness-ata.git /tmp/stranger-gh
env -i PATH="$PATH" HOME="$HOME" /tmp/stranger-gh/demo.sh | rg -i 'required check'

# 1b — clean on this tree
env -i PATH="$PATH" HOME="$HOME" ./demo.sh | rg -i 'required check' || echo clean

# 3 — endpoint split
python3 -c "import json,urllib.request as u
a=json.load(u.urlopen('https://fleet-wedge-33kamss2jq-uc.a.run.app/audit'))
e=json.load(u.urlopen('https://fleet-wedge-33kamss2jq-uc.a.run.app/audit/export'))
print('audit', len(a['events']), 'open', sum(1 for x in a['events'] if x.get('open') is True), 'closed', sum(1 for x in a['events'] if x.get('open') is False))
print('export', len(e['events']), 'open_clear', sum(1 for x in e['events'] if x.get('kind')=='clearance' and x.get('open') is True))"

# 8
rg -n 'append only' demo/demo-final-v2.srt

# 9
python3 eval/run_eval.py | tail -20
```
