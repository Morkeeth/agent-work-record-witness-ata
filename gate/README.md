# The Claim Gate — nothing an agent says is "done" ships until the object confirms it

**Run it:** `python3 -m gate.tonight_cases` → exits 1, blocks 3 of 4 real claims.

## Why this is the company, not a feature

Observability scores the **trace** — what the agent did. This gates the **claim** — whether what it
*said* is true. And tonight proved the false claim is almost never a fabricated commit SHA. It is:

| The claim | What it was really | Probe |
|---|---|---|
| "meets all 3 required technologies at runtime" | an **import** mistaken for a **call** (store was JsonlStore) | exercise, don't import |
| "scores 7/8, beats the baseline" | **one sample** quoted as a measurement (moved 7→6 on re-run) | power: n<30 is not a measurement |
| "the sweep says scale to ~180 live" | the **wrong room** (offline GGUF fires 100%; live is 37) | right-object: kind must match |
| "the extractor works, suite is green" | **green tests on the wrong fixtures** (98.8% empty on real data) | right-object: real corpus ≠ fixtures |

**Every row happened in this fleet on 2026-08-22, is in `CURSOR-LOG.md` with its commit, and would
have shipped.** The gate's test suite is a logged case series a competitor cannot fake.

## The three lenses

- **Judge (40%, "friction removed on its own"):** blocking a false "done" is a bigger, clearer
  autonomous consequence than propagating a prompt — and every agent PR passing through one gate is
  the "scalable network of institutional agents" the track asks for.
- **User (platform lead):** won't open a prompt-analytics dashboard daily. *Will* refuse to let an
  agent's 2am PR auto-merge on an unverified "done." This is in the critical path, not adjacent.
- **VC:** "prompt analytics" is a crowded feature with a soft budget. "The verification gate an
  autonomous workforce must pass before production" is a category being born now, with a hard budget
  — you cannot let agents merge unverified. Snyk for the AI workforce.

## Where prompt-propagation goes

It becomes **one downstream feature** — once a claim passes the gate, propagate what worked. The gate
is the painkiller that gets the product bought; propagation is the expansion that makes it sticky.

## The four probe types (extensible — each new failure mode is a new probe)
`probe_repo` (claimed SHA/path exists) · `probe_power` (a rate quoted as a result survives its own n) ·
`probe_exercise` (a service is called, not imported) · `probe_right_object` (checked against the
object the claim is about). Each names its probe and returns UNMEASURED rather than guessing.
