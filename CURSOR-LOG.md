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
