# Film quant receipt · ATA · 16 Sep 2026 (night wave refresh)

**Runner:** Cloud Agent (preflight + live probes)  
**Repo:** `Morkeeth/agent-work-record-witness-ata` @ branch `cursor/night-wave-sealed-stranger-d799`  
**Live URL:** `https://fleet-wedge-33kamss2jq-uc.a.run.app`  
**Probed at:** 2026-09-16

Supersedes the 29 Aug receipt for preflight drift only. Film capture still Oscar-only.

---

## Summary

| Metric | Result |
|--------|--------|
| Preflight | **PREFLIGHT PASS** (command: `./film/preflight.sh`) |
| New checks this run | film scripts ban `required check` · `judgeSafeText` present in hold console |
| Voiceover / subtitle cues | **8 = 8** |
| `./demo.sh` cold | exit **0** |
| Hero `H-a6151a95ac` | present in `/audit/export` |
| Film object | `demo/demo-final-v2.mp4` md5 `d327a995166b63ad3a64f248d5104397` · duration **228.35s** |

---

## Preflight log (verbatim tail)

```
ok: film scripts ban 'required check'
ok: hold console carries judgeSafeText scrub
ok: hold console carries 41.7 -> 8.1, H-a6151a95ac, finding + stack screens
ok: 8 spoken lines match 8 subtitle blocks
ok: ./demo.sh (cold, no network)
ok: demo.sh exit 0
ok: /health live payload
ok: record row H-a6151a95ac
ok: record H-a6151a95ac present
ok: PR #1 verify-claims red-by-design
ok: PR #1 open
ok: verify-claims conclusion=failure (red by design, asserted at the object)

PREFLIGHT PASS — safe to run ./film/capture.sh and record.
```

---

## Drift fixed this run (not film audio)

- Oscar film spine (`docs/PITCH-WHEN-YOU-ARE-BACK.md`) said "required check" — scrubbed to `verify-claims`
- `film/voiceover.txt` / `film/subtitles.srt` already clean — preflight now enforces the ban
- Deployed Cloud Run HTML does **not** yet include `judgeSafeText` — Oscar redeploy before camera if audit fallback must scrub live

---

## Not done (Oscar)

- [ ] `./film/capture.sh` / screen record ≤4:00
- [ ] Cloud Run redeploy of `surface/hold/index.html`
- [ ] Devpost submit · share repo with judges
