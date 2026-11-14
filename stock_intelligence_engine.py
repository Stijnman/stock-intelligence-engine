#!/usr/bin/env python3
"""Stock Intelligence Engine CLI entrypoint."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from sie.analyzer import run_report
from sie.config import load_config

__version__ = "2.75.0"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=f"Stock Intelligence Engine v{__version__}", allow_abbrev=False
    )
    parser.add_argument("--no-tokenized-equity-premium", action="store_true",
                        help="Disable Tokenized Equity Continuous Pricing Premium Overlay")
    parser.add_argument("--no-agentic-mcp-tool-call-latency", action="store_true",
                        help="Disable Agentic MCP Tool-Call Chain Latency & Success Rate Overlay")
    parser.add_argument("--no-expert-network-call-novelty", action="store_true",
                        help="Disable Expert Network Call Novelty & Sentiment Velocity Overlay")
    parser.add_argument("--no-signed-options-flow-toxicity", action="store_true",
                        help="Disable Signed Options Flow Toxicity & Informed Trading Probability Overlay")
    parser.add_argument("--no-unified-multi-source-narrative-freshness", action="store_true",
                        help="Disable Unified Real-Time Multi-Source Narrative Freshness Overlay")
    parser.add_argument("--no-investment", action="store_true",
                        help="Skip live Yahoo/SEC market and fundamental analysis")
    parser.add_argument("--news", action="store_true",
                        help="Fetch recent headlines and sentiment for each watchlist ticker")
    parser.add_argument("--export", action="store_true",
                        help="Export overlay rows to CSV")
    parser.add_argument("--output-dir", type=Path, default=Path("exports"),
                        help="Directory for CSV exports (default: exports)")
    parser.add_argument("--json", action="store_true",
                        help="Print the complete report as JSON")
    args = parser.parse_args(argv)

    cfg = load_config()
    switches = (
        (args.no_tokenized_equity_premium, "tokenized_equity_premium"),
        (args.no_agentic_mcp_tool_call_latency, "agentic_mcp_tool_call_latency"),
        (args.no_expert_network_call_novelty, "expert_network_call_novelty"),
        (args.no_signed_options_flow_toxicity, "signed_options_flow_toxicity"),
        (args.no_unified_multi_source_narrative_freshness, "unified_multi_source_narrative_freshness"),
    )
    for disabled, key in switches:
        if disabled:
            cfg.setdefault(key, {})["enabled"] = False

    report = run_report(
        config=cfg,
        include_investment=not args.no_investment,
        include_news=args.news,
        export=args.export,
        export_dir=args.output_dir,
    )
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False, default=str))
    else:
        print(f"Stock Intelligence Engine v{__version__}")
        print(f"Rows: {len(report.get('rows', []))}")
        print(f"Overlays enabled: {', '.join(report.get('overlays', [])) or 'none'}")
        for row in report.get("rows", [])[:3]:
            print(f"  {row['ticker']}: signal={row.get('signal')} "
                  f"tep_boost={row.get('tep_boost')} mcp_boost={row.get('mcp_boost')} "
                  f"enc_boost={row.get('enc_boost')} oft_boost={row.get('oft_boost')} "
                  f"ums_boost={row.get('ums_boost')}")
        analyses: dict[str, Any] = report.get("investment_analysis", {})
        for ticker, analysis in analyses.items():
            market = analysis.get("market", {})
            valuation = analysis.get("valuation", {})
            base = valuation.get("base", {}) if isinstance(valuation, dict) else {}
            print(f"  {ticker} market={market.get('price', 'n/a')} {market.get('currency', '')} "
                  f"DCF_base={base.get('intrinsic_value_per_share', 'n/a')}")
        if report.get("export_path"):
            print(f"CSV export: {report['export_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
