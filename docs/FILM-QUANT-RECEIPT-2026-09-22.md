# Film quant receipt · ATA · 22 Sep 2026 night wave

**Runner:** Cloud Agent (night wave · sealed + stranger + embarrassment)  
**Repo:** `Morkeeth/agent-work-record-witness-ata` · branch `cursor/night-wave-sealed-stranger-e87b`  
**Live URL:** `https://fleet-wedge-33kamss2jq-uc.a.run.app`  
**Probed at:** 2026-09-22 (UTC)

---

## Summary

| Metric | Result |
|--------|--------|
| Preflight | **PASS** (exit 0 · measured 2026-09-22 night wave) |
| Voiceover / subtitle beat count | **8** = **8** |
| `"required check"` in `film/voiceover.txt` + `film/subtitles.srt` | **absent** (grep -qi; also added as preflight control) |
| Hero `H-a6151a95ac` in `/audit/export` | **yes** |
| PR #1 `verify-claims` | **failure** (red by design) |
| PR #1 `witness-findings` (P3) | **failure** · summary `**BLOCK** — 2 BLOCK · 0 UNVERIFIABLE · 0 PASS` |

---

## Film spine scrub

| Surface | Status |
|---------|--------|
| `film/voiceover.txt` | Uses `verify-claims` · says both 3/3 and 1/3 · no `"required check"` |
| `film/subtitles.srt` | Matches 8 spoken lines · no `"required check"` |
| `docs/PITCH-WHEN-YOU-ARE-BACK.md` | Was `"required check fails"` → scrubbed to `verify-claims` |
| Live Firestore `report_preview` on hero | **Still contains** `"required check"` from pre-scrub fixture — not rewritten tonight |

### Oscar decision (spoken eligibility)

Voiceover line 7: *"three of three with credentials here; one of three on a cold clone without GCP."*

Re-measured 2026-09-22:

| Arm | n OF 3 | Exit |
|-----|--------|------|
| ADC + Vertex + Firestore | unmeasured on this VM | — |
| `google-adk` installed, no ADC | **1** | 1 |
| Pip-free cold (`PYTHONNOUSERSITE=1`) | **0** | 1 |

The spoken "one of three" is true for the **ADK-installed** cold arm (film machine shape). It is **false** for a pip-free stranger clone. `./demo.sh` still exits 0 with no packages. Oscar: re-speak to name both cold arms, or keep as-is and let README/PACK carry the three-tier table.

---

## Preflight log

```
ok: checking canonical numbers in voiceover + SUBMISSION.md
ok: voiceover + subtitles clean of 'required check'
ok: hold console carries 41.7 -> 8.1, H-a6151a95ac, finding + stack screens
ok: 8 spoken lines match 8 subtitle blocks
ok: ./demo.sh (cold, no network)
ok: demo.sh exit 0
ok: /health live payload
  health fields match
ok: record row H-a6151a95ac
ok: record H-a6151a95ac present
  note: .hold_api_token missing — create before live break-glass on camera (read probe passed without it)
ok: PR #1 verify-claims red-by-design
ok: PR #1 open
ok: verify-claims conclusion=failure (red by design, asserted at the object)

PREFLIGHT PASS — safe to run ./film/capture.sh and record.
PREFLIGHT_EXIT:0
```

---

*Night wave · do not run `./film/capture.sh` from the agent.*
