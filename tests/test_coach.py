"""Coach parsing + gating + survival-tier tests on a fully-synthetic fixture.

The fixture carries NO real transcript text (privacy: real ~/.claude logs are $HOME data
and never enter git). It exercises the moat gate, the four survival tiers, episode
segmentation with a correction, and the pattern extractor. The real-log run is the proof
of value; this test is the proof of correctness.
"""
import unittest
from pathlib import Path

from fleet.coach import (
    TIER_ARTIFACT, TIER_COMMIT, TIER_NONE, TIER_REVERTED,
    coach, extract_episodes, prompt_patterns, rank_patterns,
)
from fleet.human import load_transcript

FIX = Path(__file__).resolve().parents[1] / "fixtures/coach/operator-coach-synthetic.jsonl"


class CoachTests(unittest.TestCase):
    def setUp(self):
        self.rows = load_transcript(str(FIX))
        self.eps = extract_episodes(self.rows, source=str(FIX))

    def test_moat_gate_drops_sdk_and_tool_results(self):
        # 6 human-typed prompts exist, but sdk + tool_result turns must NOT open episodes.
        # Correction merges into EP4, so 5 episodes, none opened by the injected turns.
        openers = [e["opener"] for e in self.eps]
        self.assertEqual(len(self.eps), 5)
        self.assertNotIn("SDK injected turn that is not the human", openers)
        self.assertNotIn("tool result echoed back", openers)

    def test_tiers_assigned_correctly(self):
        by_open = {e["opener"][:20]: e for e in self.eps}
        self.assertEqual(by_open["add a retry decorato"]["tier"], TIER_COMMIT)
        self.assertEqual(by_open["write a short summar"]["tier"], TIER_ARTIFACT)
        self.assertEqual(by_open["make it faster"]["tier"], TIER_NONE)      # read-only bash
        self.assertEqual(by_open["the thing keeps drop"]["tier"], TIER_NONE)  # no tool
        self.assertEqual(by_open["bump the version to "]["tier"], TIER_REVERTED)

    def test_survived_only_commit_and_artifact(self):
        self.assertEqual(sum(1 for e in self.eps if e["survived"]), 2)

    def test_correction_merges_into_one_episode(self):
        ep = next(e for e in self.eps if e["opener"].startswith("the thing keeps"))
        self.assertEqual(ep["corrective_turns"], 2)
        self.assertFalse(ep["survived"])

    def test_reverted_commit_is_not_durable(self):
        ep = next(e for e in self.eps if e["opener"].startswith("bump the version"))
        self.assertFalse(ep["survived"])
        self.assertEqual(ep["probe"], "COMMIT-THEN-REVERTED")

    def test_pattern_tags_are_mechanical(self):
        tags = prompt_patterns("add a retry decorator to fetch_url in client.py")
        self.assertIn("intent:CHANGE", tags)
        self.assertIn("names-a-concrete-object", tags)
        self.assertIn("cites-a-file-or-path", tags)

        vague = prompt_patterns("make it faster")
        self.assertIn("no-object (pronoun/vague)", vague)
        self.assertIn("terse (<8 words)", vague)

    def test_rank_patterns_survival_rate(self):
        pats = {p["pattern"]: p for p in rank_patterns(self.eps)}
        # every episode touched by 'cites-a-file-or-path': EP1(commit), EP2(artifact),
        # EP5(reverted) -> 2/3 durable.
        cf = pats["cites-a-file-or-path"]
        self.assertEqual(cf["n"], 3)
        self.assertEqual(cf["survived"], 2)

    def test_coach_end_to_end_shape(self):
        res = coach(str(FIX), "fixture-op")
        self.assertEqual(res["episodes"], 5)
        self.assertEqual(res["durable"], 2)
        self.assertIsNotNone(res["best_prompt"])
        self.assertTrue(res["best_prompt"]["survived"])
        self.assertIsNotNone(res["worst_prompt"])
        self.assertFalse(res["worst_prompt"]["survived"])
        # the best landed prompt is the commit-witnessed one
        self.assertEqual(res["best_prompt"]["tier"], TIER_COMMIT)


if __name__ == "__main__":
    unittest.main()
