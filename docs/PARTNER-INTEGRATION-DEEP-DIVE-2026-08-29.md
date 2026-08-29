# Partner integration deep dive · ATA · 29 Aug 2026

**Question:** How do we use Google (and adjacent) partners **more deeply** without theater?

**Canonical stack probe:** `python3 contract/eligibility.py` · **GEAP measurement:** `docs/GEAP-GAP-2026-08-27.md`  
**Architecture:** `docs/ARCHITECTURE.md` · **Ingest vision:** `docs/GEMINI-STACK-TAILORING.md`

Not legal advice. Not a commitment to build everything here before Devpost.

---

## 1. Two partner layers

| Layer | Who | Relationship to Witness |
|-------|-----|------------------------|
| **Mandatory (hackathon)** | Gemini 3.5+ · ADK · Cloud Run · Firestore | Must be **exercised**, not imported — eligibility script is the bar |
| **Complementary (ecosystem)** | GitHub · Transcripto · Zenity · Qodo · Langfuse | **Not competitors** — they lack transcript + claim-vs-object; Witness fills the gap |
| **GEAP enterprise (judge vocabulary)** | Registry · Runtime · Memory Bank · Identity · Gateway · Model Armor · Observability | Map Witness features to **their words**; only claim what is wired |

**The moat sentence (keep):** Zenity governs *actions*; Qodo reviews *diffs*; Langfuse scores *traces*; **none holds the transcript**, so none can answer what happened before the claim was written.

---

## 2. Current depth vs possible depth

| Partner / surface | Today (probed) | Deeper (honest) | Theater (do not claim) |
|-------------------|----------------|-----------------|------------------------|
| **Gemini / Vertex** | `classify()` in eligibility; task-class path | **Explain BLOCK** on clearance — model narrates findings, never overrules probe | "Gemini decides merge" |
| **ADK** | `build_agent()` on `/health`; **`POST /agent/run`** with Runner + tool calls | Call **`run_agent()` after HOLD** with findings as context; store receipt on record | `type(LlmAgent)` on `/health` = "agent ran" |
| **Cloud Run** | `fleet-wedge` live · `/health` · auth on mutating routes | Same service; show `*.run.app` on film | Multi-service mesh |
| **Firestore** | Append-only record · `H-a6151a95ac` from real Action | Index by `session`, `repo`, `source` for console browse | "Real-time analytics" |
| **GitHub Actions** | Composite action · PR #1 posts `/clearance` | **Checks API** annotations · pass `session` + `actor` in JSON body | "Required check" (branch unprotected) |
| **GEAP Sessions** | `session` field on record (foreign key) | **VertexAiSessionService** — resume ADK run with same session id | "Memory Bank" without retrieval |
| **GEAP Memory Bank** | Not wired | Write clearance summary artifact; read on repeat query | Retrieval loop that does not exist |
| **Cloud Trace / OTel** | Not wired | Span per `/clearance` · `trace_id` on Firestore row | "Full observability platform" |
| **Transcripto** | Roadmap in diagram | Action posts `session=<transcripto-id>`; join opens transcript | Corpus on film without judge DB |
| **Model Armor (Google product)** | Not wired | Local injection guard on `report` text before probe | Name the product without API |
| **Agent Registry (GEAP)** | `/prove` = prompt propagation | **`GET /registry`** for skill versions — call it **skill registry** | Call `/prove` a "registry" |
| **Pub/Sub** | Not wired | Publish `clearance.hold` events for SIEM | Fan-out analysts |

**Score today (GEAP seven):** 0 present · 3 partial (Gateway, Observability, Identity) · 4 absent — see gap doc.

---

## 3. The integration spine (one sentence)

```
GitHub Action (local probe) → POST /clearance → Firestore record → /hold/ join → session/transcript
                                    ↓ optional
                              ADK + Gemini (explain only, never overrule)
```

**Load-bearing rule:** Probes decide PASS/BLOCK/UNVERIFIABLE/HOLD. Partners **surround** that decision — they do not replace it.

---

## 4. Google stack — five depths (pick per slice)

### Depth A · Compliance (where you are)

- `eligibility.py` → 3/3 with ADC, 1/3 cold
- Film: show **both** numbers

### Depth B · Gateway + record (where you win)

- Cloud Run policy · enforce vs report-only · break-glass with reason
- Firestore export · `/audit/export` for auditors
- **Film beat:** PR #1 red → row `H-a6151a95ac` → export JSON

### Depth C · ADK on the witness path (best 48h upgrade)

**Problem:** `/clearance` constructs ADK but sets `agent_invoked: false` — Gemini is not load-bearing on the product path.

**Build:** After `evaluate_report`, if HOLD/BLOCK:

```text
receipt = run_agent(
  prompt=f"Explain these findings to a human reviewer. Do not change verdicts: {findings}",
  session_id=body.get('session') or record['id'],
)
record['agent_explanation'] = receipt  # invoked, model, tool_calls — or error
```

- Gemini **explains** the deterministic gate — satisfies "friction removed" (30% demo criterion)
- Still honest: `agent_invoked: true` only when Runner actually ran
- **Effort:** ~3–4h · touches `cloud/service.py` + one test

### Depth D · Session + Memory (post-submit or ambitious 48h)

- GitHub Action: pass `session: ${{ github.event.pull_request.head.sha }}` or Transcripto id
- ADK `VertexAiSessionService` with that id — second clearance on same PR resumes context
- **Do not** call Memory Bank until a read path exists

### Depth E · Observability (judge keyword)

- OpenTelemetry span around `run_clearance` → Cloud Trace
- Store `trace_id` on Firestore document · link from `/hold/` UI
- **Effort:** ~4–6h · new dependency

---

## 5. Ecosystem partners — how to use them *more* (without building them)

| Partner | Use Witness **with** them | 48h action |
|---------|----------------------------|------------|
| **GitHub** | Action stays local; only verdict crosses network | Add **Check run summary** markdown from gate output; document Checks API in README |
| **Transcripto** | `session` on clearance → join | Doc + action input `session-id` optional env |
| **Zenity** | Export HOLD rows as evidence Zenity actions were overridden | One paragraph in Devpost "Challenges" — complementary |
| **Qodo / CodeRabbit** | They review diff; Witness reviews **PR body claims** | Side-by-side diagram in architecture (mermaid) |
| **Langfuse** | Trace id on record could correlate with Langfuse span | Roadmap bullet only |
| **Cursor / Claude Code** | Transcripto ingest → corpus → `witness-corpus` | Week-two; sample fixture on film |

**Cinema's Parallel partner is a different repo** (`cleared`) — do not mix into ATA Devpost stack.

---

## 6. Ranked build list — partner depth per hour

*Reordered from GEAP-GAP for **Witness path** first (not org-lift `/prove`).*

| Rank | Work | Partner | Hours | Judge sees |
|------|------|---------|-------|------------|
| **P1** | ADK explain on HOLD clearance (Depth C) | Gemini + ADK | 3–4 | Model narrates red PR; probe still blocked |
| **P2** | GitHub Action: post `session`, `actor`, `head_sha` in clearance JSON | GitHub | 1 | Join metadata on real row |
| **P3** | Check run **summary** from gate (annotations API optional) | GitHub | 2 | Richer red check UI |
| **P4** | Cloud Trace span + `trace_id` on record | GCP Observability | 4–6 | Trace link in export |
| **P5** | Vertex session service on `/agent/run` | GEAP Runtime + Memory (partial) | 4–6 | Resumed session on second call |
| **P6** | Input guard on `report` (regex/length) before probe | Model Armor (local) | 3 | Refusal reason in findings |
| **P7** | Pub/Sub publish on HOLD | GCP | 2 | Architecture only unless consumer exists |

**Do not in 48h:** full Registry · GEAP Memory Bank retrieval · Pub/Sub analyst fan-out · GitHub App.

---

## 7. Film — show partner depth honestly (add 30s)

After PR #1 red beat:

1. **`curl .../health`** — `store: firestore`, ADK constructed, `auth_required: true`
2. **`python3 contract/eligibility.py`** — 3/3 then **repeat cold** 1/3
3. **Optional if P1 shipped:** re-post clearance or show record with `agent_explanation` from Gemini

Say: *"Gemini explains the gate; Python owns the verdict."*

---

## 8. Devpost copy upgrade (paste block)

Add under "How we built it":

```text
Integration shape: the GitHub Action runs deterministic probes in the customer's CI —
no repo read access on our side. Only the verdict and session pointer cross to Cloud Run,
where Firestore append-only storage and IAM-gated APIs hold the record. ADK + Vertex Gemini
explain HOLD decisions for humans; they never override a probe. Cold eligibility: 1/3 without
GCP credentials; 3/3 on the deployed path — both measured, not claimed.
```

---

## 9. Decision for Oscar

| Path | Tradeoff |
|------|----------|
| **Ship Mon as-is** | Strong honesty · partner depth = Gateway + Firestore + constructed ADK |
| **+ P1 before film** | Best ROI — Gemini load-bearing on **witness** path · ~4h |
| **+ P1+P2+P4** | Maximum Google story · risks film slip |

**Recommendation:** **P1 + P2** if an agent has Sat–Sun; film Mon. Skip Registry/Memory Bank naming on camera.

---

## Log

- 2026-08-29 · Deep dive written; answers "use partners more" without theater list violations.
