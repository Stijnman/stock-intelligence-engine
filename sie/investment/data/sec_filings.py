"""SEC EDGAR Form 4 and 13F filing adapters (free public filings; contact User-Agent required)."""
from __future__ import annotations

import json
import os
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

from .base import get_bytes
from ..providers import sec_cik_for_ticker

SUBMISSIONS_URL = "https://data.sec.gov/submissions"
ARCHIVES_URL = "https://www.sec.gov/Archives/edgar/data"


def _headers() -> dict[str, str]:
    agent = os.getenv("SEC_USER_AGENT", "").strip()
    if not agent or "@" not in agent:
        raise RuntimeError(
            "Set SEC_USER_AGENT to identify your application and include a contact email address."
        )
    return {"User-Agent": agent, "Accept-Encoding": "gzip, deflate"}


def _json(url: str, cache_key: str, ttl: int = 3600) -> dict:
    body = get_bytes(url, cache_key=cache_key, ttl=ttl, headers=_headers())
    try:
        return json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Invalid SEC JSON response from {urlparse(url).netloc}") from exc


def _xml(url: str, cache_key: str) -> ET.Element:
    body = get_bytes(url, cache_key=cache_key, ttl=86400, accept="application/xml,text/xml,*/*", headers=_headers())
    try:
        return ET.fromstring(body)
    except ET.ParseError as exc:
        raise RuntimeError(f"Invalid SEC XML filing at {url}") from exc


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _child_text(node: ET.Element, path: str) -> str | None:
    current = node
    for part in path.split("/"):
        current = next((child for child in current if _local_name(child.tag) == part), None)
        if current is None:
            return None
    return current.text.strip() if current.text else None


def _float(value: str | None) -> float | None:
    try:
        return float(value) if value not in (None, "") else None
    except (TypeError, ValueError):
        return None


def _recent_filings(ticker: str, forms: set[str], limit: int) -> tuple[str, list[dict]]:
    if not 1 <= limit <= 100:
        raise ValueError("limit must be between 1 and 100")
    _headers()  # Fail before any SEC request if the required contact-bearing User-Agent is absent.
    cik = sec_cik_for_ticker(ticker)
    payload = _json(f"{SUBMISSIONS_URL}/CIK{cik}.json", f"sec-submissions-{cik}", ttl=3600)
    recent = (payload.get("filings") or {}).get("recent") or {}
    count = len(recent.get("form", []))
    filings = []
    for index in range(count):
        form = recent["form"][index]
        if form not in forms:
            continue
        accession = recent["accessionNumber"][index]
        primary = recent["primaryDocument"][index]
        accession_path = accession.replace("-", "")
        cik_path = str(int(cik))
        filings.append({
            "form": form,
            "items": (recent.get("items") or [""] * count)[index],
            "filing_date": recent["filingDate"][index],
            "report_date": (recent.get("reportDate") or [""] * count)[index],
            "accession_number": accession,
            "primary_document": primary,
            "archive_path": f"{ARCHIVES_URL}/{cik_path}/{accession_path}",
            "source_url": f"{ARCHIVES_URL}/{cik_path}/{accession_path}/{primary}",
        })
        if len(filings) >= limit:
            break
    return cik, filings


def fetch_form4_transactions(ticker: str, *, limit_filings: int = 10, include_amendments: bool = False) -> list[dict]:
    """Fetch and parse recent Form 4 non-derivative and derivative transactions."""
    forms = {"4", "4/A"} if include_amendments else {"4"}
    _, filings = _recent_filings(ticker, forms, limit_filings)
    transactions = []
    for filing in filings:
        root = _xml(filing["source_url"], f"sec-form4-{filing['accession_number']}")
        owners = []
        for owner in root.iter():
            if _local_name(owner.tag) == "reportingOwner":
                owners.append({
                    "name": _child_text(owner, "reportingOwnerId/rptOwnerName"),
                    "cik": _child_text(owner, "reportingOwnerId/rptOwnerCik"),
                    "is_director": _child_text(owner, "reportingOwnerRelationship/isDirector"),
                    "is_officer": _child_text(owner, "reportingOwnerRelationship/isOfficer"),
                    "officer_title": _child_text(owner, "reportingOwnerRelationship/officerTitle"),
                    "is_ten_percent_owner": _child_text(owner, "reportingOwnerRelationship/isTenPercentOwner"),
                })
        owner = owners[0] if owners else {}
        for node in root.iter():
            kind = _local_name(node.tag)
            if kind not in {"nonDerivativeTransaction", "derivativeTransaction"}:
                continue
            shares = _float(_child_text(node, "transactionAmounts/transactionShares/value"))
            price = _float(_child_text(node, "transactionAmounts/transactionPricePerShare/value"))
            code = _child_text(node, "transactionCoding/transactionCode")
            acquired_disposed = _child_text(node, "transactionAmounts/transactionAcquiredDisposedCode/value")
            transactions.append({
                "ticker": ticker.upper(),
                "filing_form": filing["form"],
                "filing_date": filing["filing_date"],
                "report_date": filing["report_date"],
                "transaction_date": _child_text(node, "transactionDate/value"),
                "security_title": _child_text(node, "securityTitle/value"),
                "shares": shares,
                "price": price,
                "transaction_value": shares * price if shares is not None and price is not None else None,
                "transaction_code": code,
                "acquired_disposed": acquired_disposed,
                "ownership_nature": _child_text(node, "ownershipNature/directOrIndirectOwnership/value"),
                "is_10b5_1": _child_text(node, "transactionCoding/aff10b5One"),
                "owner": owner,
                "accession_number": filing["accession_number"],
                "source_url": filing["source_url"],
                "source": "SEC EDGAR Form 4",
                "source_status": "LIVE_SOURCE_FILING",
            })
    return transactions


def fetch_13f_holdings(ticker: str, *, limit_filings: int = 1) -> list[dict]:
    """Fetch holdings from the latest 13F-HR information-table XML filing.

    Values are reported in USD thousands. 13F is a delayed long-equity disclosure,
    not a complete real-time portfolio (short positions and many asset classes are absent).
    """
    _, filings = _recent_filings(ticker, {"13F-HR"}, limit_filings)
    holdings = []
    for filing in filings:
        index_url = f"{filing['archive_path']}/index.json"
        index_payload = _json(index_url, f"sec-index-{filing['accession_number']}", ttl=86400)
        items = (index_payload.get("directory") or {}).get("item") or []
        info_docs = [
            item for item in items
            if "INFORMATION TABLE" in str(item.get("type", "")).upper()
            or str(item.get("name", "")).lower().endswith(("infotable.xml", "informationtable.xml"))
        ]
        if not info_docs:
            raise RuntimeError(f"No 13F information-table XML found in {filing['accession_number']}")
        for doc in info_docs:
            url = f"{filing['archive_path']}/{doc['name']}"
            root = _xml(url, f"sec-13f-{filing['accession_number']}-{doc['name']}")
            for node in root.iter():
                if _local_name(node.tag) != "infoTable":
                    continue
                holdings.append({
                    "manager_ticker": ticker.upper(),
                    "filing_date": filing["filing_date"],
                    "report_date": filing["report_date"],
                    "issuer": _child_text(node, "nameOfIssuer"),
                    "title_of_class": _child_text(node, "titleOfClass"),
                    "cusip": _child_text(node, "cusip"),
                    "value_usd_thousands": _float(_child_text(node, "value")),
                    "shares": _float(_child_text(node, "shrsOrPrnAmt/sshPrnamt")),
                    "share_type": _child_text(node, "shrsOrPrnAmt/sshPrnamtType"),
                    "put_call": _child_text(node, "putCall"),
                    "investment_discretion": _child_text(node, "investmentDiscretion"),
                    "voting_authority_sole": _float(_child_text(node, "votingAuthority/Sole")),
                    "voting_authority_shared": _float(_child_text(node, "votingAuthority/Shared")),
                    "voting_authority_none": _float(_child_text(node, "votingAuthority/None")),
                    "source": "SEC EDGAR Form 13F-HR",
                    "source_url": url,
                    "accession_number": filing["accession_number"],
                    "source_status": "LIVE_SOURCE_FILING",
                })
    return holdings

def fetch_reported_earnings_filings(ticker: str, *, limit_filings: int = 20) -> list[dict]:
    """Return official SEC 8-K filings that disclose earnings under Item 2.02.

    This is a reported-results history, not a forward earnings calendar and does
    not provide analyst consensus or EPS surprise estimates. Foreign private
    issuers commonly use 6-K and are not included by this Item 2.02 filter.
    """
    if not 1 <= limit_filings <= 100:
        raise ValueError("limit_filings must be between 1 and 100")
    _, candidates = _recent_filings(ticker, {"8-K"}, 100)
    results = []
    for filing in candidates:
        items = {value.strip() for value in str(filing.get("items") or "").split(",")}
        if "2.02" not in items:
            continue
        results.append({
            "ticker": ticker.upper(),
            "date": filing["filing_date"],
            "report_date": filing.get("report_date"),
            "status": "reported",
            "event_type": "SEC Form 8-K Item 2.02",
            "items": filing.get("items"),
            "accession_number": filing["accession_number"],
            "source": "SEC EDGAR",
            "source_url": filing["source_url"],
            "source_status": "LIVE_SOURCE_FILING",
        })
        if len(results) >= limit_filings:
            break
    return results
