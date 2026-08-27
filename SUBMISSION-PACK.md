# HOLD — All Things Agentic submission pack (paste-ready)

_Product home: this repo only. Brand on camera: **HOLD**. `agent-claims-inbox` = disclosure, not a second entry._  
_Film checklist: [`docs/ATA-FILM-AND-SHIP.md`](docs/ATA-FILM-AND-SHIP.md) · Product: [`hack.md`](hack.md) **(canonical)**_

- **Deadline:** Aug 31 2026 · **17:00 PDT** (≤4:00 unedited video)
- **Devpost:** https://allthingsagentichackathon.devpost.com/
- **Track:** **Fortified Enterprise Fleet**
- **Repo (private):** https://github.com/Morkeeth/hack-fleet-ata — share with `testing@devpost.com` **and** `cloudhackathons@google.com`
- **Console:** https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/
- **Judging:** Innovation & Operational Utility 40% · Architecture 30% · Demo readiness 30%

---

## Live probe receipt (re-check before film)

| Probe | Expect |
|---|---|
| `GET /health` | `product: HOLD` · `auth_required: true` · `demo_seed_enabled: false` · store firestore · ADK agent |
| `GET /hold/` | HTTP 200 console |
| `GET /audit/export` | JSON download |
| Anon `POST /clearance` | **401** |
| `POST /demo/seed-hold` | **403** (film uses a real agent PR) |
| `python3 contract/eligibility.py` | **3 OF 3 MET** |

Cold start: first `/health` may hang once — retry.

---

# 1 · Devpost paste

### Project name
```
HOLD
```

### Tagline
```
GEAP governs the agents. HOLD governs the release.
```

### Track
```
Fortified Enterprise Fleet
```

### Hosted project URL
```
https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/
```
Also: `GET /health` · `POST /clearance` (token) · `POST /prove` · `GET /audit/export`

### Repository URL
```
https://github.com/Morkeeth/hack-fleet-ata
```

### What it does
```
Enterprises run coding-agent fleets and can see seats and spend — not whether "done"
is true before merge. At fleet scale (overnight agents, auto-merge), prose is an
ungoverned production surface.

HOLD is outcome clearance — the Gateway before agent work is production-real.
An agent-authored PR hits a required check; claims are probed against the object
(git cat-file, path exists). CONTRADICTED claims fail closed. Humans only see the
Hold Queue when something is red. Break-glass is ledgered. Auditors export the log.
A Registry module can promote literal surviving practice into the org skill file
(UNMEASURED on a field of 2 — no fake org lift).

Not observability. Not code review. Not a claims inbox.
Install shape: GitHub Action → Cloud Run policy. Mandate shape: required for agent paths.
```

### How we built it (Google stack)
```
- Gemini 3.5 via Vertex AI — exercised on the service path (eligibility probe CALLS it)
- Google ADK — LlmAgent constructed on the Gateway (visible in /health)
- Google Cloud — Cloud Run service + Firestore ledger
- HOLD console at /hold/ · APIs /clearance /queue /break-glass /audit /policy /prove
- GitHub Action .github/workflows/outcome-gate.yml (agent-scoped) posts to /clearance
- Deterministic probes decide CLEAR/HOLD; the model does not get a veto on truth

python3 contract/eligibility.py → 3 OF 3 MET (called, not imported).
```

### Challenges
```
Our own overnight fleet reported "done" on eligibility while the object disagreed
(import mistaken for a call). The gate that blocks false done is the product; catching
ourselves is the honesty beat, not an apology. Trust boundary: mutating APIs require
HOLD_API_TOKEN; demo seed is off so the film must use a real agent-labeled PR.
Practice propagate on n=2 stays UNMEASURED_FOR_ORG_CLAIM.
```

### What's next
```
GitHub App + Check Runs (packaged install). Transcripto as silent provenance on claims.
Deploy/CI witnesses beyond SHA/path. Helicon memory-truth as an optional probe pack —
same Gateway, not a second product.
```

### Architecture
Source: `docs/ARCHITECTURE.md` (export PNG for the form). Narrate: Action → Cloud Run Gateway → Firestore · ADK/Gemini · object probes · console exception desk.

---

# 2 · Video beat sheet (≤4:00, unedited)

**Line:** *GEAP governs the agents. HOLD governs the release.*

| Time | Beat | On camera |
|------|------|-----------|
| 0:00–0:25 | Problem | Seats ≠ truth; overnight false done |
| 0:25–0:50 | Product | HOLD = outcome clearance Gateway |
| 0:50–1:15 | Eligibility | `eligibility.py` → 3/3 |
| 1:15–1:40 | GCP | Cloud Run + `/health` (say URL) |
| 1:40–2:30 | **Real PR** | agent label + false-done body → red `verify-claims` + Hold Strip + probe |
| 2:30–3:00 | Break-glass + audit | reason → ledger; Export JSON |
| 3:00–3:30 | Registry | `/prove` + UNMEASURED |
| 3:30–4:00 | Close | Install path + roadmap (App); spine line |

**Do not:** Seed button · `/healthz` · org lift · Witness/Claims Inbox names · CLI as the product.

Pre-roll: `docs/ATA-FILM-AND-SHIP.md` §2.

---

# 3 · Disclosure

- [transcripto](https://github.com/Morkeeth/transcripto) — authorship-gated corpus spine (roadmap provenance)
- Local `agent-claims-inbox` — claim/repo witness patterns
- Product composition (Gateway, console, Action, Registry) submitted in this repo
