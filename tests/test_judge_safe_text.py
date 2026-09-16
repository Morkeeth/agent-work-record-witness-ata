#!/usr/bin/env python3
"""Prove judgeSafeText strips banned 'required check' lines from report_preview."""
import re

SAMPLE = """# Agent false-done report
# Used to prove HOLD as a required check without /demo/seed-hold.
## Summary
Fixed the auth race and shipped.
"""


def judge_safe_text(s: str) -> str:
    lines = []
    for line in s.splitlines():
        t = line.strip()
        if not t:
            continue
        if re.search(r"required check", t, re.I):
            continue
        if t.startswith("#"):
            continue
        lines.append(t)
    return " ".join(lines).strip()


out = judge_safe_text(SAMPLE)
assert "required check" not in out.lower(), out
assert "Fixed the auth race" in out, out
assert "Used to prove" not in out, out
print("PASS  judgeSafeText strips banned preview lines")
print("OUT  ", out[:120])
