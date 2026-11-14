import unittest

from sie.investment.data.eurostat import _unflatten_jsonstat
from sie.investment.providers import _annual_series
from sie.investment.data.ecb import convert_foreign_to_eur


class PublicDataTests(unittest.TestCase):
    def test_sec_annual_series_uses_fiscal_year_and_full_year_duration(self):
        facts = {"facts": {"us-gaap": {"Revenue": {"units": {"USD": [
            {"form": "10-K", "fy": 2025, "start": "2024-09-29", "end": "2025-09-27", "filed": "2025-10-30", "val": 100},
            {"form": "10-Q", "fy": 2025, "start": "2025-04-01", "end": "2025-06-30", "filed": "2025-08-01", "val": 25},
            {"form": "10-K", "fy": 2025, "start": "2024-09-29", "end": "2025-09-27", "filed": "2025-11-01", "val": 101}
        ]}}}}}
        self.assertEqual(_annual_series(facts, ("Revenue",)), {2025: 101.0})

    def test_sec_instant_series_rejects_duration_fact(self):
        facts = {"facts": {"us-gaap": {"Cash": {"units": {"USD": [
            {"form": "10-K", "fy": 2025, "start": "2024-09-29", "end": "2025-09-27", "filed": "2025-10-30", "val": 100},
            {"form": "10-K", "fy": 2025, "end": "2025-09-27", "filed": "2025-10-30", "val": 80}
        ]}}}}}
        self.assertEqual(_annual_series(facts, ("Cash",), instant=True), {2025: 80.0})

    def test_ecb_foreign_currency_conversion(self):
        self.assertAlmostEqual(convert_foreign_to_eur(110.0, "USD", 1.10), 100.0)
        self.assertEqual(convert_foreign_to_eur(100.0, "EUR", 1.10), 100.0)

    def test_jsonstat_unflatten(self):
        payload = {
            "id": ["geo", "time"], "size": [2, 2],
            "dimension": {
                "geo": {"category": {"index": {"BE": 0, "NL": 1}}},
                "time": {"category": {"index": {"2024": 0, "2025": 1}}}
            },
            "value": [1.0, 2.0, 3.0, 4.0]
        }
        self.assertEqual(_unflatten_jsonstat(payload), [
            ({"geo": "BE", "time": "2024"}, 1.0),
            ({"geo": "BE", "time": "2025"}, 2.0),
            ({"geo": "NL", "time": "2024"}, 3.0),
            ({"geo": "NL", "time": "2025"}, 4.0),
        ])


if __name__ == "__main__":
    unittest.main()
