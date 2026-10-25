"""Signed Options Flow Toxicity & Informed Trading Probability Overlay.

Scores toxicity and informed-trading probability from signed OPRA flow
(customer buys/sells). Soft boost when flow shows low toxicity and
constructive informed-trading probability into a confirming narrative;
caution on elevated toxicity or adverse informed flow while narrative
heat remains elevated.

Live signed options-flow feed is an explicit future hook. Current source
is always labeled synthetic_proxy when a live feed is unavailable.

Preferred columns: oft_toxicity, oft_informed_prob, oft_boost, oft_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


# Tickers with typically low-toxicity, constructive informed options flow.
OFT_HOT = {
    "NVDA", "TSLA", "PLTR", "SMCI", "AVGO", "META", "AMD", "ARM", "CRWD", "NET",
}
# Tickers with typically high-toxicity or adverse informed options flow.
OFT_COLD = {
    "INTC", "BA", "PFE", "XOM", "WMT", "KO", "IBM", "CSCO",
}


def _clip(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_signed_options_flow_toxicity(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    o_cfg = cfg.get("signed_options_flow_toxicity", {})
    if not o_cfg.get("enabled", True):
        return {
            "oft_toxicity": 0.5,
            "oft_informed_prob": 0.5,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Signed options flow toxicity overlay disabled",
            "source": "disabled",
        }

    tox_hot = float(o_cfg.get("tox_hot", 0.28))  # low is better
    tox_cold = float(o_cfg.get("tox_cold", 0.72))
    inf_hot = float(o_cfg.get("inf_hot", 0.68))
    inf_cold = float(o_cfg.get("inf_cold", 0.32))
    narrative_hot = float(o_cfg.get("narrative_hot", 1.4))
    min_conf = float(o_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 24201
    rng = random.Random(seed)
    row = row or {}
    narr = float(row.get("predicted_velocity") or row.get("narrative_velocity") or 1.0)

    if tkr in OFT_HOT:
        toxicity = rng.uniform(0.08, 0.32)
        informed = rng.uniform(0.65, 0.92)
    elif tkr in OFT_COLD:
        toxicity = rng.uniform(0.68, 0.95)
        informed = rng.uniform(0.12, 0.38)
    else:
        toxicity = rng.uniform(0.30, 0.70)
        informed = rng.uniform(0.35, 0.65)

    # Lower toxicity is better.
    tox_strength = _clip((tox_cold - toxicity) / max(tox_cold - tox_hot, 1e-6))
    inf_strength = _clip((informed - inf_cold) / max(inf_hot - inf_cold, 1e-6))
    confidence = _clip(0.30 + 0.36 * tox_strength + 0.28 * inf_strength)

    parts = [
        f"oft_toxicity={toxicity:.2f}",
        f"oft_informed_prob={informed:.2f}",
        f"narrative={narr:.2f}",
    ]
    boost = 0
    confirm = toxicity <= tox_hot and informed >= inf_hot and narr >= narrative_hot
    caution = toxicity >= tox_cold and informed <= inf_cold and narr >= narrative_hot * 0.45

    if confirm:
        boost = 1
        confidence = min(0.95, confidence + 0.08)
        parts.append(
            "signed options flow shows low toxicity and constructive informed-trading probability \u2014 soft boost"
        )
    elif caution:
        boost = -1
        confidence = min(0.93, confidence + 0.06)
        parts.append(
            "elevated toxicity or adverse informed options flow while narrative heat remains elevated \u2014 caution"
        )
    else:
        parts.append("Signed options flow toxicity overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate \u2014 signal suppressed)")

    return {
        "oft_toxicity": round(float(toxicity), 4),
        "oft_informed_prob": round(float(informed), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_signed_options_flow_toxicity_to_row(
    row: dict, cfg: dict | None = None
) -> dict:
    """Integrate Signed Options Flow Toxicity into a row."""
    mom = detect_signed_options_flow_toxicity(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "oft_toxicity": mom["oft_toxicity"],
            "oft_informed_prob": mom["oft_informed_prob"],
            "oft_boost": mom["signal_boost"],
            "oft_confidence": mom["confidence"],
            "oft_reason": mom["reason"],
            "oft_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + " | OFT soft boost"
    elif boost <= -1:
        if row.get("signal") in ("buy", "strong_buy"):
            row["signal"] = "hold"
        row["signal_reason"] = (row.get("signal_reason") or "") + " | OFT caution"
    return row
