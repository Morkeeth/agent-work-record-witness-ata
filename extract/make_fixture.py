#!/usr/bin/env python3
"""Inherit the SHAPE of a real session; author the CONTENT.

WHY NOT JUST SHIP A REAL SESSION
--------------------------------
The requirement was: do not invent a `tool_use` record, because an invented record
fixes the numerator and leaves the shape imagined. Correct.

But this repo is going to a PUBLIC remote, and Oscar's real transcripts contain his
work, his paths, and other people's names. Shipping one is an irreversible disclosure
that no hackathon deadline justifies -- and it is his call, not a lane's.

So: TAKE THE SHAPE, AUTHOR THE CONTENT. Every field name, every nesting level, every
record type and the exact tool_use / toolUseResult layout is inherited from a real
session and cannot be wrong about what a tool call looks like. Only the text is written
by hand. That satisfies the actual requirement -- the shape was the thing that could be
wrong -- without publishing anything of his.

Read-only on the source. Prints the SHAPE, never the content.
"""
import glob, json, os, sys
from collections import OrderedDict

ROOT = os.path.expanduser("~/.claude/projects")


def shape_of(value, depth=0):
    """Structure only. Strings collapse to their type, never their value."""
    if depth > 4:
        return "..."
    if isinstance(value, dict):
        return OrderedDict((k, shape_of(v, depth + 1)) for k, v in value.items())
    if isinstance(value, list):
        return [shape_of(value[0], depth + 1)] if value else []
    if isinstance(value, str):
        return "<str>"
    if value is None:
        return None
    return type(value).__name__


def find_session():
    """Newest session carrying a human turn AND a file-writing tool_use."""
    files = sorted(glob.glob(os.path.join(ROOT, "*", "*.jsonl")),
                   key=os.path.getmtime, reverse=True)[:400]
    for path in files:
        human = tool = result = None
        try:
            for line in open(path, errors="replace"):
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if (human is None and r.get("type") == "user"
                        and r.get("promptSource") in ("typed", "queued")
                        and not r.get("isMeta") and not r.get("isSidechain")
                        and r.get("toolUseResult") is None):
                    human = r
                msg = r.get("message") or {}
                for b in (msg.get("content") or []):
                    if (isinstance(b, dict) and b.get("type") == "tool_use"
                            and b.get("name") in ("Write", "Edit") and tool is None):
                        tool = r
                if result is None and r.get("toolUseResult") is not None:
                    result = r
        except OSError:
            continue
        if human and tool and result:
            return human, tool, result
    return None, None, None


if __name__ == "__main__":
    h, t, res = find_session()
    if not h:
        print("No session found carrying all three record shapes.")
        sys.exit(2)
    print("=" * 74)
    print("INHERITED SHAPE — structure only, every string collapsed to <str>")
    print("=" * 74)
    for label, rec in (("HUMAN TURN", h), ("ASSISTANT with tool_use", t),
                       ("TOOL RESULT (arrives as type:'user')", res)):
        print(f"\n--- {label}")
        print(json.dumps(shape_of(rec), indent=1)[:1100])
    print("\n" + "=" * 74)
    print("No content from any real session was printed or written.")
