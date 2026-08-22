#!/usr/bin/env python3
"""Measure the real corpus: which records are a human, and which only look like one.

Read-only. Prints counts and one SHAPE TEMPLATE (structure, no content).
Never writes a transcript's text anywhere.

THE GATE, from the measured reference (re-measured 2026-08-13, 10,866 records / 537 human):
  promptSource in ("typed","queued")   <- NOT "typed" alone; that dropped 106 queued keystrokes
  and not isMeta                        <- injected skill bodies, image refs
  and not isSidechain                   <- sub-agent traffic
  and toolUseResult is None             <- a tool RESULT arrives as type:"user"

THE THIRD SHAPE: type == "queue-operation" carries its text in a TOP-LEVEL `content`
field, not message.content. A parser reading message.content sees nothing at all.
Counted separately here and NEVER bulk-included -- 4,596 of them against 537 real
prompts in the reference window, overwhelmingly the fleet's own traffic.
"""
import glob, json, os, sys
from collections import Counter

ROOT = os.path.expanduser("~/.claude/projects")


def is_human(r):
    return (r.get("type") == "user"
            and r.get("promptSource") in ("typed", "queued")
            and not r.get("isMeta") and not r.get("isSidechain")
            and r.get("toolUseResult") is None)


def main(limit_files=400):
    files = sorted(glob.glob(os.path.join(ROOT, "*", "*.jsonl")),
                   key=os.path.getmtime, reverse=True)[:limit_files]
    c = Counter()
    tool_sessions = []          # sessions that carry BOTH a human turn and a tool_use
    for path in files:
        has_human = has_tool = False
        try:
            for line in open(path, errors="replace"):
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    c["unparseable"] += 1
                    continue
                t = r.get("type")
                c[f"type:{t}"] += 1
                if t == "user":
                    if r.get("toolUseResult") is not None:
                        c["user-but-tool-result"] += 1
                    elif r.get("isMeta"):
                        c["user-but-isMeta"] += 1
                    elif r.get("isSidechain"):
                        c["user-but-sidechain"] += 1
                    elif is_human(r):
                        c["HUMAN"] += 1; has_human = True
                    else:
                        c[f"user-but-promptSource:{r.get('promptSource')}"] += 1
                elif t == "queue-operation":
                    c["queue-operation (text in TOP-LEVEL content)"] += 1
                msg = r.get("message") or {}
                for b in (msg.get("content") or []):
                    if isinstance(b, dict) and b.get("type") == "tool_use":
                        c["tool_use blocks"] += 1
                        has_tool = True
                        if b.get("name") in ("Write", "Edit", "NotebookEdit"):
                            c["tool_use that WRITES a file"] += 1
        except OSError:
            continue
        if has_human and has_tool:
            tool_sessions.append(path)

    total_user = c["type:user"]
    human = c["HUMAN"]
    print("=" * 74)
    print(f"CORPUS MEASURED — {len(files)} most recent session files")
    print("=" * 74)
    for k in sorted(c, key=lambda k: -c[k]):
        if c[k] > 2:
            print(f"  {c[k]:>7,}  {k}")
    print("-" * 74)
    if total_user:
        pct = 100.0 * (total_user - human) / total_user
        print(f"  type:'user' records ......... {total_user:,}")
        print(f"  actually written by a human .. {human:,}")
        print(f"  NOT the human ................ {pct:.1f}%   <- measured here, today")
    print(f"  sessions with BOTH a human turn and a tool_use: {len(tool_sessions)}")
    print("=" * 74)
    return tool_sessions


if __name__ == "__main__":
    s = main()
    print("\nA fixture needs one of those sessions for LANDED to be computable.")
    print("Content is NOT printed and NOT written anywhere by this script.")
