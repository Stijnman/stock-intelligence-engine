"""Listed Event-Contract Book Depth vs Offshore Prediction-Market Basis Overlay.

Scores listed event-contract book depth versus offshore prediction-market basis.
Soft boost when listed depth supports a rich constructive basis into a confirming narrative;
caution on thin listed depth with adverse basis while narrative heat remains elevated.

Live listed + offshore book feed is an explicit future hook. Current source is always labeled
synthetic_proxy when a live feed is unavailable.

Preferred columns: lec_basis_bps, lec_listed_depth, lec_boost, lec_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


# Tickers with typically deep listed event-contract books and constructive basis.
LEC_HOT = {
    "NVDA", "TSLA", "AMD", "META", "GOOGL", "MSFT", "AMZN", "AAPL", "PLTR", "SMCI",
}
# Tickers with typically thin listed depth or adverse basis.
LEC_COLD = {
    "INTC", "IBM", "PFE", "JNJ", "BA", "XOM", "CVX", "GE",
}


def _clip(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_listed_event_contract(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    l_cfg = cfg.get("listed_event_contract", {})
    if not l_cfg.get("enabled", True):
        return {
            "lec_basis_bps": 0.0,
            "lec_listed_depth": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Listed event-contract basis overlay disabled",
            "source": "disabled",
        }

    basis_hot = float(l_cfg.get("basis_hot_bps", 35.0))
    basis_cold = float(l_cfg.get("basis_cold_bps", -25.0))
    depth_hot = float(l_cfg.get("depth_hot", 0.72))
    depth_cold = float(l_cfg.get("depth_cold", 0.28))
    narrative_hot = float(l_cfg.get("narrative_hot", 1.4))
    min_conf = float(l_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 7741
    rng = random.Random(seed)
    row = row or {}
    narr = float(row.get("predicted_velocity") or row.get("narrative_velocity") or 1.0)

    if tkr in LEC_HOT:
        basis_bps = rng.uniform(18.0, 55.0)
        listed_depth = rng.uniform(0.68, 0.92)
    elif tkr in LEC_COLD:
        basis_bps = rng.uniform(-40.0, -5.0)
        listed_depth = rng.uniform(0.12, 0.38)
    else:
        basis_bps = rng.uniform(-12.0, 28.0)
        listed_depth = rng.uniform(0.38, 0.68)

    basis_strength = _clip((basis_bps - basis_cold) / max(basis_hot - basis_cold, 1e-6))
    depth_strength = _clip((listed_depth - depth_cold) / max(depth_hot - depth_cold, 1e-6))
    confidence = _clip(0.36 + 0.34 * basis_strength + 0.20 * depth_strength)

    parts = [
        f"lec_basis_bps={basis_bps:.1f}",
        f"lec_listed_depth={listed_depth:.2f}",
        f"narrative={narr:.2f}",
    ]
    boost = 0
    confirm = basis_bps >= basis_hot and listed_depth >= depth_hot and narr >= narrative_hot
    caution = basis_bps <= basis_cold and listed_depth <= depth_cold and narr >= narrative_hot * 0.45

    if confirm:
        boost = 1
        confidence = min(0.95, confidence + 0.07)
        parts.append(
            "deep listed event-contract book supports rich constructive basis into confirming narrative — soft boost"
        )
    elif caution:
        boost = -1
        confidence = min(0.93, confidence + 0.06)
        parts.append(
            "thin listed depth with adverse basis while narrative heat remains elevated — caution"
        )
    else:
        parts.append("Listed event-contract basis overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "lec_basis_bps": round(float(basis_bps), 1),
        "lec_listed_depth": round(float(listed_depth), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_listed_event_contract_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate Listed Event-Contract Book Depth vs Offshore Basis into a row."""
    mom = detect_listed_event_contract(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "lec_basis_bps": mom["lec_basis_bps"],
            "lec_listed_depth": mom["lec_listed_depth"],
            "lec_boost": mom["signal_boost"],
            "lec_confidence": mom["confidence"],
            "lec_reason": mom["reason"],
            "lec_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | lec {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | lec {mom['reason']}"
    return row
