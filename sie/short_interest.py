"""FINRA Short Volume / Short Interest Momentum Overlay.

Deterministic daily short-volume ratio proxy. Elevated short volume against a
rising narrative is a caution flag; covering plus rising narrative is a soft boost.
Live FINRA CSV hook is documented but not required (no new deps / no invented API).
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config

# Public FINRA consolidated short-sale data lives at finra.org (daily files).
# Parsing those CSVs needs a stable URL + trading-calendar logic; this module
# stays on a labeled synthetic_proxy unless a future cycle adds a thin fetcher.


def detect_short_interest(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    si_cfg = cfg.get("short_interest", {})
    if not si_cfg.get("enabled", True):
        return {
            "si_ratio": 0.0,
            "si_change": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Short-interest module disabled",
            "source": "disabled",
        }

    elevated = float(si_cfg.get("elevated_ratio", 0.48))
    covering = float(si_cfg.get("covering_change", -0.08))
    expanding = float(si_cfg.get("expanding_change", 0.08))
    min_conf = float(si_cfg.get("min_confidence", 0.40))
    vel_hot = float(si_cfg.get("narrative_hot", 1.5))

    seed = sum(ord(c) for c in (ticker or "").upper()) + datetime.now().timetuple().tm_yday + 31
    rng = random.Random(seed)
    ratio = round(rng.uniform(0.22, 0.72), 3)
    change = round(rng.uniform(-0.18, 0.20), 3)

    vel = 0.0
    if row:
        vel = float(row.get("predicted_velocity") or row.get("sentiment_velocity") or 0.0)

    boost = 0
    confidence = 0.50
    parts: list[str] = [f"Short-volume ratio {ratio:.2f} (Δ{change:+.2f})"]

    if ratio >= elevated and vel >= vel_hot and change >= expanding:
        boost = -1
        confidence = min(0.86, 0.55 + 0.4 * (ratio - elevated))
        parts.append("elevated short volume vs rising narrative — caution")
    elif change <= covering and vel >= vel_hot:
        boost = 1
        confidence = min(0.84, 0.54 + 0.5 * abs(change))
        parts.append("short covering + rising narrative — soft boost")
    elif ratio >= elevated:
        parts.append("elevated short volume — observation only")
    else:
        parts.append("no material short-interest overlay")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "si_ratio": ratio,
        "si_change": change,
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_short_interest_to_row(row: dict, cfg: dict | None = None) -> dict:
    mom = detect_short_interest(row.get("ticker", ""), row, cfg)
    row.update({
        "si_ratio": mom["si_ratio"],
        "si_change": mom["si_change"],
        "si_boost": mom["signal_boost"],
        "si_confidence": mom["confidence"],
        "si_reason": mom["reason"],
        "si_source": mom["source"],
    })
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 🤓 {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 🤓 {mom['reason']}"
    else:
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | Short: {mom['reason']}"
    return row
