"""Episode structure — corrective UNDECIDABLE keeps one episode (no Gemini)."""

import json
import unittest
from pathlib import Path
from unittest.mock import patch

from fleet.episodes import extract_episodes
from fleet.human import load_transcript


class EpisodeStructureTests(unittest.TestCase):
    def test_fixture_b_one_episode_two_correctives(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "fixtures/operators/operator-b-refactor.jsonl"
        rows = load_transcript(str(path))

        def fake_classify(a, b):
            if "never mind" in b.lower():
                return "DIFFERENT"
            if a == b:
                return "SAME"
            return "UNDECIDABLE"

        with patch("fleet.episodes.classify", side_effect=fake_classify):
            eps = extract_episodes(rows)
        self.assertEqual(len(eps), 1)
        self.assertEqual(eps[0]["signal"], "landed_corrected")
        self.assertEqual(eps[0]["corrective_turns"], 2)


if __name__ == "__main__":
    unittest.main()
