"""FRED/ALFRED observations adapter. Requires a free, user-owned FRED API key."""
from __future__ import annotations

import os
from urllib.parse import urlencode

from .base import get_json

BASE_URL = "https://api.stlouisfed.org/fred"


def fetch_series(
    series_id: str, *, start: str | None = None, end: str | None = None,
    api_key: str | None = None, limit: int = 100000,
) -> list[dict]:
    """Fetch one FRED series; key may be supplied or read from FRED_API_KEY."""
    key = api_key or os.getenv("FRED_API_KEY")
    if not key:
        raise RuntimeError("FRED_API_KEY is required. Create a free FRED account and API key.")
    series_id = series_id.strip().upper()
    if not series_id or not series_id.replace("_", "").isalnum():
        raise ValueError("Invalid FRED series_id")
    if not 1 <= limit <= 100000:
        raise ValueError("limit must be between 1 and 100000")
    params = {
        "series_id": series_id, "api_key": key, "file_type": "json",
        "sort_order": "asc", "limit": str(limit),
    }
    if start:
        params["observation_start"] = start
    if end:
        params["observation_end"] = end
    url = f"{BASE_URL}/series/observations?{urlencode(params)}"
    payload = get_json(url, cache_key=f"fred-{series_id}-{start}-{end}-{limit}", ttl=6 * 3600)
    rows = []
    for item in payload.get("observations", []):
        raw = item.get("value")
        try:
            value = float(raw) if raw not in (None, "", ".") else None
        except (TypeError, ValueError):
            value = None
        rows.append({
            "source": "FRED",
            "series": series_id,
            "period": item.get("date"),
            "value": value,
            "realtime_start": item.get("realtime_start"),
            "realtime_end": item.get("realtime_end"),
            "status": "OBSERVED" if value is not None else "MISSING",
            "source_url": f"https://fred.stlouisfed.org/series/{series_id}",
        })
    return rows
