import unittest

from sie.investment.advanced import (
    backtest_buy_and_hold, backtest_target_weights, belgian_investment_taxes, broker_cost_estimate, correlation_matrix,
    data_provenance, dcf_sensitivity, dividend_sustainability, earnings_calendar_risk,
    earnings_surprise, eur_portfolio_report, fair_value_consensus, factor_exposure,
    financial_distress_score, generate_alerts, insider_sentiment, institutional_holding_changes, market_regime,
    monte_carlo_projection, normalize_insider_transactions,
    optimize_portfolio, options_risk_snapshot, portfolio_risk, sector_rotation,
    supply_chain_graph, ucits_etf_screen, rank_watchlist, screen_stocks,
)


def prices(n=260, start=100.0, daily=0.001):
    result = [start]
    for i in range(n - 1):
        result.append(result[-1] * (1 + daily * (1 if i % 3 else -0.5)))
    return result


class AdvancedInvestmentTests(unittest.TestCase):
    def test_portfolio_risk_returns_metrics_and_weights(self):
        result = portfolio_risk({"AAA": prices(), "BBB": prices(daily=0.0005)}, {"AAA": 2, "BBB": 1})
        self.assertEqual(result["status"], "ok")
        self.assertAlmostEqual(result["weights"]["AAA"], 2 / 3)
        self.assertGreaterEqual(result["annual_volatility_pct"], 0)
        self.assertLessEqual(result["max_drawdown_pct"], 0)
        self.assertGreaterEqual(result["historical_cvar_pct"], 0)

    def test_portfolio_risk_handles_zero_weights(self):
        self.assertEqual(portfolio_risk({"A": [1, 2, 3]}, {"A": 0})["status"], "unavailable")

    def test_correlation_matrix(self):
        result = correlation_matrix({"A": prices(), "B": prices()})
        self.assertEqual(result["status"], "ok")
        self.assertAlmostEqual(result["matrix"]["A"]["A"], 1)
        self.assertAlmostEqual(result["matrix"]["A"]["B"], 1)

    def test_optimizers_are_long_only_and_fully_invested(self):
        for objective in ("max_sharpe", "min_volatility", "risk_parity"):
            result = optimize_portfolio({"A": prices(), "B": prices(daily=.0007)}, objective=objective, iterations=100)
            self.assertEqual(result["status"], "ok")
            self.assertAlmostEqual(sum(result["weights"].values()), 1)
            self.assertTrue(all(0 <= value <= 1 for value in result["weights"].values()))

    def test_optimizer_rejects_unknown_objective(self):
        with self.assertRaises(ValueError):
            optimize_portfolio({"A": prices(), "B": prices()}, objective="magic")

    def test_optimizer_rejects_infeasible_max_weight(self):
        result = optimize_portfolio({"A": prices(), "B": prices(), "C": prices()}, max_weight=.3)
        self.assertEqual(result["status"], "unavailable")

    def test_monte_carlo_is_reproducible(self):
        a = monte_carlo_projection(1000, .06, .18, years=3, simulations=300, seed=7)
        b = monte_carlo_projection(1000, .06, .18, years=3, simulations=300, seed=7)
        self.assertEqual(a, b)
        self.assertTrue(a["p05"] <= a["median"] <= a["p95"])

    def test_monte_carlo_validates_inputs(self):
        with self.assertRaises(ValueError):
            monte_carlo_projection(1000, .05, .2, simulations=10)

    def test_backtest_accounts_for_friction(self):
        result = backtest_buy_and_hold([100, 110], initial_cash=1000)
        self.assertEqual(result["status"], "ok")
        self.assertLess(result["final_value"], 1100)

    def test_factor_exposure_beta(self):
        result = factor_exposure([.01, .02, -.01, .03], {"market": [.01, .02, -.01, .03]})
        self.assertAlmostEqual(result["factors"]["market"]["beta"], 1)

    def test_market_regime_needs_sufficient_history(self):
        self.assertEqual(market_regime({"SPY": prices(80)})["status"], "unavailable")

    def test_dividend_sustainability(self):
        self.assertEqual(dividend_sustainability(2, eps=1, fcf=10, shares=10)["assessment"], "stretched")

    def test_dcf_sensitivity_grid(self):
        result = dcf_sensitivity(100, 10, discount_rates=(.02, .09))
        self.assertEqual(result["status"], "ok")
        self.assertIsNone(result["per_share_value"]["0.08"]["0.02"])
        self.assertGreater(result["per_share_value"]["0.08"]["0.09"], 0)

    def test_earnings_surprise(self):
        result = earnings_surprise(1.2, 1.0)
        self.assertEqual(result["direction"], "beat")
        self.assertAlmostEqual(result["surprise_pct"], 20)

    def test_financial_distress_flags(self):
        result = financial_distress_score(50, 100, 200, 10, -5, 10)
        self.assertIn("current_ratio_below_1", result["risk_flags"])
        self.assertIn("negative_ebit", result["risk_flags"])

    def test_belgian_tax_calculator(self):
        result = belgian_investment_taxes(10000, tob_rate=.0035, dividend_gross_eur=100)
        self.assertAlmostEqual(result["estimated_tob_eur"], 35)
        self.assertAlmostEqual(result["net_dividend_eur"], 70)

    def test_fair_value_consensus(self):
        result = fair_value_consensus({"dcf": 100, "multiples": 120}, current_price=80)
        self.assertEqual(result["median_fair_value"], 110)
        self.assertAlmostEqual(result["upside_pct"], 37.5)

    def test_alert_generation(self):
        alerts = generate_alerts(
            {"max_drawdown_pct": -25, "historical_cvar_pct": 30},
            {"assessment": "stretched"}, {"upside_pct": -25}, ["stale"],
        )
        self.assertEqual(len(alerts), 5)

    def test_insider_transactions_not_live(self):
        result = normalize_insider_transactions([{"shares": 10, "price": 5, "transaction_code": "P"}])
        self.assertEqual(result["purchase_value"], 50)
        self.assertEqual(result["source_status"], "caller_supplied_not_live_verified")

    def test_options_chain_snapshot(self):
        result = options_risk_snapshot([
            {"implied_volatility": .3, "open_interest": 10, "volume": 5, "type": "call"},
            {"implied_volatility": .4, "open_interest": 20, "volume": 10, "type": "put"},
        ])
        self.assertEqual(result["put_call_volume_ratio"], 2)
        self.assertEqual(result["contracts"], 2)

    def test_data_provenance(self):
        self.assertEqual(data_provenance("live", "SEC")["status"], "LIVE")
        with self.assertRaises(ValueError):
            data_provenance("imaginary")


    def test_sector_rotation_relative_momentum(self):
        result = sector_rotation({"tech": prices(daily=.002), "staples": prices(daily=.0002)}, prices(daily=.001))
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["ranking"][0]["sector"], "tech")

    def test_earnings_calendar_normalizes_dates(self):
        result = earnings_calendar_risk([{"ticker": "ASML", "date": "2026-11-15"}], as_of="2026-11-14")
        self.assertEqual(result["events"][0]["days_until"], 1)
        self.assertEqual(result["source_status"], "caller_supplied_not_live_verified")

    def test_etf_screen_flags_incomplete_metadata(self):
        result = ucits_etf_screen([{"ticker": "VWCE", "isin": "IE00"}])
        self.assertEqual(result["funds"][0]["screen_status"], "incomplete_metadata")

    def test_broker_cost_estimate(self):
        result = broker_cost_estimate(1000, commission_eur=2, fx_spread_pct=.25, tob_eur=3)
        self.assertAlmostEqual(result["total_cost_eur"], 7.5)

    def test_eur_report_requires_fx(self):
        result = eur_portfolio_report(
            [{"ticker": "AAA", "currency": "USD", "market_value": 100},
             {"ticker": "BBB", "currency": "EUR", "market_value": 50}],
            {"USD": .9},
        )
        self.assertAlmostEqual(result["total_eur"], 140)
        self.assertEqual(result["status"], "ok")

    def test_institutional_holdings_change(self):
        result = institutional_holding_changes(
            [{"manager": "M", "issuer": "X", "shares": 10}],
            [{"manager": "M", "issuer": "X", "shares": 15}],
        )
        self.assertEqual(result["holdings"][0]["change_type"], "increased")

    def test_supply_chain_graph_keeps_disclosure_metadata(self):
        result = supply_chain_graph([{"supplier": "A", "customer": "B", "source_url": "https://example.org"}])
        self.assertEqual(result["edge_count"], 1)
        self.assertEqual(result["edges"][0]["source_url"], "https://example.org")

    def test_insider_sentiment_excludes_other_codes(self):
        result = insider_sentiment([
            {"shares": 10, "price": 5, "transaction_code": "P"},
            {"shares": 10, "price": 5, "transaction_code": "S"},
            {"shares": 100, "price": 5, "transaction_code": "A"},
        ])
        self.assertEqual(result["purchase_value"], 50)
        self.assertEqual(result["sale_value"], 50)
        self.assertEqual(result["sentiment_score"], 0)


    def test_periodic_weight_backtest(self):
        result = backtest_target_weights({"A": prices(), "B": prices(daily=.0005)}, {"A": .6, "B": .4})
        self.assertEqual(result["status"], "ok")
        self.assertAlmostEqual(sum(result["target_weights"].values()), 1)
        self.assertGreater(result["cumulative_one_way_turnover"], 0)

    def test_stock_screener_requires_values_for_active_filters(self):
        result = screen_stocks([
            {"ticker": "A", "pe": 12, "market_cap": 1_000_000},
            {"ticker": "B", "pe": 30},
        ], min_market_cap=100_000, max_pe=20)
        self.assertEqual(result["match_count"], 1)
        self.assertEqual(result["results"][0]["ticker"], "A")

    def test_watchlist_ranking_is_transparent(self):
        result = rank_watchlist([
            {"ticker": "A", "margin_of_safety_pct": 20, "roe_pct": 10},
            {"ticker": "B", "margin_of_safety_pct": 5, "roe_pct": 5},
        ])
        self.assertEqual(result["ranking"][0]["ticker"], "A")


if __name__ == "__main__":
    unittest.main()
