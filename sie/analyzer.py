"""Analyzer wiring Tokenized Equity Continuous Pricing Premium Overlay (v2.75.0).

Also retains prior Agentic MCP Tool-Call Latency, Expert Network Call Novelty, Signed Options Flow Toxicity and Unified Multi-Source Narrative Freshness for continuity.
"""
from __future__ import annotations

from typing import Any

from sie.config import load_config
from sie.tokenized_equity_premium import integrate_tokenized_equity_premium_to_row
from sie.agentic_mcp_tool_call_latency import integrate_agentic_mcp_tool_call_latency_to_row
from sie.expert_network_call_novelty import integrate_expert_network_call_novelty_to_row
from sie.signed_options_flow_toxicity import integrate_signed_options_flow_toxicity_to_row
from sie.unified_multi_source_narrative_freshness import (
    integrate_unified_multi_source_narrative_freshness_to_row,
)


def run_report(export: bool = False, backtest: bool = False, **kwargs: Any) -> dict[str, Any]:
    """Produce a report exercising the latest overlays."""
    cfg = load_config()
    tickers = list(cfg.get("tickers", {}).keys()) or ["NVDA", "TSLA", "INTC", "AAPL", "MSFT"]
    rows = []
    for tkr in tickers[:5]:
        row = {
            "ticker": tkr,
            "signal": "hold",
            "signal_reason": "baseline",
            "predicted_velocity": 1.5,
        }
        row = integrate_unified_multi_source_narrative_freshness_to_row(row, cfg)
        row = integrate_signed_options_flow_toxicity_to_row(row, cfg)
        row = integrate_expert_network_call_novelty_to_row(row, cfg)
        row = integrate_agentic_mcp_tool_call_latency_to_row(row, cfg)
        row = integrate_tokenized_equity_premium_to_row(row, cfg)
        rows.append(row)
    return {"rows": rows, "version": "2.75.0", "overlays": ["ums", "oft", "enc", "mcp", "tep"]}
