"""Patent & Intellectual Property Filing Momentum Overlay.

Monitors USPTO/EPO patent applications, grants, and forward-citation velocity
as a forward-looking innovation and economic-moat signal. Soft boost for names
showing accelerating high-quality patent activity that aligns with or leads
the current narrative theme (especially AI / semiconductor / biotech).

Uses a deterministic synthetic proxy (ticker + day seeded) with realistic
filing / citation momentum ranges. Live feeds (USPTO PatentsView, EPO OPS,
Google Patents public data) are left as an explicit future hook — no invented
endpoints. Source is always labeled synthetic_proxy when live data is
unavailable.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config

# Names that historically show higher patent / IP activity in AI, semiconductor,
# biotech and deep-tech themes.
HIGH_IP_SENSITIVE = {
    "NVDA", "TSM", "AMD", "AVGO", "MU", "CRDO", "SMCI", "ASML", "AMAT", "LRCX",
    "KLAC", "CBRS", "GOOGL", "MSFT", "META", "AMZN", "TSLA", "QCOM", "INTC",
    "MRNA", "REGN", "VRTX", "BIIB",
}


def detect_patent_momentum(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    pm_cfg = cfg.get("patent_momentum", {})
    if not pm_cfg.get("enabled", True):
        return {
            "pm_filing_velocity": 0.0,
            "pm_citation_velocity": 0.0,
            "pm_grant_ratio": 0.0,
            "pm_direction": "flat",
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Patent & IP filing momentum module disabled",
            "source": "disabled",
        }

    boost_vel = float(pm_cfg.get("boost_velocity", 0.15))
    penalty_vel = float(pm_cfg.get("penalty_velocity", -0.12))
    min_grant_ratio = float(pm_cfg.get("min_grant_ratio", 0.30))
    min_conf = float(pm_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 311
    rng = random.Random(seed)

    if tkr in HIGH_IP_SENSITIVE:
        # AI / semi / biotech names: wider range, slight positive bias in current theme
        filing_vel = round(rng.uniform(-0.22, 0.48), 3)
        citation_vel = round(rng.uniform(-0.18, 0.55), 3)
        grant_ratio = round(rng.uniform(0.22, 0.88), 3)
    else:
        filing_vel = round(rng.uniform(-0.15, 0.25), 3)
        citation_vel = round(rng.uniform(-0.12, 0.28), 3)
        grant_ratio = round(rng.uniform(0.15, 0.70), 3)

    # Composite momentum for direction
    composite = 0.55 * filing_vel + 0.45 * citation_vel

    if composite >= 0.10:
        direction = "accelerating"
    elif composite <= -0.08:
        direction = "decelerating"
    else:
        direction = "flat"

    source = "synthetic_proxy"
    conf_base = 0.54 if tkr in HIGH_IP_SENSITIVE else 0.42

    boost = 0
    confidence = conf_base
    parts: list[str] = [
        f"Patent filing velocity {filing_vel:+.1%} (citations {citation_vel:+.1%}, grant ratio {grant_ratio:.0%}, {direction})"
    ]

    if filing_vel >= boost_vel and grant_ratio >= min_grant_ratio and citation_vel > -0.05:
        boost = 1
        confidence = min(0.90, conf_base + 0.28 * min(filing_vel, 0.40) + 0.12 * grant_ratio + 0.10 * max(0.0, citation_vel))
        parts.append("accelerating high-quality patent activity — soft confirmation of innovation / moat strength")
    elif filing_vel <= penalty_vel and grant_ratio >= min_grant_ratio * 0.6:
        boost = -1
        confidence = min(0.86, conf_base + 0.22 * min(abs(filing_vel), 0.30) + 0.10 * grant_ratio)
        parts.append("decelerating patent momentum — caution on innovation pipeline / moat durability")
    elif abs(filing_vel) >= 0.08 or abs(citation_vel) >= 0.10:
        parts.append("moderate patent / citation activity — observation only")
    else:
        parts.append("no material patent filing momentum signal")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "pm_filing_velocity": filing_vel,
        "pm_citation_velocity": citation_vel,
        "pm_grant_ratio": grant_ratio,
        "pm_direction": direction,
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": source,
    }


def integrate_patent_momentum_to_row(row: dict, cfg: dict | None = None) -> dict:
    mom = detect_patent_momentum(row.get("ticker", ""), row, cfg)
    row.update({
        "pm_filing_velocity": mom["pm_filing_velocity"],
        "pm_citation_velocity": mom["pm_citation_velocity"],
        "pm_grant_ratio": mom["pm_grant_ratio"],
        "pm_direction": mom["pm_direction"],
        "pm_boost": mom["signal_boost"],
        "pm_confidence": mom["confidence"],
        "pm_reason": mom["reason"],
        "pm_source": mom["source"],
    })
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 📜 {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 📜 {mom['reason']}"
    else:
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | Patent: {mom['reason']}"
    return row
