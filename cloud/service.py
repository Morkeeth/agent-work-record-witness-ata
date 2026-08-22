#!/usr/bin/env python3
"""Fleet wedge API — Cloud Run entry (stdlib HTTP).

Bind port FIRST. Construct ADK / Firestore lazily so Cloud Run health checks pass.
"""

import glob
import json
import os
import sys
import tempfile
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from http.server import BaseHTTPRequestHandler, HTTPServer  # noqa: E402

DEFAULT_TOPIC = (
    "Refactor the auth module: extract validate_token into auth/validate.py, "
    "keep tests green, show me the diff before applying."
)


def _store():
    from cloud.store import get_store
    return get_store()


def _agent():
    from cloud.agent import build_agent
    return build_agent()


def run_wedge(topic: str, target: str, corpus_glob: str = "fixtures/operators/*.jsonl",
              apply: bool = True) -> dict:
    from fleet.propagate import find_best_prompt, propagate_prompt, witness_propagation
    agent = _agent()
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = glob.glob(os.path.join(root, corpus_glob))
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


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _send(self, code, payload):
        body = json.dumps(payload, indent=1, default=str).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read(self):
        n = int(self.headers.get("Content-Length") or 0)
        if not n:
            return {}
        try:
            return json.loads(self.rfile.read(n))
        except json.JSONDecodeError:
            return None

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        # NOTE: GFE returns a platform HTML 404 for GET /healthz on this service —
        # use / or /health for smoke / video. Keep /healthz in code for local only.
        path = self.path.split("?", 1)[0]
        if path in ("/", "/health", "/ready", "/healthz"):
            info = {"ok": True, "service": "fleet-wedge", "route": path}
            try:
                st = _store()
                info["store"] = getattr(st, "backend", type(st).__name__)
            except Exception as e:
                info["store_error"] = f"{type(e).__name__}: {e}"
            try:
                a = _agent()
                info["agent"] = type(a).__module__ + "." + type(a).__name__
            except Exception as e:
                info["agent_error"] = f"{type(e).__name__}: {e}"
            return self._send(200, info)
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
        try:
            if self.path == "/wedge":
                topic = (body.get("topic") or DEFAULT_TOPIC).strip()
                target = body.get("target") or "/tmp/propagated-skill.md"
                apply = body.get("apply", True)
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
            if self.path == "/prove":
                out = run_prove(body.get("topic"))
                if out.get("ok"):
                    try:
                        _store().put({"kind": "prove", "delta": out.get("delta"),
                                      "vc": out.get("vc_one_liner")})
                    except Exception as e:
                        out["store_error"] = f"{type(e).__name__}: {e}"
                return self._send(201 if out.get("ok") else 422, out)
        except Exception as e:
            return self._send(500, {"error": f"{type(e).__name__}: {e}",
                                   "trace": traceback.format_exc()[-1500:]})
        self._send(404, {"error": f"no route {self.path}"})

    def log_message(self, fmt, *a):
        sys.stderr.write("%s %s\n" % (self.address_string(), fmt % a))


def main():
    port = int(os.environ.get("PORT", 8080))
    sys.stderr.write(f"fleet wedge api binding :{port}\n")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
