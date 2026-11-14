"""World Bank Indicators API v2 adapter (free, no API key)."""
from __future__ import annotations

from urllib.parse import urlencode
from .base import get_json

BASE_URL = "https://api.worldbank.org/v2"


def fetch_indicator(country: str, indicator: str, *, start: int | str | None = None,
                    end: int | str | None = None, per_page: int = 20000,
                    max_pages: int = 10) -> list[dict]:
    country = country.strip().lower()
    indicator = indicator.strip()
    if not country or not indicator:
        raise ValueError("country and indicator are required")
    if not 1 <= per_page <= 20000:
        raise ValueError("per_page must be between 1 and 20000")
    params = {"format": "json", "per_page": per_page}
    if start is not None or end is not None:
        params["date"] = f"{start or ''}:{end or ''}"
    url = f"{BASE_URL}/country/{country}/indicator/{indicator}?{urlencode(params)}"
    rows: list[dict] = []
    for page in range(1, max_pages + 1):
        page_url = url + f"&page={page}"
        payload = get_json(page_url, cache_key=f"worldbank-{country}-{indicator}-{start}-{end}-p{page}", ttl=86400)
        if not isinstance(payload, list) or len(payload) < 2 or not isinstance(payload[1], list):
            raise RuntimeError(f"Unexpected World Bank response for {country}/{indicator}: {payload!r}")
        metadata, observations = payload
        for item in observations:
            value = item.get("value")
            if value is None:
                continue
            rows.append({
                "source": "World Bank",
                "dataset": "World Development Indicators",
                "series": indicator,
                "country": (item.get("country") or {}).get("id", country.upper()),
                "country_name": (item.get("country") or {}).get("value"),
                "period": str(item.get("date")),
                "value": float(value),
                "unit": item.get("unit") or None,
                "currency": None,
                "retrieved_at": None,
                "status": item.get("obs_status") or None,
                "decimals": item.get("decimal"),
                "source_url": f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}",
            })
        pages = int(metadata.get("pages", 1))
        if page >= pages:
            break
    return sorted(rows, key=lambda row: row["period"])
