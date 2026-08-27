# FOR CURSOR — build lane

**This repo only.** Cursor works inside one repo; git is the mailbox. Do not reach into
`~/CODE/hack-agent-science` or maintain a second copy of `~/CODE/transcripto` — read it,
don't fork it. Spine copies come from `~/CODE/agent-claims-inbox` per `CONTEXT.md`.

## What this is
All Things Agentic (Devpost, **Aug 31 2026 5:00pm PDT**). Org-level fleet and prompt
management on the transcripto corpus. **Phase 1** — spec extract done; build starts Phase 4.

Read order: `PHASE-0.md` → `CONTEXT.md` → `docs/WEDGE.md` → `docs/SPEC-EXTRACT.md` → `LANE.md`.

## Current work — build the wedge loop

The EYES panel (Aug 22, `CURSOR-LOG.md`) reframed Surface 5: the agent **propagates** the best
operator prompt, it does not show a coaching card. See `docs/WEDGE.md` for the exact loop.

### Next code slices (in order)
1. **`fixtures/`** — synthetic operator-a / operator-b transcripts + minimal org repo
2. **Inherit spine** — `claims_inbox.py` discovery, `repo_witness.py`, `cloud/*` from agent-claims-inbox
3. **`fleet/signals.py`** — one signal: survive vs abandon (probe named, UNMEASURED OK)
4. **`fleet/propagate.py`** — `find_best_prompt` · `propagate_prompt` · `witness_propagation`
5. **`cloud/agent.py`** — ADK wrap (same pattern as claims-inbox; UNVERIFIED until GCP live)
6. **Stranger script** — empty HOME, one command, golden witness output

### Do not start until Oscar clears (outward acts)
- Cloud Run deploy · Firestore · live Gemini — blocked on Aug 26 kill condition

## The house rules
- **Cite the object, not the note.** Every number here is a claim with an author.
- Append to `CURSOR-LOG.md`; never overwrite another lane's file.
- **Outward acts are Oscar's alone** — push, deploy, publish, submit.

## Resolved from review lane (Aug 22)
- Hours: 52h floor, submission path = wedge loop only (`PHASE-0.md` #2)
- Fourth incumbent: Langfuse / Copilot OTel (`CONTEXT.md`)
- Moat: 94.48% measured on this machine — probe in transcripto DB
- Wedge: propagation not rewrite (`docs/WEDGE.md`)

---

# ROUND 1 ASK — the build plan (added 2026-08-22)

`docs/SPEC-EXTRACT.md` and `docs/BUILD-PLAN.md` are new. Attack them in this order.

## 1. THE GEAP FORK — the highest-value ruling you can give
The plan bets on **Gemini Enterprise Agent Platform** (Agent Registry + Memory Bank) instead of
the obvious Gemini + ADK + Cloud Run + Firestore. Reasoning: a 600-entry field all submits the
obvious three; GEAP is the sponsor's newest strategic product and scores the 30% architecture
criterion harder.

**The risk is that GEAP is new, thin on docs, and eats two of nine days.**

Go and look — GEAP docs, quickstarts, whether the Agent Registry is even publicly usable, whether
it needs an org/enterprise tier a solo entrant cannot get. **Then rule: bet or fold.** If it needs
an enterprise account, the bet is dead and the plan must change today, not on day four.

## 2. Is the COACH defensible, or does it collapse?
Slice 3 is the wedge: retrieve the org's best-performing prompt for an intent and adapt it.
**Break it.** Does it reduce to "an LLM rewrites your prompt"? What makes retrieval-from-your-own-
corpus different in a way a judge can see in 30 seconds? If it collapses, the product has no wedge
and we need to know now.

## 3. "Best operator" — the denominator
The plan proposes *fewest retries to a landed change, on comparable task classes.* **Attack it.**
Comparable how? What stops it rewarding someone who only does easy work? An unpinned denominator
is the exact failure this project exists to catch, and shipping one would be fatal on camera.

## 4. Is ~52h honest for 9 days? (unchanged, still #1 in practice)
See `PHASE-0.md` ladder #2. Slice 0 alone is a first-ever Cloud Run deploy.

## Protocol
Append findings to `CURSOR-LOG.md` — never edit `docs/*` or this file. Cite the object, not the
note. Outward acts are Oscar's alone.
