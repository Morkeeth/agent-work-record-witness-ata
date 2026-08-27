#!/usr/bin/env python3
"""Post gate findings to the Witness gateway and set the CI exit code.

Lifted out of a heredoc inside .github/workflows/outcome-gate.yml so it can be
READ, TESTED AND INSTALLED. A check that only exists inside a YAML string cannot
be unit-tested, cannot be run by a customer debugging their install, and cannot be
shipped by `uses:`.

The session join is deliberately NOT re-implemented here. cloud/hold_api.py already
recovers it from the report with `extract_session_ref`, and putting a second copy of
that parser on the client would let the two sides drift — the failure this product
exists to catch. One parser, server side, reading the report this script already
sends. What this script does is REPORT whether the join resolved, so an untraceable
hold is visible in the CI log instead of silently being nobody's session.
"""
import json
import os
import sys
import urllib.error
import urllib.request

CLEARANCE_SUFFIX = "/clearance"


def load_findings(path: str) -> dict:
    """Read the gate's output, or fail loudly.

    Never treat an unreadable findings file as "nothing to report". The gate failing
    is exactly the condition a customer must be told about — it used to surface as a
    JSONDecodeError from an empty file, which reads as a broken product rather than
    a missing probe.
    """
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        sys.exit(f"HOLD: the gate wrote no findings file at {path} — it did not run. "
                 f"This is a broken install, not a clean PR.")
    except json.JSONDecodeError as e:
        size = os.path.getsize(path) if os.path.exists(path) else 0
        sys.exit(f"HOLD: findings file at {path} is not JSON ({size} bytes): {e}. "
                 f"The gate failed before it could report. This is a broken install, "
                 f"not a clean PR.")


def post(url: str, payload: dict, token: str) -> dict:
    if not url.rstrip("/").endswith(CLEARANCE_SUFFIX):
        url = url.rstrip("/") + CLEARANCE_SUFFIX
    headers = {"Content-Type": "application/json"}
    if token:
        headers["X-HOLD-Token"] = token
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def main() -> int:
    findings_path = os.environ.get("HOLD_FINDINGS", "/tmp/hold-findings.json")
    findings = load_findings(findings_path)
    exit_hint = int(findings.get("exit_hint") or 0)
    print(f"local_gate {findings.get('gate')} exit_hint {exit_hint}")
    print(json.dumps(findings, indent=2))

    url = (os.environ.get("HOLD_POLICY_URL") or "").strip()
    if not url:
        print("HOLD_POLICY_URL unset — enforcing local probe only")
        return exit_hint

    payload = {
        "report": os.environ.get("PR_BODY") or "",
        "findings": findings.get("findings"),
        "pr": os.environ.get("PR_NUMBER"),
        "repo": os.environ.get("REPO"),
        "actor": "github-action",
        "source": "github-action",
    }
    try:
        body = post(url, payload, (os.environ.get("HOLD_API_TOKEN") or "").strip())
    except urllib.error.HTTPError as e:
        print("HOLD gateway HTTP", e.code, e.read()[:500])
        return exit_hint or 1
    except OSError as e:
        print(f"HOLD gateway unreachable: {type(e).__name__}: {e}")
        return exit_hint or 1

    print(json.dumps(body, indent=2))

    clearance = body.get("clearance") or {}
    if clearance.get("traceable"):
        # "decision", not "hold": this line prints on a CLEAR too.
        print(f"TRACEABLE — this {clearance.get('decision', 'decision')} opens back to "
              f"session {clearance.get('session')}")
    else:
        print("UNTRACEABLE — no session reference in the PR body, so this decision "
              "cannot be opened back to the run that produced it. Put the session URL "
              "or a 'Claude-Session:' line in the PR body to make it traceable. "
              "No id is ever invented for you.")

    if not body.get("recorded", True):
        print(f"WARNING: the gateway did not record this decision: "
              f"{body.get('store_error')}")

    if body.get("ci_should_fail"):
        return 1
    if body.get("ci_should_warn") and clearance.get("policy_mode") == "enforce":
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
