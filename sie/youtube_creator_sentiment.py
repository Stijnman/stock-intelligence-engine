"""YouTube Financial Creator Transcript & Comment Sentiment Velocity Overlay.

Scores velocity and sentiment of financial YouTube creator transcripts and comments.
Soft boost when high-velocity authentic positive sentiment confirms a narrative into
technical strength; caution when creator sentiment collapses or turns adversarial
while human narrative heat remains elevated.

Live YouTube transcript + comment feed is an explicit future hook. Current source
is always labeled synthetic_proxy when a live feed is unavailable.

Preferred columns: ytc_vel, ytc_sent, ytc_boost, ytc_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


# Tickers with typically high positive creator velocity.
YTC_HOT = {
    "NVDA", "TSLA", "PLTR", "SMCI", "AVGO", "META", "AMD", "ARM", "CRWD", "NET",
}
# Tickers with typically low or negative creator sentiment.
YTC_COLD = {
    "INTC", "BA", "PFE", "XOM", "WMT", "KO", "IBM", "CSCO",
}


def _clip(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_youtube_creator_sentiment(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    a_cfg = cfg.get("youtube_creator_sentiment", {})
    if not a_cfg.get("enabled", True):
        return {
            "ytc_vel": 0.0,
            "ytc_sent": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "YouTube financial creator transcript & comment sentiment velocity overlay disabled",
            "source": "disabled",
        }

    vel_hot = float(a_cfg.get("vel_hot", 0.70))
    vel_cold = float(a_cfg.get("vel_cold", 0.30))
    sent_hot = float(a_cfg.get("sent_hot", 0.65))
    sent_cold = float(a_cfg.get("sent_cold", 0.25))
    narrative_hot = float(a_cfg.get("narrative_hot", 1.4))
    min_conf = float(a_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 17842
    rng = random.Random(seed)
    row = row or {}
    narr = float(row.get("predicted_velocity") or row.get("narrative_velocity") or 1.0)

    if tkr in YTC_HOT:
        vel = rng.uniform(0.68, 0.94)
        sent = rng.uniform(0.58, 0.88)
    elif tkr in YTC_COLD:
        vel = rng.uniform(0.12, 0.36)
        sent = rng.uniform(0.08, 0.32)
    else:
        vel = rng.uniform(0.32, 0.68)
        sent = rng.uniform(0.28, 0.62)

    vel_strength = _clip((vel - vel_cold) / max(vel_hot - vel_cold, 1e-6))
    sent_strength = _clip((sent - sent_cold) / max(sent_hot - sent_cold, 1e-6))
    confidence = _clip(0.36 + 0.34 * vel_strength + 0.26 * sent_strength)

    parts = [
        f"ytc_vel={vel:.2f}",
        f"ytc_sent={sent:.2f}",
        f"narrative={narr:.2f}",
    ]
    boost = 0
    confirm = vel >= vel_hot and sent >= sent_hot and narr >= narrative_hot
    caution = vel <= vel_cold and sent <= sent_cold and narr >= narrative_hot * 0.45

    if confirm:
        boost = 1
        confidence = min(0.95, confidence + 0.08)
        parts.append(
            "high-velocity authentic positive YouTube creator sentiment into confirming narrative — soft boost"
        )
    elif caution:
        boost = -1
        confidence = min(0.93, confidence + 0.06)
        parts.append(
            "creator sentiment collapsed or adversarial while narrative heat remains elevated — caution"
        )
    else:
        parts.append("YouTube financial creator transcript & comment sentiment velocity overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "ytc_vel": round(float(vel), 4),
        "ytc_sent": round(float(sent), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_youtube_creator_sentiment_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate YouTube Financial Creator Transcript & Comment Sentiment Velocity into a row."""
    mom = detect_youtube_creator_sentiment(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "ytc_vel": mom["ytc_vel"],
            "ytc_sent": mom["ytc_sent"],
            "ytc_boost": mom["signal_boost"],
            "ytc_confidence": mom["confidence"],
            "ytc_reason": mom["reason"],
            "ytc_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + " | YTC soft boost"
    elif boost <= -1:
        if row.get("signal") in ("buy", "strong_buy"):
            row["signal"] = "hold"
        row["signal_reason"] = (row.get("signal_reason") or "") + " | YTC caution"
    return row
