import unittest
from unittest.mock import patch

from sie.investment.data.cftc import fetch_legacy_futures_only, positioning_summary
from sie.investment.data.fred import fetch_series


class CFTCAdapterTests(unittest.TestCase):
    def test_cftc_normalizes_positions_and_net_exposure(self):
        payload = [{
            "report_date_as_yyyy_mm_dd": "2026-11-10T00:00:00.000",
            "market_and_exchange_names": "GOLD - COMEX",
            "contract_market_name": "GOLD",
            "commodity_name": "GOLD",
            "open_interest_all": "1000",
            "noncomm_positions_long_all": "600",
            "noncomm_positions_short_all": "250",
            "comm_positions_long_all": "200",
            "comm_positions_short_all": "550",
        }]
        with patch("sie.investment.data.cftc.get_json", return_value=payload) as mocked:
            rows = fetch_legacy_futures_only(commodity="gold", limit=10)
        self.assertEqual(rows[0]["noncommercial_net"], 350)
        self.assertEqual(rows[0]["commercial_net"], -350)
        self.assertEqual(rows[0]["noncommercial_net_pct_open_interest"], 35)
        self.assertIn("6dca-aqww", mocked.call_args.args[0])

    def test_cftc_rejects_invalid_dataset_and_dates(self):
        with self.assertRaises(ValueError):
            fetch_legacy_futures_only(dataset="not-a-dataset")
        with self.assertRaises(ValueError):
            fetch_legacy_futures_only(start_date="last-friday")

    def test_cftc_summary_compares_weekly_positioning(self):
        result = positioning_summary([
            {"report_date": "2026-11-03", "noncommercial_net": 100, "commodity": "GOLD", "contract": "GOLD"},
            {"report_date": "2026-11-10", "noncommercial_net": 150, "commodity": "GOLD", "contract": "GOLD"},
        ])
        self.assertEqual(result["noncommercial_net_change"], 50)
        self.assertEqual(result["direction"], "net_long")

    def test_cftc_summary_never_compares_different_contracts(self):
        result = positioning_summary([
            {"report_date": "2026-11-03", "noncommercial_net": -200, "contract": "MICRO GOLD"},
            {"report_date": "2026-11-03", "noncommercial_net": 1000, "contract": "GOLD"},
            {"report_date": "2026-10-27", "noncommercial_net": 900, "contract": "GOLD"},
        ])
        gold = next(item for item in result["contracts"] if item["contract"] == "GOLD")
        self.assertEqual(gold["noncommercial_net_change"], 100)
        micro = next(item for item in result["contracts"] if item["contract"] == "MICRO GOLD")
        self.assertIsNone(micro["noncommercial_net_change"])

    def test_cftc_summary_separates_same_contract_name_by_exchange(self):
        result = positioning_summary([
            {"report_date": "2026-11-03", "noncommercial_net": 10, "contract": "GOLD", "market": "GOLD - EXCHANGE A"},
            {"report_date": "2026-11-03", "noncommercial_net": 1000, "contract": "GOLD", "market": "GOLD - EXCHANGE B"},
            {"report_date": "2026-10-27", "noncommercial_net": 900, "contract": "GOLD", "market": "GOLD - EXCHANGE B"},
        ])
        exchange_b = next(item for item in result["contracts"] if item["market"] == "GOLD - EXCHANGE B")
        self.assertEqual(exchange_b["noncommercial_net_change"], 100)
        exchange_a = next(item for item in result["contracts"] if item["market"] == "GOLD - EXCHANGE A")
        self.assertIsNone(exchange_a["noncommercial_net_change"])

    def test_fred_requires_own_api_key(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(RuntimeError):
                fetch_series("DFF")

    def test_fred_normalizes_missing_observations(self):
        payload = {"observations": [
            {"date": "2026-10-01", "value": "3.5", "realtime_start": "2026-10-02", "realtime_end": "9999-12-31"},
            {"date": "2026-11-01", "value": ".", "realtime_start": "2026-11-02", "realtime_end": "9999-12-31"},
        ]}
        with patch("sie.investment.data.fred.get_json", return_value=payload):
            rows = fetch_series("DFF", api_key="test-key")
        self.assertEqual(rows[0]["value"], 3.5)
        self.assertIsNone(rows[1]["value"])
        self.assertEqual(rows[1]["status"], "MISSING")


if __name__ == "__main__":
    unittest.main()
