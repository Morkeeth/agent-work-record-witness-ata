#!/usr/bin/env python3
"""The demo reel is real: four confident 'done' claims from ONE night, each caught by the gate.

These are not invented fixtures. Every one happened in this fleet on 2026-08-22 and is in
CURSOR-LOG.md with its commit. That is the pitch a competitor cannot fake: the gate's test suite
IS a logged case series of agents and tools being confidently wrong, and the object being right.
"""
from gate.claim_gate import (probe_power, probe_exercise, probe_right_object)


def CASES():
    v = []

    # 1. "3 of 3 eligibility" — an import mistaken for a call.
    #    eligibility.py checked sys.modules; the store on the default path was JsonlStore.
    v.append(probe_exercise(
        'agent: "the submission meets all 3 required Google technologies at runtime"',
        call=lambda: "JsonlStore",                        # what get_store() actually returned
        want=lambda backend: backend == "FirestoreStore"))

    # 2. "7/8" — one sample quoted as a measurement. It moved 7->6 on a re-run.
    v.append(probe_power(
        'agent: "the classifier scores 7/8, clearly beating the baseline"',
        k=7, n=8))                                        # n=8 is one control set, not a measurement

    # 3. "the sweep is running / scale it to 180" — a kernel run mistaken for a scored submission,
    #    measured in a GGUF room that fires 100% on the baseline that scores 37 live.
    v.append(probe_right_object(
        'agent: "the sweep says scale to N=2000, expect ~180 live"',
        observed="100% fire on every framing",
        expected_kind="live-scorer",
        actual_kind="offline-GGUF-room"))

    # 4. "human_text works — suite green" — green on hand-written fixtures, run against the wrong
    #    object. On REAL sessions message.content is a string, not a block list; the parser returned
    #    empty for 556 of 563 real human turns (98.8%). Green tests, wrong fixtures.
    v.append(probe_right_object(
        'agent: "the extractor works — the whole test suite is green"',
        observed="556 of 563 real human turns returned empty",
        expected_kind="real-session-corpus",
        actual_kind="hand-written-fixtures"))

    return v


if __name__ == "__main__":
    import sys
    from gate.claim_gate import report
    sys.exit(report(CASES()))
