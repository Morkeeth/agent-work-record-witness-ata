#!/usr/bin/env python3
"""How stable is the classifier? Per row, across N runs.

An aggregate range hides WHICH row moves. A product statement needs to know whether
the demo row is stable and one edge case flickers, or whether everything wobbles.

Quota-aware: the free tier is 20/day PER MODEL across a 5-rung ladder, so this stops
cleanly when the rungs exhaust and reports the N it actually achieved. A run that
claims N=10 having managed 4 is the same error this file exists to catch.
"""
import os, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from contract.task_class import CONTROLS
from contract.gemini_impl import classify_gemini, LAST_MODEL

N = int(os.environ.get("N", "10"))
seen = defaultdict(list)
runs_done = 0
for run_i in range(N):
    row_results = {}
    for cid, a, b, expected, why in CONTROLS:
        v = classify_gemini(a, b)
        if str(v).startswith(("API-ERROR", "NO-CANDIDATE")):
            print(f"\n  quota exhausted during run {run_i + 1} at {cid} ({v}).")
            print(f"  Stopping. N ACHIEVED = {runs_done}, not {N}.")
            run_i = None
            break
        row_results[cid] = v
    if run_i is None:
        break
    for cid, v in row_results.items():
        seen[cid].append(v)
    runs_done += 1

if not runs_done:
    print("  No complete run. NO RESULT — not a score of zero.")
    sys.exit(2)

print(f"\n{'='*74}\n  PER-ROW STABILITY over N={runs_done} complete runs\n{'='*74}")
totals = []
for cid, a, b, expected, why in CONTROLS:
    vals = seen[cid]
    c = Counter(vals)
    stable = len(c) == 1
    correct = sum(1 for v in vals if v == expected)
    totals.append(correct)
    flag = "STABLE  " if stable else "*FLICKS*"
    dist = " ".join(f"{k}x{n}" for k, n in c.most_common())
    print(f"  {flag} {cid}  expected {expected:<11} got {dist:<32} {correct}/{runs_done} correct")

per_run = [sum(1 for cid, a, b, e, w in CONTROLS if seen[cid][i] == e) for i in range(runs_done)]
print("-" * 74)
print(f"  per-run scores : {per_run}")
print(f"  range          : {min(per_run)}-{max(per_run)} of 8")
print(f"  mode           : {Counter(per_run).most_common(1)[0][0]}/8")
flicky = [cid for cid in seen if len(Counter(seen[cid])) > 1]
print(f"  rows that move : {flicky or 'none'}")
print(f"  rung distribution: {dict(Counter(LAST_MODEL))}")
print("=" * 74)
print("  Stubs for comparison, deterministic, zero API calls:")
print("    always-DIFFERENT 3/8 every run  ·  always-SAME 4/8 every run  ·  frozen baseline 3/8")
