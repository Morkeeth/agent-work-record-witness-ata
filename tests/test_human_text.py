"""Control: human_text must handle string message.content (98.8% of real sessions)."""

import json
import tempfile
import unittest
from pathlib import Path

from fleet.human import human_text, is_human_turn, load_transcript


class HumanTextTests(unittest.TestCase):
    def test_string_content(self):
        rec = {"type": "user", "promptSource": "typed",
               "message": {"role": "user", "content": "hello from a real session"}}
        self.assertEqual(human_text(rec), "hello from a real session")
        self.assertTrue(is_human_turn(rec))

    def test_list_content_blocks(self):
        rec = {"type": "user", "promptSource": "typed",
               "message": {"role": "user", "content": [{"type": "text", "text": "block form"}]}}
        self.assertEqual(human_text(rec), "block form")

    def test_tool_result_not_human(self):
        rec = {"type": "user", "toolUseResult": "ok", "promptSource": None}
        self.assertFalse(is_human_turn(rec))

    def test_fixture_a_has_tool_use(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "fixtures/operators/operator-a-refactor.jsonl"
        rows = load_transcript(str(path))
        self.assertTrue(any("tool_use" in json.dumps(r) for r in rows))


if __name__ == "__main__":
    unittest.main()
