#!/usr/bin/env python3
"""Purge staged/dev rows from the HOLD store so the film opens on a calm, real queue.

Why this exists (2026-08-27): the live queue held rows authored by `phase-a` with reports
like "Committed as deadbee", while SUBMISSION-PACK cites `demo_seed_enabled: false` as proof
that nothing is staged. Both cannot be true on camera. There is no DELETE route on the
gateway by design, so this is a deliberate, local, credentialed operation.

DRY RUN BY DEFAULT. It prints what it would delete and exits without touching anything.
Deleting is not reversible, so `--apply` is required and is Oscar's call.

    PYTHONPATH=. python3 scripts/purge_demo_rows.py             # show me
    PYTHONPATH=. python3 scripts/purge_demo_rows.py --apply      # actually delete
    PYTHONPATH=. python3 scripts/purge_demo_rows.py --actor phase-a --apply
"""
import argparse
import json
import sys

# Actors and report markers that only ever come from staging or development.
DEV_ACTORS = {"phase-a", "phase-b", "demo", "seed", "test", "fixture"}
DEV_MARKERS = ("deadbee", "cafebabe", "/tmp/pwned", "lorem", "example.com")


def looks_staged(rec: dict, extra_actors: set) -> tuple[bool, str]:
    """Return (is_staged, why). Conservative: a record must announce itself as dev."""
    actor = str(rec.get("actor") or rec.get("author") or "").strip().lower()
    if actor in (DEV_ACTORS | extra_actors):
        return True, f"actor={actor}"
    blob = json.dumps(rec, default=str).lower()
    for m in DEV_MARKERS:
        if m in blob:
            return True, f"marker={m}"
    return False, ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="actually delete. Without this it is a dry run.")
    ap.add_argument("--actor", action="append", default=[],
                    help="extra actor name to treat as staged (repeatable)")
    a = ap.parse_args()

    try:
        from cloud.store import get_store
    except Exception as e:
        print(f"cannot import the store: {type(e).__name__}: {e}", file=sys.stderr)
        print("run from the repo root with GCP credentials present.", file=sys.stderr)
        return 2

    store = get_store()
    if not hasattr(store, "all"):
        print(f"store {type(store).__name__} has no all(); cannot enumerate.", file=sys.stderr)
        return 2

    records = list(store.all())
    extra = {x.strip().lower() for x in a.actor}
    staged = [(r, why) for r in records for ok, why in [looks_staged(r, extra)] if ok]

    print(f"store        : {type(store).__name__}")
    print(f"total records: {len(records)}")
    print(f"staged       : {len(staged)}")
    print(f"keeping      : {len(records) - len(staged)}")
    print()
    for r, why in staged:
        rid = r.get("id") or r.get("_id") or "?"
        rep = str(r.get("report") or r.get("kind") or "")[:60].replace("\n", " ")
        print(f"  {rid}  [{why}]  {rep}")

    if not staged:
        print("\nnothing staged. The queue is already clean.")
        return 0

    if not a.apply:
        print(f"\nDRY RUN. Nothing deleted. Re-run with --apply to remove {len(staged)}.")
        return 0

    if not hasattr(store, "delete"):
        print(f"\nstore {type(store).__name__} has no delete(); add one or clear by console.",
              file=sys.stderr)
        return 2

    gone = 0
    for r, _ in staged:
        rid = r.get("id") or r.get("_id")
        if not rid:
            print(f"  skip: record with no id: {str(r)[:70]}")
            continue
        try:
            store.delete(rid)
            gone += 1
        except Exception as e:
            print(f"  FAILED {rid}: {type(e).__name__}: {e}", file=sys.stderr)
    print(f"\ndeleted {gone} of {len(staged)}.")
    return 0 if gone == len(staged) else 1


if __name__ == "__main__":
    raise SystemExit(main())
