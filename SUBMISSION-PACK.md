# THE AGENT WORK RECORD WITNESS — All Things Agentic submission pack (paste-ready)

_Product home: this repo only. Brand on camera: **THE AGENT WORK RECORD WITNESS**, said in full.
`agent-claims-inbox` = disclosure, not a second entry._
_Film checklist: [`docs/ATA-FILM-AND-SHIP.md`](docs/ATA-FILM-AND-SHIP.md) · **Oscar start here:** [`docs/PITCH-WHEN-YOU-ARE-BACK.md`](docs/PITCH-WHEN-YOU-ARE-BACK.md) · Product: [`hack.md`](hack.md) **(canonical)** · Why: [`docs/WHY-THIS-MATTERS.md`](docs/WHY-THIS-MATTERS.md)_

> **Naming discipline.** The product is **THE AGENT WORK RECORD WITNESS** — long and descriptive on
> purpose, in a research-paper register (ruled by Oscar 2026-08-27). **Do not shorten it in
> judge-facing copy.** "Hold" survives only as the name of the queue inside the product, and
> `HOLD` as a verdict value.

- **Deadline:** Aug 31 2026 · **17:00 PDT** (≤4:00 unedited video)
- **Devpost:** https://allthingsagentichackathon.devpost.com/
- **Track:** **Fortified Enterprise Fleet**
- **Repo (public):** https://github.com/Morkeeth/agent-work-record-witness-ata — also share with `testing@devpost.com` **and** `cloudhackathons@google.com`
- **Console:** https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/
- **Judging:** Innovation & Operational Utility 40% · Architecture 30% · Demo readiness 30%

---

## Live probe receipt (re-check before film)

| Probe | Expect |
|---|---|
| `GET /health` | `auth_required: true` · `demo_seed_enabled: false` · store firestore · ADK agent |
| `GET /hold/` | HTTP 200 console |
| `GET /audit/export` | JSON download |
| Anon `POST /clearance` | **401** |
| Anon `POST /break-glass` | **401** |
| Anon `POST /prove` | **401** (was 201 before the 2026-08-27 redeploy — re-probe it) |
| `POST /demo/seed-hold` | **403** (film uses a real agent PR) |
| `python3 contract/eligibility.py` **with ADC** | **3 OF 3 MET**, exit 0 |
| `python3 contract/eligibility.py` **cold, no GCP creds** | **1 OF 3 MET** (ADK only), **exit 1** — by design |

**Both eligibility rows are true and a judge may see either one.** Do not paste "3 of 3" anywhere
without the cold number beside it: a judge who clones this repo and runs the script with no
credentials gets 1 of 3 and a non-zero exit. That is the designed honest result. Claiming 3 of 3
unqualified is the exact composition error this product exists to catch.

Cold start: first `/health` may hang once — retry.

---

# 1 · Devpost paste

### Project name
```
THE AGENT WORK RECORD WITNESS
```

### Tagline
```
Run your agents. Check the math.
```

### Track
```
Fortified Enterprise Fleet
```

### Hosted project URL
```
https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/
```
Also: `GET /health` · `POST /clearance` (token) · `GET /audit/export` · `POST /break-glass` (token)

### Repository URL
```
https://github.com/Morkeeth/agent-work-record-witness-ata
```

### What it does
```
You can see how many agent seats you bought. You cannot see what those agents actually
did, or how much of what they reported was true. At fleet scale — overnight agents,
auto-merge — an agent's prose is an ungoverned production surface, and once it scrolls
past, nothing remembers it.

THE AGENT WORK RECORD WITNESS is the system of record for agent work: who claimed what,
whether the object agreed, whether the work survived, and the session behind each claim.

The gate is how it gets installed and how the record fills. An agent-authored PR hits a
check; each claim is probed against the object — git cat-file, path exists, test ran.
Claims the object contradicts fail closed and land in the Hold queue. Humans only look
when something is red. Break-glass is recorded with a reason. Auditors export the log.

The part nobody else can build is the join: a held claim opens back to the session that
produced it. Zenity governs agent actions. Norm Ai does content compliance. Qodo reviews
the diff. Langfuse scores the trace. None of them holds the agent's transcript, so none
of them can answer what actually happened before the claim was written.

Then we pointed it at 78,618 real agent messages — 144,306 sit in the corpus and the
scan examines the assistant turns; both numbers travel together because a result
quoted against the wrong denominator is the thing this product catches — and it found our own defect first. Raw, it said 41.7% of commit claims
disagreed with the repo. Corrected: 8.1% (19/236). The whole gap was ours. 73 of 103 "wrong"
claims were real commits in a DIFFERENT repo on the same disk, because an agent's cwd
is where it was standing, not where it committed. Ten more were shas inside shell
commands, six of them our OWN test fixture, found in transcripts about building this
gate. "42% of agent claims are wrong" was a real number from a real corpus and it was
false by 5x; the only reason it did not ship is that we wrote the denominator down
before we looked. Neither figure is an incidence rate and we do not present one: hand
labelling put extractor precision at 13 of 40 on conversational prose, n=13, and the
labelled sample ships so you can disagree.

That is also how you use it: measure the transcripts you already have BEFORE you install
anything. `witness-corpus --db <yours>`. Value first, adoption second.

Not observability. Not code review. Not a claims inbox.
Install shape: GitHub Action to Cloud Run policy.
```

### How we built it (Google stack)
```
- Gemini 3.5 via Vertex AI — exercised on the service path (the eligibility probe CALLS it)
- Google ADK — LlmAgent constructed on the Gateway, visible in /health
- Google Cloud — Cloud Run service + Firestore as the record
- Console at /hold/ · APIs /clearance /queue /break-glass /audit /audit/export /policy /prove
- GitHub Action .github/workflows/outcome-gate.yml (agent-scoped) posts to /clearance
- Deterministic probes decide CLEAR or HOLD; the model explains and never overrules

python3 contract/eligibility.py calls all three services rather than importing them.
With ADC on a Firestore + Vertex project it prints 3 OF 3 MET and exits 0. Cold, with no
credentials, it prints 1 OF 3 MET and exits 1 — deliberately, because import is not call
and credentials you do not have do not count.

Integration shape: the GitHub Action runs deterministic probes in the customer's CI —
no repo read access on our side. Only the verdict and session pointer cross to Cloud Run,
where Firestore append-only storage and token-gated APIs hold the record — the gate is an
application-level bearer token, not IAM; Cloud Run is public at the IAM layer. ADK + Vertex Gemini
explain HOLD decisions for humans; they never override a probe.
```

### Challenges
```
Our own overnight fleet reported "done" on eligibility while the object disagreed — an
import mistaken for a call. Then the coordinator building this joined 24 prove-kind store
rows to 30 audit events and produced a ratio that is true under no denominator, and put it
in three documents before a lane probed it. Then the gateway that blocks false done claims
turned out to be running out of a working tree that existed in no repository.

Then the hardest one: pointed at a real corpus, the gate reported 41.7% of agent commit
claims wrong. The number was ours, not theirs — the probe only ever asked the agent's cwd,
so a commit made in a sibling repo read as a lie, and 73 of 103 failures evaporated when we
asked the other repos. Building the control for that fix surfaced a second defect nobody was
looking for: when an agent's recorded working directory no longer exists, the probe
short-circuited to BLOCK before running at all. An agent was being called a liar by a check
that never ran.

The gate that blocks false "done" is the product. Catching ourselves with it four times in
one day is the honesty beat, not an apology — and every one of those catches came from
opening the object, never from re-reading the note.

Trust boundary: mutating routes require HOLD_API_TOKEN; the demo seed is off, so the film
must use a real agent-labelled PR. Practice propagation on a field of 2 stays
UNMEASURED_FOR_ORG_CLAIM.
```

### What's next
```
Separate a citation from a claim. "Commit X landed" and "Committed as X" are the same
string; only the speech act differs, and that is why precision on prose is 13 of 40. We
shipped the two cheap halves — scope to a declared report region, drop machinery — and
refused to build a classifier, because the labelled set does not exist and inventing one is
the failure this product exists to catch. It is the first contribution we are asking for.

One real agent pull request — ten minutes, and it turns three demo gaps into a product.
GitHub App with Check Runs, so install is a click and the check can honestly be called
required. Transcripto as silent provenance on every claim. Survival scoring per actor:
what share of an engineer's agent claims were still standing a month later. Deploy and CI
witnesses beyond SHA and path.
```

### Architecture
Source: `docs/ARCHITECTURE.md` (mermaid) → export `docs/architecture.png` for the form.
**PNG on disk:** `docs/architecture.png` (re-probed 2026-08-30).
Narrate **record first**: the record is the product · the gate is its intake · Action → Cloud Run
Gateway → Firestore · the join back to the session · console and export are what people open.

---

# 2 · Video beat sheet (≤4:00, unedited)

**Line:** *Run your agents. Check the math.*

**Open on week four, not week one.** A platform lead opens a held claim and it resolves to the
session that produced it. The red check is the second beat, not the first.

| Time | Beat | On camera |
|------|------|-----------|
| 0:00–0:30 | Problem | Seats and spend are visible; what the agents did is not |
| 0:30–1:10 | **The record** | `/hold/` — a held claim, opened, resolving to its session |
| 1:10–1:35 | How it fills | the gate: agent PR → probe vs object → HOLD |
| 1:35–2:15 | **Real PR** | agent label + false-done body → red `verify-claims` + Hold row |
| 2:15–2:40 | Break-glass + audit | reason → recorded; Export JSON |
| 2:40–3:05 | GCP | `/health` live (say the `*.run.app` URL) · `eligibility.py` → 3/3, **and say cold is 1/3** |
| 3:05–3:30 | Honest state | PR #1 red · row `H-a6151a95ac` · still `clear: 0` |
| 3:30–4:00 | Close | install path + roadmap; the line |

**Say the product name in full at least twice.** Never "HOLD" as the product.

**Do not:** the Seed button · `/healthz` · org lift at n=2 · the words "required check" while
requiredness is unresolved · Witness / Claims Inbox / hack-fleet-ata as names · the CLI as the product.

Pre-roll: `docs/ATA-FILM-AND-SHIP.md` §2.

---

# 3 · Honest state — roadmap, never claims

Measured 2026-08-29 by probing the live service and GitHub PR #1, not quoted from a note.

| Gap | Measured | Say it as |
|---|---|---|
| Real agent work in the record | **1 github-action clearance `H-a6151a95ac`** (PR #1, `source=github-action`, traceable, session `01Lzbh4XPYTAgCKg1dciFS3Q`, BLOCK/HOLD on `deadbee` + missing path) + older staged rows | "One real agent PR went through the gate — it failed on purpose and is in Hold." |
| Nothing has ever cleared | `GET /audit` → **`clear: 0`** | "Nothing has passed — the real row is a HOLD, not a clear." |
| Check fired on a real PR | PR #1 open · `verify-claims` → **FAILURE** | **claim this — red by design.** The PR body claims false done; the gate BLOCKed, posted `H-a6151a95ac`, workflow exited 1. A green check would mean the demo broke. |
| `/audit` vs `/audit/export` counts | **by design, not a defect.** `/audit` returns every event; `/audit/export` returns clearance/exception/policy only and drops prove-only rows; `?include_prove=1` returns the full set and the two agree exactly. Re-probed live 2026-08-28 (31 vs 7 at that moment, 32 vs 8 an hour later — **these are live counters, do not pin a number to them on camera**). | explain the filter, never quote the count |
| `docs/architecture.png` for Devpost | **exported 2026-08-29** from `docs/ARCHITECTURE.md` mermaid | attach on paste |
| Deployed revision behind repo | **closed 2026-08-28.** anon `POST /prove` → **401** `HOLD_API_TOKEN required`, probed against the live service. (That is what was probed; the running revision is not claimed to be byte-identical to `main`.) | fixed — the auth gate is live |
| Agent genuinely invoked | `GET /audit` carries an `agent_run`: `invoked: true`, `google.adk.runners.Runner`, `gemini-3.5-flash-lite`, 3 tool calls | **claim this — it is live and recorded** |
| `/health` reports a run receipt | deployed: `constructed: true`; P1 adds `agent_explanation` on HOLD when redeployed | **claim receipt on `/agent/run`**; explain-on-HOLD after deploy |
| Install path | repo is public, action ships the probe, `uses:` resolves from a foreign repo | works — but zero non-author installs |
| Non-author installs | **zero** | roadmap. The 2026-08-27 foreign-repo run does not count: we wrote the test organisation and scripted its PRs. It proves the chain, not adoption. |
| Org lift | field of 2 → `UNMEASURED_FOR_ORG_CLAIM` | never claim a population effect |

`tests/test_auth_gate.sh` is green **against a local server**. It is not a statement about the
deployed revision, and on 2026-08-27 the deployed revision disagreed with it.

---

# 4 · Disclosure

- [transcripto](https://github.com/Morkeeth/transcripto) — authorship-gated corpus spine (roadmap provenance)
- Local `agent-claims-inbox` — claim/repo witness patterns
- Product composition (the record, the join, Gateway, console, Action) submitted in this repo
