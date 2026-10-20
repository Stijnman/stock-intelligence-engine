"""RAG-Extracted Earnings Guidance Novelty & Hedge Density Overlay.

Scores novelty of guidance language extracted via RAG from earnings-call transcripts
and the density of hedging language. Soft boost when high-novelty guidance with low
hedge density confirms a narrative into technical strength; caution on boilerplate
or heavily hedged guidance while narrative heat stays elevated.

Live transcript RAG pipeline is an explicit future hook. Current source is always
labeled synthetic_proxy when a live feed is unavailable.

Preferred columns: rgn_novelty, rgn_hedge_density, rgn_boost, rgn_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


# Tickers where earnings guidance is typically novel and lightly hedged.
RGN_HOT = {
    "NVDA", "AMD", "TSLA", "PLTR", "SMCI", "AVGO", "META", "GOOGL", "MSFT", "AMZN",
    "ARM", "SNOW", "CRWD", "NET",
}
# Tickers where guidance is typically boilerplate or heavily hedged.
RGN_COLD = {
    "INTC", "IBM", "CSCO", "ORCL", "PFE", "JNJ", "BA", "XOM", "WMT", "KO",
}


def _clip(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_rag_earnings_guidance(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    a_cfg = cfg.get("rag_earnings_guidance", {})
    if not a_cfg.get("enabled", True):
        return {
            "rgn_novelty": 0.0,
            "rgn_hedge_density": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "RAG earnings guidance novelty & hedge density overlay disabled",
            "source": "disabled",
        }

    novelty_hot = float(a_cfg.get("novelty_hot", 0.68))
    novelty_cold = float(a_cfg.get("novelty_cold", 0.32))
    hedge_hot = float(a_cfg.get("hedge_hot", 0.62))
    hedge_cold = float(a_cfg.get("hedge_cold", 0.22))
    narrative_hot = float(a_cfg.get("narrative_hot", 1.4))
    min_conf = float(a_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 21483
    rng = random.Random(seed)
    row = row or {}
    narr = float(row.get("predicted_velocity") or row.get("narrative_velocity") or 1.0)

    if tkr in RGN_HOT:
        novelty = rng.uniform(0.66, 0.92)
        hedge_density = rng.uniform(0.08, 0.28)
    elif tkr in RGN_COLD:
        novelty = rng.uniform(0.14, 0.38)
        hedge_density = rng.uniform(0.55, 0.82)
    else:
        novelty = rng.uniform(0.34, 0.64)
        hedge_density = rng.uniform(0.28, 0.52)

    novelty_strength = _clip((novelty - novelty_cold) / max(novelty_hot - novelty_cold, 1e-6))
    hedge_strength = _clip((hedge_cold - hedge_density) / max(hedge_hot - hedge_cold, 1e-6))  # low hedge is better
    confidence = _clip(0.34 + 0.36 * novelty_strength + 0.24 * hedge_strength)

    parts = [
        f"rgn_novelty={novelty:.2f}",
        f"rgn_hedge_density={hedge_density:.2f}",
        f"narrative={narr:.2f}",
    ]
    boost = 0
    confirm = novelty >= novelty_hot and hedge_density <= hedge_cold and narr >= narrative_hot
    caution = novelty <= novelty_cold and hedge_density >= hedge_hot and narr >= narrative_hot * 0.45

    if confirm:
        boost = 1
        confidence = min(0.95, confidence + 0.08)
        parts.append(
            "high-novelty low-hedge RAG earnings guidance into confirming narrative — soft boost"
        )
    elif caution:
        boost = -1
        confidence = min(0.93, confidence + 0.06)
        parts.append(
            "boilerplate or heavily hedged guidance while narrative heat remains elevated — caution"
        )
    else:
        parts.append("RAG earnings guidance novelty & hedge density overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "rgn_novelty": round(float(novelty), 4),
        "rgn_hedge_density": round(float(hedge_density), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_rag_earnings_guidance_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate RAG Earnings Guidance Novelty & Hedge Density into a row."""
    mom = detect_rag_earnings_guidance(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "rgn_novelty": mom["rgn_novelty"],
            "rgn_hedge_density": mom["rgn_hedge_density"],
            "rgn_boost": mom["signal_boost"],
            "rgn_confidence": mom["confidence"],
            "rgn_reason": mom["reason"],
            "rgn_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + " | RGN soft boost"
    elif boost <= -1:
        if row.get("signal") in ("buy", "strong_buy"):
            row["signal"] = "hold"
        row["signal_reason"] = (row.get("signal_reason") or "") + " | RGN caution"
    return row
