# Partner integrations · remaining · refreshed 20 Sep 2026

**Found by handbook + deep-dive pass.** What exists vs what judges could still see.

---

## Shipped (code in repo · live where noted)

| ID | Partner | What | Live? |
|----|---------|------|-------|
| P1 | Gemini + ADK | explain on HOLD clearance | ✅ live on hero `H-a6151a95ac` (`agent_explanation.invoked: true`, model `gemini-3.5-flash-lite`) — re-probed 2026-09-20 |
| P2 | GitHub Action | session · actor · head_sha in JSON | ✅ hero carries `head_sha` + `session` · PR #1 join |
| P3 | GitHub Checks | `gate/check_run_summary.py` — summary + annotations + `witness-findings` check | ✅ on main path (`action.yml` step `summary`) · PR #1 shows `witness-findings` FAILURE · receipt [`P3-CHECK-SUMMARY-RECEIPT-2026-09-20.md`](P3-CHECK-SUMMARY-RECEIPT-2026-09-20.md) |

---

## Still buildable (ranked)

| ID | Hours | Partner | Judge sees | Mon? |
|----|-------|---------|------------|------|
| **P4** | 4–6h | Cloud Trace | `trace_id` on export · GEAP Observability | Post-submit |
| **P5** | 4–6h | Vertex session | second `/agent/run` resumes session | Post-submit |
| **P6** | 3h | local guard | injection/length on `report` before probe | Post-submit |
| **P7** | 2h | Pub/Sub | fan-out without consumer | **Skip** |

---

## GEAP gap (R-ranks) · not on witness path

| ID | Surface | Note |
|----|---------|------|
| R4 | Memory Bank | VertexAiSessionService — same as P5 |
| R5 | Observability | same as P4 |
| R6 | Identity | per-agent tokens — 6h |
| R7 | Model Armor | local guard — same as P6; **never name Google product** |
| R8 | Registry | skill registry — 1 day; `/prove` is not a registry |

---

## Theater to avoid (already scrubbed or off-path)

| Item | Status |
|------|--------|
| `gemini_same_count` on `surface/org-proof.html` | **Off film path** — org-lift; F2 in GEAP-GAP |
| Memory Bank / Registry claims | roadmap only in copy |
| `/prove` on `/hold/` Registry tab | labeled module not hero |
| Calling the check "required" | scrubbed 2026-09-20 — workflow comment, pitch docs, fixture used by `./demo.sh` |

---

## Load-bearing sentence (paste-ready)

> Without **Cloud Run + Firestore**, the CI probe has nowhere to write the receipt the auditor exports. Without **GitHub Actions**, the probe never runs in the customer's repo. **Gemini explains; Python decides.**

---

## Next

1. Oscar: film / Devpost — outward acts only
2. P4 only if calendar allows
