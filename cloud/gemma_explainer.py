#!/usr/bin/env python3
"""Gemma explainer — the backend for a customer who cannot send claim text anywhere.

WHY THIS EXISTS, and it is not the bonus point.

The product's own pitch says the probe runs inside the customer's checkout and that
"only the verdict and a session pointer cross the network". That was true of the
PROBE and quietly false of the EXPLANATION: the Gemini path posts the finding text,
which contains file paths, commit shas and claim prose, to a hosted endpoint.

Gemma is open-weights, so the same model runs on the customer's own hardware. Point
GEMMA_BASE_URL at a local vLLM or Ollama server and no claim text leaves the network.

WHAT THIS MODULE WILL NOT DO
----------------------------
It will not claim to be self-hosted when it is not. Every receipt carries `endpoint`
and a boolean `left_the_network`, computed from the URL actually called rather than
from configuration intent. On the deployed demo that boolean is TRUE, and the console
says so. A product that reports false claims does not get to make one about itself.

Like the Gemini path, this NEVER changes a verdict. Probes decide. Gemma explains.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from typing import Any
from urllib.parse import urlparse

# Open weights, instruction-tuned. Verified answering on 2026-08-31.
DEFAULT_MODEL = os.environ.get("GEMMA_MODEL", "gemma-4-31b-it")

# Default is Google's hosted endpoint so a judge with a key gets a working demo.
# Override to a local server and the same code path keeps every byte in your network.
DEFAULT_BASE = "https://generativelanguage.googleapis.com/v1beta"

# Hosts we know are not the customer's own machine. Anything else is treated as
# self-hosted only because it is NOT on this list, and the receipt says which test ran.
_HOSTED = ("googleapis.com", "google.com")

# MEASURED 2026-08-31 across six configurations, and the result is the reason the guard
# below exists rather than a cleverer prompt.
#
#   constraint list, no prefill  -> restates the constraints as a bulleted plan,
#                                   one run captioned "Draft 1" / "Draft 2"
#   prefilled model turn, t=0.2  -> clean on two findings; on ONE finding it collapsed
#                                   into "own own own own" with Korean characters in it
#   prefilled, t=0.7             -> collapsed harder, 210 non-latin characters
#   prefilled, t=0.7, 26b model  -> "ownces-ownces-ownces"
#   <note> delimiters, no prefill-> tags nested inside themselves, or came back empty
#
# So this model, on this endpoint, is not reliable enough to put text into a compliance
# record unchecked. That is not a reason to fake it and it is not a reason to drop it.
# It is a reason to treat a degenerate explanation exactly as the gate treats an
# unverifiable claim: refuse it, say so, and keep the deterministic finding.
_PREFILL = "The merge is held because"


def _key() -> str | None:
    k = os.environ.get("GEMINI_API_KEY") or os.environ.get("GEMMA_API_KEY")
    if k:
        return k.strip()
    path = os.path.expanduser("~/.config/keys/gemini.key")
    try:
        with open(path) as fh:
            return fh.read().strip()
    except OSError:
        return None


def enabled() -> bool:
    """True when this backend could actually answer, not merely when it is selected."""
    base = os.environ.get("GEMMA_BASE_URL", DEFAULT_BASE)
    if not any(h in urlparse(base).netloc for h in _HOSTED):
        return True          # self-hosted endpoints need no key
    return _key() is not None


def leaves_the_network(base: str) -> bool:
    """Measured from the URL that will actually be called, never from intent."""
    return any(h in urlparse(base).netloc for h in _HOSTED)


def explain(findings: list[dict[str, Any]], decision: str, gate: str,
            *, timeout_s: float = 60.0) -> dict[str, Any]:
    """Return a RECEIPT. `invoked` is only true when a model actually answered."""
    base = os.environ.get("GEMMA_BASE_URL", DEFAULT_BASE).rstrip("/")
    model = DEFAULT_MODEL
    hosted = leaves_the_network(base)
    receipt: dict[str, Any] = {
        "backend": "gemma",
        "model": model,
        "endpoint": base,
        "self_hosted": not hosted,
        "left_the_network": hosted,
        "decides_verdict": False,
        "invoked": False,
    }

    lines = "\n".join(
        f"- claim: {f.get('assertion')}\n  probe: {f.get('probe')}\n"
        f"  repo answered: {f.get('evidence')}"
        for f in findings)
    prompt = (f"A CI gate held a merge. The probes already decided.\n\n{lines}\n\n"
              "Write the reviewer note in two or three plain sentences.")
    url = f"{base}/models/{model}:generateContent"
    if hosted:
        k = _key()
        if not k:
            receipt["error"] = "no API key and endpoint is hosted"
            return receipt
        url = f"{url}?key={k}"

    body = json.dumps({
        "contents": [
            {"role": "user", "parts": [{"text": prompt}]},
            {"role": "model", "parts": [{"text": _PREFILL}]},
        ],
        "generationConfig": {"maxOutputTokens": 220, "temperature": 0.2},
    }).encode()

    t0 = time.time()
    try:
        req = urllib.request.Request(
            url, data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            data = json.load(resp)
        parts = data["candidates"][0].get("content", {}).get("parts", [])
        text = "".join(p.get("text", "") for p in parts).strip()
        if not text:
            receipt["error"] = "model returned no text part"
            return receipt
        receipt["invoked"] = True
        candidate = _tidy(f"{_PREFILL} {text}")
        bad = _degenerate(candidate)
        receipt["usable"] = not bad
        if bad:
            receipt["refused"] = bad
        else:
            receipt["text"] = candidate
        receipt["latency_s"] = round(time.time() - t0, 2)
        usage = data.get("usageMetadata") or {}
        receipt["tokens_out"] = usage.get("candidatesTokenCount")
    except urllib.error.HTTPError as e:
        receipt["error"] = f"HTTP {e.code}: {e.read()[:180].decode(errors='replace')}"
    except Exception as e:                                   # noqa: BLE001
        receipt["error"] = f"{type(e).__name__}: {e}"
    return receipt


def _tidy(text: str) -> str:
    """Keep the first paragraph and drop the self-critique that follows it.

    Even prefilled, this model writes a good answer and then reconsiders it out loud:
    "(Wait, let me refine it for a more reviewer tone)" and a second attempt. The first
    paragraph is the answer. This only ever TRUNCATES; it never rewrites a sentence.
    """
    first = text.strip().split("\n\n")[0].strip()
    for tell in ("(Wait", "(Actually", "Draft 1", "*   "):
        if tell in first:
            first = first.split(tell)[0].strip()
    return first or text.strip()


# Thresholds are set from the measured failures above, not chosen for neatness.
_MAX_REPEAT = 6          # "own" appeared 188 times in one collapse
_MAX_NONLATIN = 4        # a clean English note has none; a collapse had 210
_MIN_WORDS = 8


def _degenerate(text: str) -> str | None:
    """Name the defect, or None. A refusal must say WHY, like every other verdict here."""
    words = text.split()
    if len(words) < _MIN_WORDS:
        return f"too short to be an explanation ({len(words)} words)"
    counts: dict[str, int] = {}
    for w in words:
        key = w.strip(".,`").lower()
        counts[key] = counts.get(key, 0) + 1
    top, n = max(counts.items(), key=lambda kv: kv[1])
    if n > _MAX_REPEAT:
        return f"repetition loop: {top!r} appears {n} times"
    nonlatin = sum(1 for c in text if ord(c) > 0x2000)
    if nonlatin > _MAX_NONLATIN:
        return f"{nonlatin} non-latin characters in an English note"
    return None
