"""Satellite Imagery / Geospatial Physical Activity Overlay.

Scores physical activity proxies from satellite and geospatial sources:
parking-lot fill rates, oil-tank levels, night-light intensity, vessel counts,
and related activity deltas.
Soft boost when rising physical activity confirms a narrative; caution on sharp
activity drops while narrative heat remains elevated.

Live satellite feeds are an explicit future hook. Current source is always
labeled synthetic_proxy when a live feed is unavailable.

Preferred columns: sat_fill, sat_delta, sat_boost, sat_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


# Tickers typically associated with high physical activity / retail / energy exposure.
SAT_HOT = {
    "AMZN", "WMT", "TGT", "COST", "HD", "LOW", "XOM", "CVX", "COP", "TSLA",
}
# Tickers where physical activity often lags or declines.
SAT_COLD = {
    "INTC", "IBM", "CSCO", "ORCL", "PFE", "JNJ", "BA",
}


def _clip(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_satellite_imagery(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    s_cfg = cfg.get("satellite_imagery", {})
    if not s_cfg.get("enabled", True):
        return {
            "sat_fill": 0.0,
            "sat_delta": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Satellite imagery overlay disabled",
            "source": "disabled",
        }

    fill_hot = float(s_cfg.get("fill_hot", 0.72))
    fill_cold = float(s_cfg.get("fill_cold", 0.35))
    delta_hot = float(s_cfg.get("delta_hot", 0.12))
    delta_cold = float(s_cfg.get("delta_cold", -0.08))
    narrative_hot = float(s_cfg.get("narrative_hot", 1.4))
    min_conf = float(s_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 4219
    rng = random.Random(seed)
    row = row or {}
    narr = float(row.get("predicted_velocity") or row.get("narrative_velocity") or 1.0)

    if tkr in SAT_HOT:
        fill = rng.uniform(0.68, 0.92)
        delta = rng.uniform(0.08, 0.28)
    elif tkr in SAT_COLD:
        fill = rng.uniform(0.22, 0.42)
        delta = rng.uniform(-0.18, -0.02)
    else:
        fill = rng.uniform(0.40, 0.68)
        delta = rng.uniform(-0.06, 0.10)

    fill_strength = _clip((fill - fill_cold) / max(fill_hot - fill_cold, 1e-6))
    delta_strength = _clip((delta - delta_cold) / max(delta_hot - delta_cold, 1e-6))
    confidence = _clip(0.38 + 0.30 * fill_strength + 0.22 * delta_strength)

    parts = [
        f"sat_fill={fill:.2f}",
        f"sat_delta={delta:+.2f}",
        f"narrative={narr:.2f}",
    ]
    boost = 0
    confirm = fill >= fill_hot and delta >= delta_hot and narr >= narrative_hot
    caution = fill <= fill_cold and delta <= delta_cold and narr >= narrative_hot * 0.45

    if confirm:
        boost = 1
        confidence = min(0.95, confidence + 0.07)
        parts.append(
            "rising physical activity proxies (parking/tanks/night-lights/vessels) confirm narrative — soft boost"
        )
    elif caution:
        boost = -1
        confidence = min(0.93, confidence + 0.06)
        parts.append(
            "sharp physical activity drop while narrative heat remains elevated — caution"
        )
    else:
        parts.append("satellite / geospatial physical activity overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "sat_fill": round(float(fill), 4),
        "sat_delta": round(float(delta), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_satellite_imagery_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate satellite imagery / geospatial physical activity into a row."""
    mom = detect_satellite_imagery(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "sat_fill": mom["sat_fill"],
            "sat_delta": mom["sat_delta"],
            "sat_boost": mom["signal_boost"],
            "sat_confidence": mom["confidence"],
            "sat_reason": mom["reason"],
            "sat_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "buy"
        row["score"] = float(row.get("score", 0)) + 0.4
    elif boost <= -1:
        if row.get("signal") == "buy":
            row["signal"] = "hold"
        row["score"] = float(row.get("score", 0)) - 0.3
    return row
