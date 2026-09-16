#!/usr/bin/env python3
"""Prove judgeSafeText strips banned 'required check' lines from report_preview."""
import re

SAMPLE = """# Agent false-done report
# Used to prove HOLD as a required check without /demo/seed-hold.
## Summary
Fixed the auth race and shipped.
- Committed as deadbee
"""


def judge_safe_text(s: str) -> str:
    lines = []
    for line in s.splitlines():
        t = line.strip()
        if not t:
            continue
        if re.search(r"required check", t, re.I):
            continue
        if re.match(r"^#[^#]", t) or t == "#":
            continue
        lines.append(t)
    return " ".join(lines).strip()


out = judge_safe_text(SAMPLE)
assert "required check" not in out.lower(), out
assert "Fixed the auth race" in out, out
assert "## Summary" in out, out
assert "Committed as deadbee" in out, out
assert "Used to prove" not in out, out
print("PASS  judgeSafeText strips banned preview lines, keeps body")
print("OUT  ", out[:160])

# Live-truncated shape: only comment lines
TRUNC = """# Agent false-done report — paste as PR body when labeling a PR `agent`.
# Used to prove HOLD as a required check without /demo/seed-hold.
# The Session trailer is what makes the hold traceable: the console opens it back to
# what the agent
"""
empty = judge_safe_text(TRUNC)
assert empty == "", repr(empty)
print("PASS  truncated comment-only preview scrubs to empty (card falls back to assertion)")
