"""CLI for the free-first Investment Intelligence engine."""
import argparse, json, sys
from pathlib import Path
from sie.investment.analyst import analyze_stock
from sie.investment.etfs import analyze_etf
from sie.investment.portfolio import analyze_portfolio
from sie.investment.providers import quote_and_history
from sie.investment.technical import analyze_history

def main() -> int:
    parser = argparse.ArgumentParser(prog="sie-invest", description="Free-first stock and ETF research")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("analyze", "quote"):
        p = sub.add_parser(name); p.add_argument("ticker")
    compare = sub.add_parser("compare"); compare.add_argument("tickers", help="Comma-separated ticker symbols")
    portfolio = sub.add_parser("portfolio"); portfolio.add_argument("csv_path", type=Path)
    etf = sub.add_parser("etf"); etf.add_argument("metadata_json", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "analyze": payload = analyze_stock(args.ticker)
        elif args.command == "quote":
            raw = quote_and_history(args.ticker)
            payload = {"market": {k: v for k, v in raw.items() if k not in {"history", "dividends"}},
                       "technical": analyze_history(raw["history"])}
        elif args.command == "compare":
            symbols = [x.strip().upper() for x in args.tickers.split(",") if x.strip()]
            if not symbols: raise ValueError("Provide at least one ticker")
            payload = {"comparisons": [analyze_stock(symbol) for symbol in symbols]}
        elif args.command == "portfolio": payload = analyze_portfolio(args.csv_path)
        else: payload = analyze_etf(json.loads(args.metadata_json.read_text(encoding="utf-8")))
        print(json.dumps(payload, indent=2, ensure_ascii=False)); return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr); return 2

if __name__ == "__main__":
    raise SystemExit(main())
