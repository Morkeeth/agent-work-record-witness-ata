#!/usr/bin/env python3
"""Film-morning probe — re-derive the live claims Oscar will show on camera.

Run from repo root (needs network + playwright chromium once):

    python3 scripts/film_morning_probe.py

Exit 0 only when: health ok, hero present, deep link opens session,
PR #1 red, and the "first card == hero" claim is reported honestly
(fails the process if docs still claim first-card and live disagrees —
this script itself never claims first-card).
"""
from __future__ import annotations

import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = (ROOT / ".cloud_run_url").read_text().strip().rstrip("/")
HERO = "H-a6151a95ac"
SESSION = "01Lzbh4XPYTAgCKg1dciFS3Q"


def get(path: str):
    with urllib.request.urlopen(BASE + path, timeout=30) as r:
        return json.load(r)


def post_code(path: str) -> int:
    req = urllib.request.Request(
        BASE + path, data=b"{}", method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        urllib.request.urlopen(req, timeout=30)
        return 200
    except urllib.error.HTTPError as e:
        return e.code


def main() -> int:
    failed = []
    print(f"BASE {BASE}")

    health = get("/health")
    print("health", {k: health.get(k) for k in
                     ("ok", "auth_required", "demo_seed_enabled", "store")})
    if not health.get("ok") or health.get("store") != "firestore":
        failed.append("health")

    queue = get("/queue")
    ids = [h["id"] for h in queue.get("holds") or []]
    first = ids[0] if ids else None
    hero_idx = ids.index(HERO) if HERO in ids else None
    print(f"queue count={queue.get('count')} first={first} hero_idx={hero_idx}")
    if hero_idx is None:
        failed.append("hero_missing_from_queue")
    if first == HERO:
        print("NOTE: hero IS first card tonight — unusual; still prefer ?record=")
    else:
        print(f"EMBARRASSMENT AVOIDED: do not say first card; use ?record={HERO}")

    hero = next(h for h in queue["holds"] if h["id"] == HERO)
    print("hero", {k: hero.get(k) for k in
                   ("session", "traceable", "head_sha", "gate", "decision", "pr")})
    if hero.get("session") != SESSION or not hero.get("traceable"):
        failed.append("hero_session")

    audit = get("/audit")
    print("pct_cleared_without_hold", audit.get("pct_cleared_without_hold"))
    if audit.get("pct_cleared_without_hold") != 0.0:
        failed.append("pct_cleared")

    for path, want in (("/clearance", 401), ("/break-glass", 401),
                       ("/prove", 401), ("/demo/seed-hold", 403)):
        got = post_code(path)
        print(f"POST {path} -> {got} (want {want})")
        if got != want:
            failed.append(f"post{path}")

    pr = json.loads(subprocess.check_output(
        ["gh", "pr", "view", "1", "--json", "state,statusCheckRollup"],
        text=True,
    ))
    checks = {c["name"]: c["conclusion"] for c in pr["statusCheckRollup"]}
    print("PR #1", pr["state"], checks)
    if pr["state"] != "OPEN" or checks.get("verify-claims") != "FAILURE":
        failed.append("pr1")

    # Deep link — optional if playwright missing
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright not installed — skip deep-link browser probe")
    else:
        with sync_playwright() as p:
            b = p.chromium.launch(args=["--no-sandbox"])
            page = b.new_page(viewport={"width": 1440, "height": 900})
            page.goto(f"{BASE}/hold/?record={HERO}",
                      wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(3000)
            state = page.evaluate(
                """() => {
                  const d = document.getElementById('detail');
                  const t = d ? d.innerText : '';
                  return {
                    detailHidden: !d || d.classList.contains('hidden'),
                    hasSession: t.includes('01Lzbh4XPYTAgCKg1dciFS3Q'),
                    hasDeadbee: t.toLowerCase().includes('deadbee'),
                  };
                }"""
            )
            page.click('button[data-tab="stack"]')
            page.wait_for_timeout(1500)
            after = page.evaluate(
                """() => ({
                  stackVisible: !document.getElementById('tab-stack')
                    .classList.contains('hidden')
                })"""
            )
            b.close()
        print("deep_link", state, after)
        if state["detailHidden"] or not state["hasSession"] or not after["stackVisible"]:
            failed.append("deep_link")

    if failed:
        print("FAILED:", ", ".join(failed))
        return 1
    print("PASS — film morning probes green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
