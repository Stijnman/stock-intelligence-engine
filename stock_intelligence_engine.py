__version__ = "2.7.0"

"""
Stock Intelligence Engine v2.7.0
Multi-source Narrative Velocity Forecasting + Backtesting Framework + Real-time Dashboard.
"""
import argparse
from sie.analyzer import run_report
from sie.config import load_config

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--backtest', action='store_true', help='Run backtest on watchlist')
    args = parser.parse_args()
    cfg = load_config()
    if args.backtest:
        from sie.backtest import backtest_watchlist
        results = backtest_watchlist(cfg)
        print("\n=== 📊 Backtesting Results ===")
        for ticker, res in results.items():
            print(f"{ticker}: {res}")
    else:
        run_report(backtest=True)

if __name__ == "__main__":
    main()
