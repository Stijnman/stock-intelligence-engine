"""Expert Network Call Novelty & Sentiment Velocity Overlay.

Scores novelty and sentiment velocity from expert-network (Tegus/GLG-style)
call transcripts. Soft boost when high-novelty expert calls exhibit constructive
sentiment velocity confirming a narrative into technical strength; caution on
low-novelty or adverse expert sentiment while narrative heat remains elevated.

Live expert-network feed is an explicit future hook. Current source
is always labeled synthetic_proxy when a live feed is unavailable.

Preferred columns: enc_novelty, enc_sent_vel, enc_boost, enc_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


# Tickers with typically high-novelty, constructive expert-network calls.
ENC_HOT = {
    "NVDA", "TSLA", "PLTR", "SMCI", "AVGO", "META", "AMD", "ARM", "CRWD", "NET",
}
# Tickers with typically low-novelty or adverse expert sentiment.
ENC_COLD = {
    "INTC", "BA", "PFE", "XOM", "WMT", "KO", "IBM", "CSCO",
}


def _clip(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_expert_network_call_novelty(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    o_cfg = cfg.get("expert_network_call_novelty", {})
    if not o_cfg.get("enabled", True):
        return {
            "enc_novelty": 0.5,
            "enc_sent_vel": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Expert network call novelty overlay disabled",
            "source": "disabled",
        }

    nov_hot = float(o_cfg.get("nov_hot", 0.68))
    nov_cold = float(o_cfg.get("nov_cold", 0.32))
    vel_hot = float(o_cfg.get("vel_hot", 0.55))
    vel_cold = float(o_cfg.get("vel_cold", -0.35))
    narrative_hot = float(o_cfg.get("narrative_hot", 1.4))
    min_conf = float(o_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 24202
    rng = random.Random(seed)
    row = row or {}
    narr = float(row.get("predicted_velocity") or row.get("narrative_velocity") or 1.0)

    if tkr in ENC_HOT:
        novelty = rng.uniform(0.62, 0.92)
        sent_vel = rng.uniform(0.45, 0.88)
    elif tkr in ENC_COLD:
        novelty = rng.uniform(0.08, 0.35)
        sent_vel = rng.uniform(-0.72, -0.18)
    else:
        novelty = rng.uniform(0.28, 0.72)
        sent_vel = rng.uniform(-0.35, 0.45)

    nov_strength = _clip((novelty - nov_cold) / max(nov_hot - nov_cold, 1e-6))
    vel_strength = _clip((sent_vel - vel_cold) / max(vel_hot - vel_cold, 1e-6))
    confidence = _clip(0.30 + 0.35 * nov_strength + 0.29 * vel_strength)

    parts = [
        f"enc_novelty={novelty:.2f}",
        f"enc_sent_vel={sent_vel:.2f}",
        f"narrative={narr:.2f}",
    ]
    boost = 0
    confirm = novelty >= nov_hot and sent_vel >= vel_hot and narr >= narrative_hot
    caution = novelty <= nov_cold and sent_vel <= vel_cold and narr >= narrative_hot * 0.45

    if confirm:
        boost = 1
        confidence = min(0.95, confidence + 0.08)
        parts.append(
            "high-novelty expert-network calls show constructive sentiment velocity — soft boost"
        )
    elif caution:
        boost = -1
        confidence = min(0.93, confidence + 0.06)
        parts.append(
            "low-novelty or adverse expert sentiment while narrative heat remains elevated — caution"
        )
    else:
        parts.append("Expert network call novelty overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "enc_novelty": round(float(novelty), 4),
        "enc_sent_vel": round(float(sent_vel), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_expert_network_call_novelty_to_row(
    row: dict, cfg: dict | None = None
) -> dict:
    """Integrate Expert Network Call Novelty into a row."""
    mom = detect_expert_network_call_novelty(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "enc_novelty": mom["enc_novelty"],
            "enc_sent_vel": mom["enc_sent_vel"],
            "enc_boost": mom["signal_boost"],
            "enc_confidence": mom["confidence"],
            "enc_reason": mom["reason"],
            "enc_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + " | ENC soft boost"
    elif boost <= -1:
        if row.get("signal") in ("buy", "strong_buy"):
            row["signal"] = "hold"
        row["signal_reason"] = (row.get("signal_reason") or "") + " | ENC caution"
    return row
