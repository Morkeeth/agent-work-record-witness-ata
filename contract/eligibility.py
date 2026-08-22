#!/usr/bin/env python3
"""Is this submission eligible? Run it, do not argue it.

The three mandatory requirements, quoted from the Devpost rules:
  1. "Gemini 3.5 or newer accessed through Gemini API or Vertex AI"
  2. "at least one Google Agent Framework: Google ADK, GenAI SDK, Antigravity SDK or GenKit"
  3. "at least one Google Cloud infrastructure service (such as Cloud Run, Cloud SQL,
      Firestore, GKE, Pub/Sub)"

THE HOUSE TEST, and it is the whole point of this file:
  STRIP THE ENVIRONMENT. RUN THE ENTRY POINT. REPORT WHAT ACTUALLY EXECUTED.

"It works on my machine with my exports" is a seam, not a call. A judge clones the repo
and runs it with THEIR environment, so anything that only fires behind a flag or an env
var fires for nobody. This is the product's own law -- a claim is prose until something
probes it -- pointed at the submission itself.

REQUIREMENT 1 AND 3 ARE SEPARATE SLOTS AND VERTEX FILLS ONLY THE FIRST.
Requirement 1 explicitly names Vertex AI as a way to satisfy requirement 1. Every example
under requirement 3 is infrastructure -- compute, database, messaging. One aiplatform call
cannot fill both. Settled 2026-08-22; do not let a later reading quietly re-merge them.
"""
import os, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Run in a stripped environment: no exports of ours, only what a stranger would have.
STRIP = ["GEMINI_MODEL", "GEMINI_FORCE_KEY", "GEMINI_PACE_SECONDS", "FLEET_STORE",
         "FLEET_STORE_PATH", "GOOGLE_CLOUD_PROJECT", "GOOGLE_APPLICATION_CREDENTIALS", "N"]

PROBE = r'''
import sys, os
sys.path.insert(0, %(repo)r)
os.chdir(%(repo)r)
fired = {"gemini": None, "framework": None, "cloud": None}

# --- requirement 1: a real Gemini call, and by which path
try:
    from fleet.task_class import classify
    from contract.gemini_impl import LAST_MODEL
    v = classify("fix auth", "clean up the token validation in auth")
    fired["gemini"] = (LAST_MODEL[-1] if LAST_MODEL else None, v)
except Exception as e:
    fired["gemini"] = ("EXCEPTION", f"{type(e).__name__}: {e}")

# --- entry path: load ADK + Firestore modules (seams that never import do not count)
try:
    from fleet.bootstrap import ensure_google_stack
    fired["bootstrap"] = ensure_google_stack()
except Exception as e:
    fired["bootstrap"] = {"error": f"{type(e).__name__}: {e}"}

# --- requirement 2 and 3: did the modules actually LOAD on this path
fired["framework"] = sorted(m for m in sys.modules
                            if m.startswith(("google.adk", "google.genai", "genkit")))
fired["cloud"] = sorted(m for m in sys.modules
                        if m.startswith(("google.cloud.firestore", "google.cloud.pubsub",
                                         "google.cloud.sql", "google.cloud.run")))
import json; print("PROBE_RESULT " + json.dumps(fired))
''' % {"repo": REPO}


def main():
    env = {k: v for k, v in os.environ.items() if k not in STRIP}
    env["PATH"] = os.path.expanduser("~/google-cloud-sdk/bin") + ":" + env.get("PATH", "")
    out = subprocess.run([sys.executable, "-c", PROBE], capture_output=True, text=True,
                         env=env, timeout=180)
    line = next((l for l in out.stdout.splitlines() if l.startswith("PROBE_RESULT ")), None)
    if not line:
        print("NO PROBE RESULT — the stripped run did not complete.")
        print(out.stderr[-900:])
        return 2
    import json
    f = json.loads(line[len("PROBE_RESULT "):])

    print("=" * 74)
    print("  ELIGIBILITY, MEASURED — environment stripped, entry point run")
    print("=" * 74)
    print(f"  stripped: {', '.join(STRIP)}")
    print()

    path, verdict = f["gemini"]
    r1 = bool(path) and path != "EXCEPTION"
    print(f"  {'MET    ' if r1 else 'NOT MET'}  1. Gemini 3.5+ via Gemini API or Vertex AI")
    print(f"             answering path : {path}    verdict returned: {verdict}")

    r2 = bool(f["framework"])
    print(f"  {'MET    ' if r2 else 'NOT MET'}  2. A Google Agent Framework")
    print(f"             modules loaded : {f['framework'] or 'NONE — nothing imported ADK on this path'}")

    r3 = bool(f["cloud"])
    print(f"  {'MET    ' if r3 else 'NOT MET'}  3. A Google Cloud infrastructure service")
    print(f"             modules loaded : {f['cloud'] or 'NONE — nothing imported Firestore/PubSub/Run'}")

    n = sum([r1, r2, r3])
    print("-" * 74)
    print(f"  {n} OF 3 MET ON THE PATH A JUDGE RUNS.")
    if n < 3:
        print("  The seam existing is not the service being called. A judge checks the second.")
    print("=" * 74)
    return 0 if n == 3 else 1


if __name__ == "__main__":
    sys.exit(main())
