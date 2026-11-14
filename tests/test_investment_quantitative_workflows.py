import unittest
from unittest.mock import patch

from sie.investment.quantitative import (
    analyze_live_portfolio_risk, load_aligned_price_history, run_historical_backtest,
)


def payload(dates, closes, currency="USD"):
    return {
        "history": [{"date": day, "close": close} for day, close in zip(dates, closes)],
        "currency": currency, "exchange": "TEST", "as_of": dates[-1],
        "source": "test price provider",
    }


class QuantitativeWorkflowTests(unittest.TestCase):
    @patch("sie.investment.quantitative.quote_and_history")
    def test_aligns_on_actual_dates_not_row_position(self, quote):
        quote.side_effect = [
            payload(["2026-01-01", "2026-01-02", "2026-01-05", "2026-01-06", "2026-01-07"], [10, 11, 12, 13, 14]),
            payload(["2026-01-02", "2026-01-05", "2026-01-06", "2026-01-07", "2026-01-08"], [20, 21, 22, 23, 24]),
        ]
        result = load_aligned_price_history(["aaa", "bbb"])
        self.assertEqual(result["dates"], ["2026-01-02", "2026-01-05", "2026-01-06", "2026-01-07"])
        self.assertEqual(result["histories"]["AAA"], [11, 12, 13, 14])
        self.assertEqual(result["histories"]["BBB"], [20, 21, 22, 23])

    @patch("sie.investment.quantitative.quote_and_history")
    def test_provider_error_isolated_but_successful_asset_not_fabricated(self, quote):
        quote.side_effect = [
            payload(["1", "2", "3", "4"], [10, 11, 12, 13]),
            RuntimeError("provider down"),
        ]
        result = load_aligned_price_history(["AAA", "BBB"])
        self.assertIn("BBB", result["errors"])
        self.assertEqual(result["histories"]["AAA"], [10, 11, 12, 13])

    @patch("sie.investment.quantitative.quote_and_history")
    def test_risk_output_has_real_source_and_risk_metrics(self, quote):
        quote.side_effect = [
            payload(["1", "2", "3", "4", "5"], [10, 11, 10.5, 12, 12.5]),
            payload(["1", "2", "3", "4", "5"], [20, 20.5, 21, 20.8, 22]),
        ]
        result = analyze_live_portfolio_risk(["AAA", "BBB"], {"AAA": 2, "BBB": 1})
        self.assertEqual(result["status"], "ok")
        self.assertIn("sharpe", result["risk"])
        self.assertEqual(result["source_status"], "LIVE_INDICATIVE_PRICE_DATA")
        self.assertEqual(result["observations"], 5)
        self.assertNotIn("histories", result)

    @patch("sie.investment.quantitative.quote_and_history")
    def test_backtest_uses_actual_aligned_series_and_costs(self, quote):
        quote.side_effect = [
            payload(["1", "2", "3", "4", "5"], [10, 11, 12, 11, 13]),
            payload(["1", "2", "3", "4", "5"], [20, 21, 19, 22, 24]),
        ]
        result = run_historical_backtest(["AAA", "BBB"], {"AAA": 0.6, "BBB": 0.4})
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["start_date"], "1")
        self.assertEqual(result["end_date"], "5")
        self.assertGreater(result["observations"], 2)
        self.assertIn("no dividends", " ".join(result["limitations"]).lower())

    def test_rejects_negative_backtest_weights(self):
        with patch("sie.investment.quantitative.quote_and_history") as quote:
            quote.side_effect = [payload(["1", "2", "3", "4"], [10, 11, 12, 13])]
            with self.assertRaises(ValueError):
                run_historical_backtest(["AAA"], {"AAA": -1})

    def test_rejects_invalid_backtest_costs(self):
        with patch("sie.investment.quantitative.quote_and_history") as quote:
            quote.side_effect = [payload(["1", "2", "3", "4"], [10, 11, 12, 13])]
            with self.assertRaises(ValueError):
                run_historical_backtest(["AAA"], fee_bps=6000, slippage_bps=5000)


if __name__ == "__main__":
    unittest.main()
