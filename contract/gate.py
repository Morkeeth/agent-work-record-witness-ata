"""The verification gate — one call an autonomous workforce passes before production.

The merge, made runnable. Two checks, two axes of trust:

  COMPOSITION (find_adjacency)  — is this report honestly composed? Every number can be
    true while the report still lies: "96%" over rows that sum to 50%, a count over a
    list of a different length, a success percentage over named failures. No per-claim
    attestation catches it.
  TASK/AUTHORSHIP (classify_with_confidence) — an OPTIONAL second axis when the caller
    passes a prompt pair: are two prompts the same work, and is the cheap floor confident
    or should a model decide? (see deterministic.py).

`verify_report(text)` is the gate: feed it an agent's report; it BLOCKS if the composition
lies, PASSES if it holds, and carries the exact finding so a human sees WHY. It is the CI
seam agent-claims-inbox shipped, now inside the admissible hack-fleet shell — the single
"does the reported work survive a look" call.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from contract.adjacency import find_adjacency
from contract.deterministic import classify_with_confidence

PASS = "PASS"
BLOCK = "BLOCK"


@dataclass
class GateResult:
    verdict: str                      # PASS | BLOCK
    ok: bool                          # True == safe to ship the report
    findings: list = field(default_factory=list)   # the ADJACENT-FALSE findings, if any
    why: str = ""                     # one human line
    task: Optional[dict] = None       # optional task-class axis when a prompt pair is given

    def exit_code(self) -> int:
        """0 == PASS, 1 == BLOCK — usable as a CI gate."""
        return 0 if self.ok else 1


def verify_report(text: str, *, prompt_pair: Optional[tuple[str, str]] = None) -> GateResult:
    """Run the composition check on an agent report; BLOCK if it lies by composition.

    If `prompt_pair` is given, also run the task/authorship axis (whose prompt, same work,
    and whether the free floor is confident or the model must decide) — reported, not
    gated on, because a task-class judgement is not a production-safety verdict.
    """
    findings = find_adjacency(text) or []
    if findings:
        kinds = ", ".join(sorted({f.get("kind", "?") for f in findings}))
        why = (f"{len(findings)} composition finding(s) [{kinds}] — every figure may be "
               "true while the report is not. Look before shipping.")
        result = GateResult(BLOCK, False, findings, why)
    else:
        result = GateResult(PASS, True, [], "composition holds: no true-parts-false-whole finding")

    if prompt_pair is not None:
        verdict, confident = classify_with_confidence(prompt_pair[0], prompt_pair[1])
        result.task = {"verdict": verdict, "confident": confident,
                       "tier": "floor" if confident else "defer-to-model"}
    return result


def gate_report(text: str, *, prompt_pair: Optional[tuple[str, str]] = None) -> str:
    """Human-readable one-screen gate output."""
    r = verify_report(text, prompt_pair=prompt_pair)
    lines = [f"[{r.verdict}] {r.why}"]
    for f in r.findings:
        lines.append(f"  ✗ {f.get('kind')}: {f.get('a', '')[:60]!r} ↔ {f.get('b', '')[:60]!r}")
    if r.task is not None:
        t = r.task
        lines.append(f"  task-axis: {t['verdict']} ({t['tier']})")
    return "\n".join(lines)


def main(argv=None) -> int:
    import sys
    args = argv if argv is not None else sys.argv[1:]
    text = sys.stdin.read() if not args else " ".join(args)
    r = verify_report(text)
    print(gate_report(text))
    return r.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
