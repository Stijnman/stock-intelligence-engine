"""Agent-Generated Research Memo Cascade Velocity Overlay.

Scores velocity and share of agent-generated research memos (AlphaSense SuperAnalyst-style always-on workflows).
Soft boost when high-velocity cascade of agent-generated research memos confirms a narrative into
technical strength; caution when cascade collapses or turns adversarial while human narrative heat remains elevated.

Live agent-memo monitor is an explicit future hook. Current source is always labeled synthetic_proxy when a live feed is unavailable.

Preferred columns: agc_vel, agc_memo_share, agc_boost, agc_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


# Tickers with typically high agent-memo cascade velocity.
AGC_HOT = {
    "NVDA", "TSLA", "PLTR", "SMCI", "AVGO", "META", "AMD", "ARM", "CRWD", "NET",
}
# Tickers with typically low or collapsing agent-memo cascades.
AGC_COLD = {
    "INTC", "BA", "PFE", "XOM", "WMT", "KO", "IBM", "CSCO",
}


def _clip(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_agent_generated_memo_cascade(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    a_cfg = cfg.get("agent_generated_memo_cascade", {})
    if not a_cfg.get("enabled", True):
        return {
            "agc_vel": 0.0,
            "agc_memo_share": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Agent-generated research memo cascade velocity overlay disabled",
            "source": "disabled",
        }

    vel_hot = float(a_cfg.get("vel_hot", 0.68))
    vel_cold = float(a_cfg.get("vel_cold", 0.28))
    share_hot = float(a_cfg.get("share_hot", 0.52))
    share_cold = float(a_cfg.get("share_cold", 0.16))
    narrative_hot = float(a_cfg.get("narrative_hot", 1.4))
    min_conf = float(a_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 19273
    rng = random.Random(seed)
    row = row or {}
    narr = float(row.get("predicted_velocity") or row.get("narrative_velocity") or 1.0)

    if tkr in AGC_HOT:
        vel = rng.uniform(0.66, 0.92)
        share = rng.uniform(0.48, 0.78)
    elif tkr in AGC_COLD:
        vel = rng.uniform(0.10, 0.34)
        share = rng.uniform(0.06, 0.22)
    else:
        vel = rng.uniform(0.30, 0.66)
        share = rng.uniform(0.18, 0.52)

    vel_strength = _clip((vel - vel_cold) / max(vel_hot - vel_cold, 1e-6))
    share_strength = _clip((share - share_cold) / max(share_hot - share_cold, 1e-6))
    confidence = _clip(0.34 + 0.36 * vel_strength + 0.24 * share_strength)

    parts = [
        f"agc_vel={vel:.2f}",
        f"agc_memo_share={share:.2f}",
        f"narrative={narr:.2f}",
    ]
    boost = 0
    confirm = vel >= vel_hot and share >= share_hot and narr >= narrative_hot
    caution = vel <= vel_cold and share <= share_cold and narr >= narrative_hot * 0.45

    if confirm:
        boost = 1
        confidence = min(0.95, confidence + 0.08)
        parts.append(
            "high-velocity cascade of agent-generated research memos into confirming narrative — soft boost"
        )
    elif caution:
        boost = -1
        confidence = min(0.93, confidence + 0.06)
        parts.append(
            "agent-memo cascade collapsed or turned adversarial while narrative heat remains elevated — caution"
        )
    else:
        parts.append("Agent-generated research memo cascade velocity overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "agc_vel": round(float(vel), 4),
        "agc_memo_share": round(float(share), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_agent_generated_memo_cascade_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate Agent-Generated Research Memo Cascade Velocity into a row."""
    mom = detect_agent_generated_memo_cascade(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "agc_vel": mom["agc_vel"],
            "agc_memo_share": mom["agc_memo_share"],
            "agc_boost": mom["signal_boost"],
            "agc_confidence": mom["confidence"],
            "agc_reason": mom["reason"],
            "agc_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + " | AGC soft boost"
    elif boost <= -1:
        if row.get("signal") in ("buy", "strong_buy"):
            row["signal"] = "hold"
        row["signal_reason"] = (row.get("signal_reason") or "") + " | AGC caution"
    return row
