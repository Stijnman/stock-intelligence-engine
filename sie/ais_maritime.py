"""AIS Maritime Traffic & Port Congestion Overlay.

Scores key-port congestion and vessel waiting times from AIS maritime traffic
proxies. Soft boost when congestion eases and waiting times fall into a
confirming narrative; caution on rising congestion or extended wait hours while
narrative heat remains elevated.

Live AIS feeds are an explicit future hook. Current source is always labeled
synthetic_proxy when a live feed is unavailable.

Preferred columns: ais_congestion, ais_wait_hrs, ais_boost, ais_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


# Tickers with high maritime / port / supply-chain / energy shipping exposure.
AIS_HOT = {
    "ZIM", "MATX", "DAC", "AMZN", "WMT", "TGT", "COST", "XOM", "CVX", "TSLA",
}
# Tickers where maritime congestion signals are typically less relevant or adverse.
AIS_COLD = {
    "INTC", "IBM", "CSCO", "ORCL", "PFE", "JNJ", "BA",
}


def _clip(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_ais_maritime(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    a_cfg = cfg.get("ais_maritime", {})
    if not a_cfg.get("enabled", True):
        return {
            "ais_congestion": 0.0,
            "ais_wait_hrs": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "AIS maritime overlay disabled",
            "source": "disabled",
        }

    cong_hot = float(a_cfg.get("cong_hot", 0.72))
    cong_cold = float(a_cfg.get("cong_cold", 0.32))
    wait_hot = float(a_cfg.get("wait_hot", 48.0))
    wait_cold = float(a_cfg.get("wait_cold", 12.0))
    narrative_hot = float(a_cfg.get("narrative_hot", 1.4))
    min_conf = float(a_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 6731
    rng = random.Random(seed)
    row = row or {}
    narr = float(row.get("predicted_velocity") or row.get("narrative_velocity") or 1.0)

    if tkr in AIS_HOT:
        congestion = rng.uniform(0.18, 0.42)
        wait_hrs = rng.uniform(6.0, 18.0)
    elif tkr in AIS_COLD:
        congestion = rng.uniform(0.68, 0.92)
        wait_hrs = rng.uniform(36.0, 72.0)
    else:
        congestion = rng.uniform(0.35, 0.65)
        wait_hrs = rng.uniform(14.0, 36.0)

    # Lower congestion and wait are constructive (easing).
    cong_strength = _clip((cong_hot - congestion) / max(cong_hot - cong_cold, 1e-6))
    wait_strength = _clip((wait_hot - wait_hrs) / max(wait_hot - wait_cold, 1e-6))
    confidence = _clip(0.38 + 0.30 * cong_strength + 0.22 * wait_strength)

    parts = [
        f"ais_congestion={congestion:.2f}",
        f"ais_wait_hrs={wait_hrs:.1f}",
        f"narrative={narr:.2f}",
    ]
    boost = 0
    confirm = congestion <= cong_cold and wait_hrs <= wait_cold and narr >= narrative_hot
    caution = congestion >= cong_hot and wait_hrs >= wait_hot and narr >= narrative_hot * 0.45

    if confirm:
        boost = 1
        confidence = min(0.95, confidence + 0.07)
        parts.append(
            "key-port congestion easing and vessel waiting times falling into confirming narrative — soft boost"
        )
    elif caution:
        boost = -1
        confidence = min(0.93, confidence + 0.06)
        parts.append(
            "rising AIS port congestion or extended vessel wait hours while narrative heat remains elevated — caution"
        )
    else:
        parts.append("AIS maritime traffic / port congestion overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "ais_congestion": round(float(congestion), 4),
        "ais_wait_hrs": round(float(wait_hrs), 2),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_ais_maritime_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate AIS maritime traffic & port congestion into a row."""
    mom = detect_ais_maritime(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "ais_congestion": mom["ais_congestion"],
            "ais_wait_hrs": mom["ais_wait_hrs"],
            "ais_boost": mom["signal_boost"],
            "ais_confidence": mom["confidence"],
            "ais_reason": mom["reason"],
            "ais_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | ais {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | ais {mom['reason']}"
    return row
