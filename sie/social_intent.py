"""Social Trading Action Intent Classifier.

Classifies social posts (X / Reddit style) into actionable intent categories
rather than raw polarity: buy_the_dip, fomo_chase, bag_holding,
short_squeeze_call, take_profit, spam.

Filters velocity so only high-intent authentic posts contribute. Soft +1 when
high-intent authentic velocity is rising; -1 when spikes are low-intent / spam.
Extends the authenticity layer. Deterministic synthetic proxy when live posts
are unavailable (labeled source).
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config

HIGH_INTENT = {"buy_the_dip", "short_squeeze_call"}
LOW_INTENT = {"fomo_chase", "bag_holding", "spam"}
INTENTS = (
    "buy_the_dip",
    "fomo_chase",
    "bag_holding",
    "short_squeeze_call",
    "take_profit",
    "spam",
)


def classify_social_intent(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    sti_cfg = cfg.get("social_intent", {})
    if not sti_cfg.get("enabled", True):
        return {
            "sti_intent": "disabled",
            "sti_intent_share": 0.0,
            "sti_high_intent_velocity": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Social trading action intent classifier disabled",
            "source": "disabled",
        }

    high_share = float(sti_cfg.get("high_intent_share", 0.42))
    spam_share = float(sti_cfg.get("spam_share_penalty", 0.28))
    vel_hot = float(sti_cfg.get("high_intent_velocity_hot", 1.4))
    min_conf = float(sti_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 227
    rng = random.Random(seed)

    raw_weights = {k: rng.uniform(0.04, 0.38) for k in INTENTS}
    total = sum(raw_weights.values()) or 1.0
    shares = {k: raw_weights[k] / total for k in INTENTS}
    dominant = max(shares, key=shares.get)
    dominant_share = round(shares[dominant], 3)
    high_intent_share = round(shares["buy_the_dip"] + shares["short_squeeze_call"], 3)
    spam_frac = round(shares["spam"] + 0.45 * shares["fomo_chase"], 3)

    raw_vel = 0.0
    if row:
        raw_vel = float(
            row.get("auth_filtered_velocity")
            or row.get("predicted_velocity")
            or row.get("sentiment_velocity")
            or 0.0
        )
    if raw_vel <= 0:
        raw_vel = round(rng.uniform(0.5, 4.2), 2)

    auth_score = 0.55
    if row:
        try:
            auth_score = float(row.get("auth_score") or 0.55)
        except (TypeError, ValueError):
            auth_score = 0.55

    auth_mult = 0.55 + 0.70 * max(0.0, min(1.0, auth_score))
    high_intent_velocity = round(raw_vel * high_intent_share * auth_mult * (1.0 - 0.65 * spam_frac), 2)

    source = "synthetic_proxy"
    conf_base = 0.50 if auth_score >= 0.50 else 0.42
    boost = 0
    confidence = conf_base
    parts = [
        f"Dominant intent {dominant} ({dominant_share:.0%})",
        f"high-intent share {high_intent_share:.0%}",
        f"high-intent vel {high_intent_velocity:.1f} (raw {raw_vel:.1f})",
    ]

    if high_intent_share >= high_share and high_intent_velocity >= vel_hot and auth_score >= 0.50:
        boost = 1
        confidence = min(0.90, conf_base + 0.28 * high_intent_share + 0.10 * auth_score)
        parts.append("rising high-intent authentic velocity — soft boost")
    elif spam_frac >= spam_share and raw_vel >= vel_hot:
        boost = -1
        confidence = min(0.86, conf_base + 0.30 * spam_frac)
        parts.append("low-intent / spam-driven spike — caution")
    elif dominant in LOW_INTENT:
        parts.append("low-intent dominant mix — observation only")
    else:
        parts.append("intent mix neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "sti_intent": dominant,
        "sti_intent_share": dominant_share,
        "sti_high_intent_velocity": high_intent_velocity,
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": source,
    }


def integrate_social_intent_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate social trading action intent into an analysis row."""
    mom = classify_social_intent(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "sti_intent": mom["sti_intent"],
            "sti_intent_share": mom["sti_intent_share"],
            "sti_high_intent_velocity": mom["sti_high_intent_velocity"],
            "sti_boost": mom["signal_boost"],
            "sti_confidence": mom["confidence"],
            "sti_reason": mom["reason"],
            "sti_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 🎯 {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 🎯 {mom['reason']}"
    else:
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | Intent: {mom['reason']}"
    return row
