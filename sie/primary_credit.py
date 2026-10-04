"""Primary Credit Issuance / New-Issue Concession & Supply Pressure Overlay.

Scores the new-issue concession (bps cheap to the issuer secondary curve)
and the primary calendar supply score. Distinct from TRACE secondary
customer flow and from CDS spread momentum.

Live syndicate books / TRACE new-issue prints are an explicit future hook.
Current source is always labeled synthetic_proxy when the calendar is
unavailable.

Preferred columns: pci_concession_bp, pci_supply_score, pci_boost, pci_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


# Frequent IG/HY primary issuers — wide books and crowded calendars.
PCI_HEAVY = {
    "T", "VZ", "F", "BA", "CVNA", "AMC", "WBD", "PARA", "RIVN", "LCID",
}
# Cash-rich names that rarely print primary paper.
PCI_QUIET = {
    "AAPL", "MSFT", "NVDA", "GOOGL", "META", "AVGO",
}


def _clip(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_primary_credit(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    pci_cfg = cfg.get("primary_credit", {})
    if not pci_cfg.get("enabled", True):
        return {
            "pci_concession_bp": 0.0,
            "pci_supply_score": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Primary credit issuance overlay disabled",
            "source": "disabled",
        }

    concession_tight = float(pci_cfg.get("concession_tight_bp", 8.0))
    concession_wide = float(pci_cfg.get("concession_wide_bp", 22.0))
    supply_hot = float(pci_cfg.get("supply_hot", 0.62))
    supply_cold = float(pci_cfg.get("supply_cold", 0.28))
    narrative_hot = float(pci_cfg.get("narrative_hot", 1.4))
    min_conf = float(pci_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 5252
    rng = random.Random(seed)
    row = row or {}

    if tkr in PCI_HEAVY:
        concession_bp = rng.uniform(14.0, 48.0)
        supply_score = rng.uniform(0.58, 0.96)
    elif tkr in PCI_QUIET:
        concession_bp = rng.uniform(0.0, 11.0)
        supply_score = rng.uniform(0.04, 0.32)
    else:
        concession_bp = rng.uniform(4.0, 28.0)
        supply_score = rng.uniform(0.18, 0.72)

    narr = float(
        row.get("predicted_velocity")
        or row.get("sentiment_velocity")
        or rng.uniform(0.3, 3.4)
    )
    # Higher concession and higher supply both pressure the equity/credit tape.
    pressure = _clip((concession_bp / 40.0) * 0.55 + supply_score * 0.45)

    parts = [
        f"concession={concession_bp:.1f}bp",
        f"supply={supply_score:.2f}",
    ]
    boost = 0
    confidence = 0.36 + 0.22 * (1.0 - abs(supply_score - 0.45))

    scarce = (
        concession_bp <= concession_tight
        and supply_score <= supply_cold
        and narr >= narrative_hot * 0.45
    )
    flooded = concession_bp >= concession_wide and supply_score >= supply_hot

    if scarce:
        boost = 1
        confidence = min(
            0.90,
            0.48
            + 0.18 * (1.0 - concession_bp / max(concession_tight, 1.0))
            + 0.12 * (1.0 - supply_score)
            + 0.08 * min(narr / 4.0, 1.0),
        )
        parts.append("tight new-issue concession and scarce primary supply — soft boost")
    elif flooded:
        boost = -1
        confidence = min(
            0.92,
            0.50 + 0.18 * min(concession_bp / 40.0, 1.0) + 0.16 * supply_score,
        )
        parts.append("wide new-issue concession into a crowded primary calendar — supply-pressure caution")
    else:
        parts.append("primary credit issuance / concession overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "pci_concession_bp": round(float(concession_bp), 2),
        "pci_supply_score": round(float(supply_score), 4),
        "pci_pressure": round(float(pressure), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_primary_credit_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate new-issue concession and primary supply pressure into a row."""
    mom = detect_primary_credit(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "pci_concession_bp": mom["pci_concession_bp"],
            "pci_supply_score": mom["pci_supply_score"],
            "pci_pressure": mom.get("pci_pressure", 0.0),
            "pci_boost": mom["signal_boost"],
            "pci_confidence": mom["confidence"],
            "pci_reason": mom["reason"],
            "pci_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | pci {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | pci {mom['reason']}"
    return row
