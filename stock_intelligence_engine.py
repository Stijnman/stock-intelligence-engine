# Stock Intelligence Engine v1.0.6

import argparse
import yfinance as yf
from datetime import datetime
import pandas as pd
import logging
import yaml
import schedule
import time
from functools import lru_cache

__version__ = "1.0.6"

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

try:
    with open("config.yaml", "r") as f:
        CONFIG = yaml.safe_load(f) or {}
except Exception:
    CONFIG = {}

TICKERS = CONFIG.get("tickers", ["NVDA", "TSM", "CBRS", "CRDO", "MU"])
THEME = CONFIG.get("narrative", {}).get("theme", "AI Inference Boom")

@lru_cache(maxsize=32)
def get_cached_price(ticker):
    try:
        return yf.Ticker(ticker).info.get('regularMarketPrice', 'N/A')
    except Exception as e:
        logger.warning(f"Failed to fetch price for {ticker}: {e}")
        return "Error"

def get_news_headlines(ticker, limit=3):
    try:
        news_items = yf.Ticker(ticker).news or []
        return [{"title": item.get("title", ""), "publisher": item.get("publisher", "")} 
                for item in news_items[:limit]]
    except Exception as e:
        logger.warning(f"Could not fetch news for {ticker}: {e}")
        return []

def run_analysis():
    print(f"\n=== Stock Intelligence Engine {__version__} ===")
    print(f"Theme: {THEME} | Updated: {datetime.now().strftime('%H:%M:%S')}\n")
    results = []
    for ticker in TICKERS:
        price = get_cached_price(ticker)
        print(f"• {ticker}: ${price}")
        headlines = get_news_headlines(ticker)
        if headlines:
            print("  🗞️ Headlines:")
            for h in headlines:
                print(f"     - {h['title']}")
        results.append({"Ticker": ticker, "Price": price})
    return results

def daemon_mode(minutes):
    print(f"Starting daemon mode (refresh every {minutes} minutes)...")
    run_analysis()
    schedule.every(minutes).minutes.do(run_analysis)
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    parser = argparse.ArgumentParser(description=f"Stock Intelligence Engine {__version__}")
    parser.add_argument("--export", action="store_true")
    parser.add_argument("--news", action="store_true")
    parser.add_argument("--refresh", type=int, default=0)
    args = parser.parse_args()

    if args.refresh > 0:
        daemon_mode(args.refresh)
    else:
        results = run_analysis()
        if args.export:
            pd.DataFrame(results).to_csv("stock_intelligence_export.csv", index=False)
            print("\n✅ Exported to stock_intelligence_export.csv")

if __name__ == "__main__":
    main()