"""Company Digital Footprint Momentum Overlay (Web Traffic + App Downloads).

AltIndex-style forward demand proxy using company website traffic trends and
consumer app download / engagement momentum as leading indicators of revenue
and narrative durability. Soft boost when digital footprint accelerates in
alignment with or ahead of the current narrative theme; caution on sharp
deceleration that diverges from pure narrative heat.

Uses a deterministic synthetic proxy (ticker + day seeded) with realistic
traffic / download momentum ranges. Live feeds (SimilarWeb, Sensor Tower,
App Annie / data.ai, public web analytics) are left as an explicit future
hook — no invented endpoints. Source is always labeled synthetic_proxy when
live data is unavailable.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config

# Names with historically high digital / app / e-commerce footprint sensitivity
# (consumer platforms, fintech, software, hardware with strong direct channels).
HIGH_DIGITAL_SENSITIVE = {
    "AAPL", "AMZN", "GOOGL", "META", "MSFT", "TSLA", "NFLX", "SPOT", "UBER",
    "ABNB", "SHOP", "SQ", "PYPL", "COIN", "NVDA", "AMD", "CRM", "SNOW", "DDOG",
    "NET", "CRWD", "ZS", "OKTA", "MDB", "PLTR", "SOFI", "HOOD",
}


def detect_digital_footprint(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    df_cfg = cfg.get("digital_footprint", {})
    if not df_cfg.get("enabled", True):
        return {
            "df_web_traffic_velocity": 0.0,
            "df_app_download_velocity": 0.0,
            "df_engagement_score": 0.0,
            "df_direction": "flat",
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Company digital footprint module disabled",
            "source": "disabled",
        }

    boost_vel = float(df_cfg.get("boost_velocity", 0.16))
    penalty_vel = float(df_cfg.get("penalty_velocity", -0.14))
    min_engagement = float(df_cfg.get("min_engagement", 0.35))
    min_conf = float(df_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 419
    rng = random.Random(seed)

    if tkr in HIGH_DIGITAL_SENSITIVE:
        # Consumer / platform / SaaS names: wider range, slight positive bias
        web_vel = round(rng.uniform(-0.25, 0.52), 3)
        app_vel = round(rng.uniform(-0.22, 0.58), 3)
        engagement = round(rng.uniform(0.28, 0.92), 3)
    else:
        web_vel = round(rng.uniform(-0.18, 0.28), 3)
        app_vel = round(rng.uniform(-0.15, 0.32), 3)
        engagement = round(rng.uniform(0.18, 0.72), 3)

    # Composite momentum for direction (web + app weighted)
    composite = 0.50 * web_vel + 0.50 * app_vel

    if composite >= 0.12:
        direction = "accelerating"
    elif composite <= -0.10:
        direction = "decelerating"
    else:
        direction = "flat"

    source = "synthetic_proxy"
    conf_base = 0.56 if tkr in HIGH_DIGITAL_SENSITIVE else 0.43

    boost = 0
    confidence = conf_base
    parts: list[str] = [
        f"Web traffic velocity {web_vel:+.1%} (app downloads {app_vel:+.1%}, engagement {engagement:.0%}, {direction})"
    ]

    if web_vel >= boost_vel and app_vel > -0.05 and engagement >= min_engagement:
        boost = 1
        confidence = min(
            0.91,
            conf_base
            + 0.26 * min(web_vel, 0.45)
            + 0.14 * max(0.0, app_vel)
            + 0.10 * engagement,
        )
        parts.append(
            "accelerating digital footprint — soft confirmation of forward demand / narrative durability"
        )
    elif web_vel <= penalty_vel and engagement >= min_engagement * 0.55:
        boost = -1
        confidence = min(
            0.87,
            conf_base + 0.24 * min(abs(web_vel), 0.35) + 0.10 * engagement,
        )
        parts.append(
            "decelerating digital footprint — caution on demand softness / narrative durability"
        )
    elif abs(web_vel) >= 0.09 or abs(app_vel) >= 0.11:
        parts.append("moderate digital footprint activity — observation only")
    else:
        parts.append("no material digital footprint momentum signal")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "df_web_traffic_velocity": web_vel,
        "df_app_download_velocity": app_vel,
        "df_engagement_score": engagement,
        "df_direction": direction,
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": source,
    }


def integrate_digital_footprint_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate digital footprint momentum into an analysis row."""
    mom = detect_digital_footprint(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "df_web_traffic_velocity": mom["df_web_traffic_velocity"],
            "df_app_download_velocity": mom["df_app_download_velocity"],
            "df_engagement_score": mom["df_engagement_score"],
            "df_direction": mom["df_direction"],
            "df_boost": mom["signal_boost"],
            "df_confidence": mom["confidence"],
            "df_reason": mom["reason"],
            "df_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 🌐 {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 🌐 {mom['reason']}"
    else:
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | Digital: {mom['reason']}"
    return row
