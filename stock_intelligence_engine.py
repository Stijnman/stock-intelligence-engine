#!/usr/bin/env python3
"""
Stock Intelligence Engine v2.0.0
Narrative-aware stock intelligence with technical confirmation.
"""

from __future__ import annotations

import argparse
import time

from sie.analyzer import run_report

__version__ = "2.0.0"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Stock Intelligence Engine — narrative + technical analysis"
    )
    parser.add_argument("--lang", default="en", choices=["en", "nl"])
    parser.add_argument("--news", action="store_true", help="Include recent headlines per ticker")
    parser.add_argument("--export", action="store_true", help="Export results to exports/*.csv")
    parser.add_argument("--email", action="store_true", help="Email report (requires .env SMTP config)")
    parser.add_argument(
        "--refresh",
        type=int,
        default=0,
        metavar="MINUTES",
        help="Daemon mode: re-run every N minutes (0 = once)",
    )
    args = parser.parse_args()

    def cycle() -> None:
        run_report(
            lang=args.lang,
            include_news=args.news,
            export=args.export,
            email=args.email,
        )

    if args.refresh <= 0:
        cycle()
        return

    print(f"Daemon mode: refresh every {args.refresh} minute(s). Ctrl+C to stop.\n")
    while True:
        cycle()
        time.sleep(max(args.refresh, 1) * 60)


if __name__ == "__main__":
    main()