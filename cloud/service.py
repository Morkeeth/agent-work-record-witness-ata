#!/usr/bin/env python3
"""HOLD + fleet wedge API — Cloud Run entry (stdlib HTTP).

Bind port FIRST. Construct ADK / Firestore lazily so Cloud Run health checks pass.
HOLD routes: /clearance /queue /break-glass /audit /policy + console at /hold/
Legacy: /wedge /prove /health
"""

from __future__ import annotations


import glob
import json
import mimetypes
import os
import sys
import tempfile
import traceback
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from http.server import BaseHTTPRequestHandler, HTTPServer  # noqa: E402

DEFAULT_TOPIC = (
    "Refactor the auth module: extract validate_token into auth/validate.py, "
    "keep tests green, show me the diff before applying."
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOLD_CONSOLE = os.path.join(ROOT, "surface", "hold")

# In-process policy for demo (also persisted as kind=policy)
_POLICY = None


def _api_token() -> str:
    return (os.environ.get("HOLD_API_TOKEN") or "").strip()


def _demo_seed_enabled() -> bool:
    return os.environ.get("HOLD_DEMO_MODE", "").strip().lower() in ("1", "true", "yes", "on")


def _store():
    from cloud.store import get_store
    return get_store()


def _agent():
    from cloud.agent import build_agent
    return build_agent()


def _policy():
    global _POLICY
    from cloud.hold_api import default_policy
    if _POLICY is None:
        _POLICY = default_policy()
        # hydrate from store if present
        try:
            for r in reversed(_store().all()):
                if r.get("kind") == "policy":
                    _POLICY.update({k: r[k] for k in ("mode", "agent_only", "label", "break_glass_role") if k in r})
                    break
        except Exception:
            pass
    return _POLICY


def run_wedge(topic: str, target: str, corpus_glob: str = "fixtures/operators/*.jsonl",
              apply: bool = True) -> dict:
    from fleet.propagate import find_best_prompt, propagate_prompt, witness_propagation
    agent = _agent()
    paths = glob.glob(os.path.join(ROOT, corpus_glob))
    found = find_best_prompt(topic, paths)
    if "error" in found:
        return {"find": found, "ok": False, "agent": type(agent).__name__}
    field = found.get("field_size") or 0
    org_claim = "OK" if field >= 3 else "UNMEASURED_FOR_ORG_CLAIM"
    if not apply:
        return {"find": found, "dry_run": True, "org_claim": org_claim,
                "agent": type(agent).__module__ + "." + type(agent).__name__, "ok": True}
    prop = propagate_prompt(found["prompt_text"], target,
                            operator=found["operator"], topic=topic)
    wit = witness_propagation(target)
    return {"find": found, "propagate": prop, "witness": wit, "org_claim": org_claim,
            "agent": type(agent).__module__ + "." + type(agent).__name__,
            "ok": wit.get("verdict") == "VERIFIED-BY-REPO"}


def run_prove(topic: str | None = None) -> dict:
    from fleet.org_proof import build_proof, write_surface
    _agent()
    target = os.path.join(tempfile.gettempdir(), "fleet-prove-skill.md")
    proof = build_proof(anchor=topic or DEFAULT_TOPIC, target=target)
    html_path = write_surface(proof)
    return {
        "vc_one_liner": proof.get("vc_one_liner"),
        "delta": proof.get("delta"),
        "find": proof.get("find"),
        "witness": proof.get("witness"),
        "honest_limit": proof.get("honest_limit"),
        "html": html_path,
        "ok": (proof.get("witness") or {}).get("verdict") == "VERIFIED-BY-REPO",
    }


def run_clearance(body: dict) -> dict:
    from cloud.hold_api import (
        evaluate_precomputed,
        evaluate_report,
        make_clearance_record,
    )
    policy = _policy()
    report = body.get("report") or body.get("pr_body") or ""
    findings = body.get("findings")
    repo_path = body.get("repo_path") or os.environ.get("GATE_REPO") or ROOT
    source = body.get("source") or "api"

    # Trust boundary: precomputed PASS/CLEAR findings only from token-bearing CI.
    # Anonymous callers must run evaluate_report (or send BLOCK/HOLD findings for demo seed).
    if findings and source == "github-action":
        evaluation = evaluate_precomputed(findings, report)
    elif findings and source == "demo-seed" and _demo_seed_enabled():
        evaluation = evaluate_precomputed(findings, report)
    elif findings:
        # Re-probe when possible; ignore client PASS claims without CI source
        evaluation = evaluate_report(report, repo_path)
    else:
        evaluation = evaluate_report(report, repo_path)

    # report-only: still ledger HOLD/CLEAR but tell CI not to fail hard
    enforced = policy.get("mode") != "report-only"
    record = make_clearance_record(
        evaluation=evaluation,
        policy=policy,
        # The join: carry the session that produced the claim, so a hold opens back to
        # what the agent actually did rather than stopping at what it wrote.
        session=body.get("session"),
        head_sha=body.get("head_sha"),
        report=report,
        pr=body.get("pr"),
        repo=body.get("repo"),
        actor=body.get("actor") or "agent",
        source=source,
    )
    record["enforced"] = enforced
    try:
        sid = _store().put(record)
        record["store_id"] = sid
    except Exception as e:
        record["store_error"] = f"{type(e).__name__}: {e}"

    # Construct ADK on every clearance path. On HOLD, optionally invoke Runner so
    # Gemini explains findings — probes still own the verdict (P1 partner depth).
    try:
        a = _agent()
        record["agent_class"] = type(a).__module__ + "." + type(a).__name__
    except Exception as e:
        record["agent_error"] = f"{type(e).__name__}: {e}"

    from cloud.hold_api import attach_agent_explanation

    attach_agent_explanation(
        record,
        evaluation,
        session_id=body.get("session") or record.get("session") or record.get("id"),
    )

    if record.get("agent_explanation") and "store_error" not in record:
        try:
            _store().put(record)
        except Exception as e:
            record["store_update_error"] = f"{type(e).__name__}: {e}"

    # A gateway that sells an audit trail must not report success over a failed write.
    # Storing is the product here: if the record did not land, the caller has to know,
    # or HOLD is making exactly the kind of true-looking claim it exists to block.
    # The verdict is still returned and CI still fails on a BLOCK; only the claim about
    # having RECORDED it changes.
    recorded = "store_error" not in record
    return {
        "ok": recorded,
        "recorded": recorded,
        "store_error": record.get("store_error"),
        "product": "THE AGENT WORK RECORD WITNESS",
        "clearance": record,
        "ci_should_fail": bool(enforced and evaluation["decision"] == "HOLD" and evaluation["gate"] == "BLOCK"),
        "ci_should_warn": bool(evaluation["gate"] == "HOLD"),
    }


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _send(self, code, payload):
        body = json.dumps(payload, indent=1, default=str).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_bytes(self, code, data: bytes, content_type: str, *, filename: str | None = None):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        if filename:
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _read(self):
        n = int(self.headers.get("Content-Length") or 0)
        if not n:
            return {}
        try:
            return json.loads(self.rfile.read(n))
        except json.JSONDecodeError:
            return None

    def _extract_token(self) -> str:
        h = self.headers.get("X-HOLD-Token") or ""
        if h.strip():
            return h.strip()
        auth = self.headers.get("Authorization") or ""
        if auth.lower().startswith("bearer "):
            return auth[7:].strip()
        return ""

    def _require_token(self) -> bool:
        """When HOLD_API_TOKEN is set, mutating routes require it. Returns False if rejected."""
        expected = _api_token()
        if not expected:
            return True  # open mode (local/dev)
        got = self._extract_token()
        if got and got == expected:
            return True
        self._send(401, {
            "ok": False,
            "error": "HOLD_API_TOKEN required — set header X-HOLD-Token or Authorization: Bearer",
            "product": "THE AGENT WORK RECORD WITNESS",
        })
        return False

    def _serve_hold_static(self, rel: str):
        rel = rel.lstrip("/") or "index.html"
        if ".." in rel or rel.startswith("/"):
            return self._send(400, {"error": "bad path"})
        path = os.path.join(HOLD_CONSOLE, rel)
        if not os.path.isfile(path):
            # SPA fallback
            path = os.path.join(HOLD_CONSOLE, "index.html")
        if not os.path.isfile(path):
            return self._send(404, {"error": "HOLD console missing — surface/hold/index.html"})
        ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
        with open(path, "rb") as f:
            return self._send_bytes(200, f.read(), ctype)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-HOLD-Token")
        self.end_headers()

    def do_GET(self):
        raw = self.path.split("?", 1)[0]
        path = urllib.parse.unquote(raw)

        if path in ("/", "/health", "/ready", "/healthz"):
            info = {
                "ok": True,
                "service": "agent-work-record-witness-gateway",
                "product": "THE AGENT WORK RECORD WITNESS",
                "route": path,
                "console": "/hold/",
                "auth_required": bool(_api_token()),
                "demo_seed_enabled": _demo_seed_enabled(),
            }
            try:
                st = _store()
                info["store"] = getattr(st, "backend", type(st).__name__)
            except Exception as e:
                info["store_error"] = f"{type(e).__name__}: {e}"
            # A class name proves an import, not a run. /health reports the last real
            # invocation through the ADK Runner, and says so plainly when there has
            # not been one. `agent_class` stays, labelled as what it is.
            try:
                from cloud.agent import last_run
                a = _agent()
                run = last_run()
                agent = {
                    "class": type(a).__module__ + "." + type(a).__name__,
                    "constructed": True,
                    # process-scoped: honest that a cold container has not run yet
                    "invoked_this_process": bool(run and run.get("invoked")),
                    "last_run": run or "never invoked in this process — POST /agent/run",
                }
                # durable answer: has the agent EVER run, per the record? This is what
                # /audit shows, so /health no longer contradicts it on a cold container.
                try:
                    agent["ever_invoked"] = any(
                        r.get("agent_invoked") for r in _store().all()
                    )
                except Exception:
                    agent["ever_invoked"] = None
                info["agent"] = agent
            except Exception as e:
                info["agent_error"] = f"{type(e).__name__}: {e}"
            info["policy"] = _policy()
            return self._send(200, info)

        if path == "/config":
            return self._send(200, {
                "ok": True,
                "product": "THE AGENT WORK RECORD WITNESS",
                "auth_required": bool(_api_token()),
                "demo_seed_enabled": _demo_seed_enabled(),
                "clearance_url": "/clearance",
                "agent_run_url": "/agent/run",
                "workflow": ".github/workflows/outcome-gate.yml",
            })

        if path in ("/hold", "/hold/"):
            return self._serve_hold_static("index.html")
        if path.startswith("/hold/"):
            return self._serve_hold_static(path[len("/hold/"):])

        if path == "/policy":
            return self._send(200, {"ok": True, "policy": _policy()})

        if path == "/queue":
            try:
                from cloud.hold_api import filter_queue
                rows = filter_queue(_store().all())
                return self._send(200, {
                    "ok": True,
                    "product": "THE AGENT WORK RECORD WITNESS",
                    "calm": len(rows) == 0,
                    "count": len(rows),
                    "holds": rows,
                    "message": "No agent releases need attention." if not rows else None,
                })
            except Exception as e:
                return self._send(500, {"error": f"{type(e).__name__}: {e}"})

        if path == "/audit":
            try:
                from cloud.hold_api import filter_audit
                rows = filter_audit(_store().all())
                clears = [r for r in rows if r.get("kind") == "clearance" and r.get("decision") == "CLEAR"]
                holds = [r for r in rows if r.get("kind") == "clearance" and r.get("decision") == "HOLD"]
                exceptions = [r for r in rows if r.get("kind") == "exception"]
                total = len(clears) + len(holds)
                pct = round(100.0 * len(clears) / total, 1) if total else None
                # Spec metric: clears / (clears + holds) ignoring prove spam in numerator story
                return self._send(200, {
                    "ok": True,
                    "product": "THE AGENT WORK RECORD WITNESS",
                    "events": rows[:200],
                    "pct_cleared_without_hold": pct,
                    "counts": {
                        "clear": len(clears),
                        "hold": len(holds),
                        "exception": len(exceptions),
                        "total_clearance": total,
                    },
                })
            except Exception as e:
                return self._send(500, {"error": f"{type(e).__name__}: {e}"})

        if path == "/audit/export":
            try:
                from cloud.hold_api import filter_audit
                rows = filter_audit(_store().all())
                # Drop noisy prove-only wedge spam from export default; keep clearance/exception/policy
                export_rows = [
                    r for r in rows
                    if r.get("kind") in ("clearance", "exception", "policy")
                    or (r.get("product") == "HOLD" and r.get("kind") != "prove")
                ]
                # include prove only if explicitly asked
                qs = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
                if (qs.get("include_prove") or [""])[0] in ("1", "true"):
                    export_rows = rows
                payload = {
                    "product": "THE AGENT WORK RECORD WITNESS",
                    "exported_at": __import__("datetime").datetime.now(
                        __import__("datetime").timezone.utc
                    ).isoformat(timespec="seconds"),
                    "events": export_rows,
                }
                data = json.dumps(payload, indent=2, default=str).encode()
                return self._send_bytes(
                    200, data, "application/json",
                    filename="hold-audit-export.json",
                )
            except Exception as e:
                return self._send(500, {"error": f"{type(e).__name__}: {e}"})

        if path == "/propagations":
            try:
                return self._send(200, {"propagations": _store().all()})
            except Exception as e:
                return self._send(500, {"error": f"{type(e).__name__}: {e}"})

        self._send(404, {"error": f"no route {path}"})

    def do_POST(self):
        body = self._read()
        if body is None:
            return self._send(400, {"error": "body is not valid JSON"})
        path = self.path.split("?", 1)[0]
        try:
            if path == "/clearance":
                if not self._require_token():
                    return
                out = run_clearance(body if isinstance(body, dict) else {})
                return self._send(201, out)

            if path == "/break-glass":
                if not self._require_token():
                    return
                from cloud.hold_api import make_exception_record
                cid = (body.get("clearance_id") or "").strip()
                reason = (body.get("reason") or "").strip()
                actor = (body.get("actor") or "break-glass").strip()
                if not cid or not reason:
                    return self._send(400, {"error": "clearance_id and reason required"})
                # An exception must name what it let through. Read the clearance FIRST
                # so pr/repo/session are inherited from it: an auditor reading the
                # exceptions alone could not otherwise see which PR was merged past a
                # hold without joining back on clearance_id, and the break-glass caller
                # has no reason to retype what the record already knows.
                held = None
                try:
                    for row in _store().all():
                        if row.get("id") == cid and row.get("kind") == "clearance":
                            held = row
                            break
                except Exception:
                    held = None
                rec = make_exception_record(
                    clearance_id=cid,
                    reason=reason,
                    actor=actor,
                    pr=body.get("pr") or (held or {}).get("pr"),
                    repo=body.get("repo") or (held or {}).get("repo"),
                )
                if held is not None:
                    rec["session"] = (held.get("session") or None)
                    rec["traceable"] = bool(held.get("session"))
                    rec["excepted_decision"] = held.get("decision")
                else:
                    rec["clearance_missing"] = True
                try:
                    if held is not None:
                        closed = dict(held)
                        closed["open"] = False
                        closed["kind"] = "clearance"
                        closed["closed_by_exception"] = True
                        _store().put(closed)
                    sid = _store().put(rec)
                    rec["store_id"] = sid
                except Exception as e:
                    rec["store_error"] = f"{type(e).__name__}: {e}"
                return self._send(201, {"ok": True, "exception": rec, "product": "THE AGENT WORK RECORD WITNESS"})

            if path == "/policy":
                if not self._require_token():
                    return
                global _POLICY
                p = _policy()
                for k in ("mode", "agent_only", "label", "break_glass_role"):
                    if k in body:
                        p[k] = body[k]
                if p.get("mode") not in ("report-only", "enforce"):
                    return self._send(400, {"error": "mode must be report-only|enforce"})
                _POLICY = p
                row = {"kind": "policy", "product": "THE AGENT WORK RECORD WITNESS", **p}
                try:
                    _store().put(row)
                except Exception as e:
                    row["store_error"] = f"{type(e).__name__}: {e}"
                return self._send(200, {"ok": True, "policy": p})

            if path == "/demo/seed-hold":
                if not _demo_seed_enabled():
                    return self._send(403, {
                        "ok": False,
                        "error": "demo seed disabled — set HOLD_DEMO_MODE=1 to enable; film should use a real agent PR",
                        "product": "THE AGENT WORK RECORD WITNESS",
                    })
                if not self._require_token():
                    return
                # Precomputed findings — Cloud Run may not ship git; CI Action does.
                fake = {
                    "report": (
                        "Fixed the auth race. Committed as deadbee. "
                        "Wrote docs/auth-migration-2026.md. Everything is done and merged."
                    ),
                    "findings": [
                        {
                            "assertion": "committed as deadbee",
                            "verdict": "BLOCK",
                            "probe": "git cat-file -t deadbee",
                            "evidence": "NOT a commit in this repo",
                        },
                        {
                            "assertion": "wrote docs/auth-migration-2026.md",
                            "verdict": "BLOCK",
                            "probe": "stat docs/auth-migration-2026.md",
                            "evidence": "NO SUCH PATH in the repo",
                        },
                    ],
                    "pr": body.get("pr") or "demo/pr-1",
                    "repo": body.get("repo") or "acme/payments",
                    "actor": "coding-agent[bot]",
                    "source": "demo-seed",
                }
                return self._send(201, run_clearance(fake))

            if path == "/wedge":
                # Writes are gated. This route runs the propagation loop and can write a
                # file at `target`, so it is a mutating route like /clearance, not a read.
                if not self._require_token():
                    return
                topic = (body.get("topic") or DEFAULT_TOPIC).strip()
                target = body.get("target") or "/tmp/propagated-skill.md"
                # Default to a dry run. A write is opt-in, never the fallback: an omitted
                # field must not be the difference between reading and writing to disk.
                apply = body.get("apply", False)
                out = run_wedge(topic, target,
                                body.get("corpus_glob") or "fixtures/operators/*.jsonl",
                                apply=bool(apply))
                if out.get("ok") and apply and out.get("witness"):
                    try:
                        _store().put({"kind": "wedge", "topic": topic,
                                      "witness": out["witness"],
                                      "org_claim": out.get("org_claim")})
                    except Exception as e:
                        out["store_error"] = f"{type(e).__name__}: {e}"
                return self._send(201 if out.get("ok") else 422, out)

            if path == "/agent/run":
                # The one endpoint where a model actually reasons. Gated with the
                # other mutating routes: it spends tokens and writes a receipt.
                if not self._require_token():
                    return
                from cloud.agent import run_agent
                receipt = run_agent(prompt=(body.get("prompt") or None),
                                    session_id=(body.get("session_id") or "witness-run"))
                try:
                    _store().put(dict(receipt, kind="agent_run", product="HOLD"))
                except Exception as e:
                    receipt["store_error"] = f"{type(e).__name__}: {e}"
                return self._send(201 if receipt.get("invoked") else 502, receipt)

            if path == "/prove":
                # Writes a record to the store, so it is gated with the other mutating routes.
                if not self._require_token():
                    return
                out = run_prove(body.get("topic"))
                if out.get("ok"):
                    try:
                        _store().put({
                            "kind": "prove",
                            "product": "THE AGENT WORK RECORD WITNESS",
                            "delta": out.get("delta"),
                            "vc": out.get("vc_one_liner"),
                            "org_claim": "UNMEASURED_FOR_ORG_CLAIM",
                        })
                    except Exception as e:
                        out["store_error"] = f"{type(e).__name__}: {e}"
                return self._send(201 if out.get("ok") else 422, out)
        except Exception as e:
            return self._send(500, {"error": f"{type(e).__name__}: {e}",
                                   "trace": traceback.format_exc()[-1500:]})
        self._send(404, {"error": f"no route {path}"})

    def log_message(self, fmt, *a):
        sys.stderr.write("%s %s\n" % (self.address_string(), fmt % a))


def main():
    port = int(os.environ.get("PORT", 8080))
    sys.stderr.write(
        f"HOLD gateway binding :{port} auth={'on' if _api_token() else 'off'} "
        f"demo_seed={'on' if _demo_seed_enabled() else 'off'}\n"
    )
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
