#!/usr/bin/env python3
"""Pre-push repository checks."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOCK = [
    (r"/home/[a-zA-Z0-9_-]+/", "hardcoded home path"),
    (r"\b(?:linuxmint|VivoBook)\b", "machine hostname"),
    # Match a complete email address instead of treating any @domain token as
    # personal information. Public project/support addresses and API-required
    # contact addresses are legitimate tracked content.
    (r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", "email address in tracked file"),
]

# These files legitimately contain public/project contact addresses. The
# hygiene check is intended to catch accidental workstation/user data, not
# reject documented contact metadata required by the project or external APIs.
EMAIL_ALLOWED = {
    Path("SECURITY.md"),
    Path("CODE_OF_CONDUCT.md"),
    Path("SKILL.md"),
    Path("sie/edgar.py"),
    Path(".github/ISSUE_TEMPLATE/config.yml"),
}

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
        relative = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern, label in BLOCK:
            if path.name == "check_repo.py":
                continue
            if label == "email address in tracked file" and relative in EMAIL_ALLOWED:
                continue
            if re.search(pattern, text, re.I):
                print(f"BLOCK {relative}: {label}")
                failed += 1
                break

    print("OK" if failed == 0 else f"FAILED {failed} checks")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
