"""Issuer-first ETF KID/factsheet cost extraction (Vanguard, iShares, Amundi, Xtrackers).

Values are extracted from the actual downloaded issuer document text. Heuristic
matches are returned with evidence snippets and never silently promoted to TER.
"""
from __future__ import annotations

import hashlib
import re
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
    "ishares": {"domains": ("ishares.com", "blackrock.com"),
                "search": "https://www.ishares.com/uk/individual/en/products?search={isin}"},
    "amundi": {"domains": ("amundietf.com", "amundi.com"),
               "product": "https://www.amundietf.com/amundi/lux/en/instit/{isin}"},
    "xtrackers": {"domains": ("etf.dws.com", "dws.com"),
                  "kid": "https://etf.dws.com/Download/PRIIPS%20KID/{ISIN}/EN/EN"},
}

_PERCENT = r"(\d{1,2}(?:[.,]\d{1,4})?)\s*%"


def _issuer_for(url: str | None, issuer: str | None) -> str | None:
    if issuer:
        key = issuer.strip().lower().replace(" ", "")
        aliases = {"blackrock": "ishares", "dws": "xtrackers"}
        key = aliases.get(key, key)
        if key not in ISSUERS:
            raise ValueError(f"Unsupported issuer: {issuer}")
        return key
    host = urllib.parse.urlparse(url or "").netloc.lower()
    for name, spec in ISSUERS.items():
        if any(domain in host for domain in spec["domains"]):
            return name
    return None


def _request(url: str, *, accept: str = "application/pdf,text/html;q=0.9,*/*;q=0.8") -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; SIE ETF research)", "Accept": accept})
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            return response.read()
    except Exception as exc:
        raise RuntimeError(f"Official issuer document request failed for {urllib.parse.urlparse(url).netloc}: {exc}") from exc


def _discover_document(isin: str, issuer: str, document_url: str | None) -> list[str]:
    if document_url:
        host = urllib.parse.urlparse(document_url).netloc.lower()
        if not any(domain in host for domain in ISSUERS[issuer]["domains"]):
            raise ValueError("Document URL must belong to the selected official issuer domain.")
        return [document_url]
    spec = ISSUERS[issuer]
    if issuer == "vanguard":
        return [spec["kid"].format(isin=isin.lower()), spec["factsheet"].format(isin=isin.lower())]
    if issuer == "xtrackers":
        return [spec["kid"].format(ISIN=isin.upper())]
    if issuer == "amundi":
        return [spec["product"].format(isin=isin.lower())]
    return [spec["search"].format(isin=urllib.parse.quote(isin.upper()))]


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
                    euro = re.search(r"EUR\s*([0-9][0-9.,]*)", amount_row, re.I)
                    if euro:
                        result["amount_eur"] = float(euro.group(1).replace(",", "."))
                        break
                return result
            # KID entry/exit lines are often expressed in EUR, not percent.
            for row_index in (index, index + 1):
                if 0 <= row_index < len(lines):
                    euro = re.search(r"EUR\s*([0-9][0-9.,]*)", lines[row_index], re.I)
                    if euro:
                        return {"value_eur": float(euro.group(1).replace(",", ".")),
                                "evidence": lines[row_index].strip(), "label": label,
                                "method": "issuer_pdf_text_label_euro_amount"}
    return None


def parse_issuer_cost_document(text: str, *, isin: str, issuer: str, source_url: str,
                               document_type: str = "KID", retrieved_at: str | None = None) -> dict[str, Any]:
    """Parse cost line items while preserving the original category distinctions."""
    normalized = re.sub(r"\s+", " ", text)
    isin_found = bool(re.search(rf"\b{re.escape(isin)}\b", normalized, re.I))
    kid_markers = ("key information document", "essentiële-informatiedocument", "document d'informations clés", "basisinformationsblatt", "key investor information", "what are the costs", "composition of costs", "wat zijn de kosten", "quels sont les coûts", "welche kosten")
    is_kid = any(marker in normalized.lower() for marker in kid_markers)
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
    date_match = re.search(r"(?:dated|date|as at|as of|correct as of|document is dated|gedateerd op|document is gedateerd op|document is daté du|daté du|document is dated)\s*[:\-]?\s*(\d{1,2}[./-]\d{1,2}[./-]\d{4}|\d{4}-\d{2}-\d{2}|\d{1,2}\s+[A-Za-zÀ-ÿ.]+\s+\d{4})", normalized, re.I)
    if date_match:
        asof = date_match.group(1)
    elif re.search(r"\d{4}-\d{2}-\d{2}", normalized):
        asof = re.search(r"\d{4}-\d{2}-\d{2}", normalized).group(0)
    sha = hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()
    if not isin_found:
        status = "isin_not_confirmed_in_document"
    elif not any(extracted.values()):
        status = "document_found_cost_fields_not_extracted"
    elif is_kid:
        status = "extracted_from_issuer_kid"
    else:
        status = "extracted_from_issuer_factsheet"
    return {
        "status": status, "issuer": issuer, "isin": isin, "isin_confirmed": isin_found,
        "document_type": "KID" if is_kid else document_type, "document_date": asof,
        "retrieved_at": retrieved_at or datetime.now(timezone.utc).isoformat(),
        "source_url": source_url, "document_sha256_text": sha,
        "costs": extracted,
        "quality": {"ongoing_charges_is_ter": bool(ongoing and ongoing.get("classification") == "issuer_labelled_ongoing_charge_or_ter"),
                    "kid_detected": is_kid,
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
    for url in _discover_document(isin, selected, document_url):
        try:
            raw = get_bytes(url, cache_key="etf-cost-" + hashlib.sha256(url.encode()).hexdigest()[:20], ttl=86400,
                            accept="application/pdf,text/html;q=0.9,*/*;q=0.8")
            if raw.startswith(b"%PDF-"):
                text = _extract_pdf_text(raw)
                return parse_issuer_cost_document(text, isin=isin, issuer=selected, source_url=url, document_type=document_type)
            html = raw.decode("utf-8", errors="replace")
            # iShares search pages commonly link to a product page; Amundi's
            # product pages expose document links in server-rendered markup.
            pages = [(url, html)]
            if selected == "ishares":
                product_paths = re.findall(r"href=[\"']([^\"']*/products/\d+[^\"']*)[\"']", html, re.I)
                for href in product_paths[:5]:
                    product_url = urllib.parse.urljoin(url, href)
                    if any(d in urllib.parse.urlparse(product_url).netloc for d in ISSUERS[selected]["domains"]):
                        try:
                            page = get_bytes(product_url, cache_key="etf-page-" + hashlib.sha256(product_url.encode()).hexdigest()[:20], ttl=86400, accept="text/html")
                            pages.append((product_url, page.decode("utf-8", errors="replace")))
                        except Exception as exc:
                            errors.append(str(exc))
            pdfs = []
            for page_url, page_html in pages:
                found = re.findall(r"https?://[^\"'<> ]+\.pdf(?:\?[^\"'<> ]*)?", page_html, re.I)
                found += [urllib.parse.urljoin(page_url, href) for href in re.findall(r"href=[\"']([^\"']+\.pdf[^\"']*)[\"']", page_html, re.I)]
                for pdf_url in found:
                    if any(d in urllib.parse.urlparse(pdf_url).netloc for d in ISSUERS[selected]["domains"]):
                        pdfs.append(pdf_url)
            pdfs = list(dict.fromkeys(pdfs))
            for pdf_url in pdfs:
                label = pdf_url.lower()
                if not any(term in label for term in ("kid", "priips", "factsheet", "fact-sheet", "kiid", "key-information")):
                    continue
                pdf = get_bytes(pdf_url, cache_key="etf-cost-" + hashlib.sha256(pdf_url.encode()).hexdigest()[:20], ttl=86400, accept="application/pdf")
                text = _extract_pdf_text(pdf)
                return parse_issuer_cost_document(text, isin=isin, issuer=selected, source_url=pdf_url, document_type=document_type)
            errors.append(f"No direct KID/factsheet PDF link discovered at {url}")
        except Exception as exc:
            errors.append(str(exc))
    return {"status": "unavailable", "issuer": selected, "isin": isin, "source_urls_attempted": _discover_document(isin, selected, document_url),
            "errors": errors, "costs": {}, "note": "No cost values returned because no verifiable issuer document was parsed."}
