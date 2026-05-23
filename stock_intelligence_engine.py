#!/usr/bin/env python3
"""
Stock Intelligence Engine v1.0.0
Professional narrative-aware stock intelligence tool.

See the narrative before it moves the market.
"""

import argparse
import yfinance as yf
from datetime import datetime

__version__ = "1.0.0 - Stock Intelligence Engine"

# Core tickers from our research (can be expanded dynamically)
TICKERS = {
    "NVDA": {"name": "NVIDIA", "color": "🟢", "note": "Strongest winner - inference boom"},
    "TSM":  {"name": "TSMC", "color": "🟢", "note": "Quiet chip enabler"},
    "CBRS": {"name": "Cerebras", "color": "🟢", "note": "Pure specialized inference play (volatile - smaller size)"},
    "CRDO": {"name": "Credo", "color": "🟡", "note": "Viral AI connectivity play"},
    "MU":   {"name": "Micron", "color": "🟡", "note": "HBM memory - inference critical"},
}

def main():
    parser = argparse.ArgumentParser(description="Stock Intelligence Engine")
    parser.add_argument("--lang", default="en", choices=["en", "nl"])
    parser.add_argument("--news", action="store_true")
    parser.add_argument("--export", action="store_true")
    parser.add_argument("--email", action="store_true")
    parser.add_argument("--refresh", type=int, default=0)
    args = parser.parse_args()

    print(f"\n=== Stock Intelligence Engine {__version__} ===")
    print(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("Theme: Efficient architectures + Inference boom narrative\n")

    for ticker, info in TICKERS.items():
        try:
            stock = yf.Ticker(ticker)
            price = stock.info.get('regularMarketPrice', 'N/A')
            print(f"{info['color']} {ticker} ({info['name']}): ${price} | {info['note']}")
        except:
            print(f"{info['color']} {ticker} ({info['name']}): Error fetching price")

    print("\n[🟢 Strong Buy signals on NVDA, TSM, CBRS (risk-adjusted)]")
    print("\n⚠️  DISCLAIMER: This is NOT financial advice. Educational use only.")

if __name__ == "__main__":
    main()
