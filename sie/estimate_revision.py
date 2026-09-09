"""Analyst Estimate Revision Velocity & Breadth Overlay.

Tracks the speed, direction, and coverage-breadth of consensus EPS/revenue
estimate revisions across the sell-side as a soft confirmation of narrative
durability. Rapid upward revisions with rising breadth produce a soft boost;
sharp downward revisions act as caution even when social heat remains elevated.

Uses a deterministic synthetic proxy (ticker + day seeded) with realistic
revision velocity / breadth ranges. Live feeds (Bloomberg, FactSet, Visible
Alpha, Yahoo Finance estimate history) are left as an explicit future hook —
no invented endpoints. Source is always labeled synthetic_proxy when live
data is unavailable.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config

# Names that historically show higher estimate revision activity in AI/semiconductor themes.
HIGH_REVISION_SENSITIVE = {
    "NVDA", "TSM", "AMD", "AVGO", "MU", "CRDO", "SMCI", "ASML", "AMAT", "LRCX", "KLAC", "CBRS",
}


def detect_estimate_revision(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    er_cfg = cfg.get("estimate_revision", {})
    if not er_cfg.get("enabled", True):
        return {
            "er_velocity": 0.0,
            "er_breadth": 0.0,
            "er_direction": "flat",
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Analyst estimate revision velocity module disabled",
            "source": "disabled",
        }

    boost_vel = float(er_cfg.get("boost_velocity", 0.12))
    penalty_vel = float(er_cfg.get("penalty_velocity", -0.10))
    min_breadth = float(er_cfg.get("min_breadth", 0.35))
    min_conf = float(er_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 97
    rng = random.Random(seed)

    if tkr in HIGH_REVISION_SENSITIVE:
        # AI / semi names: wider range, slight upward bias in current theme
        velocity = round(rng.uniform(-0.28, 0.42), 3)
        breadth = round(rng.uniform(0.25, 0.92), 3)
    else:
        velocity = round(rng.uniform(-0.18, 0.22), 3)
        breadth = round(rng.uniform(0.18, 0.75), 3)

    # Direction label
    if velocity >= 0.08:
        direction = "up"
    elif velocity <= -0.08:
        direction = "down"
    else:
        direction = "flat"

    source = "synthetic_proxy"
    conf_base = 0.52 if tkr in HIGH_REVISION_SENSITIVE else 0.44

    boost = 0
    confidence = conf_base
    parts: list[str] = [
        f"Estimate revision velocity {velocity:+.1%} (breadth {breadth:.0%}, {direction})"
    ]

    if velocity >= boost_vel and breadth >= min_breadth:
        boost = 1
        confidence = min(0.88, conf_base + 0.30 * min(velocity, 0.35) + 0.15 * breadth)
        parts.append("rapid upward revisions + rising breadth — soft confirmation of narrative durability")
    elif velocity <= penalty_vel and breadth >= min_breadth * 0.7:
        boost = -1
        confidence = min(0.85, conf_base + 0.25 * min(abs(velocity), 0.30) + 0.12 * breadth)
        parts.append("sharp downward revisions — caution even if social heat remains elevated")
    elif abs(velocity) >= 0.06:
        parts.append("moderate revision activity — observation only")
    else:
        parts.append("no material estimate revision signal")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "er_velocity": velocity,
        "er_breadth": breadth,
        "er_direction": direction,
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": source,
    }


def integrate_estimate_revision_to_row(row: dict, cfg: dict | None = None) -> dict:
    mom = detect_estimate_revision(row.get("ticker", ""), row, cfg)
    row.update({
        "er_velocity": mom["er_velocity"],
        "er_breadth": mom["er_breadth"],
        "er_direction": mom["er_direction"],
        "er_boost": mom["signal_boost"],
        "er_confidence": mom["confidence"],
        "er_reason": mom["reason"],
        "er_source": mom["source"],
    })
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 📊 {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 📊 {mom['reason']}"
    else:
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | EstRev: {mom['reason']}"
    return row
