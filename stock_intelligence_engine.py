#!/usr/bin/env python3
"""Stock Intelligence Engine CLI entrypoint."""
__version__ = "2.75.0"

from sie.analyzer import run_report
from sie.config import load_config
import argparse


def main():
    parser = argparse.ArgumentParser(
        description=f"Stock Intelligence Engine v{__version__}", allow_abbrev=False
    )
    parser.add_argument(
        "--no-tokenized-equity-premium",
        action="store_true",
        help="Disable Tokenized Equity Continuous Pricing Premium Overlay",
    )
    parser.add_argument(
        "--no-agentic-mcp-tool-call-latency",
        action="store_true",
        help="Disable Agentic MCP Tool-Call Chain Latency & Success Rate Overlay",
    )
    parser.add_argument(
        "--no-expert-network-call-novelty",
        action="store_true",
        help="Disable Expert Network Call Novelty & Sentiment Velocity Overlay",
    )
    parser.add_argument(
        "--no-signed-options-flow-toxicity",
        action="store_true",
        help="Disable Signed Options Flow Toxicity & Informed Trading Probability Overlay",
    )
    parser.add_argument(
        "--no-unified-multi-source-narrative-freshness",
        action="store_true",
        help="Disable Unified Real-Time Multi-Source Narrative Freshness Overlay",
    )
    args = parser.parse_args()
    cfg = load_config()
    if args.no_tokenized_equity_premium:
        cfg.setdefault("tokenized_equity_premium", {})["enabled"] = False
    if args.no_agentic_mcp_tool_call_latency:
        cfg.setdefault("agentic_mcp_tool_call_latency", {})["enabled"] = False
    if args.no_expert_network_call_novelty:
        cfg.setdefault("expert_network_call_novelty", {})["enabled"] = False
    if args.no_signed_options_flow_toxicity:
        cfg.setdefault("signed_options_flow_toxicity", {})["enabled"] = False
    if args.no_unified_multi_source_narrative_freshness:
        cfg.setdefault("unified_multi_source_narrative_freshness", {})["enabled"] = False
    result = run_report()
    print(f"Stock Intelligence Engine v{__version__}")
    print(f"Rows: {len(result.get('rows', []))}")
    for row in result.get("rows", [])[:3]:
        print(
            f"  {row.get('ticker')}: tep_boost={row.get('tep_boost')} "
            f"basis_bps={row.get('tep_basis_bps')} vol_share={row.get('tep_24_5_vol_share')} | "
            f"mcp_boost={row.get('mcp_boost')} | enc_boost={row.get('enc_boost')} | oft_boost={row.get('oft_boost')} | ums_boost={row.get('ums_boost')}"
        )


if __name__ == "__main__":
    main()
