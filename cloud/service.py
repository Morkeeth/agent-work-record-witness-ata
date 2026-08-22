#!/usr/bin/env python3
"""Fleet wedge API — stdlib HTTP for Cloud Run (no pip beyond stdlib in service path)."""

import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from http.server import BaseHTTPRequestHandler, HTTPServer  # noqa: E402

from cloud.store import get_store  # noqa: E402
from fleet.bootstrap import ensure_google_stack  # noqa: E402
from fleet.propagate import find_best_prompt, propagate_prompt, witness_propagation  # noqa: E402

ensure_google_stack()  # ADK + Firestore modules on default service import path

DEFAULT_TOPIC = (
    "Refactor the auth module: extract validate_token into auth/validate.py, "
    "keep tests green, show me the diff before applying."
)


def run_wedge(topic: str, target: str, corpus_glob: str = "fixtures/operators/*.jsonl") -> dict:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = glob.glob(os.path.join(root, corpus_glob))
    found = find_best_prompt(topic, paths)
    if "error" in found:
        return {"find": found, "ok": False}
    prop = propagate_prompt(found["prompt_text"], target,
                            operator=found["operator"], topic=topic)
    wit = witness_propagation(target)
    return {"find": found, "propagate": prop, "witness": wit,
            "ok": wit.get("verdict") == "VERIFIED-BY-REPO"}


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _send(self, code, payload):
        body = json.dumps(payload, indent=1).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
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

    def do_GET(self):
        store = get_store()
        if self.path == "/healthz":
            return self._send(200, {"ok": True, "store": store.backend, "service": "fleet-wedge"})
        if self.path == "/propagations":
            return self._send(200, {"propagations": store.all()})
        self._send(404, {"error": f"no route {self.path}"})

    def do_POST(self):
        store = get_store()
        body = self._read()
        if body is None:
            return self._send(400, {"error": "body is not valid JSON"})
        if self.path == "/wedge":
            topic = (body.get("topic") or DEFAULT_TOPIC).strip()
            target = body.get("target") or "fixtures/org-repo/.cursor/rules/propagated-skill.md"
            out = run_wedge(topic, target, body.get("corpus_glob") or "fixtures/operators/*.jsonl")
            if out.get("ok"):
                store.put({"kind": "wedge", "topic": topic, "witness": out["witness"]})
            code = 201 if out.get("ok") else 422
            return self._send(code, out)
        self._send(404, {"error": f"no route {self.path}"})

    def log_message(self, fmt, *a):
        sys.stderr.write("%s %s\n" % (self.address_string(), fmt % a))


def main():
    port = int(os.environ.get("PORT", 8080))
    store = get_store()
    sys.stderr.write(f"fleet wedge api on :{port} · store={store.backend}\n")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
