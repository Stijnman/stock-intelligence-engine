"""Unified narrative-overlay and fundamental investment analysis pipeline."""
from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sie.config import load_config
from sie.tokenized_equity_premium import integrate_tokenized_equity_premium_to_row
from sie.agentic_mcp_tool_call_latency import integrate_agentic_mcp_tool_call_latency_to_row
from sie.expert_network_call_novelty import integrate_expert_network_call_novelty_to_row
from sie.signed_options_flow_toxicity import integrate_signed_options_flow_toxicity_to_row
from sie.unified_multi_source_narrative_freshness import (
    integrate_unified_multi_source_narrative_freshness_to_row,
)

OVERLAY_PIPELINE = (
    ("unified_multi_source_narrative_freshness", integrate_unified_multi_source_narrative_freshness_to_row, "ums"),
    ("signed_options_flow_toxicity", integrate_signed_options_flow_toxicity_to_row, "oft"),
    ("expert_network_call_novelty", integrate_expert_network_call_novelty_to_row, "enc"),
    ("agentic_mcp_tool_call_latency", integrate_agentic_mcp_tool_call_latency_to_row, "mcp"),
    ("tokenized_equity_premium", integrate_tokenized_equity_premium_to_row, "tep"),
)


def run_report(
    export: bool = False,
    backtest: bool = False,
    *,
    config: dict[str, Any] | None = None,
    include_investment: bool = False,
    include_news: bool = False,
    export_dir: str | Path = "exports",
    **kwargs: Any,
) -> dict[str, Any]:
    """Build one report from the configured watchlist.

    Synthetic overlay proxies are explicitly labelled and are never presented
    as observed market data. Fundamental/market analysis is opt-in so tests,
    offline use and fast overlay-only runs remain deterministic.
    """
    cfg = config if config is not None else load_config()
    tickers_cfg = cfg.get("tickers") or {}
    tickers = list(tickers_cfg.keys()) if isinstance(tickers_cfg, dict) else list(tickers_cfg)
    tickers = [str(ticker).strip().upper() for ticker in tickers if str(ticker).strip()]
    if not tickers:
        tickers = ["NVDA", "TSLA", "INTC", "AAPL", "MSFT"]

    rows: list[dict[str, Any]] = []
    investment_results: dict[str, Any] = {}
    news_results: dict[str, Any] = {}
    enabled_overlays: list[str] = []

    for ticker in tickers[:5]:
        row: dict[str, Any] = {
            "ticker": ticker,
            "signal": "hold",
            "signal_reason": "Narrative baseline only; not a trade recommendation.",
            "predicted_velocity": 1.5,
            "overlay_data_mode": "synthetic_proxy",
            "overlay_warning": "Overlay inputs are deterministic synthetic proxies, not live market observations.",
        }
        for config_key, integrate, short_name in OVERLAY_PIPELINE:
            overlay_cfg = cfg.get(config_key, {})
            if overlay_cfg.get("enabled", True):
                row = integrate(row, cfg)
                if short_name not in enabled_overlays:
                    enabled_overlays.append(short_name)
            else:
                row[f"{short_name}_status"] = "disabled"
        rows.append(row)

        if include_investment:
            try:
                from sie.investment.analyst import analyze_stock
                investment_results[ticker] = analyze_stock(ticker)
            except Exception as exc:
                investment_results[ticker] = {
                    "ticker": ticker,
                    "status": "unavailable",
                    "error": f"{type(exc).__name__}: {exc}",
                    "data_quality": ["Market-data analysis failed; no investment conclusion generated."],
                }
            row["investment_analysis"] = investment_results[ticker]
            row["investment_status"] = investment_results[ticker].get("status", "available")

        if include_news:
            try:
                from sie.news import fetch_headlines
                headlines = fetch_headlines(ticker)
                news_results[ticker] = [
                    asdict(item) if is_dataclass(item) else dict(item)
                    for item in headlines
                ]
            except Exception as exc:
                news_results[ticker] = {"status": "unavailable", "error": str(exc)}
            row["news"] = news_results[ticker]

    result: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "2.75.0",
        "rows": rows,
        "overlays": enabled_overlays,
        "data_quality": {
            "overlay_inputs": "synthetic_proxy",
            "investment_analysis": "live_provider_data_when_requested",
            "warning": "Synthetic overlay scores must not be interpreted as real market evidence.",
        },
    }
    if include_investment:
        result["investment_analysis"] = investment_results
    if include_news:
        result["news"] = news_results
    if backtest:
        result["backtest"] = {
            "status": "not_implemented",
            "reason": "No leakage-safe historical backtest is wired into this report pipeline.",
        }
    if export:
        from sie.export import export_csv
        result["export_path"] = str(export_csv(rows, directory=export_dir))
    return result
