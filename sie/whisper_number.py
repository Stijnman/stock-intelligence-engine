"""Whisper Number / Pre-Earnings Alt-Data Beat Probability Overlay.

Fuses existing nowcasting layers (consumer spend, digital footprint,
hiring, attention, supply-chain) into a probabilistic whisper beat/miss
estimate ahead of earnings.

Soft +1 when multi-signal alt-data cluster implies high beat probability
and supportive narrative. Soft -1 when the cluster is deteriorating even
if street consensus looks stable.

Live panel / whisper-vendor feeds are an explicit future hook. Current
source is always labeled synthetic_proxy when live data is unavailable.

Preferred columns: wn_beat_prob, wn_cluster_score, wn_boost, wn_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


EARNINGS_SENSITIVE = {
    "NVDA", "TSM", "MU", "AMD", "INTC", "AAPL", "MSFT", "GOOGL", "AMZN", "META",
    "CBRS", "CRDO",
}


def _clip(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_whisper_number(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    wn_cfg = cfg.get("whisper_number", {})
    if not wn_cfg.get("enabled", True):
        return {
            "wn_beat_prob": 0.5,
            "wn_cluster_score": 0.0,
            "wn_days_to_print": None,
            "wn_consensus_gap": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Whisper-number overlay disabled",
            "source": "disabled",
        }

    beat_hot = float(wn_cfg.get("beat_prob_hot", 0.68))
    beat_cold = float(wn_cfg.get("beat_prob_cold", 0.38))
    cluster_hot = float(wn_cfg.get("cluster_hot", 0.55))
    cluster_cold = float(wn_cfg.get("cluster_cold", -0.35))
    min_conf = float(wn_cfg.get("min_confidence", 0.40))
    vel_hot = float(wn_cfg.get("narrative_hot", 1.4))
    event_window = int(wn_cfg.get("event_window_days", 21))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 773
    rng = random.Random(seed)

    if tkr in EARNINGS_SENSITIVE:
        days_to_print = int(rng.randint(2, 28))
        street_gap = round(rng.uniform(-0.18, 0.22), 3)
    else:
        days_to_print = int(rng.randint(5, 45))
        street_gap = round(rng.uniform(-0.12, 0.14), 3)

    row = row or {}

    spend = float(row.get("cs_momentum") or row.get("cs_score") or rng.uniform(-0.6, 0.8))
    digital = float(
        row.get("df_engagement_score")
        or row.get("df_web_traffic_velocity")
        or rng.uniform(-0.5, 0.9)
    )
    hiring = float(row.get("hire_momentum") or row.get("hiring_score") or rng.uniform(-0.4, 0.7))
    attn = float(row.get("attn_momentum") or rng.uniform(-0.5, 0.8))
    supply = float(row.get("sc_capex_score") or rng.uniform(-0.4, 0.7))

    cluster = (
        0.28 * spend
        + 0.24 * digital
        + 0.18 * hiring
        + 0.16 * attn
        + 0.14 * supply
    )
    cluster = round(_clip(cluster, -1.0, 1.0), 3)

    vel = float(
        row.get("predicted_velocity")
        or row.get("auth_filtered_velocity")
        or row.get("sentiment_velocity")
        or rng.uniform(0.3, 3.6)
    )

    proximity = 1.0 - _clip(days_to_print / max(event_window, 1), 0.0, 1.0)
    raw_prob = 0.50 + 0.32 * cluster + 0.18 * street_gap + 0.08 * (1.0 if vel >= vel_hot else -0.15)
    raw_prob += 0.06 * proximity * (1.0 if cluster > 0 else -1.0)
    beat_prob = round(_clip(raw_prob, 0.08, 0.94), 3)

    boost = 0
    confidence = 0.50
    parts = [
        f"WN beat-prob {beat_prob:.2f} (cluster {cluster:+.2f}, dte {days_to_print}d)",
        f"street-gap {street_gap:+.2f} vel {vel:.1f}",
    ]

    in_window = days_to_print <= event_window
    if beat_prob >= beat_hot and cluster >= cluster_hot and in_window:
        boost = 1
        confidence = min(0.92, 0.52 + 0.35 * (beat_prob - beat_hot) + 0.22 * cluster + 0.08 * proximity)
        parts.append("alt-data cluster implies high beat probability — soft boost")
    elif beat_prob <= beat_cold and cluster <= cluster_cold:
        boost = -1
        confidence = min(0.88, 0.50 + 0.32 * (beat_cold - beat_prob) + 0.24 * abs(cluster))
        parts.append("deteriorating alt-data cluster vs stable street — caution")
    elif not in_window:
        parts.append("print outside event window — observation only")
    else:
        parts.append("whisper-number overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "wn_beat_prob": beat_prob,
        "wn_cluster_score": cluster,
        "wn_days_to_print": days_to_print,
        "wn_consensus_gap": street_gap,
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_whisper_number_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate whisper-number beat probability into a row."""
    mom = detect_whisper_number(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "wn_beat_prob": mom["wn_beat_prob"],
            "wn_cluster_score": mom["wn_cluster_score"],
            "wn_days_to_print": mom["wn_days_to_print"],
            "wn_consensus_gap": mom["wn_consensus_gap"],
            "wn_boost": mom["signal_boost"],
            "wn_confidence": mom["confidence"],
            "wn_reason": mom["reason"],
            "wn_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 🤐 {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 🤐 {mom['reason']}"
    else:
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | WN: {mom['reason']}"
    return row
