"""Secondary Offering / ATM Dilution Velocity Overlay.

Scores at-the-market and secondary-offering issuance velocity plus the
recent share-count delta as a supply-pressure layer, distinct from
10b5-1 buybacks.

Live EDGAR S-3 / 424B5 parsers are an explicit future hook. Current
source is always labeled synthetic_proxy when live filings are
unavailable.

Preferred columns: dil_atm_velocity, dil_share_delta, dil_boost, dil_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


ATM_HEAVY = {
    "SMCI", "PLTR", "RIOT", "MARA", "HOOD", "COIN", "SOFI", "RIVN",
    "LCID", "AMC", "GME", "IONQ", "RKLB", "ASTS", "CVNA",
}


def _clip(v: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_dilution_atm(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    dil_cfg = cfg.get("dilution_atm", {})
    if not dil_cfg.get("enabled", True):
        return {
            "dil_atm_velocity": 0.0,
            "dil_share_delta": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "ATM dilution overlay disabled",
            "source": "disabled",
        }

    vel_hot = float(dil_cfg.get("velocity_hot", 0.55))
    vel_cold = float(dil_cfg.get("velocity_cold", 0.18))
    delta_hot = float(dil_cfg.get("share_delta_hot", 0.04))
    delta_cold = float(dil_cfg.get("share_delta_cold", 0.005))
    narrative_hot = float(dil_cfg.get("narrative_hot", 1.4))
    min_conf = float(dil_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 5517
    rng = random.Random(seed)
    row = row or {}

    if tkr in ATM_HEAVY:
        velocity = rng.uniform(0.28, 0.92)
        share_delta = rng.uniform(0.01, 0.11)
    else:
        velocity = rng.uniform(0.02, 0.38)
        share_delta = rng.uniform(-0.01, 0.025)

    narr = float(
        row.get("predicted_velocity")
        or row.get("sentiment_velocity")
        or rng.uniform(0.3, 3.4)
    )
    score = _clip(0.62 * (velocity - 0.35) + 0.38 * (share_delta / 0.06))

    parts = [
        f"atm_vel={velocity:.2f}",
        f"share_delta={share_delta:+.2%}",
    ]
    boost = 0
    confidence = 0.40 + 0.12 * min(velocity, 1.0)

    supply = velocity >= vel_hot and share_delta >= delta_hot and narr >= narrative_hot * 0.40
    paused = velocity <= vel_cold and share_delta <= delta_cold and narr >= narrative_hot * 0.50

    if supply:
        boost = -1
        confidence = min(0.91, 0.48 + 0.28 * velocity + 0.10 * min(narr / 4.0, 1.0))
        parts.append("ATM issuance accelerating — secondary supply caution")
    elif paused:
        boost = 1
        confidence = min(0.88, 0.46 + 0.20 * (1.0 - velocity) + 0.10 * min(narr / 4.0, 1.0))
        parts.append("ATM paused and share count stable into confirming narrative — soft boost")
    else:
        parts.append("secondary / ATM dilution overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "dil_atm_velocity": round(float(velocity), 4),
        "dil_share_delta": round(float(share_delta), 4),
        "dil_score": round(float(score), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_dilution_atm_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate secondary / ATM dilution velocity into a row."""
    mom = detect_dilution_atm(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "dil_atm_velocity": mom["dil_atm_velocity"],
            "dil_share_delta": mom["dil_share_delta"],
            "dil_score": mom.get("dil_score", 0.0),
            "dil_boost": mom["signal_boost"],
            "dil_confidence": mom["confidence"],
            "dil_reason": mom["reason"],
            "dil_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | dil {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | dil {mom['reason']}"
    else:
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | dil: {mom['reason']}"
    return row
