__version__ = "2.12.1"

"""
Stock Intelligence Engine v2.12.1
Congressional Trading Overlay + Portfolio Correlation Heatmap & Risk Overlay +
Institutional 13F Ownership Change Detector + Prediction Market Odds Overlay
(Polymarket) + Insider Form 4 Clustering & Confirmation Signals + Multi-source
Narrative Velocity Forecasting + Backtesting Framework + Real-time Dashboard.
"""
import argparse
from sie.analyzer import run_report
from sie.config import load_config


def main():
    parser = argparse.ArgumentParser(description="Stock Intelligence Engine v2.12.1")
    parser.add_argument("--backtest", action="store_true", help="Run backtest on watchlist")
    parser.add_argument("--portfolio", action="store_true", help="Show portfolio correlation & risk metrics")
    parser.add_argument("--no-insider", action="store_true", help="Disable insider Form 4 clustering")
    parser.add_argument("--no-pm", action="store_true", help="Disable Prediction Market Odds Overlay")
    parser.add_argument("--no-13f", action="store_true", help="Disable Institutional 13F Ownership Change Detector")
    parser.add_argument("--no-congress", action="store_true", help="Disable Congressional Trading Overlay")
    parser.add_argument("--no-social", action="store_true", help="Disable X/Twitter narrative scan")
    parser.add_argument("--no-news", action="store_true", help="Disable news headlines")
    args = parser.parse_args()
    cfg = load_config()
    if args.portfolio:
        from sie.portfolio import compute_portfolio_overlay
        overlay = compute_portfolio_overlay(cfg)
        print("\n=== 📊 Portfolio Correlation & Risk Overlay ===")
        metrics = overlay.get("metrics", {})
        print(f"Assets: {metrics.get('n_assets')} | Period: {overlay.get('period')}")
        print(f"Ann. Vol: {metrics.get('vol_ann')} | Sharpe: {metrics.get('sharpe')}")
        print(f"Max DD: {metrics.get('max_drawdown')}% | Mean Corr: {metrics.get('mean_corr')}")
        print(f"Source: {overlay.get('source')}")
        corr = overlay.get("correlation", {})
        if corr:
            print("\nCorrelation matrix (partial):")
            for t, row in list(corr.items())[:5]:
                print(f"  {t}: {row}")
    elif args.backtest:
        from sie.backtest import backtest_watchlist
        results = backtest_watchlist(cfg)
        print("\n=== 📊 Backtesting Results ===")
        for ticker, res in results.items():
            print(f"{ticker}: {res}")
        # Append portfolio metrics
        from sie.portfolio import compute_portfolio_overlay
        overlay = compute_portfolio_overlay(cfg)
        print("\n=== Equal-weight Portfolio Risk ===")
        print(overlay.get("metrics", {}))
    else:
        run_report(
            backtest=False,
            include_insider=not args.no_insider,
            include_pm=not args.no_pm,
            include_institutional=not args.no_13f,
            include_congressional=not args.no_congress,
            include_social=not args.no_social,
            include_news=not args.no_news,
        )


if __name__ == "__main__":
    main()
