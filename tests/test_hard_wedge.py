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
