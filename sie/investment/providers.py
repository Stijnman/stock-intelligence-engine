"""Keyless-by-default providers: Yahoo chart data and SEC CompanyFacts."""
from __future__ import annotations
import json, os, time, urllib.error, urllib.parse, urllib.request
from datetime import date
from pathlib import Path
from typing import Any
CACHE_DIR = Path(os.getenv("SIE_CACHE_DIR", Path.home() / ".cache/stock-intelligence"))
CACHE_DIR.mkdir(parents=True, exist_ok=True)
USER_AGENT = os.getenv("SEC_USER_AGENT", "StockIntelligenceEngine research; configure SEC_USER_AGENT")

def _get_json(url: str, cache_name: str, ttl: int = 3600) -> dict[str, Any]:
    path = CACHE_DIR / cache_name
    if path.exists() and time.time() - path.stat().st_mtime < ttl:
        try: return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError): pass
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Provider request failed ({url.split('/')[2]}): {exc}") from exc
    path.write_text(json.dumps(payload), encoding="utf-8")
    return payload

def yahoo_chart(ticker: str, range_: str = "5y", interval: str = "1d") -> dict[str, Any]:
    symbol = urllib.parse.quote(ticker.strip().upper(), safe="")
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={range_}&interval={interval}&events=div%2Csplits"
    data = _get_json(url, f"yahoo-{symbol}-{range_}-{interval}.json", ttl=900)
    result = (data.get("chart") or {}).get("result") or []
    if not result: raise RuntimeError(f"No Yahoo chart data for {ticker}: {(data.get('chart') or {}).get('error')}")
    return result[0]

def sec_cik_for_ticker(ticker: str) -> str:
    data = _get_json("https://www.sec.gov/files/company_tickers.json", "sec-company-tickers.json", ttl=30 * 86400)
    wanted = ticker.strip().upper()
    for item in data.values():
        if str(item.get("ticker", "")).upper() == wanted: return str(item["cik_str"]).zfill(10)
    raise RuntimeError(f"{wanted} not found in SEC ticker directory (US reporting issuers only)")

def sec_companyfacts(ticker: str) -> dict[str, Any]:
    cik = sec_cik_for_ticker(ticker)
    return _get_json(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", f"sec-companyfacts-{cik}.json", ttl=86400)

def _annual_series(facts: dict[str, Any], candidates: tuple[str, ...], *, instant: bool = False) -> dict[int, float]:
    """Select annual SEC facts without mixing quarterly/YTD durations or fiscal years."""
    usgaap = facts.get("facts", {}).get("us-gaap", {})
    for tag in candidates:
        node = usgaap.get(tag)
        if not node:
            continue
        units = node.get("units", {})
        values = units.get("USD") or units.get("shares") or []
        annual: dict[int, tuple[str, float]] = {}
        for item in values:
            if item.get("form") not in {"10-K", "20-F", "40-F"}:
                continue
            end = item.get("end", "")
            if len(end) < 4:
                continue
            start = item.get("start")
            if instant:
                # Balance-sheet facts are point-in-time observations.
                if start:
                    continue
            else:
                # Income/cash-flow facts must cover a full financial year.
                if not start:
                    continue
                try:
                    duration_days = (date.fromisoformat(end) - date.fromisoformat(start)).days
                except ValueError:
                    continue
                if not 300 <= duration_days <= 400:
                    continue
            fy = item.get("fy")
            try:
                year = int(fy) if fy is not None else int(end[:4])
                value = float(item.get("val", 0))
            except (TypeError, ValueError):
                continue
            filed = item.get("filed", "")
            if year not in annual or filed > annual[year][0]:
                annual[year] = (filed, value)
        if annual:
            return {year: value for year, (_, value) in sorted(annual.items())}
    return {}

def sec_financials(ticker: str) -> dict[str, Any]:
    facts = sec_companyfacts(ticker)
    tags = {
        "revenue": ("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet"),
        "net_income": ("NetIncomeLoss", "ProfitLoss"), "operating_income": ("OperatingIncomeLoss",),
        "gross_profit": ("GrossProfit",),
        "operating_cash_flow": ("NetCashProvidedByUsedInOperatingActivities",),
        "capex": ("PaymentsToAcquirePropertyPlantAndEquipment",),
        "cash": ("CashCashEquivalentsAndShortTermInvestments", "CashAndCashEquivalentsAtCarryingValue", "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"),
        "debt": ("LongTermDebt", "LongTermDebtAndFinanceLeaseObligations"),
        "diluted_shares": ("WeightedAverageNumberOfDilutedSharesOutstanding", "EntityCommonStockSharesOutstanding"),
        "equity": ("StockholdersEquity", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"),
        "current_assets": ("AssetsCurrent",), "current_liabilities": ("LiabilitiesCurrent",),
        "interest_expense": ("InterestExpenseNonOperating", "InterestAndDebtExpense"),
    }
    instant_fields = {"cash", "debt", "equity", "current_assets", "current_liabilities"}
    series = {key: _annual_series(facts, names, instant=key in instant_fields) for key, names in tags.items()}
    # If a consolidated debt tag is absent, add current and non-current components.
    if not series["debt"]:
        current = _annual_series(facts, ("LongTermDebtCurrent", "LongTermDebtAndFinanceLeaseObligationsCurrent"), instant=True)
        noncurrent = _annual_series(facts, ("LongTermDebtNoncurrent", "LongTermDebtAndFinanceLeaseObligationsNoncurrent"), instant=True)
        series["debt"] = {year: current.get(year, 0.0) + noncurrent.get(year, 0.0)
                          for year in sorted(set(current) | set(noncurrent))}
    years = sorted(set().union(*(set(v) for v in series.values())))
    annual = []
    for year in years[-6:]:
        row = {"year": year}
        for key, values in series.items(): row[key] = values.get(year)
        cfo, capex = row.get("operating_cash_flow"), row.get("capex")
        row["free_cash_flow"] = cfo - abs(capex) if cfo is not None and capex is not None else None
        annual.append(row)
    for i, row in enumerate(annual):
        revenue = row.get("revenue")
        row["revenue_growth_yoy_pct"] = ((revenue / annual[i-1]["revenue"]) - 1) * 100 if i and revenue and annual[i-1].get("revenue") else None
        row["gross_margin_pct"] = row["gross_profit"] / revenue * 100 if row.get("gross_profit") is not None and revenue else None
        row["operating_margin_pct"] = row["operating_income"] / revenue * 100 if row.get("operating_income") is not None and revenue else None
        row["net_margin_pct"] = row["net_income"] / revenue * 100 if row.get("net_income") is not None and revenue else None
        row["fcf_margin_pct"] = row["free_cash_flow"] / revenue * 100 if row.get("free_cash_flow") is not None and revenue else None
        previous_equity = annual[i-1].get("equity") if i else None
        average_equity = (row.get("equity") + previous_equity) / 2 if row.get("equity") is not None and previous_equity is not None else None
        row["roe_pct"] = row["net_income"] / average_equity * 100 if row.get("net_income") is not None and average_equity else None
        row["net_debt"] = (row.get("debt") - row.get("cash")) if row.get("debt") is not None and row.get("cash") is not None else None
        row["net_debt_to_fcf"] = row["net_debt"] / row["free_cash_flow"] if row.get("net_debt") is not None and row.get("free_cash_flow") else None
        row["current_ratio"] = row["current_assets"] / row["current_liabilities"] if row.get("current_assets") is not None and row.get("current_liabilities") else None
        row["interest_coverage"] = row["operating_income"] / row["interest_expense"] if row.get("operating_income") is not None and row.get("interest_expense") else None
    return {"ticker": ticker.upper(), "company": facts.get("entityName", ticker.upper()), "source": "SEC CompanyFacts",
            "annual": annual, "latest": annual[-1] if annual else {}}

def quote_and_history(ticker: str, range_: str = "5y") -> dict[str, Any]:
    raw = yahoo_chart(ticker, range_=range_)
    meta = raw.get("meta", {})
    timestamps = raw.get("timestamp") or []
    quote = (raw.get("indicators") or {}).get("quote", [{}])[0]
    closes, volumes = quote.get("close") or [], quote.get("volume") or []
    history = [{"date": time.strftime("%Y-%m-%d", time.gmtime(ts)), "close": float(close),
                "volume": int(volumes[i] or 0) if i < len(volumes) and volumes[i] is not None else None}
               for i, (ts, close) in enumerate(zip(timestamps, closes)) if close is not None]
    events = (raw.get("events") or {}).get("dividends") or {}
    dividends = [{"date": time.strftime("%Y-%m-%d", time.gmtime(int(k))), "amount": float(v.get("amount", 0))}
                 for k, v in events.items()]
    price = meta.get("regularMarketPrice")
    if price is None and history: price = history[-1]["close"]
    return {"ticker": ticker.upper(), "currency": meta.get("currency"), "exchange": meta.get("exchangeName"),
            "price": float(price) if price is not None else None, "market_state": meta.get("marketState"),
            "as_of": history[-1]["date"] if history else None, "history": history,
            "dividends": sorted(dividends, key=lambda x: x["date"]),
            "source": "Yahoo Finance chart (unofficial; may be delayed)"}
