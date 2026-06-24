#!/usr/bin/env python3
"""Pre-push repository checks."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOCK = [
    (r"/home/[a-zA-Z0-9_-]+/", "hardcoded home path"),
    (r"\b(?:linuxmint|VivoBook)\b", "machine hostname"),
    (r"(?<!your_)(?<!example@)@[a-zA-Z0-9.-]+\.(com|net|org)", "personal email in tracked file"),
]

REQUIRED = [
    ROOT / "README.md",
    ROOT / "LICENSE",
    ROOT / "stock_intelligence_engine.py",
    ROOT / "sie/analyzer.py",
    ROOT / "config.yaml",
]


def main() -> int:
    failed = 0
    for req in REQUIRED:
        if not req.is_file():
            print(f"MISSING {req.relative_to(ROOT)}")
            failed += 1

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts or path.suffix in {".pyc"} or ".pytest_cache" in path.parts:
            continue
        if path.suffix not in {".py", ".md", ".yaml", ".yml", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern, label in BLOCK:
            if path.name == "check_repo.py":
                continue
            if re.search(pattern, text, re.I):
                print(f"BLOCK {path.relative_to(ROOT)}: {label}")
                failed += 1
                break

    print("OK" if failed == 0 else f"FAILED {failed} checks")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())