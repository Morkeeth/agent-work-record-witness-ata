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
DEFAULT_MODEL = "gemini-3.5-flash"      # verified live 2026-08-22, not guessed
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



def _key():
    with open(KEY_PATH) as f:
        return f.read().strip()


_PACE = float(os.environ.get("GEMINI_PACE_SECONDS", "4"))


def classify_gemini(prompt_a: str, prompt_b: str) -> str:
    time.sleep(_PACE)          # stay under the free tier's 20/min rather than react to it
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
    req = urllib.request.Request(
        ENDPOINT.format(m=model),
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": _key()},
    )
    for attempt in range(5):                       # free tier is rate limited
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                out = json.load(r)
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 4:
                # Free tier: generate_content_free_tier_requests, limit 20, and the
                # server's own retryDelay came back at 37s. Measured, not guessed.
                time.sleep(40)
                continue
            return f"API-ERROR-{e.code}"
        except Exception as e:
            return f"API-ERROR-{type(e).__name__}"
    else:
        return "API-ERROR-RATE-LIMIT"
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
    g, t = run(classify_gemini, f"classify_gemini ({os.environ.get('GEMINI_MODEL', DEFAULT_MODEL)})")
    s, _ = run(classify_substring, "classify_substring (what shipped)")
    n, _ = run(classify_always_different, "classify_always_different (NEGATIVE CONTROL)")
    print("\n" + "=" * 78)
    print(f"  gemini {g}/{t}   ·   substring {s}/{t}   ·   stub-that-ignores-input {n}/{t}")
    print("=" * 78)
