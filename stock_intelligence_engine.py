#!/usr/bin/env python3
"""Stock Intelligence Engine CLI entrypoint."""
__version__ = "2.25.0"

from sie.analyzer import run_report
from sie.config import load_config
import argparse

def main():
    parser = argparse.ArgumentParser(description=f"Stock Intelligence Engine v{__version__}")
    parser.add_argument("--backtest", action="store_true", help="Run backtest on watchlist")
    parser.add_argument("--portfolio", action="store_true", help="Show portfolio correlation & risk metrics")
    parser.add_argument("--news", action="store_true", help="Include news headlines")
    parser.add_argument("--export", action="store_true", help="Export CSV")
    parser.add_argument("--no-thesis", action="store_true", help="Disable thesis generation")
    parser.add_argument("--no-brief", action="store_true", help="Disable self-explaining signal brief")
    parser.add_argument("--no-honesty", action="store_true", help="Disable honesty / contradiction detector")
    parser.add_argument("--no-confidence", action="store_true", help="Disable signal confidence calibration & self-critique")
    parser.add_argument("--no-regime", action="store_true", help="Disable market regime adaptive overlay weighting")
    args = parser.parse_args()
    run_report(
        include_news=args.news or True,
        export=args.export,
        backtest=args.backtest,
        include_thesis=not args.no_thesis,
        include_brief=not args.no_brief,
        include_honesty=not args.no_honesty,
        include_confidence=not args.no_confidence,
        include_regime=not args.no_regime,
    )

if __name__ == "__main__":
    main()
