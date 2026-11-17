#!/usr/bin/env python3
"""Tests for the cleaner. Run: python3 -m unittest discover -v"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import clean  # noqa: E402

FIXTURE = Path(__file__).parent / "data" / "messy_sales.csv"


class TestParsers(unittest.TestCase):
    def test_valid_dates(self):
        cases = {
            "2024-03-05": "2024-03-05",
            "05/03/2024": "2024-03-05",
            "2024/03/09": "2024-03-09",
            "16.03.2024": "2024-03-16",
            "Mar 11 2024": "2024-03-11",
            "  2024-03-25  ": "2024-03-25",
        }
        for raw, expected in cases.items():
            with self.subTest(raw=raw):
                self.assertEqual(clean.parse_date(raw), expected)

    def test_invalid_dates(self):
        for raw in ["", "2024-13-45", "tomorrow", "31/02/2024"]:
            with self.subTest(raw=raw):
                with self.assertRaises(ValueError):
                    clean.parse_date(raw)

    def test_amounts(self):
        cases = {
            "19.99": "19.99",
            "$19.99": "19.99",
            " 19.99 ": "19.99",
            "USD 29.00": "29.00",
            "19,99": "19.99",
            "$ 25,50": "25.50",
            "1.234,56": "1234.56",
            "0.00": "0.00",
        }
        for raw, expected in cases.items():
            with self.subTest(raw=raw):
                self.assertEqual(str(clean.parse_amount(raw)), expected)

    def test_invalid_amounts(self):
        for raw in ["", "   ", "-5.00", "free", "19.99.99"]:
            with self.subTest(raw=raw):
                with self.assertRaises(ValueError):
                    clean.parse_amount(raw)

    def test_email(self):
        self.assertEqual(clean.parse_email("ANA@Example.COM "), "ana@example.com")
        for raw in ["", "carla.ruiz@example", "no at sign.com", "@example.com"]:
            with self.subTest(raw=raw):
                with self.assertRaises(ValueError):
                    clean.parse_email(raw)

    def test_unknown_plan_does_not_crash(self):
        self.assertEqual(clean.parse_plan("PRO "), "pro")
        self.assertEqual(clean.parse_plan("Premium"), "other")

    def test_country(self):
        self.assertEqual(clean.parse_country("España"), "ES")
        self.assertEqual(clean.parse_country("chile"), "CL")
        self.assertEqual(clean.parse_country(""), "??")


class TestEndToEnd(unittest.TestCase):
    def setUp(self):
        rows = clean.read_csv(FIXTURE)
        self.cleaned, self.rejects, self.report = clean.clean_rows(rows)

    def test_counts(self):
        self.assertEqual(self.report["rows_in"], 24)
        self.assertEqual(self.report["rows_out"], 17)
        self.assertEqual(self.report["rejected"], 6)
        self.assertEqual(self.report["duplicates"], 2)
        self.assertEqual(self.report["blank_rows"], 1)

    def test_total_amount(self):
        self.assertEqual(self.report["total_amount"], "346.87")

    def test_reason_per_line(self):
        reasons = {r["line"]: r["reason"].split(":")[0] for r in self.rejects}
        self.assertEqual(reasons[4], "invalid email")
        self.assertEqual(reasons[6], "empty amount")
        self.assertEqual(reasons[7], "duplicate")
        self.assertEqual(reasons[17], "negative amount")
        self.assertEqual(reasons[20], "unrecognized date")
        self.assertEqual(reasons[25], "duplicate")

    def test_no_duplicates(self):
        keys = [(r["email"], r["signup_date"], r["amount"]) for r in self.cleaned]
        self.assertEqual(len(keys), len(set(keys)))

    def test_output_invariants(self):
        for r in self.cleaned:
            with self.subTest(email=r["email"]):
                self.assertRegex(r["signup_date"], r"^\d{4}-\d{2}-\d{2}$")
                self.assertRegex(r["amount"], r"^\d+\.\d{2}$")
                self.assertEqual(r["email"], r["email"].lower())
                self.assertNotIn("  ", r["name"])
                self.assertRegex(r["country"], r"^[A-Z?]{2}$")

    def test_idempotence(self):
        """Cleaning the output must return exactly the same output."""
        again, rejects, _ = clean.clean_rows(self.cleaned)
        self.assertEqual(again, self.cleaned)
        self.assertEqual(rejects, [])


if __name__ == "__main__":
    unittest.main()
