import unittest
from unittest.mock import patch

from sie.investment.data.macro import macro_snapshot


class MacroSnapshotIntegrationTests(unittest.TestCase):
    @patch("sie.investment.data.macro.latest_debt_snapshot", return_value={"status": "ok", "total_public_debt_usd": 100})
    @patch("sie.investment.data.macro.fetch_indicator", return_value=[{"period": "2025", "value": 1.0}])
    @patch("sie.investment.data.macro.fetch_dataset")
    @patch("sie.investment.data.macro.euro_reference_rates", return_value=[{"period": "2026-11-01", "value": 1.1}])
    def test_snapshot_includes_treasury_debt(self, fx, eurostat, worldbank, treasury):
        eurostat.side_effect = lambda dataset, filters: [
            {"period": "2025-10", "value": 100.0},
            {"period": "2026-10", "value": 102.0},
        ]
        result = macro_snapshot()
        self.assertEqual(result["us_treasury_debt"]["total_public_debt_usd"], 100)
        self.assertIn("U.S. Treasury Fiscal Data", result["sources"])

    @patch("sie.investment.data.macro.latest_debt_snapshot", side_effect=RuntimeError("offline"))
    @patch("sie.investment.data.macro.fetch_indicator", return_value=[])
    @patch("sie.investment.data.macro.fetch_dataset", return_value=[])
    @patch("sie.investment.data.macro.euro_reference_rates", return_value=[])
    def test_treasury_outage_does_not_break_macro_snapshot(self, fx, eurostat, worldbank, treasury):
        result = macro_snapshot()
        self.assertEqual(result["us_treasury_debt"]["status"], "unavailable")
        self.assertEqual(result["us_treasury_debt"]["error"], "offline")


if __name__ == "__main__":
    unittest.main()
