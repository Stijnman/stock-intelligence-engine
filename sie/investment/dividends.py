"""Dividend yield and payout diagnostics."""
from datetime import date, timedelta
from typing import Any

def analyze_dividends(events: list[dict[str, Any]], price: float | None, net_income: float | None = None,
                      diluted_shares: float | None = None) -> dict[str, Any]:
    cutoff, trailing = date.today() - timedelta(days=365), []
    for event in events:
        try: event_date = date.fromisoformat(event["date"])
        except (KeyError, ValueError): continue
        if event_date >= cutoff: trailing.append(float(event.get("amount", 0)))
    annual = sum(trailing)
    eps = net_income / diluted_shares if net_income is not None and diluted_shares and diluted_shares > 0 else None
    payout = annual / eps * 100 if eps and eps > 0 else None
    return {"trailing_12m_dividend_per_share": annual,
            "dividend_yield_pct": annual / price * 100 if price and price > 0 else None,
            "payout_ratio_pct": payout, "event_count_12m": len(trailing),
            "quality": "needs_review" if payout is None else ("stretched" if payout > 85 else "covered_on_reported_eps"),
            "note": "Trailing distributions are not a forecast; EPS payout does not replace free-cash-flow coverage."}
