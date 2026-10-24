"""Minimal analyzer wiring the Unified Multi-Source Narrative Freshness Overlay.

Production analyzer is progressively restored; this version ensures the new
overlay is callable from CLI and dashboard for verification.
"""
from __future__ import annotations

from typing import Any

from sie.config import load_config
from sie.unified_multi_source_narrative_freshness import (
    integrate_unified_multi_source_narrative_freshness_to_row,
)


def run_report(export: bool = False, backtest: bool = False, **kwargs: Any) -> dict[str, Any]:
    """Produce a minimal report that exercises the new overlay."""
    cfg = load_config()
    tickers = list(cfg.get("tickers", {}).keys()) or ["NVDA", "TSLA", "INTC"]
    rows = []
    for tkr in tickers[:5]:
        row = {
            "ticker": tkr,
            "signal": "hold",
            "signal_reason": "baseline",
            "predicted_velocity": 1.5,
        }
        row = integrate_unified_multi_source_narrative_freshness_to_row(row, cfg)
        rows.append(row)
    return {"rows": rows, "version": "2.71.0", "overlay": "ums"}
