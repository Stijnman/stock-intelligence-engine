"""Alternative-Data Provenance & AI-Synthetic Contamination Confidence Overlay.

Scores how traceable an alternative-data print is (primary filing, exchange,
or named vendor versus scraped social) and whether an independent cross-check
agrees. Distinct from the authenticity-filtered social velocity overlay and
from news-source authority weighting.

Live vendor attestation parsers are an explicit future hook. Current source is
always labeled synthetic_proxy when a signed provenance chain is unavailable.

Preferred columns: adp_provenance, adp_crosscheck, adp_boost, adp_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


# Names whose public alt-data stack is usually primary-source or vendor-attested.
ADP_CLEAN = {
    "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "JPM", "UNH", "AVGO", "COST",
}
# Names that routinely attract synthetic social prints and thin cross-checks.
ADP_CONTAMINATED = {
    "AMC", "GME", "CVNA", "RIVN", "LCID", "MARA", "BBBY", "MULN", "FFIE",
}

PROVENANCE_LABELS = ("primary", "vendor", "scraped", "synthetic")


def _clip(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_alt_data_provenance(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    adp_cfg = cfg.get("alt_data_provenance", {})
    if not adp_cfg.get("enabled", True):
        return {
            "adp_provenance": 0.0,
            "adp_crosscheck": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Alternative-data provenance overlay disabled",
            "source": "disabled",
        }

    prov_hot = float(adp_cfg.get("provenance_hot", 0.68))
    prov_cold = float(adp_cfg.get("provenance_cold", 0.34))
    cross_hot = float(adp_cfg.get("crosscheck_hot", 0.62))
    cross_cold = float(adp_cfg.get("crosscheck_cold", 0.28))
    narrative_hot = float(adp_cfg.get("narrative_hot", 1.4))
    min_conf = float(adp_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 2540
    rng = random.Random(seed)
    row = row or {}

    if tkr in ADP_CLEAN:
        provenance = rng.uniform(0.70, 0.96)
        crosscheck = rng.uniform(0.64, 0.92)
        label = "primary" if provenance >= 0.82 else "vendor"
    elif tkr in ADP_CONTAMINATED:
        provenance = rng.uniform(0.06, 0.32)
        crosscheck = rng.uniform(0.04, 0.30)
        label = "synthetic" if provenance <= 0.18 else "scraped"
    else:
        provenance = rng.uniform(0.28, 0.74)
        crosscheck = rng.uniform(0.22, 0.70)
        label = PROVENANCE_LABELS[rng.randrange(len(PROVENANCE_LABELS))]

    narr = float(
        row.get("predicted_velocity")
        or row.get("sentiment_velocity")
        or 0.0
    )
    parts = [
        f"label={label}",
        f"provenance={provenance:.2f}",
        f"crosscheck={crosscheck:.2f}",
    ]
    confidence = _clip(0.40 + 0.30 * provenance + 0.18 * crosscheck)
    boost = 0

    clean_confirm = (
        provenance >= prov_hot
        and crosscheck >= cross_hot
        and label in ("primary", "vendor")
        and narr >= narrative_hot * 0.45
    )
    synthetic_heat = (
        (provenance <= prov_cold or crosscheck <= cross_cold or label == "synthetic")
        and narr >= narrative_hot * 0.35
    )

    if clean_confirm:
        boost = 1
        confidence = min(
            0.93,
            0.48
            + 0.22 * provenance
            + 0.16 * crosscheck
            + 0.06 * min(narr / 4.0, 1.0),
        )
        parts.append("attested alt-data cross-checks into a confirming narrative — soft boost")
    elif synthetic_heat:
        boost = -1
        confidence = min(
            0.91,
            0.46 + 0.22 * (1.0 - provenance) + 0.16 * (1.0 - crosscheck),
        )
        parts.append("narrative heat on thin provenance or failed cross-check — caution")
    else:
        parts.append("alternative-data provenance overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "adp_provenance": round(float(provenance), 4),
        "adp_crosscheck": round(float(crosscheck), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_alt_data_provenance_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate provenance and cross-check confidence into a row."""
    mom = detect_alt_data_provenance(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "adp_provenance": mom["adp_provenance"],
            "adp_crosscheck": mom["adp_crosscheck"],
            "adp_boost": mom["signal_boost"],
            "adp_confidence": mom["confidence"],
            "adp_reason": mom["reason"],
            "adp_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | adp {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | adp {mom['reason']}"
    return row
