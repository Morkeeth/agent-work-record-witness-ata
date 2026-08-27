"""Hard tests — corrective markers, org-claim refuse, prove delta shape."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fleet.episodes import CORRECTIVE_MARKERS, _looks_corrective, extract_episodes
from fleet.human import load_transcript
from fleet.org_proof import build_proof


ROOT = Path(__file__).resolve().parents[1]


class CorrectiveMarkerTests(unittest.TestCase):
    def test_markers_catch_fixture_b_turns(self):
        self.assertTrue(_looks_corrective("no, I meant the token bit"))
        self.assertTrue(_looks_corrective("not that file, the validator"))
        self.assertFalse(_looks_corrective("Refactor the auth module completely"))

    def test_linguistic_beats_gemini_split(self):
        """If Gemini would DIFFERENT the clarifiers, markers still keep one episode."""
        rows = load_transcript(str(ROOT / "fixtures/operators/operator-b-refactor.jsonl"))

        def evil_classify(a, b):
            return "DIFFERENT"  # would fake a cold land without markers

        with patch("fleet.episodes.classify", side_effect=evil_classify):
            eps = extract_episodes(rows)
        self.assertEqual(len(eps), 1)
        self.assertEqual(eps[0]["signal"], "landed_corrected")
        self.assertEqual(eps[0]["corrective_turns"], 2)
        self.assertGreaterEqual(len(CORRECTIVE_MARKERS), 5)


class OrgClaimTests(unittest.TestCase):
    def test_field_of_two_is_unmeasured_for_org(self):
        from cloud.service import run_wedge
        with patch("cloud.service._agent") as ag:
            ag.return_value = type("A", (), {})()
            with patch("fleet.propagate.find_best_prompt") as find:
                find.return_value = {
                    "operator": "a",
                    "prompt_text": "hello",
                    "field_size": 2,
                    "signal": "landed",
                    "score": 4,
                }
                out = run_wedge("topic", "/tmp/x", apply=False)
        self.assertEqual(out["org_claim"], "UNMEASURED_FOR_ORG_CLAIM")
        self.assertTrue(out["ok"])

    def test_field_of_three_ok(self):
        from cloud.service import run_wedge
        with patch("cloud.service._agent") as ag:
            ag.return_value = type("A", (), {})()
            with patch("fleet.propagate.find_best_prompt") as find:
                find.return_value = {
                    "operator": "a",
                    "prompt_text": "hello",
                    "field_size": 3,
                    "signal": "landed",
                    "score": 4,
                }
                out = run_wedge("topic", "/tmp/x", apply=False)
        self.assertEqual(out["org_claim"], "OK")


class ProveDeltaTests(unittest.TestCase):
    def test_prove_delta_a0_b2(self):
        target = tempfile.mktemp(suffix="-skill.md")
        # Pairwise membership: SAME. Episode splits: linguistic markers (no Gemini).
        with patch("fleet.org_proof.classify", return_value="SAME"):
            with patch("fleet.episodes.classify", return_value="SAME"):
                proof = build_proof(target=target)
        self.assertIsNotNone(proof.get("witness"), proof.get("find"))
        d = proof["delta"]
        self.assertEqual(d["winner"], "a")
        self.assertEqual(d["loser"], "b")
        self.assertEqual(d["winner_turns"], 0)
        self.assertEqual(d["loser_turns"], 2)
        self.assertEqual(d["corrective_turn_delta"], 2)
        self.assertEqual(proof["witness"]["verdict"], "VERIFIED-BY-REPO")
        self.assertIn("validate_token", proof["find"]["prompt_text"])


if __name__ == "__main__":
    unittest.main()


# --- the corpus fixes: precision, and a repo resolution that must not go quiet ---
#
# All three are measured findings from running the shipped probe over 144,306 real
# agent messages. See docs/CORPUS-MEASUREMENT-2026-08-27.md.

def test_a_sha_in_a_sibling_repo_is_not_a_false_claim():
    """74 of 110 'wrong' SHAs in the corpus were real commits in ANOTHER repo on
    the same disk. An agent's cwd is where it stood, not where it committed."""
    import os
    from gate.outcome_gate import PASS, check_report
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    head = os.popen(f"git -C {here} rev-parse --short HEAD").read().strip()
    # Branch A: the reported cwd is a real repo that simply does not have the sha.
    other = os.path.dirname(here)  # ~/CODE itself: reachable, not this repo
    fs = check_report(f"Done. Committed as {head}.", other, sibling_repos=[here])
    sha = [f for f in fs if f.assertion.startswith("committed as")]
    assert sha and sha[0].verdict == PASS
    assert here in sha[0].evidence, sha[0].evidence

    # Branch B: the reported cwd no longer exists at all, which is ordinary in a
    # corpus. Siblings must still be asked before an agent is called a liar.
    gone = os.path.join(os.path.dirname(here), "does-not-exist-repo")
    fs = check_report(f"Done. Committed as {head}.", gone, sibling_repos=[here])
    sha = [f for f in fs if f.assertion.startswith("committed as")]
    assert sha and sha[0].verdict == PASS
    assert "unreachable" in sha[0].evidence


def test_sibling_resolution_does_not_silence_a_real_absence():
    """THE CONTROL. A fix that makes a check quieter is the dangerous kind, and
    this one makes it quieter by two thirds. A fabricated sha must still BLOCK."""
    import os
    from gate.outcome_gate import BLOCK, check_report
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fs = check_report("Done. Committed as 0000000deadfeed111.", here,
                      sibling_repos=[here])
    sha = [f for f in fs if f.assertion.startswith("committed as")]
    assert sha and sha[0].verdict == BLOCK


def test_shell_commands_and_fenced_blocks_are_not_claims():
    """8 of 40 sampled corpus hits were a sha inside a command the agent ran."""
    from gate.outcome_gate import check_report
    body = ('Looking at state.\n'
            'echo "=== ZUP fix (was b6ec7b4) ==="\n'
            '```\n0eef89f 2026-07-20 submit: add final\n```\n')
    assert [f for f in check_report(body, ".") if f.assertion.startswith("committed as")] == []


def test_our_own_fixture_is_excluded_only_when_asked():
    """`deadbee` MUST still block in the product's own demo. It is skipped only
    on the corpus path, where it is this repo's test data showing up in
    transcripts about building this gate — 6 of 40 sampled hits."""
    from gate.outcome_gate import BLOCK, check_report
    body = "Fixed the race. Committed as deadbee."
    assert any(f.verdict == BLOCK for f in check_report(body, "."))
    assert [f for f in check_report(body, ".", exclude_fixtures=True)
            if f.assertion.startswith("committed as")] == []


def test_scope_refuses_to_guess_when_there_is_no_report_section():
    """Scoped extraction reads a declared done-report, and yields nothing when the
    message has none. Refusing to guess is the same rule the rest of the gate runs on."""
    from gate.outcome_gate import check_report
    chatty = "I think commit a1b2c3d might be where that regressed, worth a look."
    assert [f for f in check_report(chatty, ".", scope=True)
            if f.assertion.startswith("committed as")] == []
    reported = "## Done\n\nCommitted as a1b2c3d.\n"
    assert [f for f in check_report(reported, ".", scope=True)
            if f.assertion.startswith("committed as")]


def test_not_checkable_drops_non_paths_and_keeps_real_ones():
    """A claim whose target was never inside a repo is not a finding — the probe is
    right and the claim was never checkable. The floor matters more than the
    ceiling: over-filtering HIDES real findings, so every real path shape below
    must survive."""
    from gate.corpus_scan import not_checkable
    for keep in ("docs/plan.md", "package.json", ".mcp.json", "config.yaml",
                 "_jed.py", "needs.ts", "src/a/b.ts", "registry.md", "init.sql"):
        assert not_checkable(keep) is None, keep
    assert "hostname" in not_checkable("github.com")
    assert "URL" in not_checkable("https://x.com/a")
    assert "outside the repository" in not_checkable("/tmp/harness.html")
    assert "code identifier" in not_checkable("task_runs.run_id")
    assert "code identifier" in not_checkable("_INDEX_OK.pop")


def test_our_own_staged_demo_path_is_excluded_only_when_asked():
    """docs/auth-migration-2026.md is the literal false-done string this repo
    stages in cloud/service.py and fixtures/agent-false-done-PR-BODY.md. It reaches
    a corpus because real messages discuss the demo while building it, and the tool
    then reports its own seed text as a caught claim. Same circularity as deadbee,
    and like deadbee it MUST still block in the product's own demo."""
    from gate.outcome_gate import BLOCK, check_report
    body = "Done. Wrote docs/auth-migration-2026.md."
    assert any(f.verdict == BLOCK for f in check_report(body, "."))
    assert [f for f in check_report(body, ".", exclude_fixtures=True)
            if f.assertion.startswith("wrote ")] == []
