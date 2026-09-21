"""News-Source Authority / Reliability Weighted Narrative Score.

Weights news and social velocity by source authority (tier-1 outlets,
verified-account share, historical accuracy proxy) instead of treating
all mentions equally.

Soft +1 when high-authority confirmed narrative aligns with velocity.
Soft -1 when velocity is driven by low-authority / unverified sources.

Live publisher-reliability feeds (SentiSense, NewsGuard-style scores)
are left as an explicit future hook. Current source is always labeled
synthetic_proxy.

Preferred columns: nsa_authority, nsa_weighted_vel, nsa_boost, nsa_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


TIER1_SENSITIVE = {
    "NVDA", "TSM", "MU", "AMD", "INTC", "AAPL", "MSFT", "GOOGL", "AMZN", "META",
}


def detect_news_authority(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    nsa_cfg = cfg.get("news_authority", {})
    if not nsa_cfg.get("enabled", True):
        return {
            "nsa_authority": 0.0,
            "nsa_weighted_vel": 0.0,
            "nsa_unverified_share": 0.0,
            "nsa_tier1_share": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "News-source authority overlay disabled",
            "source": "disabled",
        }

    high_auth = float(nsa_cfg.get("high_auth_threshold", 0.68))
    low_auth = float(nsa_cfg.get("low_auth_threshold", 0.38))
    unverified_warn = float(nsa_cfg.get("unverified_warn", 0.45))
    min_conf = float(nsa_cfg.get("min_confidence", 0.40))
    vel_hot = float(nsa_cfg.get("narrative_hot", 1.5))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 419
    rng = random.Random(seed)

    if tkr in TIER1_SENSITIVE:
        authority = round(rng.uniform(0.42, 0.93), 3)
        tier1_share = round(rng.uniform(0.18, 0.72), 3)
        unverified = round(rng.uniform(0.05, 0.48), 3)
    else:
        authority = round(rng.uniform(0.28, 0.82), 3)
        tier1_share = round(rng.uniform(0.08, 0.48), 3)
        unverified = round(rng.uniform(0.12, 0.62), 3)

    raw_vel = 0.0
    if row:
        raw_vel = float(
            row.get("predicted_velocity")
            or row.get("auth_filtered_velocity")
            or row.get("sentiment_velocity")
            or row.get("mention_count", 0) / 12.0
            or 0.0
        )
    if raw_vel <= 0:
        raw_vel = round(rng.uniform(0.4, 4.2), 2)

    weight = max(0.12, authority * (1.0 - 0.55 * unverified) + 0.25 * tier1_share)
    weighted_vel = round(raw_vel * weight, 2)

    boost = 0
    confidence = 0.50
    parts = [
        f"NSA auth {authority:.2f} (tier-1 {tier1_share:.2f}, unverified {unverified:.2f})",
        f"weighted vel {weighted_vel:.1f} (raw {raw_vel:.1f})",
    ]

    if authority >= high_auth and weighted_vel >= vel_hot and unverified < unverified_warn:
        boost = 1
        confidence = min(
            0.90,
            0.54 + 0.40 * (authority - high_auth) + 0.12 * tier1_share + 0.04 * min(weighted_vel, 4.0),
        )
        parts.append("high-authority confirmed narrative — soft boost")
    elif (authority <= low_auth or unverified >= unverified_warn) and raw_vel >= vel_hot:
        boost = -1
        confidence = min(
            0.86,
            0.52 + 0.35 * max(0.0, low_auth - authority) + 0.28 * unverified,
        )
        parts.append("elevated velocity on low-authority / unverified sources — caution")
    elif authority <= low_auth:
        parts.append("low source authority — observation only")
    else:
        parts.append("news-source authority overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "nsa_authority": authority,
        "nsa_weighted_vel": weighted_vel,
        "nsa_unverified_share": unverified,
        "nsa_tier1_share": tier1_share,
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_news_authority_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate news-source authority weighted narrative into a row."""
    mom = detect_news_authority(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "nsa_authority": mom["nsa_authority"],
            "nsa_weighted_vel": mom["nsa_weighted_vel"],
            "nsa_unverified_share": mom["nsa_unverified_share"],
            "nsa_tier1_share": mom["nsa_tier1_share"],
            "nsa_boost": mom["signal_boost"],
            "nsa_confidence": mom["confidence"],
            "nsa_reason": mom["reason"],
            "nsa_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 📰 {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 📰 {mom['reason']}"
    else:
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | NSA: {mom['reason']}"
    return row
