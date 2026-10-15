"""Multi-Agent Debate Consensus Strength Overlay.

Scores consensus strength and disagreement among specialized multi-agent debates
(fundamental, narrative, options-flow agents). Soft boost when high consensus confirms
a narrative; caution on high disagreement or rapid flip-flops while narrative heat remains elevated.

Live multi-agent orchestrator is an explicit future hook. Current source is always labeled
synthetic_proxy when a live feed is unavailable.

Preferred columns: mad_consensus, mad_disagreement, mad_boost, mad_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


# Tickers where multi-agent debate typically reaches high consensus.
MAD_HOT = {
    "NVDA", "AMD", "TSLA", "PLTR", "SMCI", "AVGO", "TSM", "META", "GOOGL", "MSFT",
}
# Tickers where debate disagreement is typically higher.
MAD_COLD = {
    "INTC", "IBM", "CSCO", "ORCL", "PFE", "JNJ", "BA", "XOM",
}


def _clip(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_multi_agent_debate(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    m_cfg = cfg.get("multi_agent_debate", {})
    if not m_cfg.get("enabled", True):
        return {
            "mad_consensus": 0.0,
            "mad_disagreement": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Multi-agent debate consensus overlay disabled",
            "source": "disabled",
        }

    consensus_hot = float(m_cfg.get("consensus_hot", 0.78))
    consensus_cold = float(m_cfg.get("consensus_cold", 0.42))
    disagreement_hot = float(m_cfg.get("disagreement_hot", 0.35))
    disagreement_cold = float(m_cfg.get("disagreement_cold", 0.15))
    narrative_hot = float(m_cfg.get("narrative_hot", 1.4))
    min_conf = float(m_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 9341
    rng = random.Random(seed)
    row = row or {}
    narr = float(row.get("predicted_velocity") or row.get("narrative_velocity") or 1.0)

    if tkr in MAD_HOT:
        consensus = rng.uniform(0.72, 0.92)
        disagreement = rng.uniform(0.08, 0.22)
    elif tkr in MAD_COLD:
        consensus = rng.uniform(0.28, 0.48)
        disagreement = rng.uniform(0.32, 0.55)
    else:
        consensus = rng.uniform(0.48, 0.72)
        disagreement = rng.uniform(0.18, 0.38)

    consensus_strength = _clip((consensus - consensus_cold) / max(consensus_hot - consensus_cold, 1e-6))
    disagreement_strength = _clip((disagreement_hot - disagreement) / max(disagreement_hot - disagreement_cold, 1e-6))
    confidence = _clip(0.38 + 0.32 * consensus_strength + 0.20 * disagreement_strength)

    parts = [
        f"mad_consensus={consensus:.2f}",
        f"mad_disagreement={disagreement:.2f}",
        f"narrative={narr:.2f}",
    ]
    boost = 0
    confirm = consensus >= consensus_hot and disagreement <= disagreement_cold and narr >= narrative_hot
    caution = consensus <= consensus_cold and disagreement >= disagreement_hot and narr >= narrative_hot * 0.45

    if confirm:
        boost = 1
        confidence = min(0.95, confidence + 0.07)
        parts.append(
            "high multi-agent debate consensus into confirming narrative — soft boost"
        )
    elif caution:
        boost = -1
        confidence = min(0.93, confidence + 0.06)
        parts.append(
            "high disagreement or low consensus while narrative heat remains elevated — caution"
        )
    else:
        parts.append("Multi-agent debate consensus strength overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "mad_consensus": round(float(consensus), 4),
        "mad_disagreement": round(float(disagreement), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_multi_agent_debate_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate Multi-Agent Debate Consensus Strength into a row."""
    mom = detect_multi_agent_debate(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "mad_consensus": mom["mad_consensus"],
            "mad_disagreement": mom["mad_disagreement"],
            "mad_boost": mom["signal_boost"],
            "mad_confidence": mom["confidence"],
            "mad_reason": mom["reason"],
            "mad_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | mad {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | mad {mom['reason']}"
    return row
