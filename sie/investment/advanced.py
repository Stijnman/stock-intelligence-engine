"""Deterministic, free-first quantitative analytics for the Investment Intelligence Engine.

All functions accept plain Python mappings/lists and return JSON-serialisable values.
No network calls, paid feeds, or trade execution occur in this module.
"""
from __future__ import annotations

import math
import random
from datetime import date, datetime
from statistics import mean, median, stdev
from typing import Any, Mapping, Sequence


def _clean(values: Sequence[float]) -> list[float]:
    return [float(x) for x in values if x is not None and math.isfinite(float(x))]


def _returns(prices: Sequence[float]) -> list[float]:
    p = _clean(prices)
    return [b / a - 1.0 for a, b in zip(p, p[1:]) if a > 0]


def _mean(values: Sequence[float]) -> float | None:
    x = _clean(values)
    return mean(x) if x else None


def _stdev(values: Sequence[float]) -> float | None:
    x = _clean(values)
    return stdev(x) if len(x) > 1 else None


def _percentile(values: Sequence[float], q: float) -> float | None:
    x = sorted(_clean(values))
    if not x:
        return None
    pos = (len(x) - 1) * min(1.0, max(0.0, q))
    lo, hi = math.floor(pos), math.ceil(pos)
    return x[lo] + (x[hi] - x[lo]) * (pos - lo)


def portfolio_risk(
    price_history: Mapping[str, Sequence[float]],
    weights: Mapping[str, float] | None = None,
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252,
    confidence: float = 0.95,
) -> dict[str, Any]:
    """Calculate long-only portfolio risk from aligned close-price series."""
    tickers = [t for t, p in price_history.items() if len(_returns(p)) >= 2]
    if not tickers:
        return {"status": "unavailable", "reason": "At least three returns per asset are required."}
    series = {t: _returns(price_history[t]) for t in tickers}
    n = min(map(len, series.values()))
    series = {t: v[-n:] for t, v in series.items()}
    raw = {t: max(0.0, float((weights or {}).get(t, 1.0 / len(tickers)))) for t in tickers}
    total = sum(raw.values())
    if total <= 0:
        return {"status": "unavailable", "reason": "Portfolio weights sum to zero."}
    w = {t: v / total for t, v in raw.items()}
    daily = [sum(w[t] * series[t][i] for t in tickers) for i in range(n)]
    mu, sigma = _mean(daily), _stdev(daily)
    annual_return = (1 + mu) ** periods_per_year - 1 if mu is not None and mu > -1 else None
    annual_vol = sigma * math.sqrt(periods_per_year) if sigma is not None else None
    downside = [min(0.0, x) for x in daily]
    downside_dev = math.sqrt(sum(x * x for x in downside) / len(downside)) * math.sqrt(periods_per_year)
    peak, nav, max_dd = 1.0, 1.0, 0.0
    for r in daily:
        nav *= 1 + r
        peak = max(peak, nav)
        max_dd = min(max_dd, nav / peak - 1)
    sorted_returns = sorted(daily)
    tail = [x for x in sorted_returns if x <= (_percentile(sorted_returns, 1 - confidence) or 0)]
    var = -(_percentile(daily, 1 - confidence) or 0) * math.sqrt(periods_per_year)
    cvar = -(mean(tail) if tail else 0.0) * math.sqrt(periods_per_year)
    sharpe = (annual_return - risk_free_rate) / annual_vol if annual_return is not None and annual_vol else None
    sortino = (annual_return - risk_free_rate) / downside_dev if annual_return is not None and downside_dev else None
    calmar = annual_return / abs(max_dd) if annual_return is not None and max_dd < 0 else None
    return {
        "status": "ok", "observations": n, "periods_per_year": periods_per_year,
        "weights": w, "annual_return_pct": annual_return * 100 if annual_return is not None else None,
        "annual_volatility_pct": annual_vol * 100 if annual_vol is not None else None,
        "sharpe": sharpe, "sortino": sortino, "max_drawdown_pct": max_dd * 100,
        "calmar": calmar, "historical_var_pct": var * 100, "historical_cvar_pct": cvar * 100,
        "downside_deviation_pct": downside_dev * 100,
        "method": "historical daily returns; no FX conversion, taxes, fees or forward-looking guarantee",
    }


def correlation_matrix(price_history: Mapping[str, Sequence[float]]) -> dict[str, Any]:
    tickers = list(price_history)
    returns = {t: _returns(price_history[t]) for t in tickers}
    if not tickers or min((len(v) for v in returns.values()), default=0) < 2:
        return {"status": "unavailable", "reason": "Insufficient overlapping price history."}
    n = min(map(len, returns.values()))
    data = {t: v[-n:] for t, v in returns.items()}
    matrix: dict[str, dict[str, float | None]] = {}
    for a in tickers:
        matrix[a] = {}
        for b in tickers:
            xa, xb = data[a], data[b]
            ma, mb = mean(xa), mean(xb)
            da = math.sqrt(sum((x - ma) ** 2 for x in xa))
            db = math.sqrt(sum((x - mb) ** 2 for x in xb))
            matrix[a][b] = sum((x - ma) * (y - mb) for x, y in zip(xa, xb)) / (da * db) if da and db else None
    pairs = sorted(
        ({"asset_a": a, "asset_b": b, "correlation": matrix[a][b]}
         for i, a in enumerate(tickers) for b in tickers[i + 1:] if matrix[a][b] is not None),
        key=lambda x: abs(x["correlation"]), reverse=True,
    )
    return {"status": "ok", "observations": n, "matrix": matrix, "highest_correlations": pairs[:10]}


def _project_simplex(values: Sequence[float]) -> list[float]:
    """Euclidean projection onto non-negative weights summing to one."""
    ordered = sorted(values, reverse=True)
    cumulative, rho = 0.0, 0
    for i, value in enumerate(ordered, 1):
        cumulative += value
        if value - (cumulative - 1.0) / i > 0:
            rho = i
    theta = (sum(ordered[:rho]) - 1.0) / rho if rho else 0.0
    projected = [max(0.0, x - theta) for x in values]
    total = sum(projected)
    return [x / total for x in projected] if total else [1.0 / len(values)] * len(values)


def optimize_portfolio(
    price_history: Mapping[str, Sequence[float]],
    objective: str = "max_sharpe",
    risk_free_rate: float = 0.0,
    max_weight: float = 1.0,
    iterations: int = 2500,
    learning_rate: float = 0.02,
) -> dict[str, Any]:
    """Long-only projected-gradient optimizer; uses historical daily returns."""
    names = list(price_history)
    data = {t: _returns(price_history[t]) for t in names}
    if len(names) < 2 or min((len(v) for v in data.values()), default=0) < 3:
        return {"status": "unavailable", "reason": "At least two assets and four prices each are required."}
    n = min(map(len, data.values()))
    x = [data[t][-n:] for t in names]
    mus = [mean(v) for v in x]
    cov = [[sum((a - mus[i]) * (b - mus[j]) for a, b in zip(x[i], x[j])) / (n - 1)
            for j in range(len(names))] for i in range(len(names))]
    w = [1.0 / len(names)] * len(names)
    obj = objective.lower()
    if obj not in {"max_sharpe", "min_volatility", "risk_parity"}:
        raise ValueError("objective must be max_sharpe, min_volatility or risk_parity")
    for step in range(max(1, iterations)):
        cw = [sum(cov[i][j] * w[j] for j in range(len(names))) for i in range(len(names))]
        variance = max(1e-12, sum(w[i] * cw[i] for i in range(len(names))))
        if obj == "risk_parity":
            contributions = [max(1e-12, w[i] * cw[i]) for i in range(len(names))]
            target = variance / len(names)
            grad = [math.log(contributions[i] / target) for i in range(len(names))]
        elif obj == "min_volatility":
            grad = [cw[i] for i in range(len(names))]
        else:
            mu = sum(w[i] * mus[i] for i in range(len(names))) - risk_free_rate / 252
            vol = math.sqrt(variance)
            grad = [-(mus[i] - risk_free_rate / 252) / vol + mu * cw[i] / (vol ** 3)
                    for i in range(len(names))]
        rate = learning_rate / math.sqrt(1 + step / 100)
        w = _project_simplex([w[i] - rate * grad[i] for i in range(len(names))])
        if max_weight < 1:
            capped = [min(max_weight, z) for z in w]
            remainder = 1 - sum(capped)
            free = [i for i, z in enumerate(capped) if z < max_weight]
            if not free and remainder > 1e-8:
                return {"status": "unavailable", "reason": "max_weight is infeasible for this asset count."}
            while remainder > 1e-10 and free:
                share = remainder / len(free)
                for i in free:
                    add = min(share, max_weight - capped[i])
                    capped[i] += add
                    remainder -= add
                free = [i for i in free if capped[i] < max_weight - 1e-10]
            w = capped
    weights = dict(zip(names, w))
    return {"status": "ok", "objective": obj, "weights": weights,
            "assumptions": "Long-only, fully invested, historical covariance; optimizer is not a forecast."}


def monte_carlo_projection(
    initial_value: float, expected_annual_return: float, annual_volatility: float,
    years: int = 10, simulations: int = 5000, seed: int = 42,
) -> dict[str, Any]:
    """Geometric-Brownian-motion scenario distribution, not a prediction."""
    if initial_value < 0 or annual_volatility < 0 or years < 1 or simulations < 100:
        raise ValueError("Require non-negative value/volatility, years >= 1 and simulations >= 100.")
    rng = random.Random(seed)
    finals = []
    drift = expected_annual_return - 0.5 * annual_volatility ** 2
    for _ in range(simulations):
        value = initial_value
        for _year in range(years):
            value *= math.exp(drift + annual_volatility * rng.gauss(0, 1))
        finals.append(value)
    return {"status": "ok", "initial_value": initial_value, "years": years, "simulations": simulations,
            "seed": seed, "p05": _percentile(finals, .05), "p25": _percentile(finals, .25),
            "median": _percentile(finals, .50), "p75": _percentile(finals, .75),
            "p95": _percentile(finals, .95), "probability_loss_pct": sum(x < initial_value for x in finals) / simulations * 100,
            "method": "annual geometric Brownian motion; user-supplied return/volatility assumptions; not a forecast"}


def backtest_buy_and_hold(
    prices: Sequence[float], initial_cash: float = 10000.0,
    fee_bps: float = 5.0, slippage_bps: float = 5.0,
    dividend_per_share: float = 0.0,
) -> dict[str, Any]:
    """Transparent single-asset buy-and-hold baseline with entry/exit friction."""
    p = _clean(prices)
    if len(p) < 2 or min(p) <= 0 or initial_cash <= 0:
        return {"status": "unavailable", "reason": "Need at least two positive prices and positive cash."}
    friction = (fee_bps + slippage_bps) / 10000
    entry = p[0] * (1 + friction)
    shares = initial_cash / entry
    gross = shares * p[-1] + shares * max(0.0, dividend_per_share)
    net = gross * (1 - friction)
    return {"status": "ok", "initial_cash": initial_cash, "final_value": net,
            "total_return_pct": (net / initial_cash - 1) * 100,
            "buy_and_hold": True, "shares": shares, "fees_and_slippage_bps_per_side": fee_bps + slippage_bps,
            "dividend_per_share_assumption": dividend_per_share,
            "warning": "No reinvestment, taxes, splits, delistings, survivorship or look-ahead adjustment."}


def factor_exposure(
    asset_returns: Sequence[float], factor_returns: Mapping[str, Sequence[float]],
) -> dict[str, Any]:
    """Single-factor OLS beta and correlation estimates using aligned observations."""
    y = _clean(asset_returns)
    if len(y) < 3:
        return {"status": "unavailable", "reason": "At least three asset returns required."}
    output = {}
    for name, raw in factor_returns.items():
        x = _clean(raw)
        n = min(len(x), len(y))
        if n < 3:
            output[name] = {"status": "unavailable"}
            continue
        xx, yy = x[-n:], y[-n:]
        mx, my = mean(xx), mean(yy)
        var = sum((v - mx) ** 2 for v in xx)
        cov = sum((a - mx) * (b - my) for a, b in zip(xx, yy))
        beta = cov / var if var else None
        corr = cov / math.sqrt(var * sum((v - my) ** 2 for v in yy)) if var and sum((v - my) ** 2 for v in yy) else None
        output[name] = {"status": "ok", "beta": beta, "correlation": corr,
                        "alpha_per_period": my - beta * mx if beta is not None else None, "observations": n}
    return {"status": "ok", "factors": output,
            "note": "One-factor-at-a-time regressions; not a joint multifactor model."}


def market_regime(price_history: Mapping[str, Sequence[float]], benchmark: str | None = None) -> dict[str, Any]:
    """Classify trend/volatility regime from a supplied benchmark or first series."""
    key = benchmark if benchmark in price_history else next(iter(price_history), None)
    if key is None:
        return {"status": "unavailable", "reason": "No benchmark history supplied."}
    p = _clean(price_history[key])
    r = _returns(p)
    if len(p) < 200 or len(r) < 30:
        return {"status": "unavailable", "reason": "Need 200 prices for long-term trend and 30 returns for volatility."}
    short_vol = stdev(r[-30:]) * math.sqrt(252)
    long_vol = stdev(r[-252:]) * math.sqrt(252) if len(r) >= 252 else stdev(r) * math.sqrt(252)
    trend = "bull" if p[-1] > mean(p[-200:]) else "bear"
    volatility = "high_volatility" if short_vol > long_vol * 1.25 else ("low_volatility" if short_vol < long_vol * .8 else "normal_volatility")
    return {"status": "ok", "benchmark": key, "trend": trend, "volatility_regime": volatility,
            "annualized_short_vol_pct": short_vol * 100, "annualized_reference_vol_pct": long_vol * 100,
            "label": f"{trend}_{volatility}", "method": "price trend and realized volatility; heuristic classification"}


def dividend_sustainability(
    dividend_per_share: float, eps: float | None = None, fcf: float | None = None,
    shares: float | None = None, net_debt: float | None = None,
) -> dict[str, Any]:
    annual_dividend = max(0.0, float(dividend_per_share))
    payout = annual_dividend / eps * 100 if eps and eps > 0 else None
    fcf_per_share = fcf / shares if fcf is not None and shares and shares > 0 else None
    fcf_cover = fcf_per_share / annual_dividend if fcf_per_share is not None and annual_dividend > 0 else None
    if payout is None and fcf_cover is None:
        grade = "insufficient_data"
    elif (payout is not None and payout > 100) or (fcf_cover is not None and fcf_cover < 1):
        grade = "stretched"
    elif (payout is None or payout <= 75) and (fcf_cover is None or fcf_cover >= 1.5):
        grade = "strong"
    else:
        grade = "watch"
    return {"status": "ok", "annual_dividend_per_share": annual_dividend, "eps_payout_pct": payout,
            "fcf_per_share": fcf_per_share, "fcf_coverage_multiple": fcf_cover,
            "net_debt": net_debt, "assessment": grade,
            "warning": "One-year accounting inputs can be cyclical; inspect multi-year cash flow and debt maturities."}


def dcf_sensitivity(
    free_cash_flow: float, shares: float, net_cash: float = 0.0,
    growth_rates: Sequence[float] = (-.02, .03, .08, .13),
    discount_rates: Sequence[float] = (.08, .09, .10, .11, .12),
    terminal_growth: float = .02, years: int = 5,
) -> dict[str, Any]:
    if free_cash_flow <= 0 or shares <= 0 or years < 1:
        raise ValueError("Positive free cash flow, shares and years are required.")
    grid = {}
    for growth in growth_rates:
        row = {}
        for discount in discount_rates:
            if discount <= terminal_growth:
                row[str(discount)] = None
                continue
            flows = [free_cash_flow * (1 + growth) ** y for y in range(1, years + 1)]
            pv = sum(cf / (1 + discount) ** y for y, cf in enumerate(flows, 1))
            terminal = flows[-1] * (1 + terminal_growth) / (discount - terminal_growth)
            row[str(discount)] = (pv + terminal / (1 + discount) ** years + net_cash) / shares
        grid[str(growth)] = row
    return {"status": "ok", "per_share_value": grid,
            "assumptions": {"terminal_growth": terminal_growth, "years": years, "net_cash": net_cash},
            "warning": "Sensitivity grid, not a price target; small assumption changes can materially alter DCF."}


def earnings_surprise(actual: float, estimate: float, metric: str = "EPS") -> dict[str, Any]:
    surprise = actual - estimate
    pct = surprise / abs(estimate) * 100 if estimate else None
    return {"metric": metric, "actual": actual, "estimate": estimate, "surprise": surprise,
            "surprise_pct": pct, "direction": "beat" if surprise > 0 else ("miss" if surprise < 0 else "inline"),
            "note": "Estimate source and timestamp must be retained by the caller."}


def financial_distress_score(
    current_assets: float | None, current_liabilities: float | None,
    total_debt: float | None, cash: float | None, ebit: float | None,
    interest_expense: float | None, retained_earnings: float | None = None,
    total_assets: float | None = None, market_cap: float | None = None,
    revenue: float | None = None, total_liabilities: float | None = None,
) -> dict[str, Any]:
    current_ratio = current_assets / current_liabilities if current_assets is not None and current_liabilities and current_liabilities > 0 else None
    cash_debt = cash / total_debt if cash is not None and total_debt and total_debt > 0 else None
    interest_cover = ebit / interest_expense if ebit is not None and interest_expense and interest_expense > 0 else None
    working_capital_assets = (current_assets - current_liabilities) / total_assets if current_assets is not None and current_liabilities is not None and total_assets and total_assets > 0 else None
    retained_assets = retained_earnings / total_assets if retained_earnings is not None and total_assets and total_assets > 0 else None
    ebit_assets = ebit / total_assets if ebit is not None and total_assets and total_assets > 0 else None
    debt_assets = total_debt / total_assets if total_debt is not None and total_assets and total_assets > 0 else None
    sales_assets = revenue / total_assets if revenue is not None and total_assets and total_assets > 0 else None
    z = None
    if all(v is not None for v in (working_capital_assets, retained_assets, ebit_assets, sales_assets)) and market_cap is not None and total_liabilities and total_liabilities > 0:
        z = 1.2 * working_capital_assets + 1.4 * retained_assets + 3.3 * ebit_assets + .6 * (market_cap / total_liabilities) + sales_assets
    flags = []
    if current_ratio is not None and current_ratio < 1: flags.append("current_ratio_below_1")
    if cash_debt is not None and cash_debt < .2: flags.append("cash_low_vs_debt")
    if interest_cover is not None and interest_cover < 1.5: flags.append("weak_interest_coverage")
    if ebit is not None and ebit < 0: flags.append("negative_ebit")
    return {"status": "ok", "current_ratio": current_ratio, "cash_to_debt": cash_debt,
            "interest_coverage": interest_cover, "altman_z_proxy": z, "risk_flags": flags,
            "warning": "Altman-style proxy; not the original model for every issuer type. Missing data is not a clean bill of health."}


def belgian_investment_taxes(
    trade_value_eur: float, instrument_type: str = "stock",
    tob_rate: float | None = None, tob_cap_eur: float | None = None,
    dividend_gross_eur: float = 0.0, withholding_rate: float = .30,
    annual_fund_tax_rate: float | None = None,
) -> dict[str, Any]:
    """Scenario calculator; rates are explicit inputs and are not tax advice."""
    if trade_value_eur < 0 or dividend_gross_eur < 0:
        raise ValueError("Amounts must be non-negative.")
    rate = tob_rate
    tob = trade_value_eur * rate if rate is not None else None
    if tob is not None and tob_cap_eur is not None:
        tob = min(tob, tob_cap_eur)
    withholding = dividend_gross_eur * withholding_rate
    annual_fund_tax = trade_value_eur * annual_fund_tax_rate if annual_fund_tax_rate is not None else None
    return {"currency": "EUR", "instrument_type": instrument_type, "trade_value_eur": trade_value_eur,
            "tob_rate_input": rate, "estimated_tob_eur": tob, "gross_dividend_eur": dividend_gross_eur,
            "withholding_rate_input": withholding_rate, "estimated_withholding_eur": withholding,
            "net_dividend_eur": dividend_gross_eur - withholding, "annual_fund_tax_eur": annual_fund_tax,
            "disclaimer": "Illustrative configurable estimates only. Verify current Belgian TOB, exemptions, caps, fund classification, Reynders tax and personal circumstances with FPS Finance or a qualified adviser."}


def fair_value_consensus(values: Mapping[str, float], current_price: float | None = None) -> dict[str, Any]:
    valid = {k: float(v) for k, v in values.items() if v is not None and float(v) > 0 and math.isfinite(float(v))}
    if not valid:
        return {"status": "unavailable", "reason": "No positive fair-value estimates supplied."}
    center = median(valid.values())
    return {"status": "ok", "median_fair_value": center, "mean_fair_value": mean(valid.values()),
            "low_estimate": min(valid.values()), "high_estimate": max(valid.values()),
            "estimate_count": len(valid), "estimates": valid,
            "upside_pct": (center / current_price - 1) * 100 if current_price and current_price > 0 else None,
            "warning": "Consensus is only as reliable as its independent inputs; do not count correlated models as independent evidence."}


def generate_alerts(
    risk: Mapping[str, Any] | None = None, dividends: Mapping[str, Any] | None = None,
    valuation: Mapping[str, Any] | None = None, data_quality: Sequence[str] = (),
) -> list[dict[str, str]]:
    alerts: list[dict[str, str]] = []
    if risk and risk.get("max_drawdown_pct") is not None and risk["max_drawdown_pct"] <= -20:
        alerts.append({"severity": "high", "type": "drawdown", "message": "Portfolio drawdown has reached 20% or more."})
    if risk and risk.get("historical_cvar_pct") is not None and risk["historical_cvar_pct"] >= 25:
        alerts.append({"severity": "high", "type": "tail_risk", "message": "Historical CVaR exceeds 25% annualized."})
    if dividends and dividends.get("assessment") in {"stretched", "watch"}:
        alerts.append({"severity": "medium", "type": "dividend", "message": "Dividend coverage requires review."})
    if valuation and valuation.get("upside_pct") is not None and valuation["upside_pct"] < -20:
        alerts.append({"severity": "medium", "type": "valuation", "message": "Current price is more than 20% above supplied fair value."})
    if data_quality:
        alerts.append({"severity": "info", "type": "data_quality", "message": f"{len(data_quality)} data-quality warning(s) need review."})
    return alerts


def normalize_insider_transactions(records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Normalize caller-supplied SEC Form 4-like records; no filing fetch is performed."""
    rows = []
    for r in records:
        try:
            shares = float(r.get("shares", 0))
            price = float(r.get("price", 0))
        except (TypeError, ValueError):
            continue
        rows.append({"issuer": r.get("issuer"), "insider": r.get("insider"), "date": r.get("date"),
                     "transaction_code": r.get("transaction_code"), "shares": shares, "price": price,
                     "value": shares * price, "source": r.get("source", "caller_supplied")})
    buys = sum(x["value"] for x in rows if x["transaction_code"] == "P")
    sells = sum(x["value"] for x in rows if x["transaction_code"] == "S")
    return {"status": "ok", "transactions": rows, "purchase_value": buys, "sale_value": sells,
            "net_purchase_value": buys - sells, "source_status": "caller_supplied_not_live_verified"}


def options_risk_snapshot(chain: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Summarize a supplied option chain; does not infer dealer gamma or signed flow."""
    rows = []
    for item in chain:
        try:
            iv = float(item["implied_volatility"])
            oi = float(item.get("open_interest", 0))
            volume = float(item.get("volume", 0))
            if iv >= 0 and oi >= 0 and volume >= 0:
                rows.append({"iv": iv, "oi": oi, "volume": volume, "type": item.get("type", "unknown")})
        except (KeyError, TypeError, ValueError):
            continue
    if not rows:
        return {"status": "unavailable", "reason": "No valid option chain supplied."}
    calls = sum(x["volume"] for x in rows if x["type"] == "call")
    puts = sum(x["volume"] for x in rows if x["type"] == "put")
    return {"status": "ok", "contracts": len(rows), "mean_iv": mean(x["iv"] for x in rows),
            "median_iv": median(x["iv"] for x in rows), "put_call_volume_ratio": puts / calls if calls else None,
            "total_open_interest": sum(x["oi"] for x in rows), "total_volume": sum(x["volume"] for x in rows),
            "warning": "Snapshot only; IV rank needs historical IV. No dealer gamma, skew surface or signed flow inferred."}


def data_provenance(status: str, source: str | None = None, as_of: str | None = None,
                    detail: str | None = None) -> dict[str, Any]:
    allowed = {"LIVE", "CACHED", "ESTIMATED", "SYNTHETIC", "UNAVAILABLE"}
    label = status.upper()
    if label not in allowed:
        raise ValueError(f"status must be one of {sorted(allowed)}")
    return {"status": label, "source": source, "as_of": as_of, "detail": detail}


def sector_rotation(
    sector_prices: Mapping[str, Sequence[float]], benchmark_prices: Sequence[float],
    lookback: int = 63,
) -> dict[str, Any]:
    """Rank sectors by relative price momentum over a shared lookback window."""
    benchmark = _clean(benchmark_prices)
    if len(benchmark) <= lookback or benchmark[-lookback - 1] <= 0:
        return {"status": "unavailable", "reason": "Benchmark history shorter than lookback."}
    benchmark_return = benchmark[-1] / benchmark[-lookback - 1] - 1
    rows = []
    for sector, raw in sector_prices.items():
        values = _clean(raw)
        if len(values) <= lookback or values[-lookback - 1] <= 0:
            continue
        ret = values[-1] / values[-lookback - 1] - 1
        rows.append({"sector": sector, "return_pct": ret * 100,
                     "relative_return_pct": (ret - benchmark_return) * 100})
    rows.sort(key=lambda row: row["relative_return_pct"], reverse=True)
    return {"status": "ok" if rows else "unavailable", "lookback_observations": lookback,
            "benchmark_return_pct": benchmark_return * 100, "ranking": rows,
            "note": "Price momentum proxy; use total-return series and timestamped constituents for production."}


def earnings_calendar_risk(events: Sequence[Mapping[str, Any]], as_of: str | None = None) -> dict[str, Any]:
    """Normalize a supplied earnings calendar and flag near-term reporting events."""
    today = date.fromisoformat(as_of) if as_of else date.today()
    rows = []
    for event in events:
        try:
            event_date = date.fromisoformat(str(event["date"])[:10])
        except (KeyError, ValueError):
            continue
        days = (event_date - today).days
        rows.append({"ticker": event.get("ticker"), "date": event_date.isoformat(), "days_until": days,
                     "session": event.get("session", "unknown"), "source": event.get("source", "caller_supplied"),
                     "risk_window": "imminent" if 0 <= days <= 2 else ("near_term" if 0 <= days <= 7 else "later")})
    rows.sort(key=lambda row: row["date"])
    return {"status": "ok", "as_of": today.isoformat(), "events": rows,
            "source_status": "caller_supplied_not_live_verified"}


def ucits_etf_screen(records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Completeness and basic eligibility screen for user/provider-supplied ETF metadata."""
    required = ("ticker", "isin", "domicile", "ter_pct", "replication", "distribution_policy", "benchmark")
    rows = []
    for item in records:
        missing = [field for field in required if item.get(field) in (None, "")]
        try:
            ter = float(item["ter_pct"]) if item.get("ter_pct") is not None else None
        except (TypeError, ValueError):
            ter = None
            missing.append("ter_pct")
        rows.append({"ticker": item.get("ticker"), "isin": item.get("isin"),
                     "missing_fields": sorted(set(missing)), "ter_pct": ter,
                     "completeness_pct": (len(required) - len(set(missing).intersection(required))) / len(required) * 100,
                     "ucits_status": item.get("ucits_status", "unverified"),
                     "source": item.get("source", "caller_supplied"),
                     "screen_status": "complete_metadata" if not missing else "incomplete_metadata"})
    return {"status": "ok", "funds": rows,
            "warning": "Metadata completeness is not legal UCITS verification, suitability or a recommendation."}


def broker_cost_estimate(
    trade_value_eur: float, commission_eur: float = 0.0, fx_spread_pct: float = 0.0,
    custody_eur: float = 0.0, tob_eur: float = 0.0, other_fees_eur: float = 0.0,
) -> dict[str, Any]:
    """Transparent one-way broker cost comparison in EUR."""
    values = (trade_value_eur, commission_eur, custody_eur, tob_eur, other_fees_eur)
    if any(v < 0 for v in values) or fx_spread_pct < 0:
        raise ValueError("Trade value and cost inputs must be non-negative.")
    fx_cost = trade_value_eur * fx_spread_pct / 100
    total = commission_eur + fx_cost + custody_eur + tob_eur + other_fees_eur
    return {"currency": "EUR", "trade_value_eur": trade_value_eur, "commission_eur": commission_eur,
            "fx_spread_cost_eur": fx_cost, "custody_eur": custody_eur, "tob_eur": tob_eur,
            "other_fees_eur": other_fees_eur, "total_cost_eur": total,
            "cost_pct_of_trade": total / trade_value_eur * 100 if trade_value_eur else None,
            "assumption": "One-way estimate; enter round-trip, exchange, connectivity and recurring fees separately."}


def eur_portfolio_report(
    positions: Sequence[Mapping[str, Any]], fx_to_eur: Mapping[str, float],
) -> dict[str, Any]:
    """Convert position values to EUR only when an explicit currency FX rate is supplied."""
    rows, total, missing = [], 0.0, []
    for position in positions:
        currency = str(position.get("currency") or "").upper()
        value = position.get("market_value")
        rate = 1.0 if currency == "EUR" else fx_to_eur.get(currency)
        if value is None or rate is None or rate <= 0:
            missing.append(position.get("ticker", "unknown"))
            eur_value = None
        else:
            eur_value = float(value) * float(rate)
            total += eur_value
        rows.append({"ticker": position.get("ticker"), "currency": currency,
                     "market_value": value, "fx_to_eur": rate, "market_value_eur": eur_value})
    for row in rows:
        row["weight_pct"] = row["market_value_eur"] / total * 100 if total and row["market_value_eur"] is not None else None
    return {"status": "partial" if missing else "ok", "currency": "EUR", "total_eur": total,
            "positions": rows, "missing_fx_or_values": missing,
            "warning": "FX rates must be supplied with source and timestamp by the caller."}


def institutional_holding_changes(
    previous: Sequence[Mapping[str, Any]], current: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Compare caller-supplied 13F-style holdings by manager and issuer."""
    def index(rows):
        result = {}
        for row in rows:
            key = (str(row.get("manager")), str(row.get("issuer")))
            try:
                result[key] = float(row.get("shares", 0))
            except (TypeError, ValueError):
                continue
        return result
    old, new = index(previous), index(current)
    changes = []
    for key in sorted(set(old) | set(new)):
        before, after = old.get(key, 0.0), new.get(key, 0.0)
        changes.append({"manager": key[0], "issuer": key[1], "previous_shares": before,
                        "current_shares": after, "change_shares": after - before,
                        "change_pct": (after / before - 1) * 100 if before else None,
                        "change_type": "new" if before == 0 and after > 0 else ("exited" if after == 0 and before > 0 else "increased" if after > before else "reduced" if after < before else "unchanged")})
    return {"status": "ok", "holdings": changes,
            "source_status": "caller_supplied_delayed_filings_not_live_flow"}


def insider_sentiment(records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Aggregate normalized Form 4 purchase/sale values without treating grants as buys."""
    normalized = normalize_insider_transactions(records)
    buys, sells = normalized["purchase_value"], normalized["sale_value"]
    denominator = buys + sells
    score = (buys - sells) / denominator if denominator else None
    return {"status": "ok", "purchase_value": buys, "sale_value": sells,
            "net_purchase_value": buys - sells, "sentiment_score": score,
            "transaction_count": len(normalized["transactions"]),
            "source_status": normalized["source_status"],
            "note": "Only transaction codes P and S count; filing amendments, indirect ownership and 10b5-1 plans need separate review."}


def supply_chain_graph(records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Build a disclosed relationship edge list; never infer undisclosed dependencies."""
    edges = []
    for item in records:
        supplier, customer = item.get("supplier"), item.get("customer")
        if not supplier or not customer:
            continue
        edges.append({"supplier": supplier, "customer": customer,
                      "relationship": item.get("relationship", "disclosed"),
                      "confidence": item.get("confidence", "unrated"),
                      "disclosed_at": item.get("disclosed_at"),
                      "source_url": item.get("source_url"),
                      "source_status": item.get("source_status", "caller_supplied")})
    return {"status": "ok", "edges": edges, "edge_count": len(edges),
            "warning": "Only supplied disclosed relationships are represented; graph completeness is unknown."}


def backtest_target_weights(
    price_history: Mapping[str, Sequence[float]], target_weights: Mapping[str, float],
    initial_cash: float = 10000.0, fee_bps: float = 5.0,
    slippage_bps: float = 5.0, rebalance_every: int = 21,
) -> dict[str, Any]:
    """Periodic target-weight backtest with turnover costs; arrays must be date-aligned."""
    names = [name for name in target_weights if name in price_history]
    if len(names) < 1 or initial_cash <= 0 or rebalance_every < 1:
        return {"status": "unavailable", "reason": "Need matching assets, positive cash and rebalance interval."}
    series = {name: _clean(price_history[name]) for name in names}
    n = min(map(len, series.values()))
    if n < 3 or any(min(values[-n:]) <= 0 for values in series.values()):
        return {"status": "unavailable", "reason": "Need at least three aligned positive prices per asset."}
    raw = [max(0.0, float(target_weights[name])) for name in names]
    if sum(raw) <= 0:
        return {"status": "unavailable", "reason": "Target weights sum to zero."}
    weights = [value / sum(raw) for value in raw]
    prices_by_asset = [series[name][-n:] for name in names]
    fee_rate = max(0.0, fee_bps + slippage_bps) / 10000
    nav, peak, max_drawdown = initial_cash, initial_cash, 0.0
    daily_returns, turnover_events, previous_weights = [], 0, list(weights)
    for day in range(1, n):
        asset_returns = [prices_by_asset[i][day] / prices_by_asset[i][day - 1] - 1 for i in range(len(names))]
        portfolio_return = sum(previous_weights[i] * asset_returns[i] for i in range(len(names)))
        nav *= 1 + portfolio_return
        if day % rebalance_every == 0 and day < n - 1:
            turnover = sum(abs(weights[i] - previous_weights[i]) for i in range(len(names))) / 2
            nav *= max(0.0, 1 - turnover * fee_rate)
            turnover_events += 1
            previous_weights = list(weights)
        daily_returns.append(nav)
        peak = max(peak, nav)
        max_drawdown = min(max_drawdown, nav / peak - 1)
    final_value = nav
    return {"status": "ok", "initial_value": initial_cash, "final_value": final_value,
            "total_return_pct": (final_value / initial_cash - 1) * 100,
            "max_drawdown_pct": max_drawdown * 100, "target_weights": dict(zip(names, weights)),
            "rebalance_events": turnover_events, "fee_bps": fee_bps, "slippage_bps": slippage_bps,
            "warning": "Simplified periodic rebalance model; excludes taxes, dividends, FX, corporate actions, cash drag and point-in-time universe bias."}


def screen_stocks(
    records: Sequence[Mapping[str, Any]], min_market_cap: float | None = None,
    max_pe: float | None = None, min_fcf_yield_pct: float | None = None,
    min_margin_of_safety_pct: float | None = None,
) -> dict[str, Any]:
    """Filter caller-supplied stock metrics; absent fields fail an active filter."""
    screened = []
    for item in records:
        checks = []
        filters = (
            ("market_cap", min_market_cap, lambda value, limit: value >= limit),
            ("pe", max_pe, lambda value, limit: value <= limit),
            ("fcf_yield_pct", min_fcf_yield_pct, lambda value, limit: value >= limit),
            ("margin_of_safety_pct", min_margin_of_safety_pct, lambda value, limit: value >= limit),
        )
        for field, threshold, predicate in filters:
            if threshold is None:
                continue
            try:
                passed = predicate(float(item[field]), threshold) if item.get(field) is not None else False
            except (TypeError, ValueError):
                passed = False
            checks.append({"filter": field, "passed": passed})
        screened.append({"ticker": item.get("ticker"), "passed": all(x["passed"] for x in checks),
                         "checks": checks, "metrics": dict(item),
                         "source_status": item.get("source_status", "caller_supplied")})
    screened.sort(key=lambda row: (not row["passed"], str(row["ticker"] or "")))
    return {"status": "ok", "results": screened, "match_count": sum(x["passed"] for x in screened),
            "warning": "Screening depends on caller-supplied definitions, currencies, periods and data quality."}


def rank_watchlist(records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Rank watchlist records on transparent supplied valuation/quality/momentum fields."""
    ranked = []
    for item in records:
        components = []
        for field, direction in (("margin_of_safety_pct", 1), ("roe_pct", 1),
                                 ("revenue_growth_yoy_pct", 1), ("drawdown_from_52w_high_pct", -1)):
            try:
                value = float(item[field])
                if math.isfinite(value):
                    components.append(value * direction)
            except (KeyError, TypeError, ValueError):
                continue
        score = mean(components) if components else None
        ranked.append({"ticker": item.get("ticker"), "score": score,
                       "observed_components": len(components),
                       "source_status": item.get("source_status", "caller_supplied")})
    ranked.sort(key=lambda row: row["score"] if row["score"] is not None else float("-inf"), reverse=True)
    return {"status": "ok", "ranking": ranked,
            "note": "Equal-weighted raw-metric heuristic, not a calibrated or risk-adjusted investment score."}
