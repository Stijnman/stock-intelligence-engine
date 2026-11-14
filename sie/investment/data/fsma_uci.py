"""Official FSMA list of foreign collective investment undertakings marketed in Belgium.

The workbook is published by the FSMA and identifies CIS/compartments. The
public list does not necessarily identify every share class/ISIN; never infer
class-specific distribution/capitalisation status from an umbrella row.
"""
from __future__ import annotations

import re
import zipfile
import xml.etree.ElementTree as ET
from io import BytesIO
from typing import Any

from .base import get_bytes

FSMA_FOREIGN_UCI_XLSX = (
    "https://www.fsma.be/sites/default/files/media/files/"
    "replacement_files/official_lists_fo_NL.xlsx"
)
FSMA_UCI_LANDING_PAGE = "https://www.fsma.be/nl/instelling-voor-collectieve-belegging-icb"
_NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def _column(cell_ref: str) -> str:
    return re.sub(r"[^A-Z]", "", cell_ref)


def _cell_text(cell: ET.Element) -> str:
    inline = cell.find("m:is/m:t", _NS)
    if inline is not None:
        return (inline.text or "").strip()
    value = cell.find("m:v", _NS)
    return (value.text or "").strip() if value is not None else ""


def parse_fsma_xlsx(content: bytes) -> dict[str, Any]:
    """Parse FSMA's single-sheet XLSX using the Python standard library."""
    try:
        archive = zipfile.ZipFile(BytesIO(content))
        sheet = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
    except (zipfile.BadZipFile, KeyError, ET.ParseError) as exc:
        raise RuntimeError("FSMA registry workbook has an unsupported or invalid format.") from exc

    rows = sheet.findall(".//m:sheetData/m:row", _NS)
    if len(rows) < 4:
        raise RuntimeError("FSMA registry workbook contains no usable rows.")
    as_of = _cell_text(rows[0].find("m:c", _NS)) if rows[0].find("m:c", _NS) is not None else None
    records = []
    for row in rows[3:]:
        values = {_column(cell.attrib.get("r", "")): _cell_text(cell)
                  for cell in row.findall("m:c", _NS)}
        if not values.get("A") or not values.get("F"):
            continue
        license_text = values.get("F", "")
        records.append({
            "fsma_code": values.get("A"),
            "fund_name_fr": values.get("C"),
            "fund_name_nl": values.get("E"),
            "license": license_text,
            "is_ucits": "UCITS" in license_text.upper(),
            "country": values.get("G"),
            "legal_form": values.get("H"),
            "management_company": values.get("M") or values.get("L"),
            "compartment_code": values.get("V"),
            "compartment_name_fr": values.get("W"),
            "compartment_name_nl": values.get("X"),
            "share_class_code": values.get("Y"),
            "share_class_name_fr": values.get("Z"),
            "share_class_name_nl": values.get("AA"),
            "share_class_type": values.get("AB") or None,
            "share_class_currency": values.get("AC") or None,
            "isin": values.get("AD") or None,
        })
    return {"as_of": as_of, "records": records}


def fetch_fsma_uci_registry(*, isin: str | None = None, name: str | None = None, limit: int = 100) -> dict[str, Any]:
    """Fetch and search the official FSMA foreign UCI register.

    Since the official list can identify the umbrella/sub-fund but omit ISIN
    and class-level data, name-only matches are returned as fund-level evidence.
    """
    if not isin and not name:
        raise ValueError("Provide an ISIN or fund/compartment name.")
    if not 1 <= limit <= 500:
        raise ValueError("limit must be between 1 and 500.")
    raw = get_bytes(
        FSMA_FOREIGN_UCI_XLSX,
        cache_key="fsma-foreign-uci-registry",
        ttl=7 * 86400,
        accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    parsed = parse_fsma_xlsx(raw)
    wanted_isin = isin.replace(" ", "").upper() if isin else None
    wanted_name = " ".join(name.casefold().split()) if name else None
    matches = []
    for record in parsed["records"]:
        names = [record.get(k) for k in (
            "fund_name_fr", "fund_name_nl", "compartment_name_fr", "compartment_name_nl"
        ) if record.get(k)]
        isin_match = bool(wanted_isin and (record.get("isin") or "").replace(" ", "").upper() == wanted_isin)
        name_match = bool(wanted_name and any(" ".join(v.casefold().split()) == wanted_name for v in names))
        if isin_match or name_match:
            matches.append({
                **record,
                "match_type": "ISIN" if isin_match else "FUND_OR_COMPARTMENT_NAME",
                "share_class_confirmed": bool(record.get("isin")),
                "ucits_status": "UCITS" if record["is_ucits"] else "NOT_UCITS_OR_OTHER",
            })
    total_matches = len(matches)
    isin_fields_available = any(record.get("isin") for record in parsed["records"])
    status = "matched" if matches else (
        "isin_not_available_in_fsma_export" if wanted_isin and not isin_fields_available else "not_found"
    )
    return {
        "status": status,
        "query": {"isin": wanted_isin, "name": name},
        "as_of": parsed["as_of"],
        "total_matches": total_matches,
        "truncated": total_matches > limit,
        "matches": matches[:limit],
        "source": "FSMA",
        "source_url": FSMA_FOREIGN_UCI_XLSX,
        "landing_page": FSMA_UCI_LANDING_PAGE,
        "limitations": [
            "The foreign-UCIs workbook currently exposes fund/compartment rows but no populated share-class ISIN fields; exact ISIN verification is therefore unavailable in this export.",
            "A fund/compartment match does not independently prove the ETF's share-class type, ISIN, TER or KID costs.",
            "Not found in this foreign-UCIs workbook is not proof that a product is not UCITS; check the issuer prospectus and relevant home regulator.",
        ],
    }
