"""NBB.Stat SDMX CSV adapter.

Use the API URL copied from NBB.Stat's 'API queries' panel. This avoids
hard-coding dataset-specific dimension codes that can change by table.
"""
from __future__ import annotations

import csv
import io
import hashlib
from datetime import datetime, timezone
from urllib.parse import urlparse
from .base import get_bytes

_ALLOWED_HOSTS = {"stat.nbb.be", "nsidisseminate-stat.nbb.be"}


def fetch_sdmx_csv(url: str, *, ttl: int = 86400) -> list[dict]:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in _ALLOWED_HOSTS:
        raise ValueError("NBB URL must be an HTTPS API URL from stat.nbb.be or nsidisseminate-stat.nbb.be")
    body = get_bytes(url, cache_key="nbb-" + hashlib.sha256(url.encode("utf-8")).hexdigest(), ttl=ttl, accept="text/csv,application/vnd.sdmx.data+csv,application/json")
    text = body.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise RuntimeError("NBB response is not a CSV dataset; copy the CSV API query URL from NBB.Stat")
    normalized = {name.upper(): name for name in reader.fieldnames}
    period_col = next((normalized[k] for k in ("TIME_PERIOD", "TIME", "PERIOD") if k in normalized), None)
    value_col = next((normalized[k] for k in ("OBS_VALUE", "VALUE") if k in normalized), None)
    if not period_col or not value_col:
        raise RuntimeError(f"NBB CSV lacks TIME_PERIOD/OBS_VALUE columns; received {reader.fieldnames}")
    rows = []
    for raw in reader:
        value_text = (raw.get(value_col) or "").strip()
        period = (raw.get(period_col) or "").strip()
        if not value_text or not period:
            continue
        try:
            value = float(value_text)
        except ValueError:
            continue
        dimensions = {k: v for k, v in raw.items() if k not in {period_col, value_col}}
        series_dimensions = [f"{k}={v}" for k, v in dimensions.items() if k not in {"DATAFLOW", "OBS_STATUS", "DECIMALS"}]
        decimals_text = raw.get(normalized.get("DECIMALS", ""), "")
        rows.append({
            "source": "National Bank of Belgium (NBB.Stat)",
            "dataset": "NBB.Stat SDMX",
            "series": "|".join(series_dimensions),
            "period": period,
            "value": value,
            "unit": raw.get(normalized.get("UNIT_MEASURE", ""), "") or None,
            "currency": raw.get(normalized.get("CURRENCY", ""), "") or None,
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "status": raw.get(normalized.get("OBS_STATUS", ""), "") or None,
            "source_url": url,
            "decimals": int(decimals_text) if decimals_text.isdigit() else None,
            "dimensions": dimensions,
        })
    return rows

# Verified query copied from the official NBB.Stat Data Explorer (DF_MIR).
# It selects the NBB's MFI interest-rate dataset slice for sector code 2250;
# all SDMX dimension codes are retained in each observation for interpretation.
PRESETS = {
    "mfi-interest-rates": {
        "title": "NBB MFI new-business interest rates (DF_MIR; sector code 2250)",
        "url": "https://nsidisseminate-stat.nbb.be/rest/data/BE2,DF_MIR,1.0/M..2250.L20+L21+L22+L23..Z.Z?startPeriod=2020-01&dimensionAtObservation=AllDimensions",
        "frequency": "Monthly",
        "note": "Filtered to MIR_ITEM=R_N (new-business interest-rate observations); raw instrument and maturity codes are preserved.",
    },
}


def list_presets() -> dict:
    return {name: {k: v for k, v in details.items() if k != "url"}
            for name, details in PRESETS.items()}


def fetch_preset(name: str, *, start_period: str | None = None) -> list[dict]:
    if name not in PRESETS:
        raise ValueError(f"Unknown NBB preset {name!r}; available: {', '.join(PRESETS)}")
    url = PRESETS[name]["url"]
    if start_period:
        import re
        if not re.fullmatch(r"\d{4}(-\d{2})?", start_period):
            raise ValueError("start_period must be YYYY or YYYY-MM")
        import re as _re
        url = _re.sub(r"startPeriod=[^&]+", f"startPeriod={start_period}", url)
    rows = fetch_sdmx_csv(url)
    if name == "mfi-interest-rates":
        rows = [row for row in rows if row.get("dimensions", {}).get("MIR_ITEM") == "R_N"]
    for row in rows:
        row["preset"] = name
        row["preset_title"] = PRESETS[name]["title"]
        row["frequency"] = PRESETS[name]["frequency"]
        row["interpretation_note"] = PRESETS[name]["note"]
    return rows
