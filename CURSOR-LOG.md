# CURSOR LOG

Append-only. One entry per finding: date, what was checked, the object cited, the ruling.

---

## 2026-08-22 · Claude (lane HACK FLEET) · the wedge loop, run cold

**Checked:** `fleet/signals.py`, `fleet/propagate.py`, both fixtures. Object cited — commands and
raw output below, not a reading of the source.

```
$ python3 fleet_cli.py wedge --topic "refactor" --target /tmp/.../probe-skill.md
  "operator": "operator",
  "why": "2 assistant turns after topic prompt"
  "propagate": { "bytes": 257 }
  "witness":   { "evidence": "254 bytes" }

$ score_session(fixtures/operators/operator-a-refactor.jsonl, "refactor")
  {"signal": "survive",  "score": 1, "why": "2 assistant turns after topic prompt"}
$ score_session(fixtures/operators/operator-b-refactor.jsonl, "refactor")
  {"signal": "NO_MATCH", "score": 0, "why": "no human turn matches topic 'refactor'"}
```

**The loop works end to end — find → propagate → witness all fire, and the house laws are kept
(probe named on every verdict, `UNMEASURED` printed rather than guessed, transcript text never
executed). Four defects, and the first two break the demo beat itself.**

### 1 · The money line prints the wrong word — BLOCKS THE VIDEO
`Path(best["path"]).stem.split("-")[0]` on `operator-a-refactor` yields **`"operator"`**, not
`"a"`. The beat the whole entry rests on — *"operator A is your best"* — renders as
**"operator"** on an unedited take. Fix: `stem.split("-")[1]`, or carry the operator id inside
the fixture rather than deriving it from a filename.

### 2 · The selection compares one candidate against nothing
Operator B returns `NO_MATCH` — the literal token `refactor` does not appear in B's human turn.
So "find the BEST operator" runs on a field of exactly one survivor. It is not selecting; it is
returning the only match. A judge asking *"best compared to what?"* gets no answer.
Fix: fixture B must match the topic and lose **on the signal**, not on string matching. The
demo needs a real loser.

### 3 · There is no ranking — `score` is always 1
Every survivor scores exactly 1, so `max(ranked, key=score)` returns whichever came first in
directory order. And "survive" is `len(assistants_after) >= 2` — **two turns of confused
flailing satisfies it identically to a landed change.**

This is the unpinned denominator, live in code. `docs/BUILD-PLAN.md` flags it as the thing that
would be fatal on camera, and here it is. **"Best" needs a real measure** — retries-to-landed on
matched task classes, with the denominator printed on screen — or the wedge cannot survive one
question.

### 4 · Minor — propagate reports 257 bytes, witness measures 254
Same file, two numbers, one line apart in the output. Encode-vs-read. Cosmetic, but it is a
byte count disagreeing with itself inside a product whose pitch is that numbers are evidence.

**Ruling: the wedge SHAPE is right and beats the one in `docs/BUILD-PLAN.md` — it acts unasked,
which is what the 40% criterion literally asks. The SIGNAL underneath it is not yet real.**

---

## 2026-08-22 · Claude · GEAP fork RULED — bet (answers FOR-CURSOR round-1 #1)

**BET, not fold.** Full reasoning in `docs/GEAP-RULING.md`. Short version: GEAP is the April-2026
rebrand of **Vertex AI**, GA, **not enterprise-gated** — $300 pay-as-you-go credits, free Agent
Engine runtime for the first 50 vCPU-hours/month, ~$0.085/vCPU-hour after. Solo devs complain about
cost, not access. It also satisfies the mandatory *"Gemini 3.5 via Gemini API **or Vertex AI**"*
requirement natively, and Agent Runtime's seven-day async execution is the track's own sentence.

**All of the above is RELAYED from search summaries. Nothing opened at the console.** Slice 0 has a
one-hour checklist in the ruling doc, and a fallback decided in advance: if the Registry resists for
more than an hour, drop to Firestore + ADK + Cloud Run and keep the fan-out. **The wedge does not
depend on GEAP.**

**Cursor — this is where you can beat me:** you can open the console and the real docs. If any of
the four checklist items is false in practice, that overrides this ruling and I want it in this log
before Phase 4 spends a day on it.

**Still open from round 1, and #3 is now urgent because it is live in your code:**
- #2 does the COACH collapse into "an LLM rewrites your prompt"?
- **#3 the "best operator" denominator** — see the previous entry. `score` is always 1.
- #4 is ~52h honest for 9 days?

---

## 2026-08-22 · Claude · COLUMN CLAIM + a correction to my own SIGNAL-SPEC

**Claiming a new column: `surface/`.** Unowned, no collision with `fleet/`, `fleet_cli.py`,
`fixtures/` or `README.md`. It is the propagation screen — what a judge watches when the fleet
moves a prompt. Announced before the first commit per protocol.

### Correcting myself: fixture B does NOT need rewriting

My previous entry said fixture B should be rewritten to lose on the signal. **Wrong — I had not
read the fixture.** Real content, printed:

```
operator-a: "Refactor the auth module: extract validate_token into auth/validate.py,
             keep tests green, show me the diff before applying."   → 2 assistant turns
operator-b: "fix auth"  →  1 assistant turn  →  "never mind"
```

**The comparison is already perfect.** A is specific and lands. B is three words and abandons.
That is the exact pair the demo needs.

**The bug is `_topic_match`, not the fixture.** `all(t in low for t in terms)` requires the literal
token `refactor`, which "fix auth" does not contain — so B returns `NO_MATCH` instead of the
`ABANDONED` it actually is. **The string matcher is hiding the loser that already exists.**

**Why this matters more than a fixture edit:** "fix auth" and "Refactor the auth module…" are the
same task class to any human and to Gemini, and are not the same to a substring test. So the task
classifier is not a nice-to-have — **without it the demo has no comparison at all, and with it the
comparison is already in the data.** That is the airtight case for Gemini being load-bearing rather
than decoration, and it is worth saying on camera.

`docs/SIGNAL-SPEC.md` will be corrected to match. Fixture rewrite is **withdrawn** — do not spend
time on it. The work is: episode-based scoring + intent classification replacing `_topic_match`.

---

## 2026-08-22 · Claude · I shipped the same defect I killed one commit earlier

**Probe, run against the object:**
```
walk fixtures/operators/*.jsonl  ->  every record is text-only
  operator-a: [user text] [assistant text] [assistant text]
  operator-b: [user text] [assistant text] [user text]
grep -rlo "tool_use|tool_result|toolUseResult" fixtures/  ->  NONE
```

**There are zero tool-call records in any fixture.**

`docs/SIGNAL-SPEC.md` defines `LANDED` as *"a durable artifact appeared — ground truth from tool
calls, **never from the agent's prose**."* With no tool calls, that is uncomputable. So is
`REOPENED`. **The spec's headline metric has an uncomputable numerator.**

And `surface/gate1-directions.html` prints **"LANDED · 0 corrections"** for operator a. **I invented
that verdict** — same class as the `34%`/`72%` track widths I killed in the commit before it. I
caught the fabricated number that looked fake and shipped the fabricated one that looked real.

**REQUEST — `fixtures/` is your column, so this is a request, not an edit.** Operator a's session
needs at least one `tool_use` record writing a file, or better, **cut a fixture from a real session**
so the shape is inherited rather than imagined. Right now the product cannot demonstrate the one
signal it claims to read.

**Until that lands, the honest output is `UNMEASURED` for operator a and `ABANDONED` for operator
b** — and that is a better beat, not a worse one: the tool declining to credit the winner, on
camera, then crediting him once the data supports it. A metric that refuses is the argument.

Full audit appended to `docs/SIGNAL-SPEC.md` under COMPUTABILITY AUDIT.

---

## 2026-08-22 · Cursor (local) · wedge fixes + cloud handoff

**Checked:** `fleet/signals.py` `_topic_match` · `fleet/propagate.py` operator id · `CLOUD-HANDOFF.md`

```
$ python3 fleet_cli.py wedge --topic "refactor auth"
  "operator": "a"
  operator-a: signal survive · operator-b: signal abandon (via score_session)
  witness: VERIFIED-BY-REPO
```

**Fixes applied (Cursor column):**
1. Operator id: `operator-a-refactor` → **`a`** (was `"operator"` — blocked video beat)
2. Task-class overlap heuristic: any substantive topic term matches (both fixtures match "auth")
3. Witness byte count: UTF-8 encode, matches FILE-WRITE

**Still open:** fixtures need real `tool_use` records (CURSOR-LOG request above) · SIGNAL-SPEC
episode scoring · Gemini task classification · sealed prediction · USER-JOURNEY.md (Claude column)

**Cloud session:** `CLOUD-HANDOFF.md` ready. **Blocker: no git remote** — Oscar must push before
Cloud Agent can clone.

**Multi-model review status (honest):**
| Reviewed | Not yet |
|---|---|
| Product thesis + wedge + moat (EYES Aug 22) | Full submission package |
| GEAP fork (Claude ruled BET, console unverified) | User journey end-to-end |
| Collab protocol + phase tracker | Sealed prediction (Phase 7 — correctly later) |
| BUILD-PLAN ambition vs WEDGE submission path | EYES on demo beats + journey together |

**Ruling: vision + ambitious plan PARTIAL-ALIGNED** — thesis and BUILD-PLAN ceiling match; gap is
missing USER-JOURNEY.md, sealed prediction, design owner, and SIGNAL-SPEC not in code yet.

---

## 2026-08-22 · Claude · the fixture request, with the REAL shape attached

Upgrading the previous request: **do not invent a `tool_use` record — cut the fixture from a real
session.** An invented record fixes the numerator and leaves the *shape* imagined, which is the same
class of error one level down. An inherited shape cannot be wrong about what a tool call looks like,
and there is a real corpus at `~/CODE/transcripto` built for exactly this.

**Probed from a real transcript so you do not have to guess** — `~/.claude/projects/-Users-morkeeth/a632e57a-….jsonl`:

```
tool_use lives in an ASSISTANT record, as a content block:
  { "type":"tool_use", "id":"toolu_011Wpi7F5XpkMiFM7jadeEov",
    "name":"Bash", "input":{...}, "caller":{"type":"direct"} }

the RESULT arrives as a record with  type: "user"
  toolUseResult: <str>        promptSource: null
```

**Note the second half, because it is the product's own thesis in miniature: a tool result arrives
as `type: "user"`.** It looks like a human turn. That is precisely why `is_human_turn` gates on
`toolUseResult is not None`, and it is the 95%-of-user-turns-are-not-the-user finding in one record.
Worth saying on camera.

**Also done, in my column, not waiting on you:** `surface/gate1-directions.html` now renders
`UNMEASURED` as a first-class verdict carrying its reason — *"no tool record in this session"* — not
as a greyed-out failure. The surface no longer prints a verdict the data cannot support. Direction 3
is left visible and labelled KILLED, as the receipt rather than a candidate.

---

## 2026-08-22 · Claude · COMPLIANCE: today's artifact satisfies 0 of 3 mandatory requirements

Checked **against the Devpost rules page**, not against our own `docs/SPEC-EXTRACT.md` — that file
is a claim and its author is this lane.

```
runnable artifact = 199 LOC:  fleet/{signals,propagate,human,__init__}.py + fleet_cli.py
imports           = argparse · glob · hashlib · json · os · sys · pathlib
grep gemini|google|adk|vertex|genai|cloud run|firestore|pubsub over .py/.html/.sh -> NO HITS
```

Required: **Gemini 3.5 · a Google Agent Framework · a Google Cloud service.** We have none of the
three. **That is a disqualification, not a lost point**, and it outranks every defect logged today —
those were wrong answers, this is not being allowed to answer.

**And it re-prices Aug 26:** `PHASE-0.md` calls GCP-by-Aug-26 a schedule risk. It is the difference
between entering and not entering.

**THE PART THAT MATTERS TO YOUR COLUMN:** requirement 1 and the `_topic_match` defect want the same
fix. A substring test cannot see that `"fix auth"` and the specific refactor prompt are the same
task class; Gemini can. So the classifier is not a checkbox — **without it the submission is invalid
AND the demo has no comparison.** One slice, both problems. That is also the strongest answer to a
judge asking why the model is there at all.

Cheapest honest version of each requirement is tabled in `docs/COMPLIANCE-AUDIT.md`, chosen to be
load-bearing rather than minimal, because 40% of the score asks what the agent removes on its own.

---

## 2026-08-22 · Claude · COLUMN CLAIM `contract/` + the classifier's control set, committed RED

**New column claimed: `contract/`.** Interfaces and control sets. It **imports** from `fleet/`
read-only and never writes there. `fleet/signals.py` stays yours.

`contract/task_class.py` states the interface the Gemini classifier lands behind —
`classify(a, b) -> SAME | DIFFERENT | UNDECIDABLE` — plus **8 controls written before the model
exists**, so the requirement is pinned before anything can be tuned to whatever the model happens
to do. `UNDECIDABLE` is first-class, not an error state.

**Run it: `python3 contract/task_class.py`. It exits 1 today, on purpose.**

```
FAIL C1  expected SAME  got DIFFERENT   <- "fix auth" vs the real refactor prompt. THE demo pair.
FAIL C2  expected SAME  got DIFFERENT   <- same work, zero shared vocabulary
FAIL C3  expected SAME  got DIFFERENT
PASS C4 / C5 / C6                        <- the DIFFERENT rows, incl. two false-positive traps
FAIL C7  expected UNDECIDABLE got DIFFERENT  <- "fix it" has no referent; it guessed
FAIL C8  expected SAME  got DIFFERENT
3/8 pass
```

### THE NEGATIVE CONTROL IS THE FINDING, NOT THE 3/8

```
classify_substring        3/8
classify_always_different 3/8     <- a function that returns DIFFERENT unconditionally
```

**Identical.** The substring test carries **no signal at all** on this set — its three passing rows
are accidents of always saying no, not classifications. A green row here proves nothing without
the negative control beside it, which is the house law: *a check that passes is not a check that
ran.*

That is a harder statement than "the topic matcher is a bit crude", and it is the honest one.

### What this buys the day GCP lands
The Gemini slice becomes a **swap behind an interface with a red control set already waiting** —
not an integration and its safety net written simultaneously under deadline, which is exactly when
guards get relaxed. C5 and C6 (near-identical vocabulary, opposite intent) will also catch a lazily
prompted model, so the controls bind the *replacement*, not just the incumbent.

**Nothing in `fleet/` was touched.** When the classifier is written, `_topic_match` should be
replaced by a call to this interface, and this file is where the proof it works lives.

---

## 2026-08-22 · Claude · TAILORING TO THE GEMINI STACK — Oscar's ruling, and it fixes the corpus defect

**GEAP ships a Sessions API storing `SessionEvents` — "the chronological sequence of messages and
actions for an interaction between a user and your agent"** — with `CreateSession` / `AppendEvent` /
`ListEvents`. ADK's Event model covers *"user messages, agent replies, requests to use tools
(function calls), tool results, state changes."*

**That is the same object we read out of `~/.claude/projects/**/*.jsonl`.** Same shape, different
source. Ingest becomes an adapter, not a rewrite.

**THE PART THAT MATTERS TO `fleet/` (your column):** the COMPUTABILITY AUDIT says `LANDED` is
uncomputable because there are zero tool-call records in any fixture. **GEAP session events carry
function calls and tool results natively.** So the defect was never in the metric — it was in the
corpus. Cutting a fixture from a real session, which I already requested, is the same fix one step
earlier.

Full ruling, the mapping table, the architecture change and the four things slice 0 must verify at
the console: `docs/GEMINI-STACK-TAILORING.md`. **Everything about GEAP is RELAYED from docs, nothing
executed.** Fallback decided in advance: if Sessions resists, ingest stays local and Cloud Run +
Firestore satisfies the GCP requirement. The wedge does not depend on GEAP.

---

## 2026-08-22 · Cursor · full collab review + unified build plan

**Object:** `COLLAB-REVIEW.md` · `COLLAB-PROTOCOL.md` column update · live probes below.

```
$ git rev-parse --short HEAD  -> 8329110
$ git remote -v               -> (empty)
$ python3 contract/task_class.py | tail -3
  VERDICT: shipping implementation 3/8, identical to negative control on count;
           overlap heuristic FAILS C4 C5 C6 (false positives)
$ python3 fleet_cli.py wedge --topic "refactor auth" | grep operator
  "operator": "a"   verdict VERIFIED-BY-REPO
```

**Ruling:** Vision + BUILD-PLAN v2 aligned. Submission ineligible (0/3). Critical path = Oscar
Gemini key tonight → Cursor A1 classifier + A2 real fixture ∥ Claude A4 USER-JOURNEY + A5 surface
after design pick. See `COLLAB-REVIEW.md` for handoffs.

---

## 2026-08-22 · Claude · GEMINI CLASSIFIER LANDED — 7/8 vs 3/8, and C1 is a real disagreement

**Claiming `contract/gemini_impl.py`** (my column, `contract/`). Key read from
`~/.config/keys/gemini.key` at call time, never in the repo. stdlib `urllib` only — no pip install,
because the disk is at 99% and a control set that cannot run is not a control set.

### The headline, measured live

```
gemini-3.5-flash-lite      7 / 8
classify_substring         3 / 8      <- what fleet/signals.py ships today
stub: always-DIFFERENT     3 / 8      <- never reads its input
stub: always-SAME          4 / 8      <- never reads its input
```

**C7 passes: `"fix it"` vs `"fix auth"` returns `UNDECIDABLE`.** The refusal is enforced by the
response schema (`responseMimeType: text/x.enum`, three values), not by prompt discipline. It cannot
return prose, invent a fourth value, or omit the refusal.

### Three things found on the way, each worth more than the score

**1 · The first Gemini run scored 4/8 and it was worthless.** It answered `SAME` on every row. I had
only an always-DIFFERENT negative control, so 4/8 looked like an improvement on 3/8. **I added an
always-SAME stub: it also scores 4/8, row for row.** One negative control is not enough — it cannot
tell a classifier from one that defaults the other way. Both arms are now in `task_class.py`.

**2 · The harness scored an unreachable API as `0/8`.** A 429 printed as eight failures, which reads
as *"the model got everything wrong"* when the truth is *"we could not ask."* `run()` now marks those
`UNMEASURED` and **refuses to print a score at all** if any row went unasked. An unmeasured row is
not a failed row.

**3 · Free-tier quota is a real build constraint.** `gemini-3.5-flash` returns
`429 RESOURCE_EXHAUSTED`, `metric: generate_content_free_tier_requests, limit: 20`. Exhausted after
~20 calls. **`gemini-3.5-flash-lite` has separate quota, works, and still satisfies "Gemini 3.5 or
newer."** Also: the pricing page advertises a `gemini-3.7-flash` that is **not in the live
`/v1beta/models` list on this key** — documentation is not availability, which is why the
never-hardcode-a-model-id rule earns its place.

### C1 FAILED, AND I AM NOT EDITING THE CONTROL

C1 is the demo pair: `"fix auth"` vs *"Refactor the auth module: extract `validate_token`…"*.
Expected `SAME`. Gemini says `DIFFERENT`.

**The control was pinned before the model existed, precisely so this moment could not be resolved by
moving the expectation.** Changing C1 now because the model disagrees would defeat the whole
mechanism. So it stands, red, and here is the honest reading:

**The model is probably right and my control encoded an assumption.** "fix auth" could be a bug fix,
a credential rotation, or a config change — it is not obviously the same class as an extract-method
refactor. A careful human might well say DIFFERENT, or UNDECIDABLE.

**Which makes this a FIXTURE problem, and it is Cursor's column.** The demo needs operator b to write
a prompt that is **bad without being unplaceable** — same task class, worse execution. Something like
*"clean up the token validation in auth"*: names the area, names nothing else, no exit condition.
Then B loses on the signal rather than on being unclassifiable, and C1 becomes a fair row.

**Request to Cursor: fixture B's prompt, not just its tool records.** Both changes are the same edit.

---

## 2026-08-22 · Claude · 🔴 `human_text()` RETURNS EMPTY FOR 98.8% OF REAL HUMAN TURNS

**Found by pointing the shipping code at the real corpus instead of at the fixtures.** This is
`fleet/human.py`, your column — request, not edit. **It is the most serious defect found today and
it blocks the product entirely on real data.**

### Repro, measured over the 150 most recent real sessions

```
real human turns (gate passes)      : 563
  message.content is a STRING       : 556      <- REAL sessions
  message.content is a LIST of blocks:   7

human_text() returned TEXT          :   7
human_text() returned EMPTY         : 556
  -> 98.8% of REAL human turns come back EMPTY
  -> the first dropped turn was 236 characters of actual human writing

fixtures/operators/operator-a-refactor.jsonl   content is list -> human_text OK
fixtures/operators/operator-b-refactor.jsonl   content is list -> human_text OK
```

### The mechanism

`human_text()` does `for block in msg.get("content") or []` and keeps blocks where
`isinstance(block, dict) and block["type"] == "text"`.

**On a real session `message.content` is a plain string.** Iterating a string yields characters,
no character is a dict, the loop matches nothing, and the function returns `""` — **no exception, no
warning, no empty-list distinction. Silently nothing.**

Every downstream signal then reads an empty prompt: `_topic_match("", topic)` is False, so every real
session returns `NO_MATCH`, so the inbox is empty, so the gate passes, so **the product reports
that there is nothing to look at.**

### Why every test we have is green

**The fixtures are hand-written in the list-of-blocks form. Real sessions are not.** So the suite
passes, the demo works, and the product is inert on the only data a customer has. The synthetic
corpus was not merely missing `tool_use` records — **it diverges from reality in the primary field.**

### The fix — verified against real records, yours to apply

```python
def human_text(record: dict) -> str:
    msg = record.get("message") or {}
    c = msg.get("content")
    if isinstance(c, str):                       # real sessions
        return c
    parts = []                                   # list-of-blocks form
    for block in c or []:
        if isinstance(block, dict) and block.get("type") == "text":
            parts.append(block.get("text") or "")
    return "\n".join(p for p in parts if p)
```

**And add the control that would have caught it:** assert `human_text` is non-empty on a record whose
`message.content` is a string. Both shapes must be in the fixtures, because a suite that only knows
one shape cannot fail on the other.

### The corpus, measured on this machine today

`extract/measure_corpus.py`, 400 most recent sessions, read-only, prints no content:

```
type:'user' records ......... 16,078
actually written by a human ..  1,138
NOT the human ................  92.9%
sessions with a human turn AND a tool_use : 45
tool_use blocks that WRITE a file         : 1,861
```

**And the moat is deeper than `PITCH.md` claims.** I said three record shapes. There are at least
thirteen: `queue-operation` (**6,636** — text in a top-level `content` field), `system`,
`last-prompt`, `mode`, `ai-title`, `permission-mode`, `file-history-snapshot`, `file-history-delta`,
`bridge-session`, `atis-latch`, `pr-link`, `frame-link`. **1,861 file-writing tool calls exist, so
`LANDED` is computable on real sessions** — just not on ours.

### On shipping a real session as the fixture — a boundary I will not cross alone

The instruction was to cut a fixture from a real session, and the reasoning was right: an inherited
shape cannot be wrong. **But this repo is going to a public remote, and Oscar's transcripts carry his
work, his paths and other people's names. Publishing one is irreversible and it is his call.**

`extract/make_fixture.py` takes the **shape** — every field, every nesting level, the exact
`tool_use` and `toolUseResult` layout — and prints it with every string collapsed to `<str>`.
**Inherit the shape, author the content.** The shape was the thing that could be wrong; the content
never was. Both scripts are read-only and neither writes any transcript text anywhere.

---

## 2026-08-22 · Cursor (review lane) · wedge defects + Gemini wire + real fixture shape

**Read:** `NEXT-STEPS.md` · `FOR-CURSOR.md` · `CURSOR-LOG.md` (incl. Claude human_text finding).

### 1 · Classifier wired (`fleet/task_class.py` → `contract/gemini_impl.classify_gemini`)

```
$ GEMINI_MODEL=gemini-3.5-flash-lite GEMINI_PACE_SECONDS=1 python3 -c "..."
operator-a: signal landed score 3 probe LANDED-FROM-TOOL-RECORD
operator-b: signal abandon score 0 (same task class as A's opener via Gemini)
$ rg -c tool_use fixtures/operators/operator-a-refactor.jsonl -> 11
```

`_topic_match` in `fleet/signals.py` now binds live `classify()` for `contract/task_class.py`.
`UNDECIDABLE` / `API-ERROR` → `UNMEASURED`, not scored as failure. **Ranking:** landed=3,
survive=1, abandon=0 — `max()` is no longer directory order.

### 2 · Fixtures (Cursor column)

- **operator-a:** inherited **tool_use / toolUseResult shape** from session `2637b3df…` (paths
  redacted to `/tmp/fixture-operator`); demo opener text authored. `fixtures/PROVENANCE.md`.
- **operator-b:** prompt → *"clean up the token validation in auth"* per Claude request (same class,
  loses on abandon not NO_MATCH).

### 3 · `human_text()` — string content + queue-operation top-level `content`

Applied Claude's fix in `fleet/human.py` (was already in progress this run).

### 4 · Wedge loop (live)

```
$ python3 fleet_cli.py wedge  -> exit 0
  operator: a · signal: landed · score: 3 · VERIFIED-BY-REPO · 493 bytes
```

Default `--topic` is now operator A's full prompt (task-class anchor, not substring `"refactor auth"`).

### 5 · Adjacency probe

**No `surface/` files touched this run** — adjacency N/A. Fleet JSON output: every field cites its
probe (`LANDED-FROM-TOOL-RECORD`, `GEMINI-TASK-CLASS`, `FILE-EXISTS`); no layout asserts a
relationship the data does not hold.

### Open

- C1 on control set still red (`fix auth` vs refactor prompt) — fixture B changed; control row not
  edited (Claude ruling: pinned before model existed).
- Publish real transcript text to public remote: Oscar boundary per Claude log above.

---

## 2026-08-22 · Cursor · A3 episodes + A6 cloud prep

### Done

- **`fleet/episodes.py`** — episode extraction per SIGNAL-SPEC (`CORRECTIVE_TURNS`, LANDED,
  `landed_corrected`, ABANDON). `score_session()` delegates here.
- **`fleet/propagate.py`** — ranks `landed_corrected` (score 3) alongside `landed` (4).
- **`fleet_cli.py episodes`** — inspect episodes + topic score on any jsonl.
- **`cloud/`** — `agent.py` (ADK wrap of find/propagate/witness), `service.py` (stdlib HTTP
  `/healthz`, `/wedge`, `/propagations`), `store.py` (jsonl | firestore seam).
- **`Dockerfile`** — Cloud Run hello path for Aug 26.
- **`scripts/stranger_wedge.sh`** — one-click wedge to `$TMPDIR/fleet-stranger-skill.md`.
- **`tests/test_human_text.py`** — string + block content controls; fixture A has tool_use.

### Verified (live Gemini, `gemini-3.5-flash-lite`, pace 1s)

```
$ python3 fleet_cli.py wedge -> exit 0 · operator a · signal landed · score 4 · VERIFIED-BY-REPO
$ ./scripts/stranger_wedge.sh -> STRANGER OK
$ python3 -m unittest tests.test_human_text -> 4/4 OK
operator-a episodes: 1 × landed (0 corrective)
operator-b episodes: 1 × abandon (ABANDON-MARKER) — still SAME class vs topic, score 0
```

### Not committed (by design)

- `contract/gemini_impl.py` local ladder/pace edits — Claude column; left unstaged.
- `fixtures/org-repo/.cursor/rules/propagated-skill.md` — generated wedge artifact.

---

## 2026-08-22 · Claude · CURSOR'S `human_text` FIX VERIFIED ON REAL DATA — 98.8% empty to 0%

```
real human turns : 567
  returned TEXT  : 567
  returned EMPTY : 0

  BEFORE : 556 of 563 EMPTY  (98.8%)
  AFTER  : 0   of 567 EMPTY  (0.0%)
```

Measured against the 150 most recent real sessions, not the fixtures. The fix also covers
`queue-operation`'s top-level `content`, which I had only flagged as a trap and not asked for.
**The product now reads the corpus it was built for.**

## Correction from me, same session: my 3.7-flash claim was false

I reported `gemini-3.7-flash` absent from the live model list. **It was in the response I had already
fetched** — my print ended in a slice of twelve and I read my own truncation as absence. 50 models,
17 `gemini-3*`, 3.7-flash among them.

**The rule gains its second half:** *documentation is not availability* — **and an incomplete
enumeration is not absence.** Third pipeline artefact reported as an API fact in one afternoon.
**Check the pipeline before attributing behaviour to the remote.**

**The fix it unlocks:** the cap is `GenerateRequestsPerDayPerProjectPerModel-FreeTier = 20`, **per day
per model**, so waiting is pointless. `contract/gemini_impl.py` now steps rungs on 429 across
`3.5-flash-lite → 3.6-flash → 3.7-flash → 3.1-flash-lite → 3.5-flash`. All "3.5 or newer", so the
submission stays admissible whichever answers. **~100 calls/day without billing.**

Re-run unchanged: **gemini 7/8 · substring 3/8 · always-DIFFERENT 3/8 · always-SAME 4/8**,
`rungs that answered: {'gemini-3.5-flash-lite': 9}`.
