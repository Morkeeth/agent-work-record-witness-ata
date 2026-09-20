# Film quant receipt · ATA · refreshed 20 Sep 2026 (orig. 29 Aug)

**Runner:** Cloud Agent night wave  
**Repo:** `Morkeeth/agent-work-record-witness-ata`  
**Live URL:** `https://fleet-wedge-33kamss2jq-uc.a.run.app`  
**Probed at:** 2026-09-20T00:06–00:10Z

---

## Summary

| Metric | Result |
|--------|--------|
| Preflight checks | **11 ok / 11 total** · `PREFLIGHT PASS` |
| `./demo.sh` cold exit | **0** |
| `film/` voiceover ? subtitles | **8 = 8** · no `required check` |
| Hero record `H-a6151a95ac` in `/audit/export` | **yes** |
| PR #1 | OPEN · `verify-claims` FAILURE · `witness-findings` FAILURE |
| Shipped film length (object) | `demo/demo-final-v2.mp4` **228.35 s = 3:48.3** · md5 `d327a995166b63ad3a64f248d5104397` |

**Verdict:** PREFLIGHT PASS — safe for Oscar to roll `./film/capture.sh` (agents: do **not** run capture).

---

## Film spine scrub (EYES B)

| Surface | `required check` | Notes |
|---------|------------------|-------|
| `film/voiceover.txt` | clean | says `verify-claims` + both eligibility numbers |
| `film/subtitles.srt` | clean | 8 cues match 8 VO lines |
| `demo/voiceover.txt` / `demo/demo-final-v2.srt` | clean of required-check | **still says "append only" twice** (lines 131, 187 in SRT) — known; needs Oscar re-cut, not an agent edit of the MP4 |

Preflight watches `film/`, not the shipped `demo/` cut. Drift called here so it cannot hide behind a green preflight.

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

Command: `./film/preflight.sh` · exit 0.

---

## Live `/health` (this run)

| Field | Value |
|-------|-------|
| `auth_required` | `true` |
| `demo_seed_enabled` | `false` |
| `store` | `firestore` |
| ADK constructed | `true` |
| product | THE AGENT WORK RECORD WITNESS |

---

## Not done (Oscar)

- [ ] Re-cut shipped film to remove "append only" (record is a keyed store)
- [ ] Devpost submit / share with judges — Oscar only

---

*Stack tab on live `/hold/` claims revision `fleet-wedge-00014-q2g` · gcloud describe not available on this runner.*
