# Film quant receipt · ATA · 16 Sep 2026 (film morning re-probe)

**Runner:** Cloud Agent (preflight + quant + Playwright)  
**Repo:** `Morkeeth/agent-work-record-witness-ata` @ branch `cursor/night-wave-film-morning-e7e3`  
**Live URL:** `https://fleet-wedge-33kamss2jq-uc.a.run.app`  
**Probed at:** 2026-09-16 (UTC)

Supersedes the 2026-08-29 receipt for any number that drifted. Numbers below were re-derived
at the object tonight — not carried forward.

---

## Summary

| Metric | Result |
|--------|--------|
| Preflight | **PASS** (`./film/preflight.sh` ? `PREFLIGHT PASS`) |
| `./demo.sh` cold exit | **0** |
| Voiceover / subtitle beats | **8 = 8** |
| "required check" in voiceover/SRT | **absent** (`rg` clean) |
| Eligibility language | says **both** 3/3 (ADC) and 1/3 (cold) — not unqualified |
| Hero in `/audit/export` | **yes** |
| Hero in `/queue` | **yes · index 13** (first card is `H-56f6e3a047`) |
| Deep link `?record=H-a6151a95ac` | **works** (Playwright · session visible · no tab loop) |
| Live `/hold/` theme | `--primary: #1a73e8` · `--sans: "Roboto"` (not Google Sans) |
| PR #1 | OPEN · `verify-claims=FAILURE` · `witness-findings=FAILURE` |

**Verdict:** PREFLIGHT PASS. Judge/film path must use `?record=H-a6151a95ac`, not "first card".

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

---

## Drift found tonight (embarrassing · fixed in docs, UI sort pending redeploy)

1. **README / PACK said "click the first card (H-a6151a95ac)".** Live `/queue` first card is
   `H-56f6e3a047` (corpus-scan, `session=null`). Hero at index 13. Fixed: deep link restored.
2. **FILM-QUANT-RECEIPT-2026-08-29 claimed `--sans: "Google Sans"`.** Live HTML (byte-identical
   to `surface/hold/index.html`) uses `"Roboto"`. Corrected in this receipt.
3. **`openClearance` re-called `tab("queue")` ? `loadQueue`**, wiping `.mark.on` on deep link.
   Fixed in `surface/hold/index.html` (needs Oscar redeploy to reach live).
4. **Queue sort buried session joins.** Client-side sort floats `session+traceable` (esp.
   `01…` Claude-shaped sessions) to the top — also needs redeploy.

---

## Hero record · live

| Field | Value |
|-------|-------|
| Record ID | `H-a6151a95ac` |
| Session | `01Lzbh4XPYTAgCKg1dciFS3Q` |
| head_sha | `c99589111f82ca4b8a074220cbb5a358b33f5941` |
| gate / decision | BLOCK / HOLD |
| agent_explanation.invoked | true · `gemini-3.5-flash-lite` |
| pct_cleared_without_hold | 0.0 |

---

## Oscar / post-receipt

- [ ] Redeploy Cloud Run so queue sort + deep-link highlight ship to live HTML
- [ ] Screen recording ?4:00 — open `?record=H-a6151a95ac`, never say "required check"
- [ ] Do **not** click the first card on an unreployed console

---

*Live HTML md5 `ca7f2c0dfbbfd2792b052ca7559b8d24` · matched repo file before this branch's UI edits.*
