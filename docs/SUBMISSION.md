# THE AGENT WORK RECORD WITNESS — canonical submission

**Supersedes:** `docs/PITCH-WHEN-YOU-ARE-BACK.md` · `docs/THE-PITCH-RULING.md`

**Lane:** film capture only. Oscar records, submits Devpost, redeploys if he chooses.
**Verified:** 2026-08-29 · `film/fixed.json` · live probes in `docs/FILM-READY-2026-08-29.md`

---

## 1 · Product

**THE AGENT WORK RECORD WITNESS** — said in full on camera, at least twice.
The queue inside it is **Hold**. `HOLD` is a verdict value, not the product name.

## 2 · Three data pipes

| Layer | Source | Stranger-safe |
|---|---|---|
| **Gate** | `./demo.sh` — synthetic repo, no network | ✅ |
| **Record** | PR #1 → Action → Firestore → `/hold/` | ✅ after `agent` label |
| **Corpus** | Customer Transcripto DB; sample in `fixtures/corpus-sample-40.json` | day-two |

## 3 · Live surfaces (film pins)

| Surface | Object |
|---|---|
| Service URL | `https://fleet-wedge-33kamss2jq-uc.a.run.app` (`.cloud_run_url`) |
| `/health` | `auth_required: true` · `demo_seed_enabled: false` · `store: firestore` |
| PR #1 | https://github.com/Morkeeth/agent-work-record-witness-ata/pull/1 · `verify-claims` → **FAILURE** |
| Record row | `H-57b130f397` on `GET /queue` |
| Corpus headline | `surface/fleet-report-page.html` → `window.__FLEET_REPORT__` |

## 4 · Capture harness

```bash
./film/preflight.sh    # must exit 0 before rolling — live == fixed-by-hash
./film/capture.sh      # one command, every beat, deterministic timing
```

Voiceover: `film/voiceover.txt` (Kokoro / `~/CODE/voice-generation`, local, free).
Subtitles: `film/subtitles.srt` — generated from the same lines; never edit separately.

## 5 · Banned on camera

Seed button · shortening the product name · "42%" without denominator · claiming green on PR #1.

## 6 · Honest limits

- `41.7% → 8.1%` is method on Oscar's `~/.trace/trace.db`, not shipped data.
- `clear: 0` — the one real claim was false and was held.
- Zero non-author installs.

## 7 · Film spine — six beats (≤3:00)

One line of voiceover per beat in `film/voiceover.txt`. Terminal capture replays the same order.

| Beat | Time | On camera | Voiceover file line |
|---|---|---|---|
| **1 · Problem** | 0:00–0:25 | Title / hold on terminal | 1 |
| **2 · Stranger gate** | 0:25–1:05 | `env -i … ./demo.sh` | 2 |
| **3 · Real PR** | 1:05–1:35 | PR #1 · `verify-claims` red | 3 |
| **4 · The record** | 1:35–2:10 | `/hold/` · open `H-57b130f397` | 4 |
| **5 · Four verdicts** | 2:10–2:40 | PASS · BLOCK · HOLD · UNVERIFIABLE | 5 |
| **6 · Honest close** | 2:40–3:00 | `41.7%` beside `8.1%` · gap was ours | 6 |

### §7 spoken numbers — inventory and proof object

Every number below appears in `film/voiceover.txt` line *n*. Preflight proves live == `film/fixed.json`.

| # | Spoken (beat) | Value | Proof object |
|---|---|---|---|
| 1 | three-minute (1) | 3:00 | `film/fixed.json` → `spine.duration_seconds` |
| 2 | fourteen tests (2) | 14 | `demo.sh` hold beat · `grep '14 tests' demo.sh` |
| 3 | exit zero (2) | 0 | `./demo.sh` → `GATE: PASS` · `exit 0` |
| 4 | exit one (2,5) | 1 | `./demo.sh` → `GATE: BLOCK` · `exit 1` |
| 5 | exit two (2,5) | 2 | `./demo.sh` → `GATE: HOLD` · `exit 2` |
| 6 | pull request one (3,4) | 1 | `gh pr view 1` · `film/fixed.json` → `pr.number` |
| 7 | forty-one point seven percent (6) | 41.7% | `surface/fleet-report-page.html` → `raw_disagree/raw_sha_claims` |
| 8 | eight point one percent (6) | 8.1% | `surface/fleet-report-page.html` → `corrected_disagree/corrected_sha_claims` |
| 9 | two hundred forty-seven (6) | 247 | `window.__FLEET_REPORT__.raw_sha_claims` |
| 10 | one hundred three (6) | 103 | `window.__FLEET_REPORT__.raw_disagree` |
| 11 | two hundred thirty-six (6) | 236 | `window.__FLEET_REPORT__.corrected_sha_claims` |
| 12 | nineteen (6) | 19 | `window.__FLEET_REPORT__.corrected_disagree` |
| 13 | seventy-three (6) | 73 | `window.__FLEET_REPORT__.resolved_in_a_sibling_repo` |
| 14 | eleven (6) | 11 | `window.__FLEET_REPORT__.dropped_as_machinery_or_fixture` |
| 15 | seven (6) | 7 | `window.__FLEET_REPORT__.path_claims_not_checkable` |
| 16 | hold id (4) | `H-57b130f397` | `GET /queue` → holds[] where `source=github-action` |
| 17 | session (4) | `01Lzbh4XPYTAgCKg1dciFS3Q` | same row · `fixtures/agent-false-done-PR-BODY.md` trailer |

**Not spoken on camera (preflight only):** `auth_required: true`, `demo_seed_enabled: false`, `store: firestore`, `constructed: true`, `invoked: false` — pinned in `film/fixed.json` → `health` so the `/health` curl in capture cannot drift.

### §7 beat commands (capture order)

```bash
./film/capture.sh
# internally:
#   beat 2 → env -i HOME=/tmp PATH=/usr/bin:/bin /bin/bash ./demo.sh
#   beat 3 → gh pr view 1 --json state,statusCheckRollup
#   beat 4 → curl -s $URL/queue | jq '.holds[] | select(.id=="H-57b130f397")'
#   beat 5 → film/verdicts.txt (PASS BLOCK HOLD UNVERIFIABLE + exit codes)
#   beat 6 → film/corpus-close.txt (41.7 / 8.1 pair from fleet-report-page.html)
```

---

## References

- `docs/FILM-READY-2026-08-29.md` — verified live state
- `docs/REDEPLOY-RUNBOOK-2026-08-29.md` — Oscar-only redeploy
- `SUBMISSION-PACK.md` — Devpost paste (not this doc)
- `FILM-SHOT-LIST-2026-08-28.md` — extended shot notes
