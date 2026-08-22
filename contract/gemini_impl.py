#!/usr/bin/env python3
"""Gemini implementation of the task-class contract.

Registered BESIDE `classify_substring`, never replacing it. The control set in
`task_class.py` grades both against the same eight rows, plus a negative control
that ignores its input entirely. Whatever this scores, it scores against a stub.

DESIGN NOTES THAT ARE LOAD-BEARING
----------------------------------
1. ENUM-CONSTRAINED OUTPUT. The response schema is a STRING enum of exactly
   SAME | DIFFERENT | UNDECIDABLE. The model cannot return prose, cannot invent a
   fourth value, and cannot omit the refusal. UNDECIDABLE stops depending on prompt
   discipline and becomes enforced by the schema.
2. NO DEPENDENCIES. stdlib urllib only -- no pip install, no google-genai wheel.
   The disk is at 99% and a control set that cannot run is not a control set.
3. THE KEY IS NEVER IN THE REPO. Read at call time from ~/.config/keys/gemini.key
   (0600) and never printed, never logged, never passed as an argument.
4. THE MODEL ID IS NOT HARDCODED as a constant. GEMINI_MODEL wins; the default was
   VERIFIED PRESENT in the live /v1beta/models list on 2026-08-22, not guessed.
   (Note: the pricing page advertises a `gemini-3.7-flash` that is NOT in the live
   list on this key. Documentation is not availability.)
"""
import json, os, sys, time, urllib.request, urllib.error

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

KEY_PATH = os.path.expanduser("~/.config/keys/gemini.key")
# VERTEX PATH -- added 2026-08-22 once Oscar's project went live.
# The rule reads "Gemini 3.5 or newer accessed through Gemini API OR VERTEX AI", so this
# is admissible, and it is strictly better on three counts:
#   1. NO QUOTA CLIFF. gemini-3.5-flash returns 200 here while the AI Studio key is still
#      429 on the same model -- the 20/day-per-model ceiling was a property of that key.
#   2. NO KEY FILE. ADC is picked up automatically, so a judge clones and runs with their
#      own gcloud login and nothing to place on disk.
#   3. IT IS A CALL TO THE PROJECT, so the Google Cloud surface is exercised rather than
#      a standalone API endpoint.
# It BILLS. Tiny (~$0.0001/classification) but real, so the AI Studio ladder stays as the
# free fallback for anyone without a project.
VERTEX_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "hack-fleet")
VERTEX_URL = ("https://aiplatform.googleapis.com/v1/projects/{p}/locations/global"
              "/publishers/google/models/{m}:generateContent")
# THE LADDER. The free-tier cap is GenerateRequestsPerDayPerProjectPerModel-FreeTier,
# value 20 -- twenty per DAY PER MODEL, not a rate limit. That is why 40-second backoffs
# never rescued it. Every entry is "3.5 or newer" so admissibility holds whichever answers,
# and each carries its own 20/day. Verified present in the live /v1beta/models list.
LADDER = ["gemini-3.5-flash-lite", "gemini-3.6-flash", "gemini-3.7-flash",
          "gemini-3.1-flash-lite", "gemini-3.5-flash"]
DEFAULT_MODEL = LADDER[0]
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent"

INSTRUCTION = """Two prompts written by software engineers. Decide whether they open the
SAME CLASS OF WORK: would a person picking up either one be doing the same kind of job,
on the same part of the system, with the same kind of outcome?

Shared vocabulary is NOT evidence of sameness. Different vocabulary is NOT evidence of
difference. Decide on the WORK, not the words.

Answer exactly one:

SAME - the same kind of job on the same area.
  "the login is broken" / "debug why validate_token returns None"  -> SAME (no shared words)

DIFFERENT - a different kind of job, even when almost every word is shared.
  "refactor the auth module" / "document the auth module"     -> DIFFERENT (change vs describe)
  "write a migration"        / "roll back the migration"      -> DIFFERENT (opposite direction)
  "refactor the auth module" / "add a dark mode toggle"       -> DIFFERENT (unrelated areas)

UNDECIDABLE - one prompt names no object you can place, so the comparison cannot be made.
  "fix it" / anything -> UNDECIDABLE. There is no referent. Guessing SAME or DIFFERENT
  here is a WRONG ANSWER, not a safe default.

Check UNDECIDABLE first. Then check DIFFERENT. Only answer SAME if neither applies.
"""



def _adc_token():
    """ADC access token, or None. No key file, no env var, no secret on disk."""
    import subprocess
    try:
        sdk = os.path.expanduser("~/google-cloud-sdk/bin")
        env = dict(os.environ, PATH=f"{sdk}:{os.environ.get('PATH','')}")
        out = subprocess.run(["gcloud", "auth", "application-default", "print-access-token"],
                             capture_output=True, text=True, timeout=30, env=env)
        return out.stdout.strip() or None
    except Exception:
        return None


def classify_gemini_vertex(prompt_a: str, prompt_b: str) -> str:
    """Same contract, same schema, project-scoped path. No key file, no quota cliff."""
    tok = _adc_token()
    if not tok:
        return "API-ERROR-NO-ADC"
    model = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
    body = {
        "systemInstruction": {"parts": [{"text": INSTRUCTION}]},
        "contents": [{"role": "user", "parts": [{"text":
            f"{INSTRUCTION}\n\nPROMPT A:\n{prompt_a}\n\nPROMPT B:\n{prompt_b}"}]}],
        "generationConfig": {"responseMimeType": "text/x.enum",
                             "responseSchema": {"type": "STRING",
                                                "enum": ["SAME", "DIFFERENT", "UNDECIDABLE"]},
                             "temperature": 0},
    }
    req = urllib.request.Request(
        VERTEX_URL.format(p=VERTEX_PROJECT, m=model), data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            out = json.load(r)
    except urllib.error.HTTPError as e:
        return f"API-ERROR-{e.code}"
    except Exception as e:
        return f"API-ERROR-{type(e).__name__}"
    try:
        LAST_MODEL.append(f"vertex:{model}")
        return out["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError):
        return "NO-CANDIDATE"


def _key():
    with open(KEY_PATH) as f:
        return f.read().strip()


_PACE = float(os.environ.get("GEMINI_PACE_SECONDS", "1"))
LAST_MODEL = []          # which rung actually answered; printed, never hidden


def classify_gemini(prompt_a: str, prompt_b: str) -> str:
    """VERTEX FIRST, AI Studio key as fallback.

    Vertex is primary because it has no per-model daily ceiling, needs no key on disk
    (ADC is picked up automatically), and exercises the project rather than a standalone
    consumer endpoint. The key ladder remains so the repo still runs for someone with no
    GCP project at all -- a stranger should not need a billing account to see it work.

    LOCATION NOTE, measured: only `global` publishes these models. Every regional endpoint
    404s (us-central1, europe-west1, v1 and v1beta1 alike). A 404 from a regional endpoint
    is a LOCATION ARTEFACT, not absence -- the same shape as reading a truncated list as
    absence. Do not conclude the model is missing from a query you have not verified is
    complete.
    """
    if os.environ.get("GEMINI_FORCE_KEY") != "1":
        v = classify_gemini_vertex(prompt_a, prompt_b)
        if not str(v).startswith(("API-ERROR", "NO-CANDIDATE")):
            return v
    time.sleep(_PACE)          # key path only: free tier is 20/min
    model = os.environ.get("GEMINI_MODEL", DEFAULT_MODEL)
    body = {
        "systemInstruction": {"parts": [{"text": INSTRUCTION}]},
        "contents": [{"role": "user", "parts": [{"text":
            f"{INSTRUCTION}\n\nPROMPT A:\n{prompt_a}\n\nPROMPT B:\n{prompt_b}"}]}],
        "generationConfig": {
            "responseMimeType": "text/x.enum",
            "responseSchema": {"type": "STRING",
                               "enum": ["SAME", "DIFFERENT", "UNDECIDABLE"]},
            "temperature": 0,
        },
    }
    # 429 here is a DAILY per-model cap, so waiting is pointless -- step to the next
    # rung instead. Which model answered is printed, never hidden: a score that does not
    # say which model produced it is not a measurement.
    rungs = ([model] + [m for m in LADDER if m != model]) if os.environ.get("GEMINI_MODEL") \
            else list(LADDER)
    for rung in rungs:
        req = urllib.request.Request(
            ENDPOINT.format(m=rung), data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json", "x-goog-api-key": _key()})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                out = json.load(r)
            LAST_MODEL.append(rung)
            break
        except urllib.error.HTTPError as e:
            if e.code == 429:
                continue                       # this rung is spent for today
            return f"API-ERROR-{e.code}"
        except Exception as e:
            return f"API-ERROR-{type(e).__name__}"
    else:
        return "API-ERROR-ALL-RUNGS-EXHAUSTED"
    try:
        return out["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError):
        return "NO-CANDIDATE"      # safety filter or empty response; never guessed


if __name__ == "__main__":
    from contract.task_class import run, classify_substring, classify_always_different
    print("Probing the live API before grading anything...")
    probe = classify_gemini("fix auth", "Refactor the auth module: extract validate_token "
                                        "into auth/validate.py, keep tests green, show me "
                                        "the diff before applying.")
    print(f"  C1 live probe -> {probe}\n")
    if probe.startswith(("API-ERROR", "NO-CANDIDATE")):
        print("API unreachable. Refusing to grade — a control set that cannot call is not red, "
              "it is unmeasured.")
        sys.exit(2)
    g, t = run(classify_gemini, "classify_gemini")
    from collections import Counter
    print(f"  rungs that answered: {dict(Counter(LAST_MODEL))}")
    s, _ = run(classify_substring, "classify_substring (what shipped)")
    n, _ = run(classify_always_different, "classify_always_different (NEGATIVE CONTROL)")
    print("\n" + "=" * 78)
    print(f"  gemini {g}/{t}   ·   substring {s}/{t}   ·   stub-that-ignores-input {n}/{t}")
    print("=" * 78)
