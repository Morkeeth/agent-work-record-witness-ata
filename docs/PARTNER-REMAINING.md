# Partner integrations · remaining · 29 Aug 2026

**Found by handbook + deep-dive pass.** What exists vs what judges could still see.

---

## Shipped (code in repo)

| ID | Partner | What | Live? |
|----|---------|------|-------|
| P1 | Gemini + ADK | explain on HOLD clearance | ⛔ needs **D1 deploy** |
| P2 | GitHub Action | session · actor · head_sha in JSON | ⛔ needs **D2 re-run PR** |
| P3 | GitHub Checks | `gate/check_run_summary.py` — summary + annotations + `witness-findings` check | ✅ live on PR #1 (`verify-claims` + `witness-findings` both failure) |

---

## Still buildable (ranked)

| ID | Hours | Partner | Judge sees | Mon? |
|----|-------|---------|------------|------|
| **D1** | 15m | Cloud Run | P1+P2 on `/clearance` | **Yes** |
| **D2** | 5m | GitHub | fresh row with metadata | **Yes** |
| **P4** | 4–6h | Cloud Trace | `trace_id` on export · GEAP Observability | If film Sat night |
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

---

## Load-bearing sentence (paste-ready)

> Without **Cloud Run + Firestore**, the CI probe has nowhere to write the receipt the auditor exports. Without **GitHub Actions**, the probe never runs in the customer's repo. **Gemini explains; Python decides.**

---

## Next agent slice

1. Push P3 · re-sync PR #1 to see `witness-findings` check + annotations  
2. Oscar: D1 deploy  
3. P4 only if calendar allows
