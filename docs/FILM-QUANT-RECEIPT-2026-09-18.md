# Film quant receipt · ATA · refreshed 18 Sep 2026

**Runner:** Cloud Agent night wave  
**Repo:** `Morkeeth/agent-work-record-witness-ata` @ branch `cursor/night-wave-sealed-stranger-fa3b`  
**Live URL:** `https://fleet-wedge-33kamss2jq-uc.a.run.app`  
**Probed at:** 2026-09-18T12:22Z (preflight re-run after scrub)

Prior: [`FILM-QUANT-RECEIPT-2026-08-29.md`](FILM-QUANT-RECEIPT-2026-08-29.md)

---

## Summary

| Metric | Result |
|--------|--------|
| Preflight | **PASS** (11 ok) |
| Voiceover / SRT beat count | **8 = 8** |
| `required check` in `film/voiceover.txt` · `subtitles.srt` · `voiceover-vo.txt` | **0** (grep) |
| Hero `H-a6151a95ac` in `/audit/export` | **yes** |
| PR #1 `verify-claims` | **failure** (red by design) |

**Verdict:** PREFLIGHT PASS — film assets match scrubbed copy (no "required check" on voiceover/subtitles). Capture still Oscar-only (`./film/capture.sh` not run).

---

## Preflight log (verbatim · this run)

```
ok: checking canonical numbers in voiceover + SUBMISSION.md
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
```

## Spine check vs EYES B

| Beat | Voiceover line | Status |
|------|----------------|--------|
| Moat at hold | "None of them holds the transcript." | present (line 2) |
| PR #1 red | verify-claims + witness-findings · deadbee · H-a6151a95ac | present (line 3) |
| Cold demo | `./demo.sh` · no account · no network | present (line 4) |
| Corpus mid-beat | 41.7 → 8.1 | present (line 6) |
| Both eligibility | 3/3 with credentials · 1/3 cold | present (line 7) |
| Ban "required check" | — | **absent** from VO + SRT |

---

*Film quant refreshed 2026-09-18 · no capture.sh*
