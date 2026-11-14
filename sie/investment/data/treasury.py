"""U.S. Treasury Fiscal Data API adapter (public, no API key)."""
from __future__ import annotations

from urllib.parse import urlencode

from .base import get_json

BASE_URL = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service"


def fetch_debt_to_penny(*, start_date: str | None = None, limit: int = 100) -> list[dict]:
    """Fetch daily U.S. federal debt outstanding, newest first."""
    from datetime import date
    if not 1 <= limit <= 10000:
        raise ValueError("limit must be between 1 and 10000")
    if start_date:
        try:
            date.fromisoformat(start_date)
        except ValueError as exc:
            raise ValueError("start_date must be YYYY-MM-DD") from exc
    params = {
        "fields": "record_date,debt_held_public_amt,intragov_hold_amt,tot_pub_debt_out_amt",
        "sort": "-record_date",
        "page[size]": str(limit),
    }
    if start_date:
        params["filter"] = f"record_date:gte:{start_date}"
    url = f"{BASE_URL}/v2/accounting/od/debt_to_penny?{urlencode(params)}"
    payload = get_json(url, cache_key=f"treasury-debt-{start_date}-{limit}", ttl=6 * 3600)
    rows = []
    for item in payload.get("data", []):
        def amount(key):
            raw = item.get(key)
            try:
                return float(raw) if raw not in (None, "") else None
            except (TypeError, ValueError):
                return None
        rows.append({
            "source": "U.S. Treasury Fiscal Data",
            "dataset": "Debt to the Penny",
            "period": item.get("record_date"),
            "debt_held_public_usd": amount("debt_held_public_amt"),
            "intragovernmental_holdings_usd": amount("intragov_hold_amt"),
            "total_public_debt_usd": amount("tot_pub_debt_out_amt"),
            "currency": "USD",
            "source_url": f"{BASE_URL}/v2/accounting/od/debt_to_penny",
            "update_frequency": "Daily business-day series; typically previous business day.",
        })
    return rows


def latest_debt_snapshot() -> dict:
    rows = fetch_debt_to_penny(limit=1)
    if not rows:
        return {"status": "unavailable", "source": "U.S. Treasury Fiscal Data"}
    return {"status": "ok", **rows[0]}
