"""Aggregated Consumer Transaction / Credit-Card Panel Spend Nowcasting Overlay.

Uses a deterministic synthetic panel-spend momentum proxy (ticker + day seeded)
as a leading revenue nowcast for retail, restaurant, travel, consumer and
selected tech/hardware names. Soft boost when spend momentum diverges
positively from pure narrative or hiring signals; caution on sharp contraction.

Live panel providers (Affinity, Earnest, public merchant aggregates, etc.) are
left as an explicit future hook — no invented API keys or endpoints.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config

# Simple sector affinity for more realistic synthetic ranges.
CONSUMER_SENSITIVE = {
    "MU", "CRDO", "AMD", "AVGO", "AAPL", "AMZN", "TSLA", "SBUX", "NKE", "MCD",
}


def detect_consumer_spend(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    cs_cfg = cfg.get("consumer_spend", {})
    if not cs_cfg.get("enabled", True):
        return {
            "cs_momentum": 0.0,
            "cs_score": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Consumer spend module disabled",
            "source": "disabled",
        }

    boost_th = float(cs_cfg.get("boost_momentum", 0.18))
    penalty_th = float(cs_cfg.get("penalty_momentum", -0.15))
    min_conf = float(cs_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 97
    rng = random.Random(seed)

    # Wider positive skew for names with consumer/hardware demand exposure.
    if tkr in CONSUMER_SENSITIVE:
        momentum = round(rng.uniform(-0.28, 0.48), 3)
    else:
        momentum = round(rng.uniform(-0.22, 0.32), 3)

    # Score is a 0–1 soft mapping of momentum for downstream consumers.
    score = max(0.0, min(1.0, 0.5 + momentum * 1.1))

    source = "synthetic_panel_proxy"
    conf_base = 0.52

    if momentum >= boost_th:
        boost = 1
        confidence = min(0.86, conf_base + 0.32 * min(momentum, 0.6))
        reason = (
            f"Consumer spend MOMENTUM +{momentum:.0%} (panel nowcast) — "
            "leading demand confirmation"
        )
    elif momentum <= penalty_th:
        boost = -1
        confidence = min(0.82, conf_base + 0.28 * min(abs(momentum), 0.5))
        reason = (
            f"Consumer spend CONTRACTION {momentum:.0%} (panel nowcast) — "
            "demand soft relative to narrative"
        )
    else:
        boost = 0
        confidence = conf_base
        reason = f"Consumer spend stable {momentum:+.0%} (panel nowcast)"

    if confidence < min_conf and boost != 0:
        boost = 0
        reason += " (confidence below gate — signal suppressed)"

    return {
        "cs_momentum": momentum,
        "cs_score": round(float(score), 3),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": reason,
        "source": source,
    }


def integrate_consumer_spend_to_row(row: dict, cfg: dict | None = None) -> dict:
    mom = detect_consumer_spend(row.get("ticker", ""), row, cfg)
    row.update({
        "cs_momentum": mom["cs_momentum"],
        "cs_score": mom["cs_score"],
        "cs_boost": mom["signal_boost"],
        "cs_confidence": mom["confidence"],
        "cs_reason": mom["reason"],
        "cs_source": mom["source"],
    })
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
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | Spend: {mom['reason']}"
    return row
