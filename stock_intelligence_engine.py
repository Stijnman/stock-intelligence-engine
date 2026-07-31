__version__ = "2.10.0"

"""
Stock Intelligence Engine v2.10.0
Institutional 13F Ownership Change Detector + Prediction Market Odds Overlay
(Polymarket) + Insider Form 4 Clustering & Confirmation Signals +
Multi-source Narrative Velocity Forecasting + Backtesting Framework +
Real-time Dashboard.
"""
import argparse
from sie.analyzer import run_report
from sie.config import load_config


def main():
    parser = argparse.ArgumentParser(description="Stock Intelligence Engine v2.10.0")
    parser.add_argument("--backtest", action="store_true", help="Run backtest on watchlist")
    parser.add_argument("--no-insider", action="store_true", help="Disable insider Form 4 clustering")
    parser.add_argument("--no-pm", action="store_true", help="Disable Prediction Market Odds Overlay")
    parser.add_argument("--no-13f", action="store_true", help="Disable Institutional 13F Ownership Change Detector")
    parser.add_argument("--no-social", action="store_true", help="Disable X/Twitter narrative scan")
    parser.add_argument("--no-news", action="store_true", help="Disable news headlines")
    args = parser.parse_args()
    cfg = load_config()
    if args.backtest:
        from sie.backtest import backtest_watchlist
        results = backtest_watchlist(cfg)
        print("\n=== 📊 Backtesting Results ===")
        for ticker, res in results.items():
            print(f"{ticker}: {res}")
    else:
        run_report(
            backtest=False,
            include_insider=not args.no_insider,
            include_pm=not args.no_pm,
            include_institutional=not args.no_13f,
            include_social=not args.no_social,
            include_news=not args.no_news,
        )


if __name__ == "__main__":
    main()
