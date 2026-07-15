__version__ = "2.3.0"

"""
Stock Intelligence Engine v2.3.0

CLI entrypoint with Telegram alerts.
"""
import argparse
from sie.analyzer import run_report
from sie.config import load_config

def main():
    parser = argparse.ArgumentParser(description="Stock Intelligence Engine")
    parser.add_argument("--no-news", action="store_true")
    parser.add_argument("--no-social", action="store_true")
    parser.add_argument("--export", action="store_true")
    parser.add_argument("--email", action="store_true")
    parser.add_argument("--telegram", action="store_true", help="Send Telegram alert")
    parser.add_argument("--lang", default="en")
    args = parser.parse_args()

    run_report(
        lang=args.lang,
        include_news=not args.no_news,
        include_social=not args.no_social,
        export=args.export,
        email=args.email,
        telegram=args.telegram,
    )

if __name__ == "__main__":
    main()
