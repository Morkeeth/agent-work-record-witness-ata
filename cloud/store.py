#!/usr/bin/env python3
"""Fleet propagation store — jsonl | firestore seam (from agent-claims-inbox)."""

import json
import os
import threading
from datetime import datetime, timezone


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class JsonlStore:
    backend = "jsonl"

    def __init__(self, path=None):
        self.path = os.path.expanduser(
            path or os.environ.get("FLEET_STORE_PATH", "~/.fleet-ata/propagations.jsonl"))
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self._lock = threading.Lock()

    def put(self, record: dict) -> str:
        record = dict(record)
        record.setdefault("stored_at", _now())
        with self._lock:
            n = sum(1 for _ in open(self.path)) if os.path.isfile(self.path) else 0
            record["id"] = record.get("id") or f"P{n + 1}"
            with open(self.path, "a") as f:
                f.write(json.dumps(record) + "\n")
        return record["id"]

    def all(self):
        if not os.path.isfile(self.path):
            return []
        out = []
        with open(self.path) as f:
            for line in f:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return out


class FirestoreStore:
    backend = "firestore"

    def __init__(self, collection="propagations", project=None):
        try:
            from google.cloud import firestore  # noqa: F401
        except ImportError as e:
            raise RuntimeError(
                "FLEET_STORE=firestore needs google-cloud-firestore + GCP credentials."
            ) from e
        from google.cloud import firestore
        self._c = firestore.Client(project=project).collection(collection)

    def put(self, record):
        record = dict(record)
        record.setdefault("stored_at", _now())
        return self._c.add(record)[1].id

    def all(self):
        return [d.to_dict() | {"id": d.id} for d in self._c.stream()]


def get_store():
    kind = os.environ.get("FLEET_STORE", "jsonl").lower()
    if kind == "firestore":
        return FirestoreStore()
    if kind == "jsonl":
        return JsonlStore()
    raise RuntimeError(f"FLEET_STORE={kind!r} — expected jsonl or firestore")
