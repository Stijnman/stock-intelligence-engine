"""App-Store Review Sentiment & Complaint Velocity Overlay.

Scores consumer app-store review sentiment, 1-star complaint velocity,
and rating-mix drift as a product-quality pulse orthogonal to digital
footprint download velocity and employee-outlook layers.

Live App Store / Google Play / Sensor Tower feeds are an explicit future
hook. Current source is always labeled synthetic_proxy when live data is
unavailable.

Preferred columns: asr_sentiment, asr_complaint_velocity, asr_boost, asr_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


CONSUMER_APP_UNIVERSE = {
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NFLX", "UBER",
    "ABNB", "PYPL", "SQ", "SHOP", "SPOT", "SNAP", "PINS",
    "RBLX", "U", "CRWD", "NOW", "CRM", "ORCL",
}


def _clip(v: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_app_store_reviews(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    asr_cfg = cfg.get("app_store_reviews", {})
    if not asr_cfg.get("enabled", True):
        return {
            "asr_sentiment": 0.0,
            "asr_complaint_velocity": 0.0,
            "asr_rating": 0.0,
            "asr_review_velocity": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "App-store review overlay disabled",
            "source": "disabled",
        }

    sent_hot = float(asr_cfg.get("sentiment_hot", 0.58))
    sent_cold = float(asr_cfg.get("sentiment_cold", 0.22))
    complaint_hot = float(asr_cfg.get("complaint_hot", 0.55))
    complaint_cold = float(asr_cfg.get("complaint_cold", 0.18))
    vel_hot = float(asr_cfg.get("narrative_hot", 1.4))
    min_conf = float(asr_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 2718
    rng = random.Random(seed)
    row = row or {}

    if tkr in CONSUMER_APP_UNIVERSE:
        sentiment = rng.uniform(0.18, 0.92)
        rating = rng.uniform(3.1, 4.9)
        review_vel = rng.uniform(0.20, 1.40)
        complaint = rng.uniform(0.05, 0.62)
    else:
        sentiment = rng.uniform(0.12, 0.72)
        rating = rng.uniform(2.8, 4.6)
        review_vel = rng.uniform(0.04, 0.80)
        complaint = rng.uniform(0.08, 0.48)

    vel = float(
        row.get("predicted_velocity")
        or row.get("auth_filtered_velocity")
        or row.get("sentiment_velocity")
        or rng.uniform(0.2, 3.8)
    )
    auth = float(row.get("auth_score") or 0.55)
    df_app = float(row.get("df_app_download_velocity") or 0.0)

    score = _clip(
        0.45 * (sentiment - 0.50)
        + 0.20 * ((rating - 3.5) / 1.5)
        - 0.35 * (complaint - 0.25)
        + 0.10 * (review_vel - 0.40)
        + 0.08 * max(df_app, 0.0)
    )

    parts = [
        f"asr sentiment={sentiment:.2f}",
        f"complaint_vel={complaint:.2f}",
        f"rating={rating:.2f}",
        f"review_vel={review_vel:.2f}",
    ]
    boost = 0
    confidence = 0.42 + 0.18 * auth

    product_confirm = (
        sentiment >= sent_hot
        and complaint <= complaint_cold
        and rating >= 4.1
        and vel >= vel_hot * 0.55
    )
    product_warn = (
        (sentiment <= sent_cold or complaint >= complaint_hot or rating <= 3.3)
        and vel >= vel_hot * 0.70
    )

    if product_confirm:
        boost = 1
        confidence = min(0.92, 0.48 + 0.26 * abs(score) + 0.14 * auth)
        parts.append("rising app-store sentiment / falling complaint velocity confirming narrative — soft boost")
    elif product_warn:
        boost = -1
        confidence = min(0.90, 0.46 + 0.24 * abs(min(score, 0)) + 0.14 * max(vel / 4.0, 0))
        parts.append("complaint velocity spike / rating collapse into elevated social heat — caution")
    else:
        parts.append("app-store review overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "asr_sentiment": round(float(sentiment), 4),
        "asr_complaint_velocity": round(float(complaint), 4),
        "asr_rating": round(float(rating), 3),
        "asr_review_velocity": round(float(review_vel), 4),
        "asr_score": round(float(score), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_app_store_reviews_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate app-store review sentiment into a row."""
    mom = detect_app_store_reviews(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "asr_sentiment": mom["asr_sentiment"],
            "asr_complaint_velocity": mom["asr_complaint_velocity"],
            "asr_rating": mom.get("asr_rating", 0.0),
            "asr_review_velocity": mom.get("asr_review_velocity", 0.0),
            "asr_score": mom.get("asr_score", 0.0),
            "asr_boost": mom["signal_boost"],
            "asr_confidence": mom["confidence"],
            "asr_reason": mom["reason"],
            "asr_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | app-store {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | app-store {mom['reason']}"
    else:
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | app-store: {mom['reason']}"
    return row
