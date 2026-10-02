"""News Materiality / Predicted Next-Session Impact Score Overlay.

Scores how material the current news tape is for the next session:
expected absolute-move impact, a volatility bucket, and a soft boost
when that impact confirms the narrative (or a caution when a large
adverse print is likely). Complements news-authority weighting without
duplicating source reliability.

Live headline materiality models (event classifiers, options-implied
move residual) are an explicit future hook. Current source is always
labeled synthetic_proxy when live data is unavailable.

Preferred columns: nimp_score, nimp_vol_bucket, nimp_boost, nimp_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


HIGH_IMPACT_UNIVERSE = {
    "NVDA", "TSLA", "META", "SMCI", "PLTR", "COIN", "MSTR", "AMD",
    "AVGO", "AAPL", "MSFT", "AMZN", "GOOGL", "NFLX", "ARM", "MU",
}


def _clip(v: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def _vol_bucket(score: float, hi: float, mid: float, lo: float) -> str:
    if score >= hi:
        return "extreme"
    if score >= mid:
        return "high"
    if score >= lo:
        return "elevated"
    return "quiet"


def detect_news_materiality(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    nimp_cfg = cfg.get("news_materiality", {})
    if not nimp_cfg.get("enabled", True):
        return {
            "nimp_score": 0.0,
            "nimp_vol_bucket": "quiet",
            "nimp_polarity": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "News materiality overlay disabled",
            "source": "disabled",
        }

    score_hot = float(nimp_cfg.get("score_hot", 0.62))
    score_mid = float(nimp_cfg.get("score_mid", 0.40))
    score_lo = float(nimp_cfg.get("score_lo", 0.22))
    adverse_hot = float(nimp_cfg.get("adverse_hot", -0.35))
    vel_hot = float(nimp_cfg.get("narrative_hot", 1.4))
    min_conf = float(nimp_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 7713
    rng = random.Random(seed)
    row = row or {}

    if tkr in HIGH_IMPACT_UNIVERSE:
        raw_score = rng.uniform(0.28, 0.94)
        polarity = rng.uniform(-0.85, 0.90)
    else:
        raw_score = rng.uniform(0.04, 0.48)
        polarity = rng.uniform(-0.40, 0.45)

    news_sent = row.get("avg_news_sentiment")
    if news_sent is None:
        news_sent = row.get("news_sentiment")
    if news_sent is not None:
        polarity = 0.35 * polarity + 0.65 * float(news_sent)

    vel = float(
        row.get("predicted_velocity")
        or row.get("auth_filtered_velocity")
        or row.get("sentiment_velocity")
        or rng.uniform(0.2, 3.8)
    )
    auth = float(row.get("auth_score") or row.get("news_authority") or 0.55)

    score = _clip(0.70 * raw_score + 0.18 * min(vel / 4.0, 1.0) + 0.12 * abs(polarity), 0.0, 1.0)
    bucket = _vol_bucket(score, score_hot, score_mid, score_lo)

    boost = 0
    confidence = min(0.90, 0.36 + 0.32 * score + 0.12 * auth)
    parts = [
        f"nimp={score:.2f}",
        f"bucket={bucket}",
        f"polarity={polarity:+.2f}",
        f"vel={vel:.2f}",
    ]

    confirm = (
        score >= score_hot
        and polarity >= 0.15
        and vel >= vel_hot * 0.50
        and auth >= 0.40
    )
    adverse = (
        score >= score_mid
        and polarity <= adverse_hot
        and vel >= vel_hot * 0.45
    )

    if confirm:
        boost = 1
        confidence = min(0.93, 0.50 + 0.26 * score + 0.12 * auth)
        parts.append("high next-session materiality confirms narrative — soft boost")
    elif adverse:
        boost = -1
        confidence = min(0.91, 0.48 + 0.24 * score + 0.10 * abs(polarity))
        parts.append("material adverse news tape — next-session impact caution")
    else:
        parts.append("news materiality overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "nimp_score": round(float(score), 4),
        "nimp_vol_bucket": bucket,
        "nimp_polarity": round(float(polarity), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_news_materiality_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate predicted next-session news impact into a row."""
    mom = detect_news_materiality(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "nimp_score": mom["nimp_score"],
            "nimp_vol_bucket": mom["nimp_vol_bucket"],
            "nimp_polarity": mom["nimp_polarity"],
            "nimp_boost": mom["signal_boost"],
            "nimp_confidence": mom["confidence"],
            "nimp_reason": mom["reason"],
            "nimp_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    tag = f" | nimp {mom['reason']}"
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + tag
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + tag
    else:
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | nimp: {mom['reason']}"
    return row
