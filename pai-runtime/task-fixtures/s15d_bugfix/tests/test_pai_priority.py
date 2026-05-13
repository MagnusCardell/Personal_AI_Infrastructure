import unittest

from src.pai_priority import normalize_priority


class NormalizePriorityTests(unittest.TestCase):
    def test_low_aliases(self):
        for value in ["low", "LOW", " lo ", "l", "minor"]:
            self.assertEqual(normalize_priority(value), "low")

    def test_medium_aliases(self):
        for value in ["medium", "MED", "normal", "m"]:
            self.assertEqual(normalize_priority(value), "medium")

    def test_high_aliases(self):
        for value in ["high", "hi", "h", "important"]:
            self.assertEqual(normalize_priority(value), "high")

    def test_urgent_aliases(self):
        for value in ["urgent", "critical", "blocker", "p0"]:
            self.assertEqual(normalize_priority(value), "urgent")

    def test_invalid_values_raise(self):
        for value in ["", "later", "unknown", "p9"]:
            with self.assertRaises(ValueError):
                normalize_priority(value)

    def test_non_string_values_raise(self):
        for value in [None, 3, object()]:
            with self.assertRaises(ValueError):
                normalize_priority(value)


if __name__ == "__main__":
    unittest.main()
