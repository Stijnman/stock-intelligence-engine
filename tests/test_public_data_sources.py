import unittest
from unittest.mock import patch

from sie.investment.data.nbb import fetch_sdmx_csv, fetch_preset, list_presets
from sie.investment.data.worldbank import fetch_indicator


class AddedPublicSourceTests(unittest.TestCase):
    def test_nbb_sdmx_csv_normalization(self):
        csv_body = b"KEY,TIME_PERIOD,OBS_VALUE,UNIT_MEASURE,OBS_STATUS\nBE,2024,2.5,PC,A\nBE,2025,3.0,PC,P\n"
        with patch("sie.investment.data.nbb.get_bytes", return_value=csv_body):
            rows = fetch_sdmx_csv("https://stat.nbb.be/rest/v1/data/example")
        self.assertEqual([r["period"] for r in rows], ["2024", "2025"])
        self.assertEqual(rows[1]["value"], 3.0)
        self.assertEqual(rows[1]["status"], "P")

    def test_nbb_rejects_non_nbb_hosts(self):
        with self.assertRaises(ValueError):
            fetch_sdmx_csv("https://example.com/data.csv")

    def test_nbb_verified_preset_listing_and_fetch(self):
        self.assertIn("mfi-interest-rates", list_presets())
        with patch("sie.investment.data.nbb.fetch_sdmx_csv", return_value=[{"period": "2025-09", "value": 2.5, "dimensions": {"MIR_ITEM": "R_N"}}, {"period": "2025-09", "value": 999, "dimensions": {"MIR_ITEM": "B_N"}}]):
            rows = fetch_preset("mfi-interest-rates", start_period="2025-09")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["preset"], "mfi-interest-rates")
        self.assertIn("DF_MIR", rows[0]["preset_title"])

    def test_nbb_preset_rejects_invalid_period(self):
        with self.assertRaises(ValueError):
            fetch_preset("mfi-interest-rates", start_period="last year")

    def test_world_bank_indicator_normalization_and_nulls(self):
        response = [
            {"pages": 1},
            [
                {"country": {"id": "BE", "value": "Belgium"}, "date": "2024", "value": 100.0, "unit": ""},
                {"country": {"id": "BE", "value": "Belgium"}, "date": "2023", "value": None, "unit": ""}
            ]
        ]
        with patch("sie.investment.data.worldbank.get_json", return_value=response):
            rows = fetch_indicator("BE", "NY.GDP.MKTP.CD", start=2020, end=2025)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["value"], 100.0)
        self.assertEqual(rows[0]["period"], "2024")

    def test_world_bank_validates_page_size(self):
        with self.assertRaises(ValueError):
            fetch_indicator("BE", "NY.GDP.MKTP.CD", per_page=0)


if __name__ == "__main__":
    unittest.main()
