"""Agentic Brokerage Account Flow & Penetration Overlay.

Scores the share of order flow originating from agentic / autonomous brokerage
accounts and the intensity of tool / API usage those accounts exhibit.
Soft boost when high agentic flow share coincides with elevated tool intensity
into a confirming narrative (machines leaning into the story). Caution when
agentic accounts are aggressively exiting or tool intensity collapses while
narrative heat remains elevated (machines fading the narrative).

Live brokerage agent-flow feeds are an explicit future hook. Current source
is always labeled synthetic_proxy when a live book is unavailable.

Preferred columns: agt_flow_share, agt_tool_intensity, agt_boost, agt_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


# Names where agentic accounts typically show high penetration and constructive flow.
AGT_HOT = {
    "NVDA", "TSLA", "PLTR", "SMCI", "ARM", "AVGO", "META", "COIN",
}
# Names where agentic accounts typically show fading / defensive flow.
AGT_COLD = {
    "INTC", "PFE", "BA", "WBA", "PYPL", "NKE", "DIS",
}


def _clip(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_agentic_flow(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    a_cfg = cfg.get("agentic_flow", {})
    if not a_cfg.get("enabled", True):
        return {
            "agt_flow_share": 0.0,
            "agt_tool_intensity": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Agentic brokerage flow overlay disabled",
            "source": "disabled",
        }

    share_hot = float(a_cfg.get("share_hot", 0.28))
    share_cold = float(a_cfg.get("share_cold", 0.08))
    intensity_hot = float(a_cfg.get("intensity_hot", 0.62))
    intensity_cold = float(a_cfg.get("intensity_cold", 0.28))
    narrative_hot = float(a_cfg.get("narrative_hot", 1.4))
    min_conf = float(a_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 3107
    rng = random.Random(seed)
    row = row or {}
    narr = float(row.get("predicted_velocity") or row.get("narrative_velocity") or 1.0)

    if tkr in AGT_HOT:
        share = rng.uniform(0.32, 0.58)
        intensity = rng.uniform(0.64, 0.88)
    elif tkr in AGT_COLD:
        share = rng.uniform(0.04, 0.12)
        intensity = rng.uniform(0.12, 0.30)
    else:
        share = rng.uniform(0.10, 0.28)
        intensity = rng.uniform(0.30, 0.55)

    share_strength = _clip((share - share_cold) / max(share_hot - share_cold, 1e-6))
    intensity_strength = _clip((intensity - intensity_cold) / max(intensity_hot - intensity_cold, 1e-6))
    confidence = _clip(0.40 + 0.28 * share_strength + 0.22 * intensity_strength)

    parts = [
        f"agt_flow_share={share:.2f}",
        f"agt_tool_intensity={intensity:.2f}",
        f"narrative={narr:.2f}",
    ]
    boost = 0
    confirm = share >= share_hot and intensity >= intensity_hot and narr >= narrative_hot
    caution = share <= share_cold and intensity <= intensity_cold and narr >= narrative_hot * 0.4

    if confirm:
        boost = 1
        confidence = min(0.94, confidence + 0.08)
        parts.append(
            "high agentic account flow share with elevated tool intensity into a confirming narrative — soft boost"
        )
    elif caution:
        boost = -1
        confidence = min(0.92, confidence + 0.06)
        parts.append(
            "agentic accounts fading / low tool intensity while narrative heat remains elevated — caution"
        )
    else:
        parts.append("agentic brokerage flow & penetration overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "agt_flow_share": round(float(share), 4),
        "agt_tool_intensity": round(float(intensity), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_agentic_flow_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate agentic brokerage account flow into a row."""
    mom = detect_agentic_flow(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "agt_flow_share": mom["agt_flow_share"],
            "agt_tool_intensity": mom["agt_tool_intensity"],
            "agt_boost": mom["signal_boost"],
            "agt_confidence": mom["confidence"],
            "agt_reason": mom["reason"],
            "agt_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | agt {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | agt {mom['reason']}"
    return row
