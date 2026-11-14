import unittest
from unittest.mock import patch

from sie.investment.data.treasury import fetch_debt_to_penny, latest_debt_snapshot


class TreasuryAdapterTests(unittest.TestCase):
    def test_debt_to_penny_normalization(self):
        payload = {"data": [{
            "record_date": "2026-11-12",
            "debt_held_public_amt": "30000000000000.00",
            "intragov_hold_amt": "7000000000000.00",
            "tot_pub_debt_out_amt": "37000000000000.00",
        }]}
        with patch("sie.investment.data.treasury.get_json", return_value=payload) as mocked:
            rows = fetch_debt_to_penny(start_date="2020-01-01", limit=5)
        self.assertEqual(rows[0]["total_public_debt_usd"], 37_000_000_000_000)
        self.assertIn("debt_to_penny", mocked.call_args.args[0])
        self.assertEqual(rows[0]["currency"], "USD")

    def test_debt_to_penny_validates_inputs(self):
        with self.assertRaises(ValueError):
            fetch_debt_to_penny(start_date="yesterday")
        with self.assertRaises(ValueError):
            fetch_debt_to_penny(limit=0)

    def test_latest_snapshot_handles_empty_data(self):
        with patch("sie.investment.data.treasury.fetch_debt_to_penny", return_value=[]):
            self.assertEqual(latest_debt_snapshot()["status"], "unavailable")


if __name__ == "__main__":
    unittest.main()
