# COMPLIANCE AUDIT — would today's artifact be a valid submission?

**Answer: NO. It satisfies 0 of 3 mandatory requirements.** Not a lost point — a disqualification.

Run 2026-08-22 **against the Devpost rules page**, deliberately not against `docs/SPEC-EXTRACT.md`,
because that file is a claim and its author is this lane.

## The requirements, quoted from the rules page

1. *"Gemini 3.5 or newer accessed through Gemini API or Vertex AI"*
2. *"at least one Google Agent Framework: Google ADK, GenAI SDK, Antigravity SDK or GenKit"*
3. *"at least one Google Cloud infrastructure service (such as Cloud Run, Cloud SQL, Firestore, GKE, Pub/Sub)"*

## What actually exists — probed, not recalled

```
$ find . -name "*.py"  ->  fleet/signals.py 59 · fleet/propagate.py 60 · fleet/human.py 38
                           fleet/__init__.py 1  ·  fleet_cli.py       = 199 LOC total
$ grep -rhE "^import |^from " fleet/*.py fleet_cli.py | sort -u
    argparse · glob · hashlib · json · os · sys · pathlib
    (+ internal fleet.* imports)
$ grep -rniE "gemini|google|adk|vertex|genai|cloud run|firestore|pubsub"  over all .py/.html/.sh
    NO HITS outside docs/ and CURSOR-LOG.md
```

**The runnable artifact is 199 lines of stdlib Python and a static HTML page. There is no Google
technology in it of any kind.**

| Requirement | Today | Gap |
|---|---|---|
| Gemini 3.5 | ❌ absent | no model call anywhere |
| Google Agent Framework | ❌ absent | `fleet_cli.py` is an argparse CLI, not an agent |
| Google Cloud service | ❌ absent | nothing deployed, nothing hosted |

**This outranks all three previously-logged defects.** Those were wrong answers. This is not being
allowed to answer.

## It also re-prices the Aug 26 kill condition

`PHASE-0.md` treats GCP-by-Aug-26 as a schedule risk. It is not. **Without it there is no valid
submission at all**, so Aug 26 is the difference between entering and not entering, and it should be
read that way when the calibration is set.

## The good news, and it is genuinely good

**Requirement 1 and the wedge's worst defect want the same fix.**

`fleet/signals.py` matches topics with `all(t in low for t in terms)` — a substring test. The real
relation is **task-class identity**: `"fix auth"` and *"Refactor the auth module: extract
`validate_token`…"* are the same intent to any human and to Gemini, and are not the same to a
substring. That is why fixture B returns `NO_MATCH` and the demo has a field of one.

So the intent classifier is **not a checkbox bolted on to satisfy a rule.** Without it:
- the submission is invalid, **and**
- the demo has no comparison to show.

One slice repairs both. **Say that on camera** — it is the strongest available answer to *"why is
the model here at all?"*

## The cheapest HONEST version of each requirement

Not the cheapest version — the cheapest one that is load-bearing, because 40% of the score asks
*"how much friction does the agent remove on its own?"* and a checkbox removes none.

| # | Requirement | The honest minimum | Load-bearing because |
|---|---|---|---|
| 1 | **Gemini 3.5** | intent classification replacing `_topic_match` | without it there is no comparison at all |
| 2 | **ADK** | the supervisor that runs discover → select → propagate → witness | the three functions already exist as plain functions; ADK wraps them, and the loop is what acts unasked |
| 3 | **Cloud Run** | deploy the supervisor + the surface | it is also the *"visual proof of Google Cloud deployment in the video"* the 30% criterion demands, so it is paid for twice |

`gcloud run deploy --source` uses Cloud Build — **no local Docker, no Colima, and it avoids the
ARM-Mac / linux-amd64 image trap.**

## What this does NOT change
The wedge, the fixtures request, the `UNMEASURED` primitive and the surface all stand. The product
is right. **It is currently ineligible, which is a different problem and a fixable one.**
