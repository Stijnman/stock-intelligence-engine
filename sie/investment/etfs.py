"""ETF analytics with source-aware Belgian retail tax calculations."""
from __future__ import annotations

from typing import Any

from .belgian_tax import calculate_net_dividend_yield, calculate_tob


def analyze_etf(metadata: dict[str, Any]) -> dict[str, Any]:
    fsma = metadata.get("fsma_registry") or {}
    fsma_matches = fsma.get("matches") or []
    fsma_ucits = any(match.get("is_ucits") for match in fsma_matches)
    ucits_value = (True if fsma_ucits else False) if fsma_matches else (None if fsma else metadata.get("ucits"))
    ucits_evidence = (
        {"status": "verified_in_fsma_register" if fsma_ucits else "matched_but_not_ucits",
         "as_of": fsma.get("as_of"), "matches": len(fsma_matches), "source_url": fsma.get("source_url")} if fsma_matches else
        ({"status": fsma.get("status", "not_checked"), "note": "No positive UCITS confirmation from this register."} if fsma else
         (metadata.get("ucits_evidence") or {"status": "user_supplied_unverified"} if metadata.get("ucits") is not None else None))
    )
    legal_form_raw = str(metadata.get("legal_form") or (fsma_matches[0].get("legal_form") if fsma_matches else "")).upper()
    legal_form = ("sicav" if legal_form_raw in {"PLC", "SANV", "ICAV", "SICAV", "SA", "NV"} else
                  "fcp" if legal_form_raw in {"FCP", "INDOVD"} else None)
    registration = metadata.get("registration") or ("fsma" if fsma_matches else "unknown")
    required = ("ticker", "ter_pct", "aum", "domicile", "ucits", "distribution")
    effective = {**metadata, "ucits": ucits_value}
    missing = [key for key in required if effective.get(key) in (None, "")]
    ter = float(metadata["ter_pct"]) if metadata.get("ter_pct") is not None else None
    distribution_value = str(metadata.get("distribution") or "").strip().lower()
    distribution_value = {"acc": "capitalisation", "accumulating": "capitalisation", "accumulation": "capitalisation", "dist": "distribution", "distributing": "distribution"}.get(distribution_value, distribution_value)
    if ter is not None and not 0 <= ter <= 10:
        raise ValueError("TER percentage must be between 0 and 10.")
    annual_cost = ter / 100 * 10000 if ter is not None else None
    result = {
        "ticker": metadata.get("ticker"),
        "isin": metadata.get("isin"),
        "metadata": metadata,
        "missing_fields": missing,
        "data_completeness_pct": round((len(required) - len(missing)) / len(required) * 100, 1),
        "checks": {
            "ucits": ucits_value,
            "ucits_evidence": ucits_evidence,
            "fsma_registration_matches": fsma_matches,
            "distribution": distribution_value or None,
            "ter_pct": ter,
            "annual_cost_per_10000_eur": round(annual_cost, 2) if annual_cost is not None else None,
            "aum": metadata.get("aum"),
            "domicile": metadata.get("domicile"),
            "legal_form": legal_form or legal_form_raw or None,
            "registration": registration,
            "replication": metadata.get("replication"),
            "benchmark": metadata.get("benchmark"),
            "holdings_count": metadata.get("holdings_count"),
        },
        "warning": "Verify TER and class data against the latest issuer KID/factsheet. KID transaction costs and RIY are not the same thing as TER.",
    }
    if metadata.get("ter_pct") is not None:
        result["ter_evidence"] = {
            "status": "source_url_provided_not_independently_verified" if metadata.get("ter_source_url") else "unverified_input",
            "source_url": metadata.get("ter_source_url"),
            "as_of": metadata.get("ter_as_of"),
            "note": "Use the latest issuer KID/factsheet ongoing-cost/TER figure; do not substitute PRIIPs RIY or transaction costs.",
        }
        result["ter_cost_projection"] = {
            "annual_eur_on_10000": round(annual_cost, 2),
            "five_year_simple_eur_on_10000": round(annual_cost * 5, 2),
            "ten_year_simple_eur_on_10000": round(annual_cost * 10, 2),
            "note": "Simple static projection; actual TER drag changes with NAV and excludes tracking difference and trading costs.",
        }
    if distribution_value == "distribution" and metadata.get("annual_distribution_per_share") is not None and metadata.get("market_price") is not None:
        if legal_form:
            result["net_dividend"] = calculate_net_dividend_yield(
                annual_distribution_per_share=float(metadata["annual_distribution_per_share"]),
                market_price=float(metadata["market_price"]), legal_form=legal_form,
                fcp_breakdown_available=bool(metadata.get("fcp_breakdown_available", False)),
                belgian_withholding_rate_pct=(float(metadata["belgian_withholding_rate_pct"]) if metadata.get("belgian_withholding_rate_pct") is not None else None),
                investor_level_foreign_withholding_pct=float(metadata.get("investor_level_foreign_withholding_pct", 0.0)),
            )
        else:
            result["net_dividend"] = {"status": "needs_legal_form_evidence", "net_cash_yield_pct": None}
    if metadata.get("tob_amount_eur") is not None:
        result["tob"] = calculate_tob(
            float(metadata["tob_amount_eur"]),
            legal_form=legal_form or str(metadata.get("legal_form", "")).lower(),
            distribution=distribution_value,
            registration=str(registration),
            listed=bool(metadata.get("listed", True)),
            side=str(metadata.get("tob_side", "buy")),
        )
    return result
