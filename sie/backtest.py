"""Price-only historical backtest compatibility wrappers.

This module deliberately avoids fabricated signals or placeholder performance.
Use the CLI quantitative backtest for multi-asset portfolios and full assumptions.
"""
from __future__ import annotations

from sie.investment.quantitative import run_historical_backtest
from sie.config import load_config


def run_backtest(ticker: str, start_date: str = "2023-01-01", end_date: str | None = None, cfg=None):
    """Run a real single-asset buy-and-hold-style backtest.

    The Yahoo chart adapter accepts named ranges rather than arbitrary dates here;
    start_date/end_date remain in the signature for backward compatibility and
    are reported as requested bounds, while the actual returned period is explicit.
    """
    range_ = (cfg or {}).get("backtest_range", "5y")
    result = run_historical_backtest(
        [ticker], {ticker.upper(): 1.0}, range_=range_,
        initial_cash=float((cfg or {}).get("backtest_initial_cash", 10000)),
        fee_bps=float((cfg or {}).get("backtest_fee_bps", 5)),
        slippage_bps=float((cfg or {}).get("backtest_slippage_bps", 5)),
        rebalance_every=252,
    )
    result["ticker"] = ticker.upper()
    result["requested_start_date"] = start_date
    result["requested_end_date"] = end_date
    result["period_note"] = "The current chart adapter uses named lookback ranges; actual start_date/end_date are returned separately."
    return result


def backtest_watchlist(cfg=None):
    cfg = cfg or load_config()
    return {
        ticker: run_backtest(ticker, cfg=cfg)
        for ticker in (cfg.get("tickers") or {})
    }
