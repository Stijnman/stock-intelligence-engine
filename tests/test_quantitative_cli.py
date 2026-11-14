import json
import unittest
from unittest.mock import patch

import sie.investment_cli as cli
from sie.backtest import run_backtest


class QuantitativeCliTests(unittest.TestCase):
    @patch("sie.investment_cli.analyze_live_portfolio_risk", return_value={"status": "ok", "risk": {"sharpe": 1.2}})
    def test_risk_cli_parses_weights_and_range(self, call):
        with patch("sys.argv", ["sie-invest", "risk", "ASML,MSFT", "--weights", "ASML=0.7,MSFT=0.3", "--range", "2y"]):
            self.assertEqual(cli.main(), 0)
        args = call.call_args
        self.assertEqual(args.args[0], ["ASML", "MSFT"])
        self.assertEqual(args.args[1], {"ASML": .7, "MSFT": .3})
        self.assertEqual(args.kwargs["range_"], "2y")

    @patch("sie.investment_cli.run_historical_backtest", return_value={"status": "ok", "total_return_pct": 12})
    def test_backtest_cli_passes_costs_and_rebalance(self, call):
        with patch("sys.argv", ["sie-invest", "backtest", "ASML,MSFT", "--cash", "5000", "--fee-bps", "8", "--slippage-bps", "12", "--rebalance-days", "30"]):
            self.assertEqual(cli.main(), 0)
        self.assertEqual(call.call_args.kwargs["initial_cash"], 5000)
        self.assertEqual(call.call_args.kwargs["fee_bps"], 8)
        self.assertEqual(call.call_args.kwargs["slippage_bps"], 12)
        self.assertEqual(call.call_args.kwargs["rebalance_every"], 30)

    @patch("sie.investment.quantitative.quote_and_history")
    def test_legacy_backtest_wrapper_has_no_fake_performance(self, quote):
        quote.return_value = {
            "history": [{"date": str(i), "close": float(100 + i)} for i in range(8)],
            "currency": "USD", "source": "test", "as_of": "7",
        }
        result = run_backtest("AAA")
        self.assertEqual(result["status"], "ok")
        self.assertNotEqual(result.get("sharpe_ratio"), 1.2)
        self.assertNotEqual(result.get("total_return_pct"), 25.5)
        self.assertIn("actual start_date/end_date", result["period_note"])


if __name__ == "__main__":
    unittest.main()
