__version__ = "2.2.0"

"""
Stock Intelligence Engine v2.2.0

Connect market narratives to your watchlist. Confirm with technicals. Explain every signal.

New in v2.2.0: FinBERT / transformer-based sentiment scoring for news headlines.
Adds numeric sentiment delta to boost signals. Config-driven, VADER fallback.
"""

from sie.analyzer import run_report
from sie.config import load_config
import argparse

def main():
    parser = argparse.ArgumentParser(description="Stock Intelligence Engine")
    parser.add_argument("--news", action="store_true", default=True, help="Include news with FinBERT sentiment")
    parser.add_argument("--social", action="store_true", default=True, help="Include X/Twitter social scan")
    parser.add_argument("--export", action="store_true")
    parser.add_argument("--email", action="store_true")
    parser.add_argument("--lang", default="en")
    args = parser.parse_args()

    run_report(
        lang=args.lang,
        include_news=args.news,
        include_social=args.social,
        export=args.export,
        email=args.email,
    )

if __name__ == "__main__":
    main()