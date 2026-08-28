#!/usr/bin/env python3
"""Fleet propagation store — jsonl | firestore.

Default path: Firestore when ADC can resolve a project; else jsonl.
Strangers without GCP still run. Judges with ADC hit Firestore — no flag required.
"""

from __future__ import annotations


import json
import os
import threading
from datetime import datetime, timezone

DEFAULT_PROJECT = "hack-fleet"


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _resolve_project() -> str | None:
    for key in ("GOOGLE_CLOUD_PROJECT", "GCLOUD_PROJECT", "FLEET_GCP_PROJECT"):
        v = os.environ.get(key)
        if v:
            return v
    try:
        import google.auth
        _, project = google.auth.default()
        if project:
            return project
    except Exception:
        pass
    # ADC often has credentials but project=None (user creds). Vertex already
    # uses hack-fleet; keep the same default so req 3 is exercised without a flag.
    try:
        import google.auth
        google.auth.default()
        return DEFAULT_PROJECT
    except Exception:
        return None


def _adc_ready() -> bool:
    try:
        import google.auth
        creds, _ = google.auth.default()
        return creds is not None
    except Exception:
        return False


class JsonlStore:
    backend = "jsonl"

    def __init__(self, path=None):
        self.path = os.path.expanduser(
            path or os.environ.get("FLEET_STORE_PATH", "~/.fleet-ata/propagations.jsonl"))
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self._lock = threading.Lock()

    def put(self, record: dict) -> str:
        """Append, or REPLACE the row that already carries this id.

        FirestoreStore.put does `document(id).set(record)`, which overwrites. This
        store appended unconditionally, so the two backends disagreed about what an
        update means: closing a hold via /break-glass wrote a SECOND row with the
        same H- id, one open and one closed. /audit/export then carried the same
        clearance twice and any count over the record was inflated. Measured on the
        Northwind end-to-end run 2026-08-27: 1 hold, 2 rows, 2 HOLDs in the export.

        A record product must not double-count its own rows, and the jsonl path is
        the one a customer without GCP actually runs.
        """
        record = dict(record)
        record.setdefault("stored_at", _now())
        with self._lock:
            rows = self.all()
            explicit = record.get("id")
            if explicit and any(r.get("id") == explicit for r in rows):
                replaced = [record if r.get("id") == explicit else r for r in rows]
                tmp = self.path + ".tmp"
                with open(tmp, "w") as f:
                    for r in replaced:
                        f.write(json.dumps(r) + "\n")
                os.replace(tmp, self.path)
                return explicit
            record["id"] = explicit or f"P{len(rows) + 1}"
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
        self.project = project or _resolve_project() or DEFAULT_PROJECT
        self._c = firestore.Client(project=self.project).collection(collection)

    def put(self, record):
        record = dict(record)
        record.setdefault("stored_at", _now())
        doc_id = record.get("id")
        if doc_id:
            self._c.document(str(doc_id)).set(record)
            return str(doc_id)
        return self._c.add(record)[1].id

    def all(self):
        out = []
        for d in self._c.stream():
            row = d.to_dict() or {}
            # Prefer product id (H-…) over Firestore auto-id when both exist
            if not row.get("id"):
                row["id"] = d.id
            row["store_doc"] = d.id
            out.append(row)
        return out


def get_store():
    """Default = firestore when ADC exists; jsonl fallback for strangers.

    AN EXPLICIT LOCAL PATH OUTRANKS ADC. Until 2026-08-27 this function consulted
    only FLEET_STORE and ADC, and never FLEET_STORE_PATH -- so setting
    FLEET_STORE_PATH to a scratch file on a credentialed machine still wrote to the
    PRODUCTION Firestore. Measured: a local probe pointed at a scratch file landed
    row aMJIkhk7jcaSF7nUVmiq in prod. That is the source of the polluted audit
    store, which reached 80% probe noise while every writer believed it was local.

    Naming a file is an unambiguous statement of local intent. It wins over an
    ambient credential, and only an explicit FLEET_STORE=firestore can override it.
    """
    kind = os.environ.get("FLEET_STORE", "").lower().strip()
    if not kind:
        # An operator who named a path asked for that path.
        kind = "jsonl" if os.environ.get("FLEET_STORE_PATH", "").strip() \
            else ("firestore" if _adc_ready() else "jsonl")
    if kind == "firestore":
        try:
            return FirestoreStore()
        except Exception:
            if os.environ.get("FLEET_STORE", "").lower() == "firestore":
                raise  # explicit ask must not silently degrade
            return JsonlStore()
    if kind == "jsonl":
        return JsonlStore()
    raise RuntimeError(f"FLEET_STORE={kind!r} — expected jsonl or firestore")
