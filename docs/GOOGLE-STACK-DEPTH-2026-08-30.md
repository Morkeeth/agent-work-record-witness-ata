# Where the Witness sits in Google's stack — measured, 2026-08-30

**Lane:** Google-stack depth · **Written:** 2026-08-29 evening, for the Mon 31 Aug 17:00 PDT deadline
**Method:** every row below was produced by running the command printed next to it against the live
`hack-fleet` project or the deployed service. Where a claim is reasoned rather than probed it says
`REASONED`. Nothing was deployed, nothing was submitted, no verdict logic was touched.

**Companion docs:** [`ARCHITECTURE.md`](ARCHITECTURE.md) · [`SUBMISSION.md`](SUBMISSION.md) ·
[`GEAP-GAP-2026-08-27.md`](GEAP-GAP-2026-08-27.md) ·
[`PARTNER-INTEGRATION-DEEP-DIVE-2026-08-29.md`](PARTNER-INTEGRATION-DEEP-DIVE-2026-08-29.md)

---

## 0 · Five corrections first, because a correction is worth more than an addition

Ranked by what a Google judge would find fastest.

### C1 — `SUBMISSION.md` §5 calls the auth gate **IAM**. It is not IAM.

The submission table row reads *"**IAM / service account** — Every mutating route returns 401 to an
anonymous caller, probed 28 Aug · ✅ verified."* The 401 is real. Attributing it to IAM is not.

```
$ gcloud run services get-iam-policy fleet-wedge --region us-central1 --project hack-fleet
bindings:
- members:
  - allUsers
  role: roles/run.invoker
```

**The only IAM binding on this service grants `roles/run.invoker` to `allUsers`.** IAM is configured
to admit everyone, and ingress is `all`. The 401 comes from `_require_token()` at
`cloud/service.py:216` — an application-level shared bearer token compared with `==`. Cloud Run's
own authentication layer is not on the request path at all.

The `/hold/` console is already closer — it says *"IAM / shared secret"* — but even that label
implies IAM participates. **Recommended wording, and it is a stronger sentence than the one it
replaces:** *"Application token gate. Cloud Run is public by design so a judge can click the console;
every mutating route is refused without a bearer token. Honest limit: one shared token, not
per-agent identity, and not IAM."*

A judge who runs `get-iam-policy` finds `allUsers` in four seconds. Fix the label before Monday.

### C2 — `ARCHITECTURE.md` "Live vs roadmap" is stale in the **under**claim direction

It lists as roadmap: *"Gemini invoked inside the container (the ADK agent is constructed and visible
in `/health`, and is not called on the request path today)."*

That is no longer true, and the live record disproves it:

```
$ curl -s https://fleet-wedge-33kamss2jq-uc.a.run.app/audit | jq '.events[0]'
  "store_id": "H-a6151a95ac",
  "agent_invoked": true,
  "agent_explanation": {
    "invoked": true,
    "model": "gemini-3.5-flash-lite",
    "framework": "google.adk.runners.Runner",
    "started_at": "2026-08-29T12:15:13+00:00"
  }
```

P1 from the partner deep dive shipped. `cloud/service.py` calls `attach_agent_explanation()` on the
clearance path and the row written by a real GitHub Action carries `invoked: true`. The doc has not
caught up with the code. **Move that line from roadmap to live.** Note the subtlety worth keeping:
`/health` still reports `invoked: false` because the receipt is per-process and the health check runs
in a different instance — the `/hold/` console already explains this correctly and should not be
changed.

### C3 — `SUBMISSION.md` §5 omits Gemini and ADK from the Google-stack table entirely

The table lists Cloud Run, Firestore, GitHub Actions, IAM. **The mandatory hackathon requirement —
Gemini 3.5+ and a Google agent framework — does not appear in the document's own "On the Google
stack" section.** `ARCHITECTURE.md` has it (the mandatory-stack table) and the `/hold/` console has
it (the "Gemini via ADK" row). The submission doc, which is the one a judge reads, does not. Add a
row. The evidence already exists: record `H-a6151a95ac`, `agent_explanation.invoked: true`.

### C4 — `GEAP-GAP` §2 marks Model Armor enablement "assumed, not verified". It is now verified.

That doc says *"whether Google **Model Armor** is enabled on the `hack-fleet` project. `gcloud
services list` was not run."* It has now been run.

```
$ gcloud services list --enabled --project hack-fleet | grep -i modelarmor
modelarmor.googleapis.com

$ curl -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    https://modelarmor.us-central1.rep.googleapis.com/v1/projects/hack-fleet/locations/us-central1/templates
{}
```

**The API is enabled and reachable with ADC and returns an empty template list.** Enabled is not
wired — the theater rule in `GEAP-GAP` §3 still stands, and nothing in `cloud/` calls it. But R7's
premise changes: the managed product is one template creation and one `sanitizeUserPrompt` call
away, not a from-scratch local guard. Update the estimate, keep the naming ban until a call is made.

### C5 — The live revision moved under us

The brief for this lane named `fleet-wedge-00010-xww`. The service is on
**`fleet-wedge-00011-p5b`**, and the Cloud Logging request log shows the cutover between 12:11 and
12:15 UTC today.

```
$ gcloud run services describe fleet-wedge --region us-central1 --format='value(status.latestReadyRevisionName)'
fleet-wedge-00011-p5b
```

Not a defect — evidence that the tree and the deployment are both moving. Anyone writing a revision
number onto a judge-facing surface should re-probe it Monday morning rather than quote this file.

**Two more, filed as honesty rather than corrections** (neither is claimed anywhere, both are things
an enterprise buyer would ask about, and saying them first is worth more than being asked):

- `HOLD_API_TOKEN` is a **plaintext environment variable** on the Cloud Run service.
  `secretmanager.googleapis.com` is enabled on the project and unused. Anyone with
  `run.services.get` on `hack-fleet` can read the token. Post-Monday: move to a Secret Manager
  reference and rotate. *(The value is deliberately not reproduced in this document.)*
- The service runs as **`568004190078-compute@developer.gserviceaccount.com`**, the default compute
  service account, which holds `roles/editor` on the project:
  ```
  $ gcloud projects get-iam-policy hack-fleet --flatten="bindings[].members" \
      --filter="bindings.members:568004190078-compute@developer.gserviceaccount.com" \
      --format="value(bindings.role)"
  roles/aiplatform.user
  roles/artifactregistry.writer
  roles/datastore.user
  roles/editor
  roles/storage.objectAdmin
  ```
  A product that sells "the record is append-only" runs under a principal that can delete the
  Firestore collection. That is a hackathon-project reality, not a design position. The fix is a
  dedicated service account with `datastore.user` only, ~30 min, post-Monday.

---

## 1 · Where this actually sits in Google's stack

The honest frame first. **The Witness is not a platform layer. It is a check that runs in CI and a
record that lives on Google Cloud.** What follows names, per Google product, the seam — the thing
that product does not do, that the Witness does. Where the product is not enabled on `hack-fleet`,
the seam is conceptual and is marked so.

**Enablement, probed** (`gcloud services list --enabled --project hack-fleet`):

| Enabled today | Not enabled |
|---|---|
| `run` · `firestore` · `bigquery` · `cloudbuild` · `artifactregistry` · `cloudtrace` · `logging` · `pubsub` · `secretmanager` · `aiplatform` · `modelarmor` · `agentregistry` · `securitycenter` (API only — see §1.6) | `binaryauthorization` · `clouddeploy` · `assuredworkloads` · `containeranalysis` · `ondemandscanning` |

### 1.1 Cloud Build — *seam: it attests the build, never the claim*

Cloud Build produces **SLSA build provenance**: this image was built from this source at this commit
by this builder. That is an unforgeable statement about *how an artifact came to exist*. It says
nothing about the sentence an agent wrote in the pull request that produced the source — *"I
refactored the auth module and the tests pass."* Provenance covers the transformation from source to
artifact; the Witness covers the transformation from **intent to source**, which is where the agent
actually acts and where nothing in the supply chain looks today.

Concretely: Cloud Build would happily produce perfect provenance for an image built from a commit
whose PR body claimed a test suite that never ran.

`cloudbuild.googleapis.com` is enabled; `gcloud builds list --project hack-fleet` returns **zero
builds** — no Cloud Build step exists in this repo today. See §3.2 for the buildable version.

### 1.2 Artifact Registry — *seam: it stores and scans artifacts, not assertions*

Artifact Registry holds images and packages and (with Artifact Analysis) scans them for known CVEs.
Its unit of analysis is a binary. The Witness's unit of analysis is a **natural-language claim about
work**, which never becomes an artifact and therefore never enters Artifact Registry's field of view.
`artifactregistry.googleapis.com` is enabled and used to host this service's own image.

### 1.3 Cloud Deploy — *seam: it orchestrates promotion, and inherits whatever entered the pipeline* · **CONCEPTUAL, API not enabled**

Cloud Deploy manages the promotion of a release through targets with approvals. Its approval gate is
a **human clicking approve**, and the thing that human is approving is a release, described by the
metadata upstream tools attached to it. Today nothing upstream attaches "were the agent's claims about
this change true". The Witness's record is exactly the missing field on that approval screen. Marked
conceptual: `clouddeploy.googleapis.com` is not enabled on `hack-fleet` and nothing in this repo
touches it.

### 1.4 Binary Authorization — *seam: it enforces attestations, and has no attestor for agent claims* · **CONCEPTUAL, API not enabled**

This is the closest analogue in Google's catalogue and the most important seam to state precisely.

Binary Authorization is a **policy engine over attestations**. It does not itself decide anything
about quality; it checks that a required attestor has signed the digest, and refuses deployment
otherwise. Google ships attestors for build provenance and for vulnerability scanning. **There is no
attestor in the catalogue whose predicate is "the claims the author made about this change survived
being checked against the repository."**

That is the shape of the argument in §2: the Witness is not a competitor to Binary Authorization, it
is a **candidate attestor** for it. Marked conceptual: `binaryauthorization.googleapis.com` is not
enabled on `hack-fleet`, no attestation is produced by any code in this repo, and the Grafeas note
format is not implemented. This is roadmap and is labelled roadmap in §4.

### 1.5 Assured Workloads — *seam: it constrains where and by whom, never what was claimed* · **CONCEPTUAL, API not enabled**

Assured Workloads enforces data residency, personnel controls and compliance regimes on a folder.
Its questions are *which region, which support personnel, which key*. It has no opinion about the
truth content of a change. In a regulated release (`SUBMISSION.md` §4 case 5) the two are
complementary: Assured Workloads makes the environment attestable, the Witness makes the **change**
attestable. Not enabled on `hack-fleet`; it is also a folder/org-level product and this project has
no org (§1.6).

### 1.6 Security Command Center — *seam: it aggregates findings about resources, not about work* · **NOT ACTIVATED, and cannot be before Monday**

SCC's model is a *finding* attached to a *resource*, emitted by a *source*, aggregated for a security
team. A HOLD is a genuinely SCC-shaped object: severity, category, resource, evidence, a state that
opens and closes. Emitting holds as findings would put agent-claim failures in the same queue as
misconfigurations and vulnerabilities, which is where a CISO already looks.

**It is not available to us.** Probed:

```
$ gcloud organizations list
Listed 0 items.

$ gcloud projects describe hack-fleet --format='yaml(parent,projectId)'
projectId: hack-fleet
   # no parent — the project has no organization

$ curl -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: hack-fleet" \
    https://securitycenter.googleapis.com/v2/projects/hack-fleet/sources
{"error":{"code":404,"message":"Requested entity was not found.","status":"NOT_FOUND"}}
```

`securitycenter.googleapis.com` appears in the enabled list, but **enabling the API is not activating
the service**. SCC sources are created under an organization; this account has none, and the
project-level v2 path returns 404 because SCC is not activated for this project. Creating an
organization requires a Cloud Identity / Workspace domain.

**Verdict: SCC emission is not buildable and not demonstrable before Monday.** Do not put it on a
slide as anything but roadmap. This "no" is one of the more useful findings in this document —
it is the row a judge would most expect us to fake.

### 1.7 Cloud Logging / Cloud Audit Logs — *seam: they record the API call, not whether the work was real*

Precision matters here, and a Google judge will notice imprecision. Two different things:

- **Cloud Audit Logs** record *which principal called which Google Cloud API*. Admin Activity logs are
  on by default; **Firestore Data Access logs are off by default**, so today no audit log exists for
  the writes into the record.
- **Cloud Run request logs** (plain platform logs, on by default) record every HTTP request to the
  service. These exist and are rich. Probed:

```
$ gcloud logging read 'resource.type="cloud_run_revision"
    AND resource.labels.service_name="fleet-wedge"
    AND httpRequest.requestUrl:"/clearance"' --limit 5 --freshness=2d \
  --format='value(timestamp,httpRequest.requestMethod,httpRequest.status,trace,resource.labels.revision_name)'

2026-08-29T15:57:37.967Z  POST  401  projects/hack-fleet/traces/816094298b2d54c7c123f4cd713b4670  fleet-wedge-00011-p5b
2026-08-29T12:15:06.735Z  POST  201  projects/hack-fleet/traces/749076b71770eb7ec8f426b0e8a5b0a6  fleet-wedge-00011-p5b
2026-08-29T12:11:52.625Z  POST  201  projects/hack-fleet/traces/ad2864028433fb06da951afbff2f4566  fleet-wedge-00010-xww
2026-08-29T12:07:51.292Z  POST  401  projects/hack-fleet/traces/b6c2ad65e4feafc81b5cf3880e990534  fleet-wedge-00010-xww
2026-08-29T12:06:02.540Z  POST  401  projects/hack-fleet/traces/6e66cee3bcad1231580c9a33e99f028f  fleet-wedge-00010-xww
```

**Two findings, both load-bearing.**

**(a) The correlation is already possible with no code change.** The Firestore row `H-a6151a95ac`
carries `stored_at: 2026-08-29T12:15:09Z`; the request that produced it is the `201` at
`12:15:06.735Z`. A 2.3-second window, one record, one log line. See §3.3.

**(b) The log holds something the record structurally cannot: the rejections.** Three `401`s appear
above. **None of them is in the Firestore record**, and that is correct — a refused write is not a
clearance. But "how many callers tried to write to the record without a token" is a real question an
auditor asks, and only the platform log can answer it. That is a genuine, non-marketing reason the
two layers belong together, and it is the sentence to use on camera: *the record says what was
decided; the log says what was attempted.*

**(c) Cloud Run already mints a trace id per request** — the `trace` field above is populated on every
line, unprompted. `GEAP-GAP` R5 estimates observability at "4–6h, new OpenTelemetry dependency". For
the judge-visible half of that — a `trace_id` on the record, linkable from `/hold/` — the platform has
already done the work: Cloud Run passes `X-Cloud-Trace-Context` to the container and the service need
only read that header and store it. **Zero new dependencies, stdlib only, well under an hour of code.**
`REASONED` on the container side: the platform side is probed above; that the header arrives inside
this specific container is not verified and would be confirmed by the same deploy that ships it.
The full OTel span tree remains a 4–6h job — but the cheap 90% of R5 is much cheaper than R5 says.

### 1.8 BigQuery — *seam: it is where the questions get asked, and the record is not there*

`SUBMISSION.md` §4 case 10 is the corpus product: *"which of our repositories, teams and agents
produce claims that hold."* That is a SQL question. The record answers it today only through
`GET /audit/export`, a JSON blob a human downloads.

```
$ bq ls --project_id=hack-fleet
   # (empty — no datasets)
```

`bigquery.googleapis.com` is enabled and **zero datasets exist**. Every enterprise that would buy this
already runs BigQuery, already has dashboards over it, and already has row-level access controls on
it. The seam is not "BigQuery cannot store JSON" — it obviously can. The seam is that **the record is
currently a file you download instead of a table you join**, so it cannot be joined to the customer's
own deployment, incident or headcount tables. That join is the entire day-two product. See §3.1.

### 1.9 Vertex AI / ADK — *seam: Vertex runs the agent; nothing checks the agent's report*

Vertex AI and ADK are where the agent *lives*. Vertex tracks model, cost, latency, safety filters and
(with Agent Engine) sessions. **None of that observes the gap between what an agent did and what it
said it did**, because the report is written after the trace ends and is evaluated by a human reading
prose. The Witness reads that prose against the repository.

This is also where the honest boundary sits: **the model gets no veto.** `attach_agent_explanation()`
narrates findings; `outcome_gate.py` owns the verdict. That boundary is what keeps a prompt-injected
report from talking its way through the gate, and it is the sentence that makes the Vertex
relationship a strength rather than a dependency: *Gemini explains. Python decides.*

### 1.10 Agent Registry — *seam: it will list your agents; nothing scores them* · **live, unexpectedly**

This one surprised the probe. `agentregistry.googleapis.com` is enabled and answers on this project:

```
$ curl -H "Authorization: Bearer $TOKEN" \
    https://agentregistry.googleapis.com/v1/projects/hack-fleet/locations/us-central1/agents
{"agents":[{"name":"projects/hack-fleet/locations/us-central1/agents/agentregistry-...",
            "agentId":"urn:agent:googleapis.com:locations:global:workspaceagent:workspaceagent--a2a",
            "displayName":"Workspace Agent","version":"1.0",
            "protocols":[{"type":"A2A_AGENT","protocolVersion":"0.3.0", ...}]}]}
```

One agent, Google's own Workspace Agent, A2A protocol 0.3.0. **`GEAP-GAP` row 1 marks Agent Registry
ABSENT, and that remains correct about our code** — `/prove` propagates a prompt and nothing is
registered. But the surrounding fact changed: Google's Agent Registry is a live, project-scoped API
reachable with plain ADC, and it is where an enterprise's agent inventory will be enumerated.

**The seam is the interesting part.** A registry answers *what agents do we have*. It has no field for
*and how much of what they claim holds up*. Every registered agent is an identity the Witness's record
could key on. That is the cleanest one-sentence statement of where this product belongs in Google's
stack a year out — and it is roadmap, see §4.

---

## 2 · The strongest single claim, argued against the real overlaps

**The claim:** *Google has an attestation chain for artifacts and an audit trail for principals. It
has neither an attestor nor an audit surface for the assertions an agent makes about its own work.
That is the gap the Witness fills.*

**Now the adversarial pass, because the brief asked for a "no" if a "no" is true.**

**Does Binary Authorization already cover it?** No, and the reason is structural rather than
rhetorical. BinAuthz is a *policy engine over attestations*: it verifies that a required attestor
signed a specific image digest, and blocks deployment otherwise. It is deliberately agnostic about
what the attestation *means*. Google supplies attestors for build provenance and vulnerability
scanning. The predicate "the author's claims about this change survived a probe against the
repository" is not among them, and could not be, because no Google product evaluates that predicate.
BinAuthz is the **consumer**; the missing piece is a **producer**. The Witness is producer-shaped.

**Does Cloud Audit Logs already cover it?** Partly, and here is the concession the brief asked for.
"Who did what" is genuinely Cloud Audit Logs' job and the Witness does not compete there and should
never claim to. If the question is *which principal called which API at what time*, use audit logs.
The Witness's question is a different one and does not reduce to it: **an audit log records that a
merge happened; it has no representation of the sentence "and the tests pass," and therefore cannot
record that the sentence was false.** Truth-of-assertion is not in the audit log's schema.

**Does Cloud Build / SLSA provenance already cover it?** No, per §1.1: provenance is unforgeable about
*source → artifact* and silent about *intent → source*. Agents act on the second edge.

**Does Vertex AI evaluation / Gen AI evaluation service already cover it?** This is the nearest real
threat and deserves a straight answer. Vertex's evaluation tooling scores model outputs against
metrics and reference answers, in a harness, before or alongside deployment. It is an **offline
quality instrument**. The Witness is an **online release control on a specific change** whose ground
truth is the customer's own repository at merge time, not a reference set. Related discipline,
different object, different moment. But an honest hedge: if Google shipped a "claim verification"
metric wired into a release pipeline, the overlap would be substantial. Nothing observed on
`hack-fleet` does that today.

**So: is it genuinely the missing attestation layer for agent-authored change?**

**As an argument, yes — and it is the right pitch.** The seam is real, structural, and no probed
Google product occupies it.

**As a built thing, not yet, and the gap should be stated plainly.** An attestation layer means: a
signed statement, in a format a policy engine ingests, that a policy engine actually enforces. The
Witness today produces an **append-only record with per-claim evidence** — which is the substance of
an attestation — and stops there. It emits no Grafeas note, signs nothing with KMS, and no BinAuthz
policy consumes it. `binaryauthorization.googleapis.com` is not even enabled on the project.

**The one sentence that is both maximally strong and entirely true:**

> Binary Authorization decides which images may deploy, based on attestations that only ever describe
> how the artifact was built. Nothing signs an attestation about whether the *agent's report* on that
> change was true — so we built the thing that produces that record, and making it a signed
> attestation a Binary Authorization policy enforces is the next step, not a shipped one.

Say "next step" out loud. That is the difference between the pitch and the falsifiable version, and
this project's whole differentiator is that it says which is which.

---

## 3 · Buildable before Monday — ranked by hours, honestly

Split by the constraint that actually discriminates: **can it be demonstrated live without a
redeploy?** A redeploy is Oscar's click, and Monday's deployment state belongs to the filming
session, not to this lane.

### Tier A — demonstrable live Monday, touches nothing on the request path

#### 3.1 · BigQuery: the record becomes a table — **RANK 1 · RUN, NOT ESTIMATED**

**This row is a receipt, not a projection. It was built and executed while writing this document,
in under 30 minutes.** The rule in this repo is that "valid" is not "it runs", so it was run.

*What:* read `GET /audit/export`, flatten each event to a row, load into dataset `witness_record`,
table `clearances`. Nested `findings[]` becomes a `REPEATED RECORD` — BigQuery's native shape for
exactly this, so the per-claim assertion, probe, verdict and evidence survive the trip rather than
collapsing into a JSON string.

```
$ bq mk --dataset --location=US hack-fleet:witness_record
Dataset 'hack-fleet:witness_record' successfully created.

$ bq load --source_format=NEWLINE_DELIMITED_JSON --autodetect --replace \
    hack-fleet:witness_record.clearances clearances.ndjson
Current status: DONE      # 12 rows, 9 carrying findings
```

*The demo query, and its real output:*

```sql
SELECT repo, actor, gate, COUNT(*) AS n,
       COUNTIF(f.verdict = 'BLOCK') AS blocked_claims
FROM `hack-fleet.witness_record.clearances`, UNNEST(findings) AS f
GROUP BY repo, actor, gate ORDER BY n DESC
```

```
+----------------------------------------+-------------------+-------+---+----------------+
|                  repo                  |       actor       | gate  | n | blocked_claims |
+----------------------------------------+-------------------+-------+---+----------------+
| Morkeeth/agent-work-record-witness-ata | Morkeeth          | BLOCK | 6 |              6 |
| acme/payments                          | coding-agent[bot] | BLOCK | 4 |              4 |
| Morkeeth/agent-work-record-witness-ata | github-action     | BLOCK | 2 |              2 |
| Morkeeth/hack-fleet-ata                | phase-a           | BLOCK | 2 |              2 |
| NULL                                   | skeptic           | BLOCK | 1 |              1 |
| Morkeeth/agent-work-record-witness-ata | test              | BLOCK | 1 |              1 |
+----------------------------------------+-------------------+-------+---+----------------+
```

That is `SUBMISSION.md` §4 case 10 — *"which repositories, teams and agents produce claims that
hold"* — ceasing to be a paragraph and becoming a result set, in the warehouse the buyer already
runs.

*Remaining work to make it demo-grade:* ~1h. Wrap the flattening in `scripts/export_to_bigquery.py`
(it currently exists only as the ad-hoc script that produced the load above), pin an explicit schema
instead of `--autodetect`, and rehearse the console view. **Total 1–1.5h, of which the risky part is
already done.**

*What to say honestly, and the table itself enforces it:*

- **A one-shot copy, not a live sink.** The service does not write to BigQuery; a script does, on
  demand. Say "the record exports into the warehouse you already run"; never say "streams". The
  continuous Firestore→BigQuery pipeline is roadmap (§4.3).
- **Every row says BLOCK, and `clear: 0` is visible in the output above.** Nothing has ever passed
  this gate because nothing real has ever gone through it — exactly what `ARCHITECTURE.md` §"What is
  NOT claimed" already states. `acme/payments` / `coding-agent[bot]` is a staged demo row and is
  identifiable as one. **Show it as-is; do not seed it.** A busy table in a weekend project is the
  thing a judge should distrust.
- **One `NULL` repo** (`actor: skeptic`) — an early probe row with no repo attached. Left in rather
  than filtered, per the repo's own rule that a filter which quietly shrinks a finding list is the
  flattering version.

*Side finding, and it corrects a pessimistic note elsewhere:* `/audit` returns **36** events
(24 `prove`, 9 `clearance`, 2 `exception`, 1 `agent_run`) but `/audit/export` returns **12** — the
export already excludes the `prove` rows. **`GEAP-GAP` §4's "the audit store is 80% probe noise"
is true of `/audit` and false of the compliance artifact a judge actually downloads.** The export is
100% decisions. Worth saying on camera, because it is the surface being sold.

*Risk:* low, and it is reversible: `bq rm -r -f hack-fleet:witness_record`. New dataset, no existing
data touched, nothing in `gate/` or `cloud/` changed, no deployment involved.

#### 3.2 · Cloud Build: the gate runs outside GitHub — **2–3h · RANK 2**

*What:* a `cloudbuild.yaml` with one `python` step that runs `gate/outcome_gate.py` against a report
body, and a second step that POSTs the verdict, with the token pulled from **Secret Manager** via
`availableSecrets` rather than an environment variable.

*Demo:* `gcloud builds submit --config cloudbuild.yaml` in front of a judge; the build goes red on a
false claim. Two things land at once: the gate is **not GitHub-shaped** — it is a probe plus an HTTP
POST and it runs anywhere CI runs — and it runs natively inside Google's own CI, which is the
question a Google judge is actually asking. It also demonstrates the Secret Manager pattern that C1's
plaintext-token finding wants, without touching the deployed service.

*What breaks:* Cloud Build needs Secret Manager accessor permission for the build service account,
and `gcloud builds list` shows **zero builds ever** on this project, so the first run will surface
whatever first-run friction exists. Budget an hour of that inside the estimate. Also: this is a
*demonstration* that the gate is portable, not a shipped Cloud Build integration — do not describe it
as "we support Cloud Build."

*Risk:* low-moderate. Nothing deployed changes; the failure mode is a red build in a project with no
build history to disturb.

#### 3.3 · Cloud Logging correlation: record ↔ request ↔ trace — **1–2h · RANK 3**

*What:* a script, or honestly just two commands and a short doc section, that takes a record id and
returns the platform log line that produced it, using `stored_at` as the join key — plus the
rejection count the record cannot show.

*Demo:* live, exactly as probed in §1.7 — `H-a6151a95ac` at `12:15:09Z` beside the `201` at
`12:15:06.735Z` on revision `fleet-wedge-00011-p5b`, then the three `401`s that never became records.
*The record says what was decided. The log says what was attempted.* Cheapest credible Google-depth
beat available and it is already proven to work, above.

*What breaks:* the join is **timestamp proximity, not a shared key** — say so. The principled fix is
storing the trace id, which needs a deploy (Tier B). Do not present a 2.3-second window as a
foreign key.

*Risk:* none. Read-only.

**Tier A total: 4–7h for three live Google-stack beats, no redeploy, no verdict logic touched — and 3.1, the highest-value one, is already proven to work.**
If only one gets built, build 3.1 — BigQuery is the layer the buyer already owns.

### Tier B — buildable this weekend, but needs a redeploy to go live

Each is code someone could write and test locally before Monday; none can be *shown running in
production* without Oscar's deploy click. If the filming session is redeploying anyway, 3.4 is the
best value in the document per hour.

| # | Work | Hours | Notes |
|---|---|---|---|
| **3.4** | Read `X-Cloud-Trace-Context` in `do_POST`, store `trace_id` on the record, link it from `/hold/` | **~1h** | Turns 3.3's timestamp join into a real key. Stdlib, **no new dependency** — the platform already mints the id (§1.7c). `GEAP-GAP` R5's "4–6h + OpenTelemetry" overstates this half by roughly 5×. |
| **3.5** | Model Armor pre-probe guard on `report` text; refusal recorded as a finding | 3–4h | API enabled and reachable (C4). Only after a real `sanitizeUserPrompt` call may the product name be used — the `GEAP-GAP` §3 ban holds until then. |
| **3.6** | `HOLD_API_TOKEN` → Secret Manager reference + rotate | ~30 min | Fixes the C-block finding. Pure deploy config, no code. |
| **3.7** | Vertex session service on `/agent/run` | 4–6h | Unchanged from `GEAP-GAP` R4 / deep-dive P5. Not worth the risk this weekend. |

### Tier C — assessed and rejected for Monday

| Candidate | Verdict | Evidence |
|---|---|---|
| **Security Command Center findings** | **Impossible before Monday** | No organization (`gcloud organizations list` → 0 items); project has no parent; SCC v1 and v2 project-source paths both return 404 NOT_FOUND. Needs an org and SCC activation, which needs a Cloud Identity domain. §1.6. |
| **Binary Authorization attestation** | Not before Monday | API not enabled; requires attestor + KMS key + Grafeas note + a policy that consumes it. Real roadmap (§4.1), 1–2 days minimum, and pointless without a GKE/Cloud Run deploy policy to enforce it. |
| **Agent Registry registration** | Possible (~1–2h) but **flagged, not recommended** | API is live (§1.10) and `POST .../agents` would register the witness. It creates a persistent cloud resource on the demo project two days before filming, for a beat that is a listing rather than a capability. **Coordinator's call, not this lane's.** |
| **Firestore→BigQuery live pipeline** | Not before Monday | Datastream/extension setup plus a schema decision. 3.1 gets the demo value at a fraction of the risk. |
| **Cloud Deploy / Assured Workloads** | Not applicable | Neither API enabled; both need infrastructure this project does not have. Conceptual seams only (§1.3, §1.5). |

---

## 4 · Roadmap — and this section is roadmap, stated as such

Nothing below is built, none of it will be built before Monday, and no item here may appear on a
judge-facing surface without the word roadmap attached. This is the "next natural step of Google's
stack" argument in its honest form: a sequence, not a claim.

**4.1 · The Witness as a Binary Authorization attestor.** The record row becomes a signed Grafeas
attestation over the commit or image digest, keyed by KMS, with a BinAuthz policy that refuses to
deploy any image whose source commit carries an open HOLD. This is the sentence in §2 becoming a
mechanism, and it is the single most valuable item on this list because it makes the Witness
*enforcing* rather than *advisory* using Google's own enforcement point rather than a new one.
*Prerequisites: an org, `binaryauthorization` + `containeranalysis` enabled, a KMS key, an attestor.*

**4.2 · Holds as Security Command Center findings.** A HOLD is finding-shaped. The moment there is an
organization with SCC activated, agent-claim failures land in the queue a CISO already reads, beside
misconfigurations and CVEs. Blocked purely on org structure, not on design (§1.6).

**4.3 · The record as a live BigQuery sink, joined to the customer's own tables.** 3.1 proves the
shape with a one-shot copy. The product is the continuous version joined to deployment, incident and
team tables — *"do the repos whose agent claims fail also produce the incidents"* is a question no
current vendor can ask, and it needs a quarter of history, which is exactly why `SUBMISSION.md` §4
case 10 calls it the compounding asset.

**4.4 · Agent Registry as the identity spine.** Today the record's `actor` is a GitHub login. In a
Google-native enterprise it should be the Agent Registry resource name, so the record answers
"which *agent*" rather than "which account opened the PR". The registry is live (§1.10); the join is
not built. This is the row that turns the record from a CI artifact into a fleet instrument.

**4.5 · Model Armor on the ingest boundary.** After 3.5 makes one real call, the roadmap version is a
template per customer with their own PII and injection policy applied to every report before it is
probed. Until that first call: **do not say Model Armor.**

**4.6 · Cloud Trace spans end to end.** 3.4 stores the id; the full version spans the GitHub Action,
the gateway and the ADK run, so a hold opens to its trace as well as its transcript.

**4.7 · Pub/Sub fan-out to enterprise SIEM.** `pubsub` is enabled and unused. A `clearance.hold`
topic is trivial to publish to and worthless without a consumer, which is why it stays here rather
than in §3. `ARCHITECTURE.md` already lists Pub/Sub fan-out under "What is NOT claimed" — keep it
there.

---

## 5 · The one measurement that would make the Google claim credible

**Carried over from the Qwen loss: every number we reported was scored against our own data, with no
arm outside our control. The corpus in `ENTERPRISE-CASE` has the same defect** — one operator, one
machine, our own transcripts, our own labels. `SUBMISSION.md` §6 already discloses it. Disclosure is
not a control arm.

**Design only. Not run — it costs more than an hour, and §5.5 says what it costs.**

### 5.1 The question, narrowed until it is falsifiable

Not *"are agents unreliable"* — unanswerable and not our claim. The claim a Google judge should be
able to falsify is narrower and is the actual product claim:

> **On pull requests we did not write, in repositories we do not own, the Witness's four-verdict probe
> separates false done-claims from true ones at a rate materially better than chance — and the
> failures it finds are specific to agent-authored PRs rather than an artifact of the extractor.**

### 5.2 The corpus, and it must be outside our control

Public GitHub pull requests **authored by identifiable coding agents** — `Copilot`, `devin-ai-integration[bot]`,
`cursoragent`, `claude[bot]` and similar — on public repositories with **no connection to Oscar**.
Sampled through the GitHub search API, frozen to a commit-pinned list **before any claim is
extracted**, and shipped as a fixture so anyone can re-run it. Target n ≈ 200 PR bodies, which is an
order of magnitude past the n = 13 that `SUBMISSION.md` §6 correctly refuses to call a measurement.

Nothing about this corpus is on our disk, and that is the entire point.

### 5.3 The control arm — the thing the Qwen run did not have

**Arm A:** agent-authored PRs. **Arm B:** human-authored PRs from the *same repositories, same time
window, matched on PR size*, run through the *identical* extractor and probe.

Arm B is what makes the result mean anything. If both arms fail at the same rate, the instrument is
measuring how people write PR descriptions, not how agents misreport work — and the headline claim is
dead. **Also run the negative control the repo already has a name for:** a stub that returns the
modal verdict for every claim, per `contract/task_class.py:81`. `ARCHITECTURE.md` records that a
defaulting stub once beat the real baseline in this repo. That mistake must not be repeatable here.

### 5.4 Preregistration and the falsifiers, written before the first look

Following `CORPUS-PREREGISTRATION-2026-08-27.md`, which is the method that saved the 41.7% → 8.1%
correction and is the strongest asset this project has. Fixed in advance: which claim types count
(SHA, path, test), the denominator, the exclusion reasons, and the sibling-repo confound that caused
the original error. Then the falsifiers, each of which kills the claim if it fires:

| # | Falsifier | Kills |
|---|---|---|
| **F1** | Arm B (human PRs) disagrees with the repo at a rate within the confidence interval of Arm A | The agent-specific claim entirely. The product measures prose, not agents. |
| **F2** | Blind hand-labelling of 40 sampled extractions puts extractor precision below 0.7 on PR bodies | The instrument. `SUBMISSION.md` §6 measured 13/40 on *conversational* prose; PR bodies should be far cleaner — **measure it, do not assume it**. |
| **F3** | Every disagreement resolves to a probe artifact (sibling repo, force-push, squash-merge rewriting SHAs) rather than a false claim | The finding. This is the 73-of-103 failure recurring, and squash-merge is a confound our own corpus never faced. |
| **F4** | The modal-verdict stub scores within noise of the real probe | The whole instrument, exactly as it did once before in this repo. |
| **F5** | Fewer than 30 probeable claims survive the pre-registered filters | Statistical power. Report "underpowered" and stop; do not soften the filters after looking. |

### 5.5 What it costs, and the one-hour version that is honest

**Full run: 3–6 hours**, dominated by corpus assembly — GitHub API pagination and rate limits, cloning
or shallow-fetching each repository so the probe has an object to check, and blind hand-labelling for
F2, which cannot be delegated to the agent that wrote the report (`ENTERPRISE-CASE` §5 already names
that as the weakest link on the page). **Out of budget before Monday. Not run.**

**The honest one-hour version, if someone has an hour Sunday:** pre-register §5.1–5.4 as a committed
document *before* touching data, then pull **20** agent-authored PR bodies and **20** human-authored
ones from public repos and run only F1 and F4. n = 40 cannot support a headline. It can support one
sentence, and it is a sentence no other submission in the track will be able to say:

> *We ran the probe on pull requests we did not write, with a human-authored control arm, and
> pre-registered the falsifiers before we looked. Here is the direction, here is n, and here is what
> would have killed it.*

**What must not happen:** running it, getting a flattering number, and reporting the number without
the control arm. That is the Qwen loss with a different logo on it.

---

## 6 · Recommendation

1. **Fix C1 and C2 in the docs.** ~20 minutes, and they are the two things a judge finds fastest.
   C1 is a wrong label on a true fact; C2 is a shipped feature the doc still calls roadmap.
2. **Finish 3.1 (BigQuery, ~1h left).** Already loaded and queried — see the receipt in §3.1. The record becomes queryable in the warehouse the buyer already
   runs. Highest Google-depth-per-hour available without a redeploy.
3. **Build 3.3 (log correlation, 1–2h)** if there is time. Already proven to work in §1.7.
4. **Say "no" about SCC out loud.** A submission whose thesis is false claims, declining to fake the
   one integration it cannot reach, is the thesis demonstrating itself.
5. **If the filming session redeploys anyway, add 3.4 (~1h)** — the trace id is nearly free and turns
   3.3's timestamp proximity into a real join.

---

*Written 2026-08-29 for the 2026-08-30 working day. No deployment, no submission, no verdict logic
touched, no history rewritten. Every command in this document was run; the two `REASONED` markers are
the only inferences.*
