"""Retail Brokerage Order-Flow Imbalance Overlay.

Scores retail buy/sell imbalance and heat from brokerage order-flow
proxies (Robinhood/Public/Webull-style participation) as an orthogonal
confirmation layer to dark-pool, unusual-options, and social-intent
overlays.

Live FINRA ATS / brokerage-flow feeds are an explicit future hook.
Current source is always labeled synthetic_proxy when live data is
unavailable.

Preferred columns: rflow_imbalance, rflow_heat, rflow_boost, rflow_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


RETAIL_HEAVY_UNIVERSE = {
    "AAPL", "TSLA", "NVDA", "AMD", "AMZN", "META", "GME", "AMC",
    "PLTR", "SOFI", "NIO", "RIVN", "COIN", "HOOD", "MARA", "RIOT",
    "SMCI", "INTC", "MSFT", "GOOGL",
}


def _clip(v: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_retail_flow(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    rf_cfg = cfg.get("retail_flow", {})
    if not rf_cfg.get("enabled", True):
        return {
            "rflow_imbalance": 0.0,
            "rflow_heat": 0.0,
            "rflow_buy_share": 0.5,
            "rflow_notional": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Retail order-flow overlay disabled",
            "source": "disabled",
        }

    imb_hot = float(rf_cfg.get("imbalance_hot", 0.28))
    imb_cold = float(rf_cfg.get("imbalance_cold", -0.28))
    heat_hot = float(rf_cfg.get("heat_hot", 0.62))
    heat_cold = float(rf_cfg.get("heat_cold", 0.22))
    vel_hot = float(rf_cfg.get("narrative_hot", 1.4))
    min_conf = float(rf_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 4096
    rng = random.Random(seed)
    row = row or {}

    if tkr in RETAIL_HEAVY_UNIVERSE:
        imbalance = rng.uniform(-0.55, 0.62)
        heat = rng.uniform(0.22, 0.95)
        notional = rng.uniform(0.35, 1.40)
    else:
        imbalance = rng.uniform(-0.32, 0.34)
        heat = rng.uniform(0.08, 0.58)
        notional = rng.uniform(0.05, 0.70)

    buy_share = _clip(0.50 + 0.50 * imbalance, 0.05, 0.95)
    vel = float(
        row.get("predicted_velocity")
        or row.get("auth_filtered_velocity")
        or row.get("sentiment_velocity")
        or rng.uniform(0.2, 3.8)
    )
    auth = float(row.get("auth_score") or 0.55)
    dp_ratio = float(row.get("dp_ratio") or row.get("dark_pool_ratio") or 0.0)

    score = _clip(
        0.55 * imbalance
        + 0.25 * (heat - 0.40)
        + 0.12 * (notional - 0.40)
        + 0.08 * max(dp_ratio, 0.0)
    )

    parts = [
        f"rflow imbalance={imbalance:+.2f}",
        f"heat={heat:.2f}",
        f"buy_share={buy_share:.2f}",
        f"notional={notional:.2f}",
    ]
    boost = 0
    confidence = 0.42 + 0.16 * auth

    flow_confirm = (
        imbalance >= imb_hot
        and heat >= heat_hot
        and vel >= vel_hot * 0.55
    )
    flow_warn = (
        imbalance <= imb_cold
        and heat >= heat_hot * 0.85
        and vel >= vel_hot * 0.70
    )

    if flow_confirm:
        boost = 1
        confidence = min(0.92, 0.48 + 0.26 * abs(score) + 0.14 * auth)
        parts.append(
            "retail buy-imbalance + heat confirming narrative — soft boost"
        )
    elif flow_warn:
        boost = -1
        confidence = min(0.90, 0.46 + 0.24 * abs(min(score, 0)) + 0.14 * max(vel / 4.0, 0))
        parts.append(
            "retail sell-imbalance into elevated heat — caution"
        )
    else:
        parts.append("retail order-flow overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "rflow_imbalance": round(float(imbalance), 4),
        "rflow_heat": round(float(heat), 4),
        "rflow_buy_share": round(float(buy_share), 4),
        "rflow_notional": round(float(notional), 4),
        "rflow_score": round(float(score), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_retail_flow_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate retail brokerage order-flow imbalance into a row."""
    mom = detect_retail_flow(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "rflow_imbalance": mom["rflow_imbalance"],
            "rflow_heat": mom["rflow_heat"],
            "rflow_buy_share": mom.get("rflow_buy_share", 0.5),
            "rflow_notional": mom.get("rflow_notional", 0.0),
            "rflow_score": mom.get("rflow_score", 0.0),
            "rflow_boost": mom["signal_boost"],
            "rflow_confidence": mom["confidence"],
            "rflow_reason": mom["reason"],
            "rflow_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | retail-flow {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | retail-flow {mom['reason']}"
    else:
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | retail-flow: {mom['reason']}"
    return row
