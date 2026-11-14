"""Network-backed quantitative workflows built on free public/indicative price history."""
from __future__ import annotations

from typing import Mapping, Sequence

from .advanced import backtest_target_weights, correlation_matrix, factor_exposure, portfolio_risk
from .providers import quote_and_history


def load_aligned_price_history(
    tickers: Sequence[str], *, range_: str = "5y"
) -> dict:
    """Load histories and align on exact trading dates; never silently truncate by row."""
    symbols = list(dict.fromkeys(str(t).strip().upper() for t in tickers if str(t).strip()))
    if not symbols:
        raise ValueError("Provide at least one ticker.")
    if len(symbols) > 30:
        raise ValueError("Maximum 30 tickers per quantitative request.")
    dated: dict[str, dict[str, float]] = {}
    metadata: dict[str, dict] = {}
    errors: dict[str, str] = {}
    for symbol in symbols:
        try:
            payload = quote_and_history(symbol, range_=range_)
            series = {
                row["date"]: float(row["close"])
                for row in payload.get("history", [])
                if row.get("date") and row.get("close") is not None and float(row["close"]) > 0
            }
            if len(series) < 4:
                raise RuntimeError("Fewer than four valid daily closes.")
            dated[symbol] = series
            metadata[symbol] = {
                "currency": payload.get("currency"),
                "exchange": payload.get("exchange"),
                "as_of": payload.get("as_of"),
                "source": payload.get("source"),
                "observations": len(series),
            }
        except Exception as exc:
            errors[symbol] = str(exc)
    common_dates = sorted(set.intersection(*(set(v) for v in dated.values()))) if dated else []
    histories = {
        symbol: [series[day] for day in common_dates]
        for symbol, series in dated.items()
    }
    if len(common_dates) < 4:
        errors["alignment"] = "Fewer than four common trading dates across successfully loaded assets."
        histories = {}
        common_dates = []
    return {
        "tickers_requested": symbols,
        "histories": histories,
        "dates": common_dates,
        "metadata": metadata,
        "errors": errors,
        "range": range_,
        "source_status": "LIVE_INDICATIVE_PRICE_DATA",
    }


def analyze_live_portfolio_risk(
    tickers: Sequence[str], weights: Mapping[str, float] | None = None, *,
    range_: str = "5y", risk_free_rate: float = 0.0,
) -> dict:
    loaded = load_aligned_price_history(tickers, range_=range_)
    histories = loaded["histories"]
    if not histories:
        return {"status": "unavailable", **loaded}
    selected_weights = {
        ticker: float((weights or {}).get(ticker, 1.0))
        for ticker in histories
    }
    if any(value < 0 for value in selected_weights.values()):
        raise ValueError("Negative weights are not supported; risk analysis is long-only.")
    risk = portfolio_risk(histories, selected_weights, risk_free_rate=risk_free_rate)
    correlations = correlation_matrix(histories)
    benchmark = "SPY" if "SPY" in histories else None
    factor = {}
    if benchmark:
        benchmark_returns = [
            b / a - 1 for a, b in zip(histories[benchmark], histories[benchmark][1:]) if a > 0
        ]
        factor = {
            ticker: factor_exposure(
                [b / a - 1 for a, b in zip(values, values[1:]) if a > 0],
                {"SPY": benchmark_returns},
            )
            for ticker, values in histories.items() if ticker != benchmark
        }
    summary = {key: value for key, value in loaded.items() if key != "histories"}
    currencies = sorted({meta.get("currency") for meta in loaded["metadata"].values() if meta.get("currency")})
    return {
        "status": risk.get("status", "unavailable"),
        "risk": risk,
        "correlation": correlations,
        "factor_exposure_vs_spy": factor or None,
        "start_date": loaded["dates"][0],
        "end_date": loaded["dates"][-1],
        "observations": len(loaded["dates"]),
        "currencies": currencies,
        "mixed_currencies": len(currencies) > 1,
        **summary,
        "limitations": [
            "Yahoo Finance chart data is unofficial and may be delayed or revised.",
            "Prices are aligned by exact trading date; no currency conversion is performed.",
            "Historical volatility and drawdown are not forecasts.",
            "Dividends, taxes, fees and corporate actions are not included in this risk estimate.",
        ],
    }


def run_historical_backtest(
    tickers: Sequence[str], target_weights: Mapping[str, float] | None = None, *,
    range_: str = "5y", initial_cash: float = 10000.0,
    fee_bps: float = 5.0, slippage_bps: float = 5.0,
    rebalance_every: int = 21,
) -> dict:
    loaded = load_aligned_price_history(tickers, range_=range_)
    histories = loaded["histories"]
    if not histories:
        return {"status": "unavailable", **loaded}
    if target_weights is None:
        target_weights = {ticker: 1.0 for ticker in histories}
    weights = {ticker: float(target_weights.get(ticker, 0.0)) for ticker in histories}
    if any(value < 0 for value in weights.values()) or sum(weights.values()) <= 0:
        raise ValueError("Backtest weights must be non-negative and sum to more than zero.")
    result = backtest_target_weights(
        histories, weights, initial_cash=initial_cash, fee_bps=fee_bps,
        slippage_bps=slippage_bps, rebalance_every=rebalance_every,
    )
    return {
        **result,
        "tickers": list(histories),
        "start_date": loaded["dates"][0],
        "end_date": loaded["dates"][-1],
        "observations": len(loaded["dates"]),
        "price_source": loaded["source_status"],
        "provider_metadata": loaded["metadata"],
        "provider_errors": loaded["errors"],
        "limitations": [
            "Yahoo Finance chart prices are unofficial and may be delayed or revised.",
            "Backtest assumes target weights at the first observation and periodic rebalancing.",
            "No dividends, withholding tax, Belgian TOB, FX, splits, delistings or survivorship-bias correction.",
            "No point-in-time fundamentals or historical signal availability; this is a transparent price-only baseline, not an alpha backtest.",
        ],
    }
