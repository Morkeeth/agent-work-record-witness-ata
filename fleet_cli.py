#!/usr/bin/env python3
"""Fleet wedge CLI — find → propagate → witness on fixtures or live corpus."""

import argparse
import glob
import json
import os
import sys

from fleet.bootstrap import ensure_google_stack
from fleet.propagate import find_best_prompt, propagate_prompt, witness_propagation
from fleet.episodes import extract_episodes, score_session_episodes
from fleet.human import load_transcript
from fleet.org_proof import build_proof, write_surface


def cmd_wedge(args):
    ensure_google_stack()
    # Construct ADK agent on the runnable path (eligibility exercises this).
    from cloud.agent import build_agent
    agent = build_agent()
    corpus = args.corpus or glob.glob(
        os.path.join(os.path.dirname(__file__), "fixtures/operators/*.jsonl"))
    result = find_best_prompt(args.topic, corpus)
    if "error" in result:
        print(json.dumps(result, indent=2))
        return 1
    prop = propagate_prompt(result["prompt_text"], args.target,
                           operator=result["operator"], topic=args.topic)
    wit = witness_propagation(args.target)
    from cloud.store import get_store
    store = get_store()
    store.put({"kind": "wedge", "topic": args.topic, "find": result,
               "witness": wit, "agent": type(agent).__module__ + "." + type(agent).__name__})
    out = {"find": result, "propagate": prop, "witness": wit,
           "agent": type(agent).__name__, "store": store.backend}
    print(json.dumps(out, indent=2))
    return 0 if wit.get("verdict") == "VERIFIED-BY-REPO" else 1


def cmd_episodes(args):
    rows = load_transcript(args.path)
    eps = extract_episodes(rows)
    if args.topic:
        scored = score_session_episodes(args.path, args.topic)
        print(json.dumps({"episodes": eps, "score": scored}, indent=2))
    else:
        print(json.dumps({"episodes": eps}, indent=2))
    return 0


def cmd_prove(args):
    """VC/judge artifact: same class, different cost, literal propagate."""
    ensure_google_stack()
    from cloud.agent import build_agent
    build_agent()
    proof = build_proof(anchor=args.topic, target=args.target)
    path = write_surface(proof, args.html)
    from cloud.store import get_store
    store = get_store()
    store.put({"kind": "prove", "delta": proof.get("delta"), "vc": proof.get("vc_one_liner")})
    slim = {
        "vc_one_liner": proof["vc_one_liner"],
        "delta": proof["delta"],
        "find": {k: proof["find"].get(k) for k in
                 ("operator", "signal", "score", "prompt_text", "field_size")
                 if isinstance(proof.get("find"), dict)},
        "witness": proof.get("witness"),
        "store": store.backend,
        "html": path,
        "honest_limit": proof["honest_limit"],
    }
    print(json.dumps(slim, indent=2))
    return 0 if (proof.get("witness") or {}).get("verdict") == "VERIFIED-BY-REPO" else 1


def main():
    p = argparse.ArgumentParser(description="hack-fleet-ata wedge loop")
    sub = p.add_subparsers(dest="cmd", required=True)
    w = sub.add_parser("wedge", help="run find → propagate → witness")
    w.add_argument("--topic", "--anchor", dest="topic", default=(
        "Refactor the auth module: extract validate_token into auth/validate.py, "
        "keep tests green, show me the diff before applying."))
    w.add_argument("--target", default="fixtures/org-repo/.cursor/rules/propagated-skill.md")
    w.add_argument("--corpus", nargs="*", help="transcript jsonl paths")
    w.set_defaults(func=cmd_wedge)
    e = sub.add_parser("episodes", help="extract episodes from a transcript jsonl")
    e.add_argument("path", help="transcript jsonl path")
    e.add_argument("--topic", "--anchor", dest="topic",
                   help="anchor prompt (full human prompt, not a bare label)")
    e.set_defaults(func=cmd_episodes)
    pr = sub.add_parser("prove", help="org-lift proof: A vs B cost + literal propagate + HTML")
    pr.add_argument("--topic", "--anchor", dest="topic", default=(
        "Refactor the auth module: extract validate_token into auth/validate.py, "
        "keep tests green, show me the diff before applying."))
    pr.add_argument("--target", default="fixtures/org-repo/.cursor/rules/propagated-skill.md")
    pr.add_argument("--html", default="surface/org-proof.html")
    pr.set_defaults(func=cmd_prove)
    args = p.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
