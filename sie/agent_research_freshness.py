"""Always-On AI Agent Research Freshness & Workflow Completion Overlay.

Scores freshness of always-on agent research (memo age, workflow completion percentage)
from SuperAnalyst-style continuous workflow proxies. Soft boost when research is fresh
and high-completion into a confirming narrative; caution when agent workflows stall or
research age spikes while narrative heat remains elevated.

Live agent-monitor feeds are an explicit future hook. Current source is always labeled
synthetic_proxy when a live feed is unavailable.

Preferred columns: agt_fresh_s, agt_workflow_pct, agt_boost, agt_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


# Tickers where always-on agent research is typically high-velocity / constructive.
AGT_HOT = {
    "NVDA", "AMD", "TSLA", "PLTR", "SMCI", "AVGO", "TSM", "META", "GOOGL", "MSFT",
}
# Tickers where agent research freshness signals are typically less relevant or lagging.
AGT_COLD = {
    "INTC", "IBM", "CSCO", "ORCL", "PFE", "JNJ", "BA", "XOM",
}


def _clip(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_agent_research_freshness(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    a_cfg = cfg.get("agent_research_freshness", {})
    if not a_cfg.get("enabled", True):
        return {
            "agt_fresh_s": 0.0,
            "agt_workflow_pct": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Always-on AI agent research freshness overlay disabled",
            "source": "disabled",
        }

    fresh_hot = float(a_cfg.get("fresh_hot", 300.0))  # seconds, lower is better
    fresh_cold = float(a_cfg.get("fresh_cold", 1800.0))
    workflow_hot = float(a_cfg.get("workflow_hot", 0.85))
    workflow_cold = float(a_cfg.get("workflow_cold", 0.45))
    narrative_hot = float(a_cfg.get("narrative_hot", 1.4))
    min_conf = float(a_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 8123
    rng = random.Random(seed)
    row = row or {}
    narr = float(row.get("predicted_velocity") or row.get("narrative_velocity") or 1.0)

    if tkr in AGT_HOT:
        fresh_s = rng.uniform(60.0, 240.0)
        workflow_pct = rng.uniform(0.78, 0.96)
    elif tkr in AGT_COLD:
        fresh_s = rng.uniform(1200.0, 3600.0)
        workflow_pct = rng.uniform(0.28, 0.52)
    else:
        fresh_s = rng.uniform(240.0, 1200.0)
        workflow_pct = rng.uniform(0.48, 0.78)

    # Lower freshness seconds and higher workflow % are constructive.
    fresh_strength = _clip((fresh_cold - fresh_s) / max(fresh_cold - fresh_hot, 1e-6))
    workflow_strength = _clip((workflow_pct - workflow_cold) / max(workflow_hot - workflow_cold, 1e-6))
    confidence = _clip(0.38 + 0.30 * fresh_strength + 0.22 * workflow_strength)

    parts = [
        f"agt_fresh_s={fresh_s:.0f}",
        f"agt_workflow_pct={workflow_pct:.2f}",
        f"narrative={narr:.2f}",
    ]
    boost = 0
    confirm = fresh_s <= fresh_hot and workflow_pct >= workflow_hot and narr >= narrative_hot
    caution = fresh_s >= fresh_cold and workflow_pct <= workflow_cold and narr >= narrative_hot * 0.45

    if confirm:
        boost = 1
        confidence = min(0.95, confidence + 0.07)
        parts.append(
            "always-on agent research fresh and high workflow completion into confirming narrative — soft boost"
        )
    elif caution:
        boost = -1
        confidence = min(0.93, confidence + 0.06)
        parts.append(
            "agent workflows stalling or research age spiking while narrative heat remains elevated — caution"
        )
    else:
        parts.append("Always-on AI agent research freshness & workflow completion overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "agt_fresh_s": round(float(fresh_s), 1),
        "agt_workflow_pct": round(float(workflow_pct), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_agent_research_freshness_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate Always-On AI Agent Research Freshness & Workflow Completion into a row."""
    mom = detect_agent_research_freshness(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "agt_fresh_s": mom["agt_fresh_s"],
            "agt_workflow_pct": mom["agt_workflow_pct"],
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
