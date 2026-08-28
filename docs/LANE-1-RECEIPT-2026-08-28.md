# Lane 1 receipt — demo stack, 2026-08-28

Every line below was probed, not carried forward. Commands are in the git history.

## Ship condition — MET

Fresh `git clone` from public GitHub, empty environment (`env -i`), `HOME=/nonexistent-stranger`,
`PATH=/usr/bin:/bin`, no `PYTHON` override, no `~/.trace`:

```
./demo.sh          -> exit 0    PASS(0) / BLOCK(1) / HOLD(2) all three shown
./tests/test_demo.sh -> exit 0  8 of 8 assertions
git status --short -> empty     the clone matches origin/main @ 3093a3e
```

A judge clones, runs one command, and watches a false claim get caught — with no account, no key,
no network call, and no file read outside the clone.

## What was broken and is not

| Was | Probe | Now |
|---|---|---|
| Service dead on stock macOS Python 3.9 | `python3 -m cloud.service` → `TypeError: unsupported operand type(s) for \|` at `cloud/service.py:89`, at **import** — every endpoint, not just `/health` | `from __future__ import annotations` in 7 modules; `requires-python >=3.9`; full suite green on 3.9.6 |
| README's first command read the author's corpus | `witness-corpus --db ~/.trace/trace.db` | `./demo.sh` is the opening move; corpus run retitled as our run on a corpus you do not have |
| No cold-clone demo existed | — | `demo.sh` + `tests/test_demo.sh` |
| `8.4%` in SUBMISSION-PACK + ENTERPRISE-CASE | canonical is 19/236 | `8.1%`, no `8.4%` left in any `.md` |
| "anon `POST /prove` → 201, open defect" | `curl -X POST <live>/prove` → **401** `HOLD_API_TOKEN required` | row closed |
| "`/audit` 31 vs `/audit/export` 6, open defect" | live: `/audit` **31**, `/audit/export` **7**, `?include_prove=1` **31** | not a defect — the prove-only filter working as designed; both rows rewritten |
| `docs/internal` said the repo is private, invite the judges | `gh repo view` → `visibility: PUBLIC` | corrected; no invite step |
| Workflow + docs pointed `uses:` at the pre-rename repo | `git diff` | `Morkeeth/agent-work-record-witness-ata` everywhere |
| 8 modified + 2 untracked files against public GitHub | `git status` | committed and pushed; clone == screen |

## Read this

**A GCP account, project number and billing account ID were sitting in
`docs/internal/CURSOR-LOG.md` in a PUBLIC repo.** Redacted in `3093a3e`. Treat them as already
exposed — the history still carries them and the repo has been public.

**The corpus story survives as method, not as data.** `41.7% → 8.1%` stays in README,
ENTERPRISE-CASE and the film shot list. Nothing a judge runs touches `~/.trace/trace.db`;
`witness-corpus` with no database prints plain words and exits 2.

**`fixtures/corpus-sample-40.json` is real transcript context**, including `cwd` paths under
`/Users/morkeeth/CODE`. It is intentionally shipped so the labels can be disputed, and it is
already public. Flagging it, not changing it.

**Not redeployed.** Cloud Run runs 3.12, where the annotation change is a no-op, and the live auth
gate is already correct (401 verified today). The deployed revision does not carry `3093a3e`.

**`HANDOVER-T4-TO-T3.md` was left untracked** — internal fleet handover, not judge-facing.

## Still Oscar's

The video, and the Devpost submit.
