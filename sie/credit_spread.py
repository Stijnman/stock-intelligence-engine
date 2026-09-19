"""Corporate Credit Spread / CDS Momentum Overlay.

Tracks relative credit-spread / CDS widening or tightening as a leading
fundamental stress / relief signal. Soft +1 when spreads tighten alongside
rising narrative velocity; -1 on rapid widening even when social heat is
elevated.

Live CDS feeds (Markit, ICE, TRACE OAS, FRED HY/IG OAS) are left as an
explicit future hook. Current source is always labeled synthetic_proxy.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config

# Names that tend to trade with more credit-sensitive synthetic ranges.
CREDIT_SENSITIVE = {
    "MU", "CRDO", "SMCI", "TSLA", "INTC", "AMD", "CERE", "CBRS",
}


def detect_credit_spread(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    cs_cfg = cfg.get("credit_spread", {})
    if not cs_cfg.get("enabled", True):
        return {
            "cds_spread_bp": 0.0,
            "cds_delta_bp": 0.0,
            "cds_direction": "disabled",
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Corporate credit spread / CDS overlay disabled",
            "source": "disabled",
        }

    tighten_bp = float(cs_cfg.get("tighten_bp", -8.0))
    widen_bp = float(cs_cfg.get("widen_bp", 12.0))
    stress_level = float(cs_cfg.get("stress_spread_bp", 180.0))
    min_conf = float(cs_cfg.get("min_confidence", 0.40))
    vel_hot = float(cs_cfg.get("narrative_hot", 1.4))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 419
    rng = random.Random(seed)

    if tkr in CREDIT_SENSITIVE:
        spread_bp = round(rng.uniform(45.0, 320.0), 1)
        delta_bp = round(rng.uniform(-28.0, 34.0), 1)
    else:
        spread_bp = round(rng.uniform(25.0, 160.0), 1)
        delta_bp = round(rng.uniform(-18.0, 22.0), 1)

    if delta_bp <= tighten_bp:
        direction = "tightening"
    elif delta_bp >= widen_bp:
        direction = "widening"
    else:
        direction = "stable"

    vel = 0.0
    if row:
        vel = float(
            row.get("predicted_velocity")
            or row.get("auth_filtered_velocity")
            or row.get("sentiment_velocity")
            or 0.0
        )

    boost = 0
    confidence = 0.50
    parts = [
        f"CDS {spread_bp:.0f}bp (Δ{delta_bp:+.1f}bp, {direction})",
        f"narrative vel {vel:.1f}",
    ]

    if direction == "tightening" and vel >= vel_hot and spread_bp < stress_level:
        boost = 1
        confidence = min(0.88, 0.52 + 0.012 * abs(delta_bp) + 0.06 * min(vel, 4.0))
        parts.append("tightening spreads + rising narrative — confirmation soft boost")
    elif direction == "widening" and (delta_bp >= widen_bp * 1.25 or spread_bp >= stress_level):
        boost = -1
        confidence = min(0.86, 0.50 + 0.010 * abs(delta_bp) + (0.08 if vel >= vel_hot else 0.0))
        parts.append("rapid CDS widening — fundamental stress caution (even if social heat elevated)")
    elif direction == "widening":
        parts.append("modest widening — observation only")
    else:
        parts.append("credit overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "cds_spread_bp": spread_bp,
        "cds_delta_bp": delta_bp,
        "cds_direction": direction,
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_credit_spread_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate corporate credit-spread / CDS momentum into an analysis row."""
    mom = detect_credit_spread(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "cds_spread_bp": mom["cds_spread_bp"],
            "cds_delta_bp": mom["cds_delta_bp"],
            "cds_direction": mom["cds_direction"],
            "cds_boost": mom["signal_boost"],
            "cds_confidence": mom["confidence"],
            "cds_reason": mom["reason"],
            "cds_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 💳 {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 💳 {mom['reason']}"
    else:
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | CDS: {mom['reason']}"
    return row
