"""Agentic MCP Tool-Call Chain Latency & Success Rate Overlay.

Scores tool-call latency and success/completion rate from agentic research
workflows against financial MCP servers (Distilla, Equibles, Alpha Vantage MCP, etc.).
Soft boost when low latency and high success rate confirm a narrative into
technical strength; caution on elevated latency, tool failures, or incomplete
chains while narrative heat remains elevated.

Live MCP telemetry is an explicit future hook. Current source is always
labeled synthetic_proxy when a live feed is unavailable.

Preferred columns: mcp_latency_ms, mcp_success_rate, mcp_boost, mcp_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


# Tickers with typically fast, high-success MCP agent chains.
MCP_HOT = {
    "NVDA", "TSLA", "PLTR", "SMCI", "AVGO", "META", "AMD", "ARM", "CRWD", "NET",
}
# Tickers with typically slow or failure-prone MCP chains.
MCP_COLD = {
    "INTC", "BA", "PFE", "XOM", "WMT", "KO", "IBM", "CSCO",
}


def _clip(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_agentic_mcp_tool_call_latency(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    o_cfg = cfg.get("agentic_mcp_tool_call_latency", {})
    if not o_cfg.get("enabled", True):
        return {
            "mcp_latency_ms": 0.0,
            "mcp_success_rate": 0.5,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Agentic MCP tool-call latency overlay disabled",
            "source": "disabled",
        }

    lat_hot = float(o_cfg.get("lat_hot", 180.0))
    lat_cold = float(o_cfg.get("lat_cold", 1200.0))
    succ_hot = float(o_cfg.get("succ_hot", 0.82))
    succ_cold = float(o_cfg.get("succ_cold", 0.45))
    narrative_hot = float(o_cfg.get("narrative_hot", 1.4))
    min_conf = float(o_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 24203
    rng = random.Random(seed)
    row = row or {}
    narr = float(row.get("predicted_velocity") or row.get("narrative_velocity") or 1.0)

    if tkr in MCP_HOT:
        latency_ms = rng.uniform(80.0, 220.0)
        success_rate = rng.uniform(0.78, 0.96)
    elif tkr in MCP_COLD:
        latency_ms = rng.uniform(900.0, 2400.0)
        success_rate = rng.uniform(0.22, 0.48)
    else:
        latency_ms = rng.uniform(250.0, 850.0)
        success_rate = rng.uniform(0.45, 0.78)

    lat_strength = _clip((lat_cold - latency_ms) / max(lat_cold - lat_hot, 1e-6))
    succ_strength = _clip((success_rate - succ_cold) / max(succ_hot - succ_cold, 1e-6))
    confidence = _clip(0.30 + 0.35 * lat_strength + 0.29 * succ_strength)

    parts = [
        f"mcp_latency_ms={latency_ms:.0f}",
        f"mcp_success_rate={success_rate:.2f}",
        f"narrative={narr:.2f}",
    ]
    boost = 0
    confirm = latency_ms <= lat_hot and success_rate >= succ_hot and narr >= narrative_hot
    caution = latency_ms >= lat_cold and success_rate <= succ_cold and narr >= narrative_hot * 0.45

    if confirm:
        boost = 1
        confidence = min(0.95, confidence + 0.08)
        parts.append(
            "low MCP tool-call latency with high success rate — soft boost"
        )
    elif caution:
        boost = -1
        confidence = min(0.93, confidence + 0.06)
        parts.append(
            "elevated MCP latency or low success rate while narrative heat remains elevated — caution"
        )
    else:
        parts.append("Agentic MCP tool-call latency overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "mcp_latency_ms": round(float(latency_ms), 1),
        "mcp_success_rate": round(float(success_rate), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_agentic_mcp_tool_call_latency_to_row(
    row: dict, cfg: dict | None = None
) -> dict:
    """Integrate Agentic MCP Tool-Call Latency into a row."""
    mom = detect_agentic_mcp_tool_call_latency(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "mcp_latency_ms": mom["mcp_latency_ms"],
            "mcp_success_rate": mom["mcp_success_rate"],
            "mcp_boost": mom["signal_boost"],
            "mcp_confidence": mom["confidence"],
            "mcp_reason": mom["reason"],
            "mcp_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + " | MCP soft boost"
    elif boost <= -1:
        if row.get("signal") in ("buy", "strong_buy"):
            row["signal"] = "hold"
        row["signal_reason"] = (row.get("signal_reason") or "") + " | MCP caution"
    return row
