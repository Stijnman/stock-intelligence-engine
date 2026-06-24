"""Headline fetch via yfinance (no API key required)."""

from __future__ import annotations

from dataclasses import dataclass

import yfinance as yf


@dataclass
class Headline:
    ticker: str
    title: str
    publisher: str
    link: str


def fetch_headlines(ticker: str, limit: int = 3) -> list[Headline]:
    try:
        raw = yf.Ticker(ticker).news or []
    except Exception:
        return []

    headlines: list[Headline] = []
    for item in raw[:limit]:
        content = item.get("content") or item
        title = content.get("title") or item.get("title") or ""
        if not title:
            continue
        headlines.append(
            Headline(
                ticker=ticker,
                title=title[:200],
                publisher=(content.get("provider") or {}).get("displayName", "") or item.get("publisher", ""),
                link=content.get("canonicalUrl", {}).get("url", "") or item.get("link", ""),
            )
        )
    return headlines