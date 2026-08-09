__version__ = "2.15.2"

"""
Stock Intelligence Engine v2.15.2
Options Implied Volatility Skew & Term Structure Overlay + Dark Pool / ATS Off-Exchange Flow Overlay +
Real-time WebSocket Price & Quote Feeds + Congressional Trading Overlay +
Portfolio Correlation Heatmap & Risk Overlay + Institutional 13F Ownership Change Detector +
Prediction Market Odds Overlay (Polymarket) + Insider Form 4 Clustering & Confirmation Signals +
Multi-source Narrative Velocity Forecasting + Backtesting Framework + Real-time Dashboard.
"""
import argparse
from sie.analyzer import run_report
from sie.config import load_config


def main():
    parser = argparse.ArgumentParser(description="Stock Intelligence Engine v2.15.2")
    parser.add_argument("--backtest", action="store_true", help="Run backtest on watchlist")
    parser.add_argument("--portfolio", action="store_true", help="Show portfolio correlation & risk metrics")
    parser.add_argument("--no-insider", action="store_true", help="Disable insider Form 4 clustering")
    parser.add_argument("--no-pm", action="store_true", help="Disable prediction markets overlay")
    parser.add_argument("--no-13f", action="store_true", help="Disable institutional 13F overlay")
    parser.add_argument("--no-congress", action="store_true", help="Disable congressional trading overlay")
    parser.add_argument("--no-realtime", action="store_true", help="Disable realtime quotes")
    parser.add_argument("--no-dark-pool", action="store_true", help="Disable dark pool overlay")
    parser.add_argument("--no-options-iv", action="store_true", help="Disable options IV skew overlay")
    parser.add_argument("--lang", default="en", help="Language code")
    args = parser.parse_args()

    cfg = load_config()
    report = run_report(
        cfg,
        include_insider=not args.no_insider,
        include_pm=not args.no_pm,
        include_institutional=not args.no_13f,
        include_congressional=not args.no_congress,
        include_realtime=not args.no_realtime,
        include_dark_pool=not args.no_dark_pool,
        include_options_iv=not args.no_options_iv,
        lang=args.lang,
        do_backtest=args.backtest,
        do_portfolio=args.portfolio,
    )
    print(report)


if __name__ == "__main__":
    main()
