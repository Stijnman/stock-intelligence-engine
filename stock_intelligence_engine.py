#!/usr/bin/env python3
"""Stock Intelligence Engine CLI entrypoint."""
__version__ = "2.71.0"

from sie.analyzer import run_report
from sie.config import load_config
import argparse


def main():
    parser = argparse.ArgumentParser(
        description=f"Stock Intelligence Engine v{__version__}", allow_abbrev=False
    )
    parser.add_argument(
        "--no-unified-multi-source-narrative-freshness",
        action="store_true",
        help="Disable Unified Real-Time Multi-Source Narrative Freshness Overlay",
    )
    args = parser.parse_args()
    cfg = load_config()
    if args.no_unified_multi_source_narrative_freshness:
        cfg.setdefault("unified_multi_source_narrative_freshness", {})["enabled"] = False
    result = run_report()
    print(f"Stock Intelligence Engine v{__version__}")
    print(f"Rows: {len(result.get('rows', []))}")
    for row in result.get("rows", [])[:3]:
        print(
            f"  {row.get('ticker')}: ums_boost={row.get('ums_boost')} "
            f"fresh_s={row.get('ums_fresh_s')} sources_ok={row.get('ums_sources_ok')}"
        )


if __name__ == "__main__":
    main()
