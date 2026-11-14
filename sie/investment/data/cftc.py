"""CFTC Commitments of Traders adapter (public Socrata API, no token normally required)."""
from __future__ import annotations

from urllib.parse import urlencode

from .base import get_json

BASE_URL = "https://publicreporting.cftc.gov/resource"
DATASETS = {
    "legacy_futures_only": "6dca-aqww",
    "legacy_all": "srt6-5q2f",
}


def fetch_legacy_futures_only(
    *, commodity: str | None = None, start_date: str | None = None,
    limit: int = 500, dataset: str = "legacy_futures_only",
) -> list[dict]:
    """Fetch CFTC Legacy futures-only COT rows, newest first.

    COT is weekly positioning data (positions as of Tuesday, generally published Friday),
    not real-time order flow. The combined legacy dataset contains futures and options;
    this adapter defaults to futures-only to avoid accidental double counting.
    """
    if dataset not in DATASETS:
        raise ValueError(f"Unsupported CFTC dataset: {dataset}")
    if not 1 <= limit <= 50000:
        raise ValueError("limit must be between 1 and 50000")
    if start_date:
        from datetime import date
        try:
            date.fromisoformat(start_date)
        except ValueError as exc:
            raise ValueError("start_date must be YYYY-MM-DD") from exc

    where = []
    if commodity:
        safe = commodity.strip().replace("'", "''")
        if not safe:
            raise ValueError("commodity cannot be blank")
        where.append(f"upper(commodity_name) like upper('%{safe}%')")
    if start_date:
        where.append(f"report_date_as_yyyy_mm_dd >= '{start_date}T00:00:00.000'")
    params = {
        "$limit": str(limit),
        "$order": "report_date_as_yyyy_mm_dd DESC",
        "$select": ",".join((
            "id", "market_and_exchange_names", "contract_market_name",
            "commodity_name", "report_date_as_yyyy_mm_dd",
            "open_interest_all", "noncomm_positions_long_all",
            "noncomm_positions_short_all", "comm_positions_long_all",
            "comm_positions_short_all",
        )),
    }
    if where:
        params["$where"] = " AND ".join(where)
    dataset_id = DATASETS[dataset]
    url = f"{BASE_URL}/{dataset_id}.json?{urlencode(params)}"
    payload = get_json(url, cache_key=f"cftc-{dataset}-{commodity}-{start_date}-{limit}", ttl=6 * 3600)
    rows = []
    for item in payload:
        def number(key):
            value = item.get(key)
            try:
                return float(value) if value not in (None, "") else None
            except (TypeError, ValueError):
                return None

        long_noncomm = number("noncomm_positions_long_all")
        short_noncomm = number("noncomm_positions_short_all")
        long_comm = number("comm_positions_long_all")
        short_comm = number("comm_positions_short_all")
        open_interest = number("open_interest_all")
        rows.append({
            "source": "CFTC Commitments of Traders",
            "dataset": dataset,
            "report_date": str(item.get("report_date_as_yyyy_mm_dd", ""))[:10],
            "market": item.get("market_and_exchange_names"),
            "contract": item.get("contract_market_name"),
            "commodity": item.get("commodity_name"),
            "open_interest": open_interest,
            "noncommercial_long": long_noncomm,
            "noncommercial_short": short_noncomm,
            "noncommercial_net": long_noncomm - short_noncomm if long_noncomm is not None and short_noncomm is not None else None,
            "commercial_net": long_comm - short_comm if long_comm is not None and short_comm is not None else None,
            "noncommercial_net_pct_open_interest": (
                (long_noncomm - short_noncomm) / open_interest * 100
                if long_noncomm is not None and short_noncomm is not None and open_interest else None
            ),
            "source_url": f"{BASE_URL}/{dataset_id}.json",
            "publication_lag": "Weekly; positions as of Tuesday, normally published Friday.",
        })
    return rows


def positioning_summary(rows: list[dict]) -> dict:
    """Summarize weekly positioning separately per contract; never compare different contracts."""
    if not rows:
        return {"status": "unavailable", "reason": "No CFTC positioning rows supplied."}

    groups = {}
    for row in rows:
        key = row.get("market") or row.get("contract") or "unknown_contract"
        groups.setdefault(key, []).append(row)

    summaries = []
    for contract, values in sorted(groups.items()):
        ordered = sorted(values, key=lambda row: row.get("report_date", ""))
        latest = ordered[-1]
        previous = ordered[-2] if len(ordered) > 1 else None
        net = latest.get("noncommercial_net")
        prior_net = previous.get("noncommercial_net") if previous else None
        summaries.append({
            "contract": contract,
            "market": latest.get("market"),
            "commodity": latest.get("commodity"),
            "latest_report_date": latest.get("report_date"),
            "noncommercial_net": net,
            "noncommercial_net_change": net - prior_net if net is not None and prior_net is not None else None,
            "noncommercial_net_pct_open_interest": latest.get("noncommercial_net_pct_open_interest"),
            "direction": "net_long" if net is not None and net > 0 else "net_short" if net is not None and net < 0 else "flat_or_unavailable",
        })
    result = {
        "status": "ok",
        "source": "CFTC Commitments of Traders",
        "contracts": summaries,
        "warning": "Weekly positioning, not real-time buying/selling or a standalone price forecast.",
    }
    if len(summaries) == 1:
        result.update(summaries[0])
    return result
