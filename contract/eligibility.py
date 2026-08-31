#!/usr/bin/env python3
"""Is this submission eligible? Run it, do not argue it — and EXERCISE, do not import.

The three mandatory requirements, quoted from the Devpost rules:
  1. "Gemini 3.5 or newer accessed through Gemini API or Vertex AI"
  2. "at least one Google Agent Framework: Google ADK, GenAI SDK, Antigravity SDK or GenKit"
  3. "at least one Google Cloud infrastructure service (Cloud Run, Cloud SQL, Firestore, ...)"

HISTORY, so it is not repeated: v1 of this file checked `sys.modules` — whether a module
IMPORTED — as a proxy for "the service is called." It reported 3 OF 3 while the store on the
default path was JsonlStore and build_agent() was never called. That is the exact seam-vs-call
error this product exists to catch, built into its own eligibility check. IMPORT IS NOT CALL.

This version EXERCISES each requirement on the stripped default path:
  - req 1: classify() returns a real verdict over a Google endpoint.
  - req 2: build_agent() CONSTRUCTS a real google.adk Agent.
  - req 3: get_store() on the default path IS FirestoreStore, and a write/read round-trips.

REQUIREMENT 1 AND 3 ARE SEPARATE SLOTS AND VERTEX FILLS ONLY THE FIRST — requirement 1 names
Vertex AI; every example under requirement 3 is infrastructure. Settled 2026-08-22.
"""
import os, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STRIP = ["GEMINI_MODEL", "GEMINI_FORCE_KEY", "GEMINI_PACE_SECONDS", "FLEET_STORE",
         "FLEET_STORE_PATH", "GOOGLE_CLOUD_PROJECT", "GOOGLE_APPLICATION_CREDENTIALS", "N"]

PROBE = (
    "import sys, os, json\n"
    "sys.path.insert(0, %r)\n"
    "os.chdir(%r)\n"
    "r = {}\n"
    "try:\n"
    "    from fleet.task_class import classify, _LAST_ERROR\n"
    "    from contract.gemini_impl import LAST_MODEL\n"
    "    v = classify('fix auth', 'clean up the token validation in auth')\n"
    "    r['gemini'] = {'met': v in ('SAME','DIFFERENT','UNDECIDABLE') and bool(LAST_MODEL),\n"
    "                   'path': (LAST_MODEL[-1] if LAST_MODEL else None), 'verdict': v,\n"
    "                   'why': (_LAST_ERROR[-1] if _LAST_ERROR else None)}\n"
    "except Exception as e:\n"
    "    r['gemini'] = {'met': False, 'error': type(e).__name__+': '+str(e)}\n"
    "try:\n"
    "    from cloud.store import get_store\n"
    "    st = get_store(); backend = type(st).__name__; used = backend == 'FirestoreStore'\n"
    "    proof = 'default path -> ' + backend\n"
    "    if used:\n"
    "        rec = {'id':'elig-exercise','operator':'probe','verdict':'SAME'}\n"
    "        (getattr(st,'save',None) or getattr(st,'put',None) or st.add)(rec)\n"
    "        back = list(st.all()) if hasattr(st,'all') else list(st.list())\n"
    "        proof = 'round-trip hit '+backend+', '+str(len(back))+' records'\n"
    "    r['cloud'] = {'met': used, 'backend': backend, 'proof': proof}\n"
    "except Exception as e:\n"
    "    r['cloud'] = {'met': False, 'error': type(e).__name__+': '+str(e)}\n"
    "try:\n"
    "    from cloud.agent import build_agent\n"
    "    a = build_agent(); cls = type(a).__module__+'.'+type(a).__name__\n"
    "    r['framework'] = {'met': cls.startswith('google.adk'), 'agent_class': cls}\n"
    "except Exception as e:\n"
    "    r['framework'] = {'met': False, 'error': type(e).__name__+': '+str(e)}\n"
    "print('PROBE_RESULT ' + json.dumps(r))\n"
) % (REPO, REPO)


def gemini_reason(g):
    """Why requirement 1 was not met, in words, from what was MEASURED.

    `classify()` does not raise when no model can be reached: every unreachable-model
    condition (no ADC, no key file, a 429, a safety filter, a socket error) collapses to
    the first-class answer UNMEASURED by design (fleet/task_class.py:73). So the probe
    caught no exception, `error` was never set, and this line printed `g.get('error','')`
    -> the empty string. A judge running the check cold saw `NOT MET  1.` followed by a
    blank line: a verdict with no explanation, which is the exact shape of claim this
    product exists to refuse. The reason is not invented here -- `classify()` already
    records the failure type in `_LAST_ERROR` and the probe now carries it out.
    """
    if g.get("error"):
        return g["error"]
    if g.get("verdict") == "UNMEASURED":
        why = g.get("why")
        return ("no model answered — classify() returned UNMEASURED"
                + (f" after {why}" if why else "")
                + "; no Gemini rung was reachable, so nothing was measured")
    return f"path {g.get('path')} -> {g.get('verdict')}"


def main():
    env = {k: v for k, v in os.environ.items() if k not in STRIP}
    env["PATH"] = os.path.expanduser("~/google-cloud-sdk/bin") + ":" + env.get("PATH", "")
    out = subprocess.run([sys.executable, "-c", PROBE], capture_output=True, text=True,
                         env=env, timeout=180)
    line = next((l for l in out.stdout.splitlines() if l.startswith("PROBE_RESULT ")), None)
    if not line:
        print("NO PROBE RESULT — the stripped run did not complete.")
        print(out.stderr[-900:]); return 2
    import json
    f = json.loads(line[len("PROBE_RESULT "):])
    print("=" * 74)
    print("  ELIGIBILITY, EXERCISED — stripped env, services CALLED not imported")
    print("=" * 74)
    print(f"  stripped: {', '.join(STRIP)}\n")

    g = f["gemini"]; r1 = g.get("met", False)
    print(f"  {'MET    ' if r1 else 'NOT MET'}  1. Gemini 3.5+ via Gemini API or Vertex AI")
    print(f"             {'path '+str(g.get('path'))+' -> '+str(g.get('verdict')) if r1 else gemini_reason(g)}")
    fr = f["framework"]; r2 = fr.get("met", False)
    print(f"  {'MET    ' if r2 else 'NOT MET'}  2. Google Agent Framework (ADK agent CONSTRUCTED)")
    print(f"             {fr.get('agent_class') if r2 else fr.get('error','')}")
    c = f["cloud"]; r3 = c.get("met", False)
    print(f"  {'MET    ' if r3 else 'NOT MET'}  3. Google Cloud service (default-path store IS Firestore)")
    print(f"             {c.get('proof', c.get('error',''))}")
    n = sum([r1, r2, r3])
    print("-" * 74)
    print(f"  {n} OF 3 MET — exercised on the path a judge runs.")
    if n < 3:
        print("  Import is not call. A judge runs the entry point and gets what this exercised.")
    print("=" * 74)
    return 0 if n == 3 else 1


if __name__ == "__main__":
    sys.exit(main())
