# THE AGENT WORK RECORD WITNESS — the submission

**One document. Pitch, who it is for, ten adoption cases, the Google stack, the evidence, and the
film spine. Supersedes `PITCH-WHEN-YOU-ARE-BACK.md` and `THE-PITCH-RULING.md`, which stay in git as
the reasoning that produced it.**

All Things Agentic · submits Mon 31 Aug 2026, 17:00 PDT
Live: https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/ · Repo: https://github.com/Morkeeth/agent-work-record-witness-ata

---

## 1 · The promise

> **Your agents write reports about work they did. This keeps the receipt.**
> Every claim an agent makes in a pull request is checked against the repository before the merge,
> and whether it held is written to a durable record your CI fills by itself. When your board
> asks whether an AI agent shipped unverified code, you hand them the record instead of an opinion.

**The constraint the whole product obeys, and the one line to remember it by:**
**it never runs a command that came out of a report.** A test claim is refused, not guessed. Code
decides what is confirmed, never the model.

---

## 2 · What it is, on one screen

Install is a YAML file. An **agent clearance check** (`verify-claims`) reads the pull request body, extracts each claim, probes it
against the object, and returns one of four verdicts.

```
$ python3 gate/outcome_gate.py --json < pr-body.md
gate: BLOCK exit_hint 1
   BLOCK         committed as a41c9f2               NOT a commit in this repo
   PASS          wrote src/northwind/cache.py       exists
   BLOCK         wrote src/northwind/validators.py  NO SUCH PATH in the repo
   UNVERIFIABLE  tests pass                         a test claim needs the suite RUN; this gate
                                                    never executes a command lifted from a report

gateway: H-03fe9c5e10 HOLD/BLOCK traceable=True session=01MS5iomniNWozqMjFTkLfUz
```

Four verdicts, and the fourth is the product: **PASS · BLOCK · UNVERIFIABLE · HOLD.** The one true
claim inside a false report still passes. The hold opens back to the session that produced it.

**Gate or record.** They are the same install. The gate is what you notice on day one. The record is
why you still have it in month six, because it is the only artifact that accumulates: every claim,
whether it held, who made it, whether the work survived.

---

## 3 · Who this is for

### Priya, the buyer
Runs the AI rollout at a 400-engineer company. She signed the seat contract and owns the budget
line. She has a seat count, a spend graph and a vendor dashboard showing tokens. She does not have
any idea whether the work those agents said they did, they did. In March her CTO asked her, in a
board deck review: *"If the regulator asks whether an AI agent shipped unverified code to
production, what do we hand them?"* She could not answer. **This product is that answer.**

### Marcus, the reviewer
Staff engineer, six agent-authored PRs a day in his queue. He reads a done-report that says a test
suite passes and has no way to know without running it himself, which defeats the point of the
agent. The gate tells him which claims in the body are already checked and which are refused, so his
review starts from four facts instead of a paragraph of prose.

### Dana, the platform owner
Owns CI. She does not want a new dashboard, a new vendor login, or an agent with write access to her
infrastructure. She wants one YAML file, no credentials, and a check that fails red. **The gate runs
with no account, offline, on stock Python 3.9.6.** Verified from a cold clone with `env -i`.

### Sam, the auditor
Arrives twice a year and asks for evidence, not assurances. He is not interested in a live
dashboard, he wants a record with timestamps he can sample. Every hold carries a session
reference when the report carried one, and says so plainly when it did not.

**What he must be told rather than left to find:** this is a keyed store, not an append-only log.
The API never deletes a document, but closing a hold rewrites that clearance in place
(`cloud/service.py`, the `/break-glass` route) rather than superseding it, so the prior version is
not recoverable from the record. Live example today: `H-1d8344f3dc` reads
`open: false, closed_by_exception: true` at its original `stored_at`.

---

## 4 · Ten ways an enterprise adopts this

*Cases 1 to 3 are demonstrated in this repository today. Cases 4 to 10 are the adoption path they
open, described by the mechanism that already exists rather than by a projected number. Nothing
here carries an invented figure.*

**1 · The false-done PR, caught at the merge.** *Demonstrated.* An agent opens a PR claiming a
commit that does not exist, a file that nearly exists, and a test run that never happened. The
The clearance check returns BLOCK on two, PASS on the one true claim, and UNVERIFIABLE on the test claim
rather than guessing. Real PR #1 on this repo, record row `H-a6151a95ac`.

**2 · The board question, answered with a document.** *Demonstrated.* "Prove no agent shipped
unverified." The record is queryable by claim, verdict, author and session. A VP Eng does not buy a
check, they buy the answer to the question their board already asked.

**3 · The audit of your own measurement.** *Demonstrated, and it is the strongest case in this
document because the product's first real finding was our own defect.* Pointed at 78,618 real agent
messages — 52,878 of them written inside one of **74 repositories** — the first pass read **41.7%**
of commit claims as wrong. The
corrected figure is **8.1%**, and the entire gap was our error, not the agents': **73 of 103
"wrong" commits were real commits in a sibling repository on the same disk.** The probe was aimed at
the wrong object, which is the exact failure this product is named after. A vendor who shows you a
number without a preregistration is showing you a negotiation.

**4 · Agent procurement.** Two coding agents on trial for a quarter. Today the comparison is vibes
and token spend. With the record, the comparison is claim accuracy per episode, on the buyer's own
repositories, using a denominator written down before anyone looked.

**5 · The regulated release gate.** Financial services, medical devices, anything where a human
attestation is already required at release. The record supplies the evidence layer under the
attestation: which claims in this release were machine-checked, which were refused as
unverifiable, and who signed off on the refusals.

**6 · Post-incident reconstruction.** After an outage, the question is what the agent believed when
it made the change. Every hold links back to the originating session, so reconstruction starts from
the transcript rather than from a commit message written by the thing under investigation.

**7 · Onboarding a team to agents at all.** The blocker is rarely capability, it is that nobody
senior will sign off on unverifiable output. Shipping the gate first makes the pilot approvable,
because the failure mode has a visible red light before it has a production incident.

**8 · Vendor and contractor oversight.** An outsourced team ships agent-assisted work. The record
is contractual evidence of what was claimed and what held, and it is generated by the buyer's CI
rather than supplied by the seller.

**9 · Internal platform reporting.** Dana already reports CI health upward. The record adds one row
per agent-authored PR to a report she already sends, with no new dashboard and no new login.

**10 · The corpus product, day two.** Once the record has a quarter of history, the questions change
from "did this claim hold" to "which of our repositories, teams and agents produce claims that
hold". That is the compounding asset, and a competitor starting today has no history to compete
with.

---

## 5 · On the Google stack

| Layer | What runs there | State |
|---|---|---|
| **Cloud Run** | The witness service on the request path. `/health` returns 200, product name, `auth_required: true`, `store: firestore` | ✅ live |
| **Firestore** | The record. Row `H-a6151a95ac` written by a real GitHub Action, not a seed. Keyed store, not an append-only log — see the auditor note above | ✅ live |
| **GitHub Actions** | The `verify-claims` check. Runs the local probe, posts the verdict to Cloud Run | ✅ live, PR #1 |
| **Application token gate** (not IAM) | Cloud Run is **public at the IAM layer by design** so a judge can click the console — the only binding on `fleet-wedge` is `allUsers → roles/run.invoker`. The 401 is application-level: every mutating route is refused without a bearer token by `_require_token()` in `cloud/service.py`, probed 28 Aug. `demo_seed_enabled: false` in production. **Honest limit: one shared token, not per-agent identity, and not IAM.** | ✅ verified, app-level |
| **Gemini 3.5 via ADK** | `google.adk.runners.Runner` drives an `LlmAgent` (`gemini-3.5-flash-lite`) that *explains* a hold and never decides one. Record `H-a6151a95ac` carries `agent_explanation.invoked: true` | ✅ live |

**Known posture, stated rather than waited for.** `HOLD_API_TOKEN` is a **plaintext environment
variable** on the Cloud Run service; `secretmanager.googleapis.com` is enabled on the project and
unused, so anyone with `run.services.get` on `hack-fleet` can read the token. The service runs as
the **default compute service account** `568004190078-compute@developer.gserviceaccount.com`, which
holds `roles/editor` — a principal that can delete the Firestore collection this product keeps
the record in. Both are hackathon-project realities, not design positions.

**The architecture in one sentence:** the probe runs locally in the customer's CI where the
repository already is, and only the verdict crosses the network, so the product never needs read
access to customer code. That is what makes Dana's YAML file a five-minute install instead of a
security review.

**Cold start is 18.4 seconds, then 0.15 seconds.** Stated because a judge will click it.

---

## 6 · The evidence, with its own limits attached

- `./demo.sh` exits 0 from a cold clone, `env -i`, stock Python 3.9.6, no network, no credentials.
  `tests/test_demo.sh` 8 of 8.
- 78,618 messages examined of 144,306 in the corpus; 52,878 of those were written inside one of
  **74 repositories** (75 checkout roots, one repository checked out twice). Derivation and its
  four controls: `docs/CORPUS-REPO-COUNT-RECEIPT-2026-08-31.md`.
- 41.7% raw → **8.1% corrected**, with all eleven exclusions listed by reason rather than silently
  dropped.
- **What this does not tell you:** 8.1% is not an incidence rate and neither was 41.7%. Hand-labelling
  a seeded random sample of 40 extractions put extractor precision on conversational prose at 13/40.
  Of those 13 real claims, 6 disagreed with the repo. **n = 13. A direction, not a measurement.**
  The sample and its labels ship in `fixtures/corpus-sample-40.json` so you can re-label them and
  disagree.
- **Installs by a person who is not the author: zero.** Northwind is our test company and we
  scripted its PRs. What that run proves is the chain, not adoption.

The preregistration that made the correction possible is
`docs/CORPUS-PREREGISTRATION-2026-08-27.md`. **The method is the product.**

---

## 7 · The film, 3 minutes

Align with **`SUBMISSION-PACK.md` §2** (record-first close). Corpus beat is mid, not finale.

| Time | Beat | Shown |
|---|---|---|
| 0:00 | Board question + promise | seats/spend visible; claims are not |
| 0:30 | **The record** | `/hold/` — held claim → session join; moat line at click |
| 1:10 | `./demo.sh` | stranger, no account, no network |
| 1:35 | PR #1 | `verify-claims` red on `deadbee` — **not** "required check" (branch unprotected) |
| 2:15 | Four verdicts + refusal | terminal; never runs a command from a report |
| 2:40 | GCP + honesty | `/health` · eligibility 3/3 **and** cold 1/3 · row `H-a6151a95ac` · `clear: 0` |
| 3:15 | Close | install path; *Gemini explains; Python decides* if P1 deployed |

Recording: flipbook screen capture, voiceover from `film/voiceover-vo.txt`, burned subtitles.
Cold review before the camera rolls, and the live surface must equal the fixed-by-hash build.

---

## 8 · Devpost fields, ready to paste

**Name:** The Agent Work Record Witness
**Tagline:** Run your agents. Check the math.
**Promise (body, not tagline field):** Your agents write reports about work they did. This keeps the receipt.
**Built with:** Python · Google Cloud Run · Firestore · GitHub Actions
**Try it:** `git clone` then `./demo.sh` — no account, no network, no credentials
**Live:** https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/

---

## 9 · Open before submit

- [ ] Film shot and cut
- [ ] Devpost form filled from §8
- [ ] Whether the bounded n=2 org-lift pages ship — **Oscar's ruling**
- [ ] GCP billing account ID in this repo's public git history — ruled a non-incident (identifier,
      not credential); recommended action is a history rewrite **after** Monday, not before
