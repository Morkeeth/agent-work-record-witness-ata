---
doc: hack
project: ATA — the verification gate for an autonomous workforce
phase: BUILD
last-touched: 2026-08-27 12:10
stale-if: not touched this working session
canonical: true   # if any other doc disagrees, THIS wins. Do not spawn a dated sibling.
supersedes: docs/WEDGE.md · docs/MOONSHOT-PLAN.md · docs/BUILD-PLAN.md · docs/THIRTY-DAY-PLAN.md · docs/HOLD-AMBITIOUS-GOAL.md · docs/internal/NEXT-STEPS.md · docs/internal/CLOSE.md
restores: docs/internal/PRD-2026-08.md (Aug 24) — the last doc that described the WHOLE product
---

# ATA — hack.md

> Restored 2026-08-27 after a scope collapse. Between Aug 24 and Aug 27 this repo went from
> ONE product to five named ideas in two families. Nobody decided that; it was the summed
> effect of three review passes, each individually correct. **A review may rule a claim
> false. It may not rule the product smaller.** Scope lives here.

---

## ⚖️ RULED BY OSCAR 2026-08-27 — THE PITCH

**The product is THE RECORD. The gate is a feature inside it.** His words: *"the RECORD is
great, but the Gate is a nice extra feature no?"*

So, settled and not to be re-litigated:
- **We pitch:** the system of record for what an agent workforce actually did. Who claimed what,
  whether the object agreed, whether the work survived, and the session behind each claim.
- **The gate is how it gets installed**, and it is the moment a claim gets caught. It is a
  feature of the record, not the headline.
- **The demo opens on week four**, not week one. See `docs/USER-JOURNEY.md`.
- Phase 3 of the playbook ladder (`docs/internal/PHASE-TRACKER.md`) has had "design owner
  unnamed" open since Aug 22. **This ruling closes the half of it that was a product question.
  The name itself is still open.**

---

## 🏷️ BRANDING  ✅ RULED 2026-08-27

**THE AGENT WORK RECORD WITNESS.**

Oscar, verbatim: *"NO THE AGENT WORK RECORD WITNESS IS GREAT! i love names like research papers"*.
He rejected a one-word brand twice. Long and descriptive is the register he asked for, and it is
the register the paper track reads in.

| Layer | Name |
|---|---|
| The product | **THE AGENT WORK RECORD WITNESS** |
| The queue inside it | **Hold** |
| The corpus layer | **Transcripto** |
| `agent-claims-inbox` | disclosure only, not a product, no git remote |

**Dead names, and a dead name in a current claim is rot:** HOLD as the product · WITNESS alone ·
Claims Inbox · hack-fleet-ata as anything but a directory. This section previously proposed
WITNESS and asked for Oscar's yes; that table is deleted rather than annotated, because a
superseded recommendation sitting under a RULED heading is the contradiction this doc exists
to prevent.

**This closes Phase 3 of the playbook ladder**, open since 2026-08-22 as "design owner unnamed"
in `docs/internal/PHASE-TRACKER.md`. Both halves, product and name, are now ruled.

---

## 🎯 NORTH STAR

**Objective.** The verification gate an autonomous workforce passes before its work counts.
One call that blocks an agent's report when the report lies, and a record of who claimed
what, whether it was true, and whether the work survived.

**The problem space.** A company hands coding agents to hundreds of engineers. Code becomes
5 to 10x faster to write, so the bottleneck inverts: **verification before merge is the
constraint, not generation.** Two failures leak past everything already deployed.

1. **The confident lie by composition.** An agent writes *"96% of projects have a phase on
   disk"* directly above *"21 no repo · 1 unknown."* Every number is true. Sign it, hash it,
   attest it, and each figure really happened. The report still says 96% where the truth is
   50%, because the denominator quietly dropped the cases named beneath it. Per-claim
   attestation cannot catch this. Code review cannot. Trace scoring cannot. They check one
   claim or one diff, and this failure needs no false sentence.
2. **Nobody can see practice.** The org sees seats and spend. It cannot see what any engineer
   typed, which prompt worked, or who is good at this. The best prompt for its codebase
   already exists; someone wrote it last Tuesday and no one else will ever see it.

**Why now.** The incidents wrote the budget. Replit deleted a production database. Amazon's
Kiro tore down a CloudFormation stack. *"Prove no agent shipped unverified"* is a board-level
line, and it has no product behind it.

**Day-two buyer.** Whoever owns the AI rollout at an org running an agent workforce with a
governance budget: VP Eng, Head of Platform, Head of Enablement. **Not a solo dev**, and the
reason is measured rather than asserted: the authorship signal is a function of fleet size.
The customer is the org whose injected traffic makes the signal exist.

**Constraints (must NOT break).**
- Transcripto never leaves the machine unless the org opts in. Local first, always.
- The gate never executes text from a report. Deterministic probes only.
- The model gets no veto. Object probes are the release authority.
- Composition BLOCKS. Task and authorship judgements are REPORTED, never gated.

**Done-when (whole project).** A blocked claim on a real PR opens to the session that produced
it, and the audit export is a document a security team could hand an auditor.

---

## 📜 CONSTITUTION

1. Scope belongs to the PRD and to Oscar. A review rules claims, never size.
2. One canonical doc. Supersede in place. Never spawn a dated sibling.
3. Every number is pinned to its measurement or written `unverified`.
4. Nothing outward without Oscar: push, deploy, submit, film, pay.
5. If it can be described as "a tool that checks X", it is plumbing and it is not the pitch.

---

## 🧱 THE MOAT

**Authorship to outcome.** Separating the small fraction of `type:user` records a human
actually typed from the injected remainder is the hard part of the whole category, and it
compounds: every week of sessions makes the next answer better, and a competitor starting in
January has no history. That corpus cannot be bought.

⚠️ **Three different figures. Never conflate them. Conflating them IS the error this product exists to catch.**

| Figure | What it measures | Scale |
|---|---|---|
| **4.9% human** (95.1% not) | 537 prompts vs 10,866 records, one 3-day window | FLEET |
| **7.1% human** (1,138 of 16,078) | a different machine-wide run | MACHINE |
| **~46% not-human** | a single terminal, one day | SOLO |

---

## 🗺️ WHITE SPACE (web-verified Aug 24, except where marked)

- **Zenity**, $125M Series C — governs agent ACTIONS, allow/modify/block an intent. Does not ask whether the agent's *report* is honestly composed.
- **Norm Ai**, $120M Series C at $1.2B — agentic COMPLIANCE, content against approved sources. Not composition-honesty of a work claim.
- **Qodo**, $70M — reviews the diff.
- **Langfuse / AgentOps** — score the trace.
- None is built to catch *"every number true, the whole a lie."*
- ⚠️ The claim that composition-honesty is unowned is a **Fable market scan, an informed negative, NOT web-verified.** An absence cannot be cited the way a funding round can.

---

## ✅ EXISTS  vs  ❌ CLAIMED

**Exists, command-verified:**
- `verify_report()`, the single gate call. Composition BLOCKS; task/authorship REPORTED.
- Adjacency, four shapes. The twist fires: piping the 22-of-23 case gives `[BLOCK] DENOMINATOR-EXCLUDES-ITS-FAILURES`, exit 1.
- The deterministic cascade. Precision on the kept set 13/13, coverage 13/24, held-out lift 5/8 vs 3/8.
- The authorship gate, `fleet/human.py::is_human_turn`. The separator behind the moat.
- The propagation loop, `fleet/propagate.py`.
- The prompting coach, `fleet/coach.py`, on 185 real transcripts and 3,438 human prompts.
- HOLD Gateway live on Cloud Run: auth on, seed off, Firestore, ADK agent, enforce mode, eligibility 3 of 3.

**Not real. Do not claim:**
- Adjacency real-corpus precision is **measured and mostly noise**: 6 of 4,785 at ~50%, a base rate of **0.13%**. Two shapes UNMEASURED. Never say "accurate", never pitch the 131.
- The Action has **zero installs by anyone who is not Oscar**, which COMPANY.md names as the only number that matters.
- Cross-harness ingestion beyond Claude Code and Codex is expansion, not built.
- GEAP Memory Bank is a stretch with a labeled Firestore fallback.

---

## 🚨 BLOCKERS FOUND 2026-08-27 (fix before anything else)

7. **⚠️ THE LIVE SERVICE IS NOT THE FIXED SERVICE.** Probed 2026-08-27: anonymous
   `POST /prove` against the live Cloud Run URL still returns **201**. The auth fix is
   committed locally and **not deployed**. Do not film the live URL and claim writes are
   locked until it is redeployed. This is now the inverse of blocker 1: the repo is ahead
   of production instead of behind it.
8. **Half the store is probe noise.** 48 records, of which **24 are `kind=prove`** left by
   testing, including two from a review agent and one from my own probe today. The Audit
   tab computes its headline percentage over these. `scripts/purge_demo_rows.py --kind prove`
   lists them. Still a dry run, nothing deleted.

1. **The product is not in git.** `cloud/hold_api.py`, `surface/hold/index.html` untracked; `service.py`, the workflow, Dockerfile, README modified and uncommitted. `origin/main` is 2 commits behind and contains no HOLD. **Cloud Run serves code that exists in no repository.**
2. **Open write routes.** `POST /wedge` and `POST /prove` call no token check (`cloud/service.py:461,477`). `/wedge` takes an arbitrary `target` path with `apply` defaulting **True**. "Writes locked" is false, on a track called Fortified.
3. **`docs/ARCHITECTURE.md` diagrams the wrong product** and is the designated artifact for the 30% Architecture score.
4. **The live queue is pre-staged**: 2 rows, actor `phase-a`, while the pack cites `demo_seed_enabled:false` as proof of no staging. 47 records of debris.
5. **Branch protection is impossible** on a free private repo (HTTP 403, upgrade or go public). Going public discloses `docs/internal/PROVISIONAL-PATENT-ANGLE1.md`.
6. **`agent-claims-inbox` has no git remote.**

---

## 🔨 BUILD PLAN

Ordered by leverage. Each slice independently verifiable. **⚑ = Oscar, everything else is agents.**

### Slice 0 — make the object true (today, ~90 min)
Commit all of HOLD. Lock `/wedge` and `/prove` behind `_require_token`. Purge the `phase-a`
rows and debris. Rewrite `ARCHITECTURE.md` for this product. Stamp the superseded docs.
**Done-when:** anonymous POST to `/wedge` and `/prove` returns 401; `/queue` returns 0; `git status` clean.
**⚑ push · set `HOLD_API_TOKEN` + `HOLD_POLICY_URL` · rule the requiredness question.**

### Slice 1 — THE JOIN  ✅ BUILT 2026-08-27
A gate decision carries the session that produced it. The console row opens the trace.
This is why the buyer is an org and not a solo dev, and it is the only claim on this board
that Zenity, Norm Ai, Qodo and Langfuse structurally cannot make: **none of them has the
agent's transcript.**
**Done-when:** a blocked row in the queue links to the real session, and the audit export carries both.
**Status: DONE.** `extract_session_ref()` recovers a session from three real report shapes;
`make_clearance_record` stores `session` + `traceable`; the console renders the trace link, and
says plainly when a claim is NOT traceable. End-to-end probe: the fixture PR body produces
HOLD / BLOCK with 2 real findings, `session=01Lzbh4XPYTAgCKg1dciFS3Q`, `traceable=true`, and
`/queue` exposes it. Tests: `tests/test_session_join.py` 14/14.

### Slice 2 — close the loop, live
Labeled PR → `verify-claims` red → Action POSTs to `/clearance` → row appears → break-glass
with a reason → `/audit/export` shows both records. Every part exists. **The chain has run zero times.**
**Done-when:** one red run and one green run, both witnessed on GitHub. **⚑ opens the PR.**

### Slice 2.5 — the record surface  ✅ BUILT 2026-08-27
`fleet/record.py` joins gate decisions into a per-actor view: claims, held, honesty rate,
traceable rate, overrides. Probe noise excluded, thin denominators labelled, practice
attached and never merged (different population). 23/23 tests.

**🔴 ITS FIRST REAL ANSWER: the store holds ZERO real agent claims.** 48 records; only 4 are
clearances and all 4 are staged (3 carry `deadbee`, 1 is actor `phase-a`); 20 are `prove`
probes; 18 have no `kind`. **The Audit tab's headline percentage is computed entirely over
demo rows.** The record is not broken. The record is telling the truth: nothing real has
happened yet, because the chain has never run on a real PR. That is Slice 2, and Slice 2
needs Oscar's click.

### Slice 3 — survival on the record
Coach's survival metric per actor in the queue. Turns a gate into a fleet.
**Done-when:** the queue shows, per actor, what share of their claims survived.

### Slice 4 — one non-Oscar install
The only number COMPANY.md says matters. **Done-when:** the Action blocks a real agent PR on someone else's repo.

**CUT:** GEAP Memory Bank · Pub/Sub · people leaderboard · GitHub App · the 0.13% detector as a headline · SSO · tenant switcher.

---

## 🎬 FILM — honest boundary

**On camera:** live `/health` and `/config` · the real red check · the queue row opening to its
session · break-glass with a reason · audit export · the honest roadmap.

**Dishonest if claimed:** the Seed button · the words "required check" unless it is actually
required · pre-staged rows as real activity · "3 of 3" implying a cold clone sees it (it needs
ADC; cold is 1 of 3) · any org-lift claim at n=2 · adjacency as "accurate."

---

## 📋 OPEN QUESTIONS

- [x] ~~is the product WITNESS~~ **RULED: THE AGENT WORK RECORD WITNESS**
- [ ] **[NEEDS CLARIFICATION: repo requiredness — GitHub Pro, public, or advisory?]** blocking Slice 2
- [ ] [NEEDS CLARIFICATION: does `agent-claims-inbox` get a remote, or fold in?] non-blocking

---

## 📜 HISTORY

- **2026-08-27** — Restored to one product after a three-review scope collapse. Blockers 1 to 6 found. This file made canonical.
- **2026-08-24** — `PRD-2026-08.md`: the whole product, two GTM stages, buyer named, moat measured, competitors web-verified.
- **2026-08-22** — WEDGE, MOONSHOT, THIRTY-DAY, BUILD-PLAN all written the same day, all claiming authority.
