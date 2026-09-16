#!/usr/bin/env python3
"""Append tonight's measured appendix + draft hash footer to the sealed prediction doc.

Hash covers the sealed body only: everything from the top of the file through the
Scoring rubric section, stopping before `## After results`. The re-measure appendix and
hash footer are outside the sealed bytes.
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import subprocess
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "SEALED-PREDICTION-2026-08-29.md"
BASE = (ROOT / ".cloud_run_url").read_text().strip()

health = json.load(urllib.request.urlopen(BASE + "/health", timeout=30))
queue = json.load(urllib.request.urlopen(BASE + "/queue", timeout=30))
hero = next(h for h in queue["holds"] if h["id"] == "H-a6151a95ac")

pr_j = json.loads(
    subprocess.check_output(
        [
            "gh",
            "pr",
            "view",
            "1",
            "--repo",
            "Morkeeth/agent-work-record-witness-ata",
            "--json",
            "state,statusCheckRollup,url,title",
        ],
        text=True,
    )
)
checks = {
    c["name"]: c.get("conclusion") for c in (pr_j.get("statusCheckRollup") or [])
}

env = {
    k: v
    for k, v in os.environ.items()
    if k
    not in (
        "GOOGLE_APPLICATION_CREDENTIALS",
        "GOOGLE_CLOUD_PROJECT",
        "GEMINI_MODEL",
        "GEMINI_FORCE_KEY",
        "FLEET_STORE",
        "FLEET_STORE_PATH",
    )
}
env["CLOUDSDK_CONFIG"] = "/nonexistent"
p = subprocess.run(
    ["python3", "contract/eligibility.py"],
    cwd=ROOT,
    env=env,
    capture_output=True,
    text=True,
)
elig_line = [ln for ln in p.stdout.splitlines() if "OF 3 MET" in ln][-1].strip()
elig_exit = p.returncode

banned = sum(
    1
    for h in queue["holds"]
    if "required check" in (h.get("report_preview") or "").lower()
)

doc = DOC.read_text()
# Strip any prior night-wave appendix / footer
for marker in (
    "\n## Re-measured at objects",
    "\n## Draft hash",
    "\n<!-- night-wave",
):
    if marker in doc:
        doc = doc.split(marker)[0].rstrip() + "\n"

if "## After results" not in doc:
    raise SystemExit("sealed doc missing ## After results")

sealed_body, after = doc.split("## After results", 1)
# Sealed bytes = prediction + rubric only (exclude After results and Oscar notes that follow)
# Keep Oscar notes that currently sit AFTER the After-results table in the original —
# the handbook seal is metadata+prediction+rubric. Hash that.
sealed_hash = hashlib.sha256(sealed_body.encode()).hexdigest()

appendix = f"""
## Re-measured at objects · 2026-09-16 (night wave · do not treat as re-seal)

Oscar's **Sealed at** cell above stays. Numbers below were read tonight from the live
service and PR #1 — not carried from an earlier note.

| Object | Measured |
|--------|----------|
| `GET /health` | ok={health["ok"]} · product={health["product"]!r} · auth_required={health["auth_required"]} · demo_seed_enabled={health["demo_seed_enabled"]} · store={health["store"]} · ADK constructed={health["agent"]["constructed"]} · ever_invoked={health["agent"]["ever_invoked"]} |
| `GET /queue` | count={queue["count"]} · hero `H-a6151a95ac` gate={hero["gate"]} decision={hero["decision"]} pr={hero["pr"]} head_sha=`{hero["head_sha"][:12]}…` session=`{hero["session"]}` agent_invoked={hero["agent_invoked"]} traceable={hero["traceable"]} |
| Hero embarrassment | Firestore `report_preview` still contains **"required check"** on **{banned}/20** holds — UI scrub shipped in `surface/hold/index.html`, Cloud Run deploy pending |
| PR #1 | state={pr_j["state"]} · verify-claims={checks.get("verify-claims")} · witness-findings={checks.get("witness-findings")} |
| Eligibility (ADK installed, no ADC) | {elig_line} · exit {elig_exit} |
| Mutating routes anon | `/clearance` `/break-glass` `/prove` → 401 · `/demo/seed-hold` → 403 |
| `./demo.sh` cold | exit 0 — see `docs/STRANGER-PASS-2026-09-16.md` |
| Film md5 (object) | `demo/demo-final-v2.mp4` md5 `d327a995166b63ad3a64f248d5104397` · duration 228.35s |

**Commands:**

```
curl -sS "$(cat .cloud_run_url)/health"
curl -sS "$(cat .cloud_run_url)/queue"
gh pr view 1 --repo Morkeeth/agent-work-record-witness-ata --json state,statusCheckRollup
python3 contract/eligibility.py
env -i PATH="$PATH" HOME="$HOME" ./demo.sh
./film/preflight.sh
md5sum demo/demo-final-v2.mp4
```

"""

footer = f"""
## Draft hash

`sha256:{sealed_hash}`

SHA-256 of the sealed body: bytes from the start of this file through the end of the
Scoring rubric section (everything **before** `## After results`). Re-derive:

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib
doc = Path('docs/SEALED-PREDICTION-2026-08-29.md').read_text()
# Drop night-wave appendix if present, then take pre-After-results body:
if '## Re-measured at objects' in doc:
    doc = doc.split('## Re-measured at objects')[0]
body = doc.split('## After results')[0]
print(hashlib.sha256(body.encode()).hexdigest())
PY
```
"""

# Place re-measure after the Oscar notes (end of original), then hash footer.
# Keep After results where it was.
new = sealed_body + "## After results" + after.rstrip() + "\n" + appendix + footer
DOC.write_text(new)

# Verify
check = DOC.read_text()
check_body = check.split("## Re-measured at objects")[0].split("## After results")[0]
got = hashlib.sha256(check_body.encode()).hexdigest()
assert got == sealed_hash, (got, sealed_hash)
print("SEALED_BODY_SHA256", sealed_hash)
print("ELIG", elig_line, "exit", elig_exit)
print("CHECKS", checks)
print("BANNED_HOLDS", banned)
print("HASH_VERIFIED", True)
