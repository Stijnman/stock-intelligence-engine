"""Free-first investment research engine. Deterministic, auditable calculations."""
__version__ = "0.2.0"

from .advanced import (
    backtest_buy_and_hold,
    backtest_target_weights,
    belgian_investment_taxes,
    broker_cost_estimate,
    correlation_matrix,
    data_provenance,
    dcf_sensitivity,
    dividend_sustainability,
    earnings_calendar_risk,
    earnings_surprise,
    eur_portfolio_report,
    fair_value_consensus,
    factor_exposure,
    financial_distress_score,
    generate_alerts,
    insider_sentiment,
    institutional_holding_changes,
    market_regime,
    monte_carlo_projection,
    normalize_insider_transactions,
    optimize_portfolio,
    options_risk_snapshot,
    portfolio_risk,
    rank_watchlist,
    screen_stocks,
    sector_rotation,
    supply_chain_graph,
    ucits_etf_screen,
)

__all__ = [
    "backtest_buy_and_hold", "backtest_target_weights", "belgian_investment_taxes", "broker_cost_estimate",
    "correlation_matrix", "data_provenance", "dcf_sensitivity",
    "dividend_sustainability", "earnings_calendar_risk", "earnings_surprise",
    "eur_portfolio_report", "fair_value_consensus", "factor_exposure",
    "financial_distress_score", "generate_alerts", "insider_sentiment",
    "institutional_holding_changes", "market_regime", "monte_carlo_projection",
    "normalize_insider_transactions", "optimize_portfolio", "options_risk_snapshot",
    "portfolio_risk", "rank_watchlist", "screen_stocks", "sector_rotation", "supply_chain_graph", "ucits_etf_screen",
]
