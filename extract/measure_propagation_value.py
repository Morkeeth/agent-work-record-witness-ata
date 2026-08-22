#!/usr/bin/env python3
"""Does the pattern the watcher propagates actually PREDICT landing? — on the real corpus.

The product's whole bet: an operator who names the file, names the symbol, and states an exit
condition lands work more often than one who types "fix auth". If that is true on real data, then
propagating the specified prompt has a measured basis. If it is not, the product is a trick.

This measures the CORRELATION on the real corpus, read-only:
  - episode opener carries the pattern (path + symbol + exit-condition markers) -> "specified"
  - vs not -> "vague"
  - LANDED = a durable file-writing tool_use appears later in the session (ground truth, not prose)
  - compare LANDED-rate between the two groups, with a significance test.

HONEST LIMIT, stated up front: this machine is ONE operator (plus agents), so this is
WITHIN-operator, not across-operator. Cross-operator lift — operator B improving after using
operator A's propagated prompt — is the day-two data the ORG provides and cannot be measured here.
What CAN be measured here is the mechanism it rests on: does specification predict landing.
No transcript text is printed or written.
"""
import glob, json, os, re, sys
from math import comb

ROOT = os.path.expanduser("~/.claude/projects")

def is_human(r):
    return (r.get("type") == "user" and r.get("promptSource") in ("typed", "queued")
            and not r.get("isMeta") and not r.get("isSidechain") and r.get("toolUseResult") is None)

def human_text(r):
    c = (r.get("message") or {}).get("content")
    if isinstance(c, str): return c
    return "\n".join(b.get("text","") for b in (c or []) if isinstance(b, dict) and b.get("type")=="text")

# the propagatable pattern — the operator-A markers, detected from the opener
PATH_RE = re.compile(r'[\w./-]+\.\w{1,5}\b|`[^`]+`')          # a file path or backticked token
SYM_RE  = re.compile(r'\b\w+_\w+\b|\b[a-z]+[A-Z]\w+\b')       # snake_case or camelCase identifier
EXIT_RE = re.compile(r'\b(test|tests|green|diff|verify|confirm|pass|before applying|show me)\b', re.I)

def specified(text):
    score = bool(PATH_RE.search(text)) + bool(SYM_RE.search(text)) + bool(EXIT_RE.search(text))
    return score >= 2          # names at least two of: a path, a symbol, an exit condition

def binom_sf(k, n, p):
    return sum(comb(n, i) * p**i * (1-p)**(n-i) for i in range(k, n+1)) if n else 1.0

def main(limit=600):
    files = sorted(glob.glob(ROOT + "/*/*.jsonl"), key=os.path.getmtime, reverse=True)[:limit]
    spec = {"n": 0, "landed": 0}; vague = {"n": 0, "landed": 0}
    for p in files:
        try: rows = [json.loads(l) for l in open(p, errors="replace") if l.strip()]
        except Exception: continue
        # find the first human opener that is a real task (>= 15 chars), classify it,
        # then LANDED = any later Write/Edit tool_use in the session
        opener = None
        for r in rows:
            if is_human(r):
                t = human_text(r).strip()
                if len(t) >= 15: opener = t; break
        if not opener: continue
        landed = any(
            isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") in ("Write","Edit")
            for r in rows for b in ((r.get("message") or {}).get("content") or [])
            if isinstance((r.get("message") or {}).get("content"), list))
        g = spec if specified(opener) else vague
        g["n"] += 1; g["landed"] += int(landed)
    return spec, vague

if __name__ == "__main__":
    spec, vague = main()
    def rate(g): return g["landed"]/g["n"] if g["n"] else 0.0
    rs, rv = rate(spec), rate(vague)
    print("="*70)
    print("  DOES SPECIFICATION PREDICT LANDING?  (real corpus, read-only)")
    print("="*70)
    print(f"  specified opener  (path+symbol+exit >=2)  landed {spec['landed']:>4}/{spec['n']:<4}  = {rs:5.1%}")
    print(f"  vague opener                              landed {vague['landed']:>4}/{vague['n']:<4}  = {rv:5.1%}")
    print("-"*70)
    if spec["n"] and vague["n"]:
        lift = rs - rv
        # is the specified group's landed-rate above what the vague base-rate predicts?
        p = binom_sf(spec["landed"], spec["n"], rv)
        print(f"  lift = {lift:+.1%}   (specified minus vague)")
        print(f"  P(specified landed >= observed | vague base-rate) = {p:.4f}")
        print(f"  read: {'REAL — specification predicts landing (p<.05)' if p<0.05 else 'NOT SIGNIFICANT at this n — report as suggestive, not proven'}")
    print("="*70)
    print("  LIMIT: one operator (this machine). Cross-operator lift is the ORG's day-two data,")
    print("  not measurable here. This measures the MECHANISM propagation rests on, not the lift.")
