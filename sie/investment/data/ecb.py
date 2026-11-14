"""ECB Data Portal SDMX CSV adapter. No API key required."""
from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from urllib.parse import urlencode

from .base import Observation, get_bytes

BASE_URL = "https://data-api.ecb.europa.eu/service/data"


def fetch_series(flow: str, key: str, *, start: str | None = None,
                 end: str | None = None, last_n: int | None = None) -> list[dict]:
    """Fetch an ECB SDMX series, e.g. flow='EXR', key='D.USD.EUR.SP00.A'."""
    params = {"format": "csvdata"}
    if start:
        params["startPeriod"] = start
    if end:
        params["endPeriod"] = end
    if last_n:
        params["lastNObservations"] = str(int(last_n))
    url = f"{BASE_URL}/{flow}/{key}?{urlencode(params)}"
    raw = get_bytes(url, cache_key=f"ecb-{flow}-{key}-{start}-{end}-{last_n}",
                    ttl=6 * 3600, accept="text/csv")
    try:
        rows = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
        observations = []
        for row in rows:
            value = row.get("OBS_VALUE")
            if value in (None, "", "NaN"):
                continue
            obs = Observation(
                source="ECB Data Portal", dataset=flow, series=key,
                period=row.get("TIME_PERIOD", ""), value=float(value),
                unit=row.get("UNIT") or row.get("UNIT_MEASURE"),
                currency=row.get("CURRENCY"), currency_denom=row.get("CURRENCY_DENOM"),
                retrieved_at=datetime.now(timezone.utc).isoformat(),
                status=row.get("OBS_STATUS"), source_url=url,
            )
            observations.append(obs.to_dict())
        return observations
    except (UnicodeDecodeError, csv.Error, ValueError) as exc:
        raise RuntimeError(f"Could not parse ECB CSV for {flow}/{key}: {exc}") from exc


def euro_reference_rates(currency: str = "USD", *, start: str | None = None,
                         end: str | None = None, last_n: int | None = None) -> list[dict]:
    """Return ECB daily reference rate series against EUR."""
    return fetch_series("EXR", f"D.{currency.upper()}.EUR.SP00.A", start=start, end=end, last_n=last_n)


def convert_foreign_to_eur(amount: float, currency: str, rate: float) -> float:
    """Convert foreign currency to EUR where rate is foreign units per EUR."""
    code = currency.upper()
    if code == "EUR":
        return float(amount)
    if rate <= 0:
        raise ValueError("ECB exchange rate must be positive")
    return float(amount) / float(rate)
