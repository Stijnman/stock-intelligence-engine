"""Join price, SEC fundamentals, DCF, dividends and technical evidence."""
from typing import Any
from .providers import quote_and_history, sec_financials
from .technical import analyze_history
from .valuation import scenario_valuation, margin_of_safety
from .dividends import analyze_dividends

def analyze_stock(ticker: str) -> dict[str, Any]:
    market = quote_and_history(ticker)
    result: dict[str, Any] = {"ticker": ticker.upper(),
        "market": {k: v for k, v in market.items() if k not in {"history", "dividends"}},
        "technical": analyze_history(market["history"]), "sources": [market["source"]], "data_quality": []}
    try:
        fundamentals = sec_financials(ticker)
        result["fundamentals"] = fundamentals
        result["sources"].append(fundamentals["source"])
        latest = fundamentals.get("latest", {})
        fcf, shares = latest.get("free_cash_flow"), latest.get("diluted_shares")
        net_cash = (latest.get("cash") or 0) - (latest.get("debt") or 0)
        if fcf and fcf > 0 and shares and shares > 0:
            result["valuation"] = scenario_valuation(fcf, shares, net_cash)
            if market.get("price"):
                for case in result["valuation"].values():
                    case["margin_of_safety_pct"] = margin_of_safety(case["intrinsic_value_per_share"], market["price"])
        else:
            result["valuation"] = {"status": "unavailable", "reason": "SEC facts lack positive annual FCF and/or diluted shares."}
            result["data_quality"].append("DCF unavailable: missing or non-positive FCF/shares.")
        result["dividends"] = analyze_dividends(market["dividends"], market.get("price"), latest.get("net_income"), shares)
    except Exception as exc:
        result["fundamentals"] = {"status": "unavailable", "reason": str(exc)}
        result["valuation"] = {"status": "unavailable", "reason": "Fundamentals unavailable; DCF not calculated."}
        result["dividends"] = analyze_dividends(market["dividends"], market.get("price"))
        result["data_quality"].append(f"SEC fundamentals unavailable: {exc}")
    result["data_quality"] += ["Yahoo chart prices can be delayed and are not guaranteed realtime.",
        "SEC CompanyFacts is for SEC reporting issuers; European issuer coverage may be incomplete."]
    result["conclusion"] = "Research snapshot only; verify filing dates, currency, assumptions and risks."
    return result
