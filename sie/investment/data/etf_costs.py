"""Issuer-first ETF KID/factsheet cost extraction (Vanguard, iShares, Amundi, Xtrackers).

Values are extracted from the actual downloaded issuer document text. Heuristic
matches are returned with evidence snippets and never silently promoted to TER.
"""
from __future__ import annotations

import hashlib
import html as html_lib
import json
import re
import xml.etree.ElementTree as ET
import shutil
import subprocess
import tempfile
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .base import get_bytes

ISSUERS = {
    "vanguard": {"domains": ("fund-docs.vanguard.com", "vanguard.com"),
                 "kid": "https://fund-docs.vanguard.com/{isin}_priipskid_en.pdf",
                 "factsheet": "https://fund-docs.vanguard.com/{isin}_EU_INT_UK_EN.pdf"},
    "ishares": {"domains": ("ishares.com", "blackrock.com")},
    "amundi": {"domains": ("amundietf.com", "amundi.com")},
    "xtrackers": {"domains": ("etf.dws.com", "dws.com"),
                  "kid": "https://etf.dws.com/Download/PRIIPS%20KID/{ISIN}/EN/EN"},
}

_PERCENT = r"(\d{1,2}(?:[.,]\d{1,4})?)\s*%"


def _is_official_host(host: str, issuer: str) -> bool:
    host = host.lower().split(":", 1)[0].rstrip(".")
    return any(host == domain or host.endswith("." + domain) for domain in ISSUERS[issuer]["domains"])


def _issuer_for(url: str | None, issuer: str | None) -> str | None:
    if issuer:
        key = issuer.strip().lower().replace(" ", "")
        aliases = {"blackrock": "ishares", "dws": "xtrackers"}
        key = aliases.get(key, key)
        if key not in ISSUERS:
            raise ValueError(f"Unsupported issuer: {issuer}")
        return key
    host = urllib.parse.urlparse(url or "").netloc.lower()
    for name in ISSUERS:
        if _is_official_host(host, name):
            return name
    return None


def _request(url: str, *, accept: str = "application/pdf,text/html;q=0.9,*/*;q=0.8") -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; SIE ETF research)", "Accept": accept})
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            return response.read()
    except Exception as exc:
        raise RuntimeError(f"Official issuer document request failed for {urllib.parse.urlparse(url).netloc}: {exc}") from exc


def _post_json(url: str, payload: dict[str, Any], *, referer: str) -> Any:
    body = json.dumps(payload).encode("utf-8")
    parsed_url = urllib.parse.urlparse(url)
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "User-Agent": "Mozilla/5.0 (compatible; SIE ETF research)", "Accept": "application/json",
        "Content-Type": "application/json", "Origin": parsed_url.scheme + "://" + parsed_url.netloc,
        "Referer": referer,
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        raise RuntimeError(f"Official issuer metadata request failed: {exc}") from exc


def _amundi_documents(isin: str) -> list[str]:
    # Resolve Amundi public product and document APIs by share-class ISIN.
    base = "https://www.amundietf.com"
    context = {"countryCode": "LUX", "languageCode": "en", "userProfileName": "INSTIT"}
    referer = f"{base}/amundi/lux/en/instit/{isin}"
    payload = {"context": context, "productIds": [isin],
               "characteristics": ["ISIN", "TER", "TICKER", "SHARE_MARKETING_NAME", "WKN", "MNEMO"],
               "filters": [], "metrics": [], "historics": [], "productType": "PRODUCT"}
    products = _post_json(base + "/mapi/ProductAPI/getProductsData", payload, referer=referer)
    rows = products.get("products", []) if isinstance(products, dict) else []
    match = next((row for row in rows if str(row.get("characteristics", {}).get("ISIN", "")).upper() == isin), None)
    if not match:
        raise RuntimeError("Amundi product API did not confirm the requested ISIN.")
    docs = _post_json(base + "/mapi/DocumentAPI/document/getByProductIdsAndContext",
                      {"productIds": [isin], "context": context}, referer=referer)
    records = docs.get(isin, []) if isinstance(docs, dict) else []
    selected: dict[str, dict[str, Any]] = {}
    for item in records:
        dtype = str(item.get("documentType", {}).get("name", "")).lower()
        if dtype not in {"kidpriips", "monthlyfactsheet"} or item.get("status") != "PUBLIC":
            continue
        if str(item.get("language", "")).lower() != "english":
            continue
        path = item.get("url") or item.get("appliedAlias")
        if not path:
            continue
        url = urllib.parse.urljoin(base, path)
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme != "https" or not _is_official_host(parsed.hostname or "", "amundi"):
            continue
        previous = selected.get(dtype)
        if previous is None or int(item.get("recordDate") or 0) > int(previous.get("recordDate") or 0):
            selected[dtype] = {"url": url, "recordDate": item.get("recordDate")}
    ordered = [selected[k]["url"] for k in ("kidpriips", "monthlyfactsheet") if k in selected]
    if not ordered:
        raise RuntimeError("Amundi product found, but no public English KID or factsheet was returned.")
    return ordered


def _ishares_documents(isin: str) -> list[str]:
    # Bing RSS is used only to discover the issuer product page; all data is
    # downloaded and verified from iShares/BlackRock-hosted PDF documents.
    query = urllib.parse.quote(f"site:ishares.com {isin}")
    rss = _request(f"https://www.bing.com/search?format=rss&q={query}", accept="application/rss+xml,application/xml,text/xml,*/*")
    try:
        root = ET.fromstring(rss)
    except ET.ParseError as exc:
        raise RuntimeError("iShares product search returned an unreadable RSS response.") from exc
    product_urls = []
    for item in root.findall(".//item"):
        link = (item.findtext("link") or "").strip()
        parsed = urllib.parse.urlparse(link)
        if parsed.scheme == "https" and _is_official_host(parsed.hostname or "", "ishares") and re.search(r"/(?:products|producten)/\d+", parsed.path, re.I):
            if link not in product_urls:
                product_urls.append(link)
    if not product_urls:
        raise RuntimeError("iShares public search index did not return an official product page for this ISIN.")
    errors = []
    for product_url in product_urls[:5]:
        try:
            page = _request(product_url, accept="text/html,application/xhtml+xml,*/*")
            html = page.decode("utf-8", errors="replace")
            if not re.search(rf"\b{re.escape(isin)}\b", html, re.I):
                continue
            links = re.findall(r'href="([^"]+)"', html, re.I) + re.findall(r"href='([^']+)'", html, re.I)
            candidates = []
            for href in links:
                url = urllib.parse.urljoin(product_url, href.replace("&amp;", "&"))
                parsed = urllib.parse.urlparse(url)
                if parsed.scheme == "https" and _is_official_host(parsed.hostname or "", "ishares"):
                    path = parsed.path.lower()
                    if path.endswith(".pdf") and ("literature/kiid" in path or "literature/fact-sheet" in path or "literature/factsheet" in path):
                        candidates.append(url)
            unique = list(dict.fromkeys(candidates))
            kids = [u for u in unique if "literature/kiid" in urllib.parse.urlparse(u).path.lower()]
            factsheets = [u for u in unique if "fact-sheet" in urllib.parse.urlparse(u).path.lower() or "factsheet" in urllib.parse.urlparse(u).path.lower()]
            priips = [u for u in kids if "priips" in urllib.parse.urlparse(u).path.lower()]
            generated_kid = None
            # The legacy KIID filename contains the canonical product slug and
            # share-class suffix. Reuse it to construct the current PRIIPs KID URL.
            for kiid_url in kids:
                filename = urllib.parse.urlparse(kiid_url).path.rsplit("/", 1)[-1]
                if filename.lower().startswith("ucits_kiid-"):
                    slug = filename[len("ucits_kiid-"):]
                    slug = re.sub(rf"-(?:gb|de|fr|nl|ie|it|es|ch|lu|se|dk|fi|no|be)-{isin.lower()}-en\.pdf$", "", slug, flags=re.I)
                    if slug != filename:
                        generated_kid = ("https://www.ishares.com/uk/professional/en/literature/kiid/"
                                         + f"eu-priips-{slug}-{isin.lower()}-en.pdf?siteEntryPassthrough=true&switchLocale=y")
                        break
            if not generated_kid:
                title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
                if title_match:
                    title = html_lib.unescape(re.sub(r"<.*?>", "", title_match.group(1))).split("|")[0].strip()
                    slug = re.sub(r"[^a-z0-9]+", "-", title.lower().replace("&", "")).strip("-")
                    generated_kid = ("https://www.ishares.com/uk/professional/en/literature/kiid/"
                                     + f"eu-priips-{slug}-{isin.lower()}-en.pdf?siteEntryPassthrough=true&switchLocale=y")
            primary_kid = priips[:1] or ([generated_kid] if generated_kid else []) or kids[:1]
            fallback_kiid = [u for u in kids if u not in primary_kid]
            ordered = primary_kid + fallback_kiid[:1] + factsheets[:1]
            if ordered:
                return ordered
        except Exception as exc:
            errors.append(str(exc))
    raise RuntimeError("No current public iShares KID/factsheet links were found on the matching product page." + (" " + "; ".join(errors[:2]) if errors else ""))


def _discover_document(isin: str, issuer: str, document_url: str | None) -> list[str]:
    if document_url:
        parsed = urllib.parse.urlparse(document_url)
        if parsed.scheme != "https" or not _is_official_host(parsed.hostname or "", issuer):
            raise ValueError("Document URL must use HTTPS and belong to the selected official issuer domain.")
        return [document_url]
    spec = ISSUERS[issuer]
    if issuer == "vanguard":
        return [spec["kid"].format(isin=isin.lower()), spec["factsheet"].format(isin=isin.lower())]
    if issuer == "xtrackers":
        return [spec["kid"].format(ISIN=isin.upper())]
    if issuer == "amundi":
        return _amundi_documents(isin)
    if issuer == "ishares":
        return _ishares_documents(isin)
    return []


def _extract_pdf_text(raw: bytes) -> str:
    if not raw.startswith(b"%PDF-"):
        raise RuntimeError("Issuer response is not a PDF document.")
    executable = shutil.which("pdftotext")
    if not executable:
        raise RuntimeError("PDF text extraction unavailable: install poppler-utils (pdftotext).")
    with tempfile.TemporaryDirectory(prefix="sie-etf-kid-") as tmp:
        source, target = Path(tmp) / "document.pdf", Path(tmp) / "document.txt"
        source.write_bytes(raw)
        result = subprocess.run([executable, "-layout", str(source), str(target)], capture_output=True, text=True, timeout=30)
        if result.returncode != 0 or not target.exists():
            raise RuntimeError("Could not extract text from issuer PDF.")
        return target.read_text(encoding="utf-8", errors="replace")


def _pct_near(text: str, patterns: list[str], *, window: int = 450) -> dict[str, Any] | None:
    """Find a percentage on the labelled row (or its immediately adjacent row).

    Do not scan an arbitrary character window: KID tables place EUR 0 for an
    entry/exit fee before the next row's TER, which can otherwise be misread.
    """
    lines = text.splitlines()
    for label in patterns:
        for index, line in enumerate(lines):
            if not re.search(label, line, flags=re.I):
                continue
            candidates = []
            # Same row is strongest evidence. One adjacent row accommodates
            # table extraction where the figure is wrapped to the next line.
            for row_index in (index, index + 1, index - 1):
                if 0 <= row_index < len(lines):
                    row = lines[row_index]
                    if row_index != index and re.search(r"(?:entry costs|exit costs|management fees|administrative or operating costs|transaction costs|performance fees)", row, re.I):
                        # Keep a child management row for the ongoing-cost group;
                        # do not cross into an unrelated category.
                        if not ("ongoing costs" in label.lower() and re.search(r"management fees", row, re.I)):
                            continue
                    candidates.extend((row, m) for m in re.finditer(_PERCENT, row))
            if candidates:
                row, pct_match = candidates[0]
                result = {"value_pct": float(pct_match.group(1).replace(",", ".")),
                          "evidence": row.strip(), "label": label,
                          "method": "issuer_pdf_text_label_adjacent_table_row"}
                # KID tables can show both a percentage and its EUR impact.
                for amount_row in (lines[index], lines[index + 1] if index + 1 < len(lines) else "", lines[index - 1] if index else ""):
                    money = re.search(r"\b(EUR|USD|GBP|CHF|SEK|NOK|DKK)\s*([0-9][0-9.,]*)|([0-9][0-9.,]*)\s*(EUR|USD|GBP|CHF|SEK|NOK|DKK)\b", amount_row, re.I)
                    if money:
                        currency = (money.group(1) or money.group(4)).upper()
                        amount = float((money.group(2) or money.group(3)).replace(",", "."))
                        result["amount_currency"] = currency
                        result["amount"] = amount
                        if currency == "EUR": result["amount_eur"] = amount
                        break
                return result
            # KID entry/exit lines are often expressed as a currency amount, not %.
            for row_index in (index, index + 1):
                if 0 <= row_index < len(lines):
                    money = re.search(r"\b(EUR|USD|GBP|CHF|SEK|NOK|DKK)\s*([0-9][0-9.,]*)|([0-9][0-9.,]*)\s*(EUR|USD|GBP|CHF|SEK|NOK|DKK)\b", lines[row_index], re.I)
                    if money:
                        currency = (money.group(1) or money.group(4)).upper()
                        amount = float((money.group(2) or money.group(3)).replace(",", "."))
                        item = {"value_amount": amount, "amount_currency": currency,
                                "evidence": lines[row_index].strip(), "label": label,
                                "method": "issuer_pdf_text_label_currency_amount"}
                        if currency == "EUR": item["value_eur"] = amount
                        return item
    return None


def parse_issuer_cost_document(text: str, *, isin: str, issuer: str, source_url: str,
                               document_type: str = "KID", retrieved_at: str | None = None) -> dict[str, Any]:
    """Parse cost line items while preserving the original category distinctions."""
    normalized = re.sub(r"\s+", " ", text)
    isin_found = bool(re.search(rf"\b{re.escape(isin)}\b", normalized, re.I))
    lower_text = normalized.lower()
    is_kiid = document_type.lower() != "factsheet" and "key investor information" in lower_text
    kid_markers = ("key information document", "essentiële-informatiedocument", "document d'informations clés", "basisinformationsblatt", "what are the costs", "composition of costs", "wat zijn de kosten", "quels sont les coûts", "welche kosten")
    is_kid = document_type.lower() != "factsheet" and any(marker in lower_text for marker in kid_markers)
    labels = {
        "ongoing_charges_pct": [r"ongoing charges", r"ongoing charge", r"ongoing costs", r"management fees and", r"management fees and other", r"administrative or operating costs", r"ongoing fee", r"total expense ratio", r"\bter\b", r"\bocf\b", r"lopende kosten", r"beheerkosten en andere", r"frais courants", r"frais de gestion et autres", r"laufende kosten", r"verwaltungsgebühren und sonstige", r"gesamtkostenquote"],
        "transaction_costs_pct": [r"transaction costs", r"portfolio transaction costs", r"transaction cost", r"transactiekosten", r"coûts de transaction", r"transaktionskosten"],
        "entry_costs_pct": [r"entry costs", r"entry charge", r"instapkosten", r"coûts d'entrée", r"einstiegskosten"],
        "exit_costs_pct": [r"exit costs", r"exit charge", r"uitstapkosten", r"coûts de sortie", r"ausstiegskosten"],
        "performance_fee_pct": [r"performance fees", r"performance fee", r"prestatievergoeding", r"commission de performance", r"performancegebühr"],
        "reduction_in_yield_pct": [r"reduction in yield", r"annual cost impact", r"impact on return", r"vermindering van het rendement", r"réduction du rendement", r"auswirkung der kosten auf die rendite"],
        "tracking_difference_pct": [r"tracking difference"],
    }
    extracted = {key: _pct_near(text, variants) for key, variants in labels.items()}
    # The PRIIPs KID composition table's management/administrative cost is the
    # closest standard proxy for recurring fund charges, but keep its exact label.
    ongoing = extracted["ongoing_charges_pct"]
    if ongoing and ("management fees and other" in ongoing["label"] or is_kid):
        ongoing["classification"] = "management_and_administrative_costs_not_labelled_ter"
    elif ongoing:
        ongoing["classification"] = "issuer_labelled_ongoing_charge_or_ter"
    for key, item in extracted.items():
        if item:
            item["source_url"] = source_url
            item["document_type"] = document_type
    asof = None
    if document_type.lower() == "factsheet":
        date_patterns = [
            r"information as at\s*:?\s*(\d{1,2}[-/ ]+[A-Za-z0-9]+[-/ ]+\d{4})",
            r"as at\s*:?\s*(\d{1,2}[-/ ]+[A-Za-z0-9]+[-/ ]+\d{4})",
            r"(?:NAV and AUM|net asset value and assets under management) as of\s*:?\s*(\d{1,2}[./-]\d{1,2}[./-]\d{4})",
        ]
        for pattern in date_patterns:
            match = re.search(pattern, normalized, re.I)
            if match:
                asof = match.group(1)
                break
        if not asof:
            # Amundi prints the factsheet's as-of date in the opening block,
            # before the performance tables and historical inception dates.
            opening = "\n".join(text.splitlines()[:18])
            date_match = re.search(r"(?<!\d)(\d{2}[./-]\d{2}[./-]\d{4})(?!\d)", opening)
            if date_match:
                asof = date_match.group(1)
    else:
        date_patterns = [
            r"(?:this document was published on|published on|date of this document is|document date|document is dated|gedateerd op|document is gedateerd op|accurate as at|information is accurate as at)\s*:?\s*(\d{1,2}[./-]\d{1,2}[./-]\d{4}|\d{1,2}\s+[A-Za-zÀ-ÿ.]+\s+\d{4}|\d{4}-\d{2}-\d{2})",
            r"(?:production date|date of production)\s*:?\s*(\d{1,2}[./-]\d{1,2}[./-]\d{4})",
        ]
        for pattern in date_patterns:
            date_match = re.search(pattern, normalized, re.I)
            if date_match:
                asof = date_match.group(1)
                break
    sha = hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()
    if not isin_found:
        status = "isin_not_confirmed_in_document"
    elif not any(extracted.values()):
        status = "document_found_cost_fields_not_extracted"
    elif is_kid:
        status = "extracted_from_issuer_kid"
    elif is_kiid:
        status = "extracted_from_issuer_kiid"
    else:
        status = "extracted_from_issuer_factsheet"
    return {
        "status": status, "issuer": issuer, "isin": isin, "isin_confirmed": isin_found,
        "document_type": "KID" if is_kid else "KIID" if is_kiid else document_type, "document_date": asof,
        "retrieved_at": retrieved_at or datetime.now(timezone.utc).isoformat(),
        "source_url": source_url, "document_sha256_text": sha,
        "costs": extracted,
        "quality": {"ongoing_charges_is_ter": bool(ongoing and ongoing.get("classification") == "issuer_labelled_ongoing_charge_or_ter"),
                    "kid_detected": is_kid, "kiid_detected": is_kiid,
                    "note": "PRIIPs transaction costs and reduction-in-yield are separate from TER/ongoing charges; never add them to TER. A factsheet TER/OCF label is retained as published."},
    }


def extract_etf_costs(isin: str, *, issuer: str | None = None, document_url: str | None = None,
                      document_type: str = "KID") -> dict[str, Any]:
    isin = isin.strip().upper().replace(" ", "")
    if not re.fullmatch(r"[A-Z]{2}[A-Z0-9]{10}", isin):
        raise ValueError("Provide a valid 12-character ISIN.")
    selected = _issuer_for(document_url, issuer)
    if not selected:
        raise ValueError("Issuer could not be inferred; specify vanguard, ishares, amundi or xtrackers.")
    errors = []
    if document_url:
        # Invalid caller-supplied URLs are input errors, not discovery misses.
        urls = _discover_document(isin, selected, document_url)
    else:
        try:
            urls = _discover_document(isin, selected, None)
        except Exception as exc:
            urls = []
            errors.append(str(exc))
    parsed_documents = []
    for url in urls:
        try:
            raw = get_bytes(url, cache_key="etf-cost-" + hashlib.sha256(url.encode()).hexdigest()[:20], ttl=86400,
                            accept="application/pdf,text/html;q=0.9,*/*;q=0.8")
            if not raw.startswith(b"%PDF-"):
                raise RuntimeError("Issuer document link did not return a PDF.")
            document_text = _extract_pdf_text(raw)
            path_lower = urllib.parse.urlparse(url).path.lower()
            kind = ("KIID" if "ucits_kiid" in path_lower else
                    "KID" if any(term in path_lower for term in ("kid", "priips", "kiid")) else
                    "factsheet" if any(term in path_lower for term in ("factsheet", "fact-sheet", "monthlyfactsheet")) else document_type)
            parsed = parse_issuer_cost_document(document_text, isin=isin, issuer=selected, source_url=url, document_type=kind)
            parsed_documents.append(parsed)
        except Exception as exc:
            errors.append(f"{urllib.parse.urlparse(url).path}: {exc}")
    if parsed_documents:
        confirmed = [doc for doc in parsed_documents if doc.get("isin_confirmed")]
        if not confirmed:
            return {
                "status": "isin_not_confirmed_in_document", "issuer": selected, "isin": isin,
                "isin_confirmed": False, "costs": {},
                "documents": [{"document_type": doc["document_type"], "document_date": doc["document_date"],
                               "source_url": doc["source_url"], "status": doc["status"], "costs": {}}
                              for doc in parsed_documents],
                "errors": errors, "note": "Issuer PDFs were found, but none confirmed the requested ISIN; no cost figures are accepted.",
            }
        primary = confirmed[0]
        primary["documents"] = [{"document_type": doc["document_type"], "document_date": doc["document_date"],
                                 "source_url": doc["source_url"], "status": doc["status"],
                                 "costs": doc["costs"] if doc.get("isin_confirmed") else {}}
                                for doc in parsed_documents]
        primary["discovery_method"] = "issuer_api_by_isin" if selected == "amundi" else "public_product_search_then_issuer_page" if selected == "ishares" else "issuer_direct_isin_route"
        if errors:
            primary["errors"] = errors
        return primary
    return {"status": "unavailable", "issuer": selected, "isin": isin, "source_urls_attempted": urls,
            "errors": errors, "costs": {}, "note": "No cost values returned because no verifiable issuer document was parsed."}
