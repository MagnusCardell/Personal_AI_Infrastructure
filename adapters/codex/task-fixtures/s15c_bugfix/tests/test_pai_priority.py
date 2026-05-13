from __future__ import annotations

import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pai_priority import normalize_priority


class NormalizePriorityTests(unittest.TestCase):
    def test_accepts_low_aliases(self):
        for value in ["low", "LOW", " lo ", "l"]:
            self.assertEqual(normalize_priority(value), "low")

    def test_accepts_medium_aliases(self):
        for value in ["medium", "MED", "normal", " m "]:
            self.assertEqual(normalize_priority(value), "medium")

    def test_accepts_high_aliases(self):
        for value in ["high", "HI", "h"]:
            self.assertEqual(normalize_priority(value), "high")

    def test_accepts_urgent_aliases(self):
        for value in ["urgent", "URGENT", "critical", "blocker"]:
            self.assertEqual(normalize_priority(value), "urgent")

    def test_rejects_invalid_values(self):
        for value in ["", "later", "highest", "none"]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    normalize_priority(value)

    def test_rejects_non_string_values(self):
        for value in [None, 1, object()]:
            with self.subTest(value=type(value).__name__):
                with self.assertRaises(ValueError):
                    normalize_priority(value)


if __name__ == "__main__":
    unittest.main()
