#!/usr/bin/env python3
"""Fleet wedge CLI — find → propagate → witness on fixtures or live corpus."""

import argparse
import glob
import json
import os
import sys

from fleet.propagate import find_best_prompt, propagate_prompt, witness_propagation
from fleet.episodes import extract_episodes, score_session_episodes
from fleet.human import load_transcript


def cmd_wedge(args):
    corpus = args.corpus or glob.glob(
        os.path.join(os.path.dirname(__file__), "fixtures/operators/*.jsonl"))
    result = find_best_prompt(args.topic, corpus)
    if "error" in result:
        print(json.dumps(result, indent=2))
        return 1
    prop = propagate_prompt(result["prompt_text"], args.target,
                           operator=result["operator"], topic=args.topic)
    wit = witness_propagation(args.target)
    out = {"find": result, "propagate": prop, "witness": wit}
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


def main():
    p = argparse.ArgumentParser(description="hack-fleet-ata wedge loop")
    sub = p.add_subparsers(dest="cmd", required=True)
    w = sub.add_parser("wedge", help="run find → propagate → witness")
    w.add_argument("--topic", default=(
        "Refactor the auth module: extract validate_token into auth/validate.py, "
        "keep tests green, show me the diff before applying."))
    w.add_argument("--target", default="fixtures/org-repo/.cursor/rules/propagated-skill.md")
    w.add_argument("--corpus", nargs="*", help="transcript jsonl paths")
    w.set_defaults(func=cmd_wedge)
    e = sub.add_parser("episodes", help="extract episodes from a transcript jsonl")
    e.add_argument("path", help="transcript jsonl path")
    e.add_argument("--topic", help="score episodes against this task class")
    e.set_defaults(func=cmd_episodes)
    args = p.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
