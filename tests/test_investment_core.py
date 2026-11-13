import unittest
from sie.investment.technical import sma, rsi, analyze_history
from sie.investment.valuation import dcf_per_share, scenario_valuation, margin_of_safety
from sie.investment.dividends import analyze_dividends
from sie.investment.etfs import analyze_etf

class InvestmentCoreTests(unittest.TestCase):
    def test_sma(self):
        self.assertEqual(sma([1, 2, 3, 4], 2), 3.5)
        self.assertIsNone(sma([1], 2))
    def test_rsi_uptrend(self):
        self.assertEqual(rsi(list(range(1, 20))), 100.0)
    def test_technical_trend(self):
        result = analyze_history([{"close": float(i)} for i in range(1, 260)])
        self.assertEqual(result["trend"], "bullish")
        self.assertEqual(result["sma200"], 159.5)
    def test_dcf_scenarios_order(self):
        cases = scenario_valuation(1_000_000_000, 100_000_000, 500_000_000)
        self.assertLess(cases["bear"]["intrinsic_value_per_share"], cases["base"]["intrinsic_value_per_share"])
        self.assertLess(cases["base"]["intrinsic_value_per_share"], cases["bull"]["intrinsic_value_per_share"])
    def test_dcf_rejects_bad_rate(self):
        with self.assertRaises(ValueError):
            dcf_per_share(100, 10, discount_rate=0.02, terminal_growth=0.03)
    def test_margin_of_safety(self):
        self.assertAlmostEqual(margin_of_safety(120, 100), 100.0 / 6.0)
    def test_dividend_yield(self):
        result = analyze_dividends([{"date": "2026-01-01", "amount": 1.0}], 50)
        self.assertAlmostEqual(result["dividend_yield_pct"], 2.0)
    def test_etf_missing_data(self):
        result = analyze_etf({"ticker": "VWCE", "ucits": True})
        self.assertIn("ter_pct", result["missing_fields"])
        self.assertLess(result["data_completeness_pct"], 100)

if __name__ == "__main__":
    unittest.main()
