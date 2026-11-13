"""Read-only CSV portfolio valuation; never writes trades."""
from __future__ import annotations
import csv
from pathlib import Path
from typing import Any
from .providers import quote_and_history


def analyze_portfolio(csv_path: str | Path) -> dict[str, Any]:
    rows = []
    with Path(csv_path).open(newline="", encoding="utf-8-sig") as handle:
        for item in csv.DictReader(handle):
            ticker = (item.get("ticker") or "").strip().upper()
            if not ticker: continue
            shares = float(item.get("shares") or 0)
            average_cost = float(item["average_cost"]) if item.get("average_cost") else None
            quote = quote_and_history(ticker, range_="1y")
            price = quote.get("price")
            value = shares * price if price is not None else None
            cost = shares * average_cost if average_cost is not None else None
            rows.append({"ticker": ticker, "shares": shares, "average_cost": average_cost,
                         "price": price, "currency": quote.get("currency"), "market_value": value,
                         "cost_basis": cost, "unrealized_pnl": value - cost if value is not None and cost is not None else None})
    totals: dict[str, float] = {}
    for row in rows:
        if row["market_value"] is not None:
            currency = row["currency"] or "UNKNOWN"
            totals[currency] = totals.get(currency, 0.0) + row["market_value"]
    for row in rows:
        currency = row["currency"] or "UNKNOWN"
        total = totals.get(currency, 0.0)
        row["weight_within_currency_pct"] = row["market_value"] / total * 100 if total and row["market_value"] is not None else None
    return {"positions": rows, "totals_by_currency": totals,
            "warnings": ["Currencies are not converted or aggregated across FX.", "CSV valuations use indicative Yahoo chart prices; verify with your broker.",
                         "Taxes, fees, accrued income and corporate actions may not be included."]}
