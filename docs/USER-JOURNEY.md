# USER JOURNEY — three actors, ranked

Every step maps to a probe and a video second. Built for the Fortified Enterprise Fleet track.

## Actor 1 — Rollout owner (VP Eng / Head of Enablement)

| Step | They do | System does | Probe | Video |
|---|---|---|---|---|
| R1 | Opt-in a team corpus | Index human turns only (`promptSource` gate) | authorship filter | 20–50s |
| R2 | Ask "who prompts well on auth refactors?" | Pairwise task-class + episode scores | `fleet_cli.py prove` | 50–110s |
| R3 | Approve propagate (or watch auto in demo) | Literal prompt → org skill file | witness `VERIFIED-BY-REPO` | 110–150s |
| R4 | See Cloud proof | Firestore / Cloud Run | `eligibility.py` 3/3 | 150–190s |

**Day-2 value they buy:** next engineer starts from the best prompt without opening a coaching UI.

## Actor 2 — Engineer B (the one who needed corrections)

| Step | They do | System does | Probe |
|---|---|---|---|
| B1 | Type a vague opener | Episode opens; corrective turns counted | `landed_corrected` |
| B2 | Receive propagated skill | Skill file present on next session | file witness |
| B3 | (Week 3) Re-run same class | Before/after corrective turns | causal falsifier |

**Honest Week 0:** B1–B2 are demoed on fixtures. B3 is the post-submit moonshot.

## Actor 3 — Stranger / judge

| Step | They do | Expected |
|---|---|---|
| S1 | `git clone` · `python3 fleet_cli.py wedge` | operator **a** · `VERIFIED-BY-REPO` |
| S2 | `python3 contract/eligibility.py` | **3 OF 3 MET** (with ADC) or honest 1/3 without |
| S3 | `python3 fleet_cli.py prove` · open HTML | A 0 vs B 2 corrective turns |
| S4 | `./scripts/stranger_wedge.sh` | STRANGER OK |
| S5 | Hit Cloud Run `/wedge` (after deploy) | 201 + Firestore record |

## Non-negotiables

- Nothing from a transcript is executed.
- `UNMEASURED` prints when the field is too thin for an org claim.
- No "8/8 classifier" seal while C1 is red.
