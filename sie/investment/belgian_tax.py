"""Belgian retail-investor ETF transaction and distribution tax estimates.

Rates are versioned and sourced from Wikifin (FSMA initiative) and FPS Finance.
TOB depends on legal form, listing and FSMA/EEA registration—not UCITS alone.
"""
from __future__ import annotations

from datetime import date
from typing import Any

RULES_VERSION = "BE-2026-01"
RULES_EFFECTIVE_FROM = "2026-01-01"
TOB_SOURCE = "https://www.wikifin.be/fr/impots-emploi-et-revenus/declaration-dimpots/vos-revenus-mobiliers/les-taxes-sur-vos"
PM_SOURCE = "https://finances.belgium.be/fr/particuliers/declaration-impot/revenus/epargne-placements"

TOB_RULES = {
    "sicav": {
        "registered": {
            "distribution": {"rate": 0.0012, "cap": 1300.0},
            "capitalisation_fsma": {"rate": 0.0132, "cap": 4000.0},
            "capitalisation_eea": {"rate": 0.0012, "cap": 1300.0},
        },
        "unregistered": {"distribution": {"rate": 0.0035, "cap": 1600.0},
                         "capitalisation": {"rate": 0.0035, "cap": 1600.0}},
    },
    "fcp": {
        "registered": {"any": {"rate": 0.0012, "cap": 1300.0}},
        "unregistered": {"any": {"rate": 0.0035, "cap": 1600.0}},
    },
}


def calculate_tob(
    amount_eur: float, *, legal_form: str, distribution: str,
    registration: str, listed: bool = True, side: str = "buy",
) -> dict[str, Any]:
    """Calculate one secondary-market ETF transaction; both buy and sell taxed."""
    if amount_eur < 0:
        raise ValueError("Transaction amount must be non-negative.")
    legal_form = legal_form.strip().lower()
    distribution = distribution.strip().lower()
    distribution = {"acc": "capitalisation", "accumulating": "capitalisation", "accumulation": "capitalisation", "dist": "distribution", "distributing": "distribution"}.get(distribution, distribution)
    registration = registration.strip().lower()
    side = side.strip().lower()
    if side not in {"buy", "sell"}:
        raise ValueError("side must be 'buy' or 'sell'.")
    if legal_form not in {"sicav", "fcp"}:
        raise ValueError("legal_form must be 'sicav' or 'fcp'.")
    if distribution not in {"distribution", "capitalisation"}:
        raise ValueError("distribution must be 'distribution' or 'capitalisation'.")
    if registration not in {"fsma", "eea", "unregistered", "unknown"}:
        raise ValueError("registration must be fsma, eea, unregistered or unknown.")
    if not listed:
        return {
            "status": "not_applicable_or_manual_review",
            "reason": "This calculator is for listed secondary-market ETFs; unlisted fund operations need separate treatment.",
            "tax_eur": None,
        }
    if registration == "unknown":
        return {
            "status": "needs_registration_evidence",
            "reason": "FSMA/EEA registration status is required to determine the applicable TOB rate.",
            "tax_eur": None,
        }
    registered = registration in {"fsma", "eea"}
    if legal_form == "sicav":
        if registered:
            key = distribution if distribution == "distribution" else (
                "capitalisation_fsma" if registration == "fsma" else "capitalisation_eea"
            )
            rule = TOB_RULES["sicav"]["registered"][key]
        else:
            rule = TOB_RULES["sicav"]["unregistered"][distribution]
    else:
        rule = TOB_RULES["fcp"]["registered" if registered else "unregistered"]["any"]
    raw = amount_eur * rule["rate"]
    tax = min(raw, rule["cap"])
    return {
        "status": "estimated_from_classification",
        "side": side,
        "taxable_amount_eur": round(amount_eur, 2),
        "rate_pct": round(rule["rate"] * 100, 4),
        "uncapped_tax_eur": round(raw, 2),
        "cap_eur": rule["cap"],
        "tob_eur": round(tax, 2),
        "rules_version": RULES_VERSION,
        "effective_from": RULES_EFFECTIVE_FROM,
        "source": "Wikifin / FSMA",
        "source_url": TOB_SOURCE,
        "note": "Buy and sell are each taxed separately. Confirm legal form and registration for the exact ETF share class before trading.",
    }


def calculate_net_dividend_yield(
    *, annual_distribution_per_share: float, market_price: float,
    legal_form: str, fcp_breakdown_available: bool = False,
    belgian_withholding_rate_pct: float | None = None,
    investor_level_foreign_withholding_pct: float = 0.0, shares: float = 1.0,
) -> dict[str, Any]:
    """Estimate cash yield after withholding, respecting SICAV/FCP differences.

    For an FCP, a valid income breakdown can exempt the cash distribution from
    a second withholding at distribution; the investor may still owe tax on the
    transparent underlying income. Without a breakdown, the distribution may
    be recharacterised as interest at 30%.
    """
    legal_form = legal_form.strip().lower()
    if legal_form not in {"sicav", "fcp"}:
        raise ValueError("legal_form must be sicav or fcp; do not guess the fund form.")
    if market_price <= 0 or annual_distribution_per_share < 0 or shares < 0:
        raise ValueError("Price must be positive; distribution and shares cannot be negative.")
    default_rate = 0.0 if legal_form == "fcp" and fcp_breakdown_available else 30.0
    belgian_rate = default_rate if belgian_withholding_rate_pct is None else belgian_withholding_rate_pct
    for label, rate in (
        ("Belgian withholding", belgian_rate),
        ("Investor-level foreign withholding", investor_level_foreign_withholding_pct),
    ):
        if not 0 <= rate <= 100:
            raise ValueError(f"{label} rate must be between 0 and 100.")
    gross = annual_distribution_per_share * shares
    foreign_tax = gross * investor_level_foreign_withholding_pct / 100
    after_foreign = gross - foreign_tax
    belgian_tax = after_foreign * belgian_rate / 100
    net = after_foreign - belgian_tax
    invested_value = market_price * shares
    return {
        "status": "cash_yield_after_assumed_withholding",
        "legal_form": legal_form,
        "fcp_breakdown_available": fcp_breakdown_available if legal_form == "fcp" else None,
        "gross_distribution_eur": round(gross, 4),
        "invested_market_value_eur": round(invested_value, 4),
        "investor_level_foreign_withholding_eur": round(foreign_tax, 4),
        "belgian_withholding_rate_pct": belgian_rate,
        "belgian_withholding_eur": round(belgian_tax, 4),
        "net_distribution_eur": round(net, 4),
        "gross_yield_pct": round(gross / invested_value * 100, 4) if invested_value else None,
        "net_cash_yield_pct": round(net / invested_value * 100, 4) if invested_value else None,
        "tax_rules_version": RULES_VERSION,
        "source": "FPS Finance / Wikifin / Belgian ruling commission",
        "source_url": PM_SOURCE,
        "limitations": [
            "SICAV distributions are normally dividends subject to 30% Belgian withholding; exceptions require separate evidence.",
            "An FCP with a valid income breakdown can avoid a second withholding on distribution, but underlying income remains taxable under transparency rules.",
            "An FCP without a valid breakdown can have distributions treated as interest and taxed at 30%.",
            "The ordinary-share dividend exemption does not apply to distributions by or through investment funds.",
            "Foreign withholding inside the ETF portfolio is not modelled; it is generally already reflected in NAV/distributions.",
            "Investor-level foreign withholding is an optional scenario input; exact treaty/custody treatment needs instrument-specific evidence.",
            "This is cash yield after assumed withholding, not a full look-through tax calculation for FCPs.",
            "Accumulating ETF share classes do not pay cash distributions; this calculation is not applicable to them.",
        ],
    }


def calculate_reynders_tax(
    *, debt_claims_pct: float, acquired_on: str,
    taxable_debt_income_eur: float | None = None, tax_rate_pct: float = 30.0,
) -> dict[str, Any]:
    """Screen for Reynders tax; calculate only with fund-reported taxable income.

    The tax base is the fund-reported taxable debt-income component (TIS), not
    the whole capital gain or a guessed percentage of it.
    """
    if not 0 <= debt_claims_pct <= 100:
        raise ValueError("Debt claims percentage must be between 0 and 100.")
    if taxable_debt_income_eur is not None and taxable_debt_income_eur < 0:
        raise ValueError("Taxable debt income cannot be negative.")
    acquired = date.fromisoformat(acquired_on)
    threshold = 25.0 if acquired < date(2018, 1, 1) else 10.0
    in_scope = debt_claims_pct > threshold
    tax_base = taxable_debt_income_eur if in_scope else 0.0
    tax = tax_base * tax_rate_pct / 100 if tax_base is not None else None
    return {
        "status": ("calculated_from_fund_tax_data" if tax is not None else "in_scope_tax_base_missing") if in_scope else "threshold_not_met",
        "debt_claims_pct": debt_claims_pct,
        "threshold_pct": threshold,
        "taxable_debt_income_eur": round(tax_base, 2) if tax_base is not None else None,
        "estimated_reynders_withholding_eur": round(tax, 2) if tax is not None else None,
        "rate_pct": tax_rate_pct,
        "source_note": "30% on the fund-reported taxable debt-income component; do not substitute the full realized gain.",
    }
