"""The record — a week of an agent fleet, per actor.

The gate knows what was CLAIMED and whether the object agreed. The corpus knows what
was actually DONE and whether it survived. Each half alone is a feature. Joined, they
answer the question an org running an agent workforce cannot answer today:

    who on this fleet ships claims that hold, and whose work stays?

Deliberate boundaries, because this surface is the pitch and it must not overstate:
  - Every rate carries its denominator. A rate over n=2 is labelled thin, not rounded up.
  - Survival is a PROXY (a durable write or an un-reverted commit), never proof of correct
    work, and the word travels with the number.
  - Probe/test records are excluded from the population by default, because an audit
    percentage computed over people testing the audit is not an audit percentage.
  - An actor with no traceable claims is reported as untraceable, not omitted.
"""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable

# Records left behind by testing rather than by a fleet doing work. Counting these
# would compute the fleet's honesty over its own dry runs.
NOISE_KINDS = {"prove", "wedge"}
NOISE_ACTORS = {"phase-a", "phase-b", "demo", "seed", "test", "fixture"}
NOISE_MARKERS = ("deadbee", "cafebabe", "/tmp/pwned")

THIN_N = 5  # below this, a rate is reported but explicitly marked thin


def _parse_ts(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def is_noise(rec: dict) -> bool:
    """True when a record came from testing the system rather than using it."""
    if str(rec.get("kind") or "").lower() in NOISE_KINDS:
        return True
    if str(rec.get("actor") or "").strip().lower() in NOISE_ACTORS:
        return True
    blob = f"{rec.get('report_preview','')}{rec.get('report','')}".lower()
    return any(m in blob for m in NOISE_MARKERS)


def _rate(num: int, den: int) -> float | None:
    return round(num / den, 3) if den else None


def build_record(
    records: Iterable[dict],
    *,
    days: int = 7,
    now: datetime | None = None,
    include_noise: bool = False,
    coach_result: dict | None = None,
) -> dict:
    """Join clearance decisions into a per-actor record for the last `days`.

    `coach_result` is an optional fleet.coach.coach() dict. When present its survival
    figures are attached to the whole window, clearly marked as operator-scoped, because
    the corpus is per-operator and the gate is per-actor: they are DIFFERENT populations
    and merging them into one number would be the composition error this product exists
    to catch.
    """
    now = now or datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days)

    all_recs = list(records)
    clearances, excluded, undated = [], 0, 0
    for r in all_recs:
        if str(r.get("kind") or "") != "clearance":
            if is_noise(r) and not include_noise:
                excluded += 1
            continue
        if not include_noise and is_noise(r):
            excluded += 1
            continue
        ts = _parse_ts(r.get("stored_at"))
        if ts is None:
            undated += 1
            continue
        if ts >= cutoff:
            clearances.append(r)

    by_actor: dict[str, dict] = defaultdict(
        lambda: {"claims": 0, "held": 0, "traceable": 0, "overridden": 0})
    exceptions = [r for r in all_recs if str(r.get("kind") or "") == "exception"]
    overridden_ids = {str(e.get("clearance_id") or "") for e in exceptions}

    for c in clearances:
        a = by_actor[str(c.get("actor") or "unknown")]
        a["claims"] += 1
        if str(c.get("decision") or "").upper() == "HOLD":
            a["held"] += 1
        if c.get("session"):
            a["traceable"] += 1
        if str(c.get("id") or "") in overridden_ids:
            a["overridden"] += 1

    actors = []
    for name, a in sorted(by_actor.items(), key=lambda kv: -kv[1]["claims"]):
        n = a["claims"]
        actors.append({
            "actor": name,
            "claims": n,
            "held": a["held"],
            "clear": n - a["held"],
            # The number a platform lead actually wants: how often this actor's "done"
            # survived contact with the object.
            "honesty_rate": _rate(n - a["held"], n),
            "traceable": a["traceable"],
            "traceable_rate": _rate(a["traceable"], n),
            "overridden": a["overridden"],
            "thin": n < THIN_N,
        })

    total = len(clearances)
    held = sum(x["held"] for x in actors)
    traceable = sum(x["traceable"] for x in actors)

    out = {
        "window_days": days,
        "generated_at": now.isoformat(),
        "claims": total,
        "held": held,
        "clear": total - held,
        "honesty_rate": _rate(total - held, total),
        "traceable": traceable,
        "traceable_rate": _rate(traceable, total),
        "overrides": len(exceptions),
        "actors": actors,
        "excluded_as_noise": excluded,
        "undated_skipped": undated,
        "thin": total < THIN_N,
        "proxy_note": "Held means the object disagreed with the claim. It is a probe result, "
                      "not a judgement of the engineer.",
    }

    if coach_result:
        # Attached, never merged. Different population, stated as such.
        out["practice"] = {
            "scope": "one operator's own corpus, NOT the fleet population above",
            "operator": coach_result.get("operator"),
            "episodes": coach_result.get("episodes"),
            "survival_rate": coach_result.get("durable_rate"),
            "human_turn_pct": coach_result.get("human_pct"),
            "proxy": coach_result.get("proxy"),
        }
    return out


def render(rec: dict) -> str:
    """Plain-text render. The console reads the JSON; this is for a terminal and a film."""
    L = []
    w = rec["window_days"]
    L.append(f"THE RECORD — last {w} days")
    L.append("=" * 62)
    if rec["claims"] == 0:
        L.append("No agent claims in this window.")
        if rec["excluded_as_noise"]:
            L.append(f"({rec['excluded_as_noise']} test/probe records excluded.)")
        return "\n".join(L)

    hr = rec["honesty_rate"]
    L.append(f"claims        : {rec['claims']}" + ("   [THIN]" if rec["thin"] else ""))
    L.append(f"held          : {rec['held']}   (the object disagreed)")
    L.append(f"honesty rate  : {hr:.0%}" if hr is not None else "honesty rate  : n/a")
    tr = rec["traceable_rate"]
    L.append(f"traceable     : {rec['traceable']} of {rec['claims']}"
             + (f"  ({tr:.0%} open back to a session)" if tr is not None else ""))
    L.append(f"overrides     : {rec['overrides']}   (break-glass, each with a reason)")
    if rec["excluded_as_noise"]:
        L.append(f"excluded      : {rec['excluded_as_noise']} test/probe records")
    L.append("")
    L.append(f"  {'actor':<22}{'claims':>7}{'held':>6}{'honest':>8}{'traceable':>11}")
    L.append("  " + "-" * 54)
    for a in rec["actors"]:
        h = f"{a['honesty_rate']:.0%}" if a["honesty_rate"] is not None else "n/a"
        t = f"{a['traceable_rate']:.0%}" if a["traceable_rate"] is not None else "n/a"
        flag = "  thin" if a["thin"] else ""
        L.append(f"  {a['actor'][:22]:<22}{a['claims']:>7}{a['held']:>6}{h:>8}{t:>11}{flag}")

    p = rec.get("practice")
    if p:
        L.append("")
        L.append("PRACTICE (attached, not merged — a different population)")
        L.append(f"  scope   : {p['scope']}")
        sr = p.get("survival_rate")
        if sr is not None:
            L.append(f"  survival: {sr:.0%} of {p.get('episodes')} episodes")
        if p.get("human_turn_pct") is not None:
            L.append(f"  human   : {p['human_turn_pct']}% of records were typed by a person")
        L.append(f"  proxy   : {p.get('proxy')}")
    L.append("")
    L.append(rec["proxy_note"])
    return "\n".join(L)
