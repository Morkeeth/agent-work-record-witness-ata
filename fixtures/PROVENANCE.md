# Fixture provenance

| File | Source | Notes |
|---|---|---|
| `operator-a-refactor.jsonl` | Claude Code session `2637b3df…` (2026-07-17) | Human opener is demo text; **tool_use / toolUseResult records inherited** from lines 45–59. Paths redacted to `/tmp/fixture-operator`. |
| `operator-b-refactor.jsonl` | Synthetic | Same task class as A per SIGNAL-SPEC: 2 corrective turns then Edit lands. Loses on signal (score 3 vs 4). |

Authorship gate: `promptSource in (typed, queued)` · drop `toolUseResult` user rows ·
`queue-operation` text lives in top-level `content` (see `fleet/human.py`).

Probe: `grep tool_use fixtures/operators/operator-a-refactor.jsonl` → must hit.
