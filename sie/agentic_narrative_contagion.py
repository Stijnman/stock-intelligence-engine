"""Agentic Narrative Contagion Velocity Overlay.

Scores velocity and agent share of narrative propagation through autonomous AI agents
(agent-to-agent contagion, generative memo cascades). Soft boost when high-velocity
agent-driven contagion confirms a narrative into technical strength; caution when
agent-driven contagion collapses or turns adversarial while human narrative heat remains elevated.

Live agent-network monitor is an explicit future hook. Current source is always labeled
synthetic_proxy when a live feed is unavailable.

Preferred columns: anc_vel, anc_agent_share, anc_boost, anc_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


# Tickers where agentic narrative contagion typically runs hot.
ANC_HOT = {
    "NVDA", "AMD", "TSLA", "PLTR", "SMCI", "AVGO", "TSM", "META", "GOOGL", "MSFT",
    "ARM", "SNOW", "CRWD", "NET",
}
# Tickers where agent-driven contagion is typically muted or adversarial.
ANC_COLD = {
    "INTC", "IBM", "CSCO", "ORCL", "PFE", "JNJ", "BA", "XOM", "WMT", "KO",
}


def _clip(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_agentic_narrative_contagion(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    a_cfg = cfg.get("agentic_narrative_contagion", {})
    if not a_cfg.get("enabled", True):
        return {
            "anc_vel": 0.0,
            "anc_agent_share": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Agentic narrative contagion velocity overlay disabled",
            "source": "disabled",
        }

    vel_hot = float(a_cfg.get("vel_hot", 0.72))
    vel_cold = float(a_cfg.get("vel_cold", 0.28))
    share_hot = float(a_cfg.get("share_hot", 0.55))
    share_cold = float(a_cfg.get("share_cold", 0.18))
    narrative_hot = float(a_cfg.get("narrative_hot", 1.4))
    min_conf = float(a_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 12847
    rng = random.Random(seed)
    row = row or {}
    narr = float(row.get("predicted_velocity") or row.get("narrative_velocity") or 1.0)

    if tkr in ANC_HOT:
        velocity = rng.uniform(0.68, 0.94)
        agent_share = rng.uniform(0.48, 0.78)
    elif tkr in ANC_COLD:
        velocity = rng.uniform(0.12, 0.34)
        agent_share = rng.uniform(0.08, 0.24)
    else:
        velocity = rng.uniform(0.32, 0.62)
        agent_share = rng.uniform(0.22, 0.48)

    vel_strength = _clip((velocity - vel_cold) / max(vel_hot - vel_cold, 1e-6))
    share_strength = _clip((agent_share - share_cold) / max(share_hot - share_cold, 1e-6))
    confidence = _clip(0.36 + 0.34 * vel_strength + 0.22 * share_strength)

    parts = [
        f"anc_vel={velocity:.2f}",
        f"anc_agent_share={agent_share:.2f}",
        f"narrative={narr:.2f}",
    ]
    boost = 0
    confirm = velocity >= vel_hot and agent_share >= share_hot and narr >= narrative_hot
    caution = velocity <= vel_cold and agent_share <= share_cold and narr >= narrative_hot * 0.45

    if confirm:
        boost = 1
        confidence = min(0.95, confidence + 0.08)
        parts.append(
            "high-velocity agentic narrative contagion into confirming narrative — soft boost"
        )
    elif caution:
        boost = -1
        confidence = min(0.93, confidence + 0.06)
        parts.append(
            "agent-driven contagion collapsed or adversarial while narrative heat remains elevated — caution"
        )
    else:
        parts.append("Agentic narrative contagion velocity overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "anc_vel": round(float(velocity), 4),
        "anc_agent_share": round(float(agent_share), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_agentic_narrative_contagion_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate Agentic Narrative Contagion Velocity into a row."""
    mom = detect_agentic_narrative_contagion(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "anc_vel": mom["anc_vel"],
            "anc_agent_share": mom["anc_agent_share"],
            "anc_boost": mom["signal_boost"],
            "anc_confidence": mom["confidence"],
            "anc_reason": mom["reason"],
            "anc_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + " | ANC soft boost"
    elif boost <= -1:
        if row.get("signal") in ("buy", "strong_buy"):
            row["signal"] = "hold"
        row["signal_reason"] = (row.get("signal_reason") or "") + " | ANC caution"
    return row
