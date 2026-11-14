"""Small Belgian/European macro snapshot assembled from free official sources."""
from __future__ import annotations
from datetime import date, datetime, timezone
from .ecb import euro_reference_rates
from .eurostat import fetch_dataset
from .worldbank import fetch_indicator
from .treasury import latest_debt_snapshot


def macro_snapshot(*, country: str = "BE", currency: str = "USD") -> dict:
    fx = euro_reference_rates(currency, last_n=3)
    filters = {"geo": country.upper(), "coicop": "CP00"}
    hicp_index = sorted(fetch_dataset("prc_hicp_midx", filters={**filters, "unit": "I15"}),
                        key=lambda row: row["period"])
    hicp_rate = sorted(fetch_dataset("prc_hicp_manr", filters={**filters, "unit": "RCH_A"}),
                       key=lambda row: row["period"])
    latest_index = hicp_index[-1] if hicp_index else None
    latest_rate = hicp_rate[-1] if hicp_rate else None
    prior = None
    if latest_index:
        try:
            previous_period = str(int(latest_index["period"][:4]) - 1) + latest_index["period"][4:]
            prior = next((row for row in hicp_index if row["period"] == previous_period), None)
        except ValueError:
            pass
    derived_yoy = ((latest_index["value"] / prior["value"] - 1) * 100
                   if latest_index and prior and prior["value"] else None)
    age_days = None
    if latest_rate:
        try:
            year, month = map(int, latest_rate["period"].split("-")[:2])
            # Age is measured from the first day of the observation month.
            age_days = (date.today() - date(year, month, 1)).days
        except (ValueError, TypeError):
            pass
    stale = age_days is not None and age_days > 90
    quality = ["Macro indicators are contextual evidence, not company forecasts."]
    if stale:
        quality.append(f"Eurostat HICP is stale: latest observation is {latest_rate['period']} ({age_days} days old).")
    world_bank = {}
    # Annual World Bank indicators add a long-run global/Belgian backdrop.
    for code, label in (("NY.GDP.MKTP.KD.ZG", "GDP annual growth (%)"),
                        ("SL.UEM.TOTL.ZS", "Unemployment (% of labour force)"),
                        ("BN.CAB.XOKA.GD.ZS", "Current account balance (% of GDP)")):
        try:
            series = fetch_indicator(country, code)
            latest = series[-1] if series else None
            latest_year = int(latest["period"]) if latest and str(latest["period"]).isdigit() else None
            age_years = (date.today().year - latest_year) if latest_year else None
            world_bank[code] = {"label": label, "latest": latest, "age_years": age_years,
                                "stale_over_3_years": age_years is not None and age_years > 3,
                                "note": "Annual series; publication can lag the current year."}
        except Exception as exc:
            world_bank[code] = {"label": label, "latest": None, "error": str(exc)}
    try:
        us_treasury_debt = latest_debt_snapshot()
    except Exception as exc:
        us_treasury_debt = {"status": "unavailable", "error": str(exc)}
    return {
        "country": country.upper(),
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "exchange_rate": fx[-1] if fx else None,
        "hicp": {
            "dataset": "prc_hicp_manr", "measure": "All-items HICP annual rate of change",
            "latest": latest_rate, "age_days": age_days, "stale_over_90_days": stale,
            "index_crosscheck": latest_index, "derived_yoy_pct_from_index": derived_yoy,
        },
        "world_bank": world_bank,
        "us_treasury_debt": us_treasury_debt,
        "sources": ["ECB Data Portal", "Eurostat", "World Bank", "U.S. Treasury Fiscal Data"],
        "data_quality": quality,
    }
