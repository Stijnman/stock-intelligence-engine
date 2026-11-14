"""Eurostat Statistics API adapter. Free, no API key; JSON-stat 2.0 output."""
from __future__ import annotations

from datetime import datetime, timezone
from urllib.parse import urlencode

from .base import Observation, get_json

BASE_URL = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"


def _unflatten_jsonstat(payload: dict) -> list[tuple[dict[str, str], float]]:
    """Expand JSON-stat dimensions and value vector into dimension/value rows."""
    dims = payload.get("id", [])
    sizes = payload.get("size", [])
    dimension = payload.get("dimension", {})
    raw_values = payload.get("value", {})
    if isinstance(raw_values, dict):
        value_items = ((int(k), v) for k, v in raw_values.items())
    else:
        value_items = enumerate(raw_values or [])
    categories: list[list[str]] = []
    for dim in dims:
        cat = dimension.get(dim, {}).get("category", {}).get("index", {})
        if isinstance(cat, list):
            categories.append([str(x) for x in cat])
        else:
            categories.append([k for k, _ in sorted(cat.items(), key=lambda kv: kv[1])])
    output = []
    for flat_index, value in value_items:
        if value is None:
            continue
        remainder = flat_index
        coordinates = [0] * len(sizes)
        for i in range(len(sizes) - 1, -1, -1):
            coordinates[i] = remainder % sizes[i]
            remainder //= sizes[i]
        labels = {dims[i]: categories[i][coordinates[i]] for i in range(len(dims))}
        output.append((labels, float(value)))
    return output


def fetch_dataset(dataset: str, *, filters: dict[str, str] | None = None,
                  lang: str = "EN") -> list[dict]:
    """Fetch a dataset with dimension filters, e.g. {'geo':'BE','coicop':'CP00'}."""
    params = {"lang": lang}
    params.update(filters or {})
    url = f"{BASE_URL}/{dataset}?{urlencode(params)}"
    payload = get_json(url, cache_key=f"eurostat-{dataset}-{urlencode(params)}", ttl=12 * 3600)
    retrieved = datetime.now(timezone.utc).isoformat()
    observations = []
    for labels, value in _unflatten_jsonstat(payload):
        period = labels.get("time", labels.get("TIME_PERIOD", ""))
        series_labels = {k: v for k, v in labels.items() if k.lower() not in {"time", "time_period"}}
        series = "|".join(f"{k}={v}" for k, v in sorted(series_labels.items()))
        obs = Observation(
            source="Eurostat", dataset=dataset, series=series, period=period,
            value=value, unit=labels.get("unit"), retrieved_at=retrieved,
            source_url=url,
        )
        observations.append(obs.to_dict())
    return observations
