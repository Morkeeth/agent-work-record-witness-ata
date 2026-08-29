#!/usr/bin/env python3
"""Prove live film surfaces equal film/fixed.json (fixed-by-hash)."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXED_PATH = Path(__file__).resolve().parent / "fixed.json"


def load_fixed() -> dict:
    return json.loads(FIXED_PATH.read_text(encoding="utf-8"))


def sha256_obj(obj: dict) -> str:
    payload = json.dumps(obj, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def health_subset(body: dict) -> dict:
    agent = body.get("agent") or {}
    return {
        "product": body.get("product"),
        "auth_required": body.get("auth_required"),
        "demo_seed_enabled": body.get("demo_seed_enabled"),
        "store": body.get("store"),
        "agent_constructed": agent.get("constructed"),
        "agent_invoked": agent.get("invoked"),
    }


def record_subset(row: dict) -> dict:
    keys = [
        "id", "kind", "source", "traceable", "session",
        "gate", "decision", "pr", "repo", "stored_at",
    ]
    return {k: row[k] for k in keys if k in row}


def corpus_subset_from_html() -> dict:
    html = (ROOT / "surface/fleet-report-page.html").read_text(encoding="utf-8")
    match = re.search(r"window\.__FLEET_REPORT__ = ({.*?});", html, re.DOTALL)
    if not match:
        raise RuntimeError("fleet-report-page.html: __FLEET_REPORT__ missing")
    data = json.loads(match.group(1))
    raw_claims = data["raw_sha_claims"]
    raw_dis = data["raw_disagree"]
    corr_claims = data["corrected_sha_claims"]
    corr_dis = data["corrected_disagree"]
    return {
        "raw_sha_claims": raw_claims,
        "raw_disagree": raw_dis,
        "raw_pct": round(100.0 * raw_dis / raw_claims, 1),
        "corrected_sha_claims": corr_claims,
        "corrected_disagree": corr_dis,
        "corrected_pct": round(100.0 * corr_dis / corr_claims, 1),
        "resolved_in_a_sibling_repo": data["resolved_in_a_sibling_repo"],
        "dropped_as_machinery_or_fixture": data["dropped_as_machinery_or_fixture"],
        "path_claims_not_checkable": data["path_claims_not_checkable"],
    }


def run_demo() -> tuple[str, int]:
    env = {
        "HOME": "/tmp",
        "PATH": "/usr/bin:/bin",
        "LANG": "C.UTF-8",
    }
    proc = subprocess.run(
        ["/bin/bash", str(ROOT / "demo.sh")],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    return proc.stdout + proc.stderr, proc.returncode


def pr_check_state(fixed: dict) -> dict:
    repo = fixed["pr"]["repo"]
    number = fixed["pr"]["number"]
    check_name = fixed["pr"]["check_name"]
    cmd = [
        "gh", "pr", "view", str(number),
        "--repo", repo,
        "--json", "state,statusCheckRollup",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"gh pr view failed: {proc.stderr.strip() or proc.stdout}")
    body = json.loads(proc.stdout)
    checks = body.get("statusCheckRollup") or []
    match = next((c for c in checks if c.get("name") == check_name), None)
    return {
        "state": body.get("state"),
        "check_name": check_name,
        "check_conclusion": (match or {}).get("conclusion"),
    }


def check_result(name: str, ok: bool, detail: str) -> dict:
    return {"name": name, "ok": ok, "detail": detail}


def run_all() -> list[dict]:
    fixed = load_fixed()
    results: list[dict] = []
    base = fixed["service_url"].rstrip("/")

    # /health
    try:
        live_health = fetch_json(f"{base}/health")
        subset = health_subset(live_health)
        live_hash = sha256_obj(subset)
        want = fixed["health"]["subset"]
        want_hash = fixed["health"]["sha256"]
        ok = subset == want and live_hash == want_hash
        results.append(check_result(
            "health",
            ok,
            f"live={live_hash[:12]}… want={want_hash[:12]}…"
            + ("" if ok else f" subset={json.dumps(subset, sort_keys=True)}"),
        ))
    except Exception as exc:
        results.append(check_result("health", False, str(exc)))

    # PR #1 verify-claims
    try:
        pr_live = pr_check_state(fixed)
        want_pr = {
            "state": fixed["pr"]["state"],
            "check_name": fixed["pr"]["check_name"],
            "check_conclusion": fixed["pr"]["check_conclusion"],
        }
        ok = pr_live == want_pr
        results.append(check_result(
            "pr_verify_claims",
            ok,
            f"live={json.dumps(pr_live)} want={json.dumps(want_pr)}",
        ))
    except Exception as exc:
        results.append(check_result("pr_verify_claims", False, str(exc)))

    # Record row H-57b130f397
    try:
        queue = fetch_json(f"{base}/queue")
        row = next(
            (h for h in queue.get("holds", []) if h.get("id") == fixed["record_row"]["subset"]["id"]),
            None,
        )
        if row is None:
            raise RuntimeError("H-57b130f397 not in /queue holds[]")
        subset = record_subset(row)
        live_hash = sha256_obj(subset)
        want_hash = fixed["record_row"]["sha256"]
        ok = subset == fixed["record_row"]["subset"] and live_hash == want_hash
        results.append(check_result(
            "record_row",
            ok,
            f"id={subset.get('id')} live={live_hash[:12]}… want={want_hash[:12]}…",
        ))
    except Exception as exc:
        results.append(check_result("record_row", False, str(exc)))

    # Corpus numbers in repo HTML
    try:
        subset = corpus_subset_from_html()
        live_hash = sha256_obj(subset)
        want_hash = fixed["corpus"]["sha256"]
        ok = subset == fixed["corpus"]["subset"] and live_hash == want_hash
        results.append(check_result(
            "corpus_numbers",
            ok,
            f"41.7→8.1 live={live_hash[:12]}… want={want_hash[:12]}…",
        ))
    except Exception as exc:
        results.append(check_result("corpus_numbers", False, str(exc)))

    # demo.sh cold clone
    try:
        out, code = run_demo()
        patterns = fixed["demo"]["patterns"]
        missing = [p for p in patterns if p not in out]
        want_codes = fixed["demo"]["exit_codes"]
        ok = code == 0 and not missing
        results.append(check_result(
            "demo_cold",
            ok,
            f"exit={code} missing_patterns={missing or 'none'}",
        ))
    except Exception as exc:
        results.append(check_result("demo_cold", False, str(exc)))

    # Voiceover numbers vs fixed inventory
    try:
        vo_path = Path(__file__).resolve().parent / "voiceover.txt"
        vo = vo_path.read_text(encoding="utf-8").strip().splitlines()
        nums = fixed["voiceover_numbers"]
        checks = {
            "three-minute": "3" in vo[0] or "three" in vo[0].lower(),
            "14 tests": "14" in vo[1] or "fourteen" in vo[1].lower(),
            "PR 1": "1" in vo[2] or "one" in vo[2].lower(),
            "H-57b130f397": "H-57b130f397" in vo[3] or "fifty-seven" in vo[3].lower(),
            "41.7": "41.7" in vo[5] or "forty-one" in vo[5].lower(),
            "8.1": "8.1" in vo[5] or "eight point one" in vo[5].lower(),
        }
        bad = [k for k, v in checks.items() if not v]
        ok = not bad and len(vo) == fixed["spine"]["beats"]
        results.append(check_result(
            "voiceover_numbers",
            ok,
            f"lines={len(vo)} bad={bad or 'none'}",
        ))
        # Cross-check spoken corpus ints against corpus subset
        corpus_ok = (
            nums["raw_pct"] == fixed["corpus"]["subset"]["raw_pct"]
            and nums["corrected_pct"] == fixed["corpus"]["subset"]["corrected_pct"]
            and nums["raw_sha_claims"] == fixed["corpus"]["subset"]["raw_sha_claims"]
        )
        results.append(check_result(
            "voiceover_vs_corpus",
            corpus_ok,
            f"raw={nums['raw_pct']}% corrected={nums['corrected_pct']}%",
        ))
    except Exception as exc:
        results.append(check_result("voiceover_numbers", False, str(exc)))

    return results


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args()
    results = run_all()
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            mark = "PASS" if r["ok"] else "FAIL"
            print(f"[{mark}] {r['name']}: {r['detail']}")
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
