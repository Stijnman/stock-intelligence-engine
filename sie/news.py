"""Headline fetch via yfinance with FinBERT sentiment scoring."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Optional

import yfinance as yf

try:
    from transformers import pipeline
    FINBERT_AVAILABLE = True
except ImportError:
    FINBERT_AVAILABLE = False


@dataclass
class Headline:
    ticker: str
    title: str
    publisher: str
    link: str
    sentiment_score: float = 0.0
    sentiment_label: str = "neutral"


def compute_finbert_sentiment(text: str) -> Dict[str, Any]:
    """Compute sentiment using FinBERT or fallback to VADER."""
    from sie.config import load_config
    cfg = load_config()
    sentiment_cfg = cfg.get("sentiment", {})
    if not sentiment_cfg.get("enabled", True):
        return {"score": 0.0, "label": "neutral", "reason": "Sentiment disabled"}

    if FINBERT_AVAILABLE and sentiment_cfg.get("model"):
        try:
            # Lazy load pipeline to avoid heavy import at startup
            pipe = pipeline("sentiment-analysis", model=sentiment_cfg.get("model", "ProsusAI/finbert"), device=-1)  # CPU
            result = pipe(text[:512])[0]
            label = result["label"].lower()
            score = result["score"]
            if label == "negative":
                score = -score
            return {"score": round(score, 3), "label": label, "reason": f"FinBERT ({label})"}
        except Exception as e:
            pass  # fallback

    # VADER fallback
    try:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        analyzer = SentimentIntensityAnalyzer()
        vs = analyzer.polarity_scores(text)
        score = vs["compound"]
        label = "positive" if score > 0.05 else "negative" if score < -0.05 else "neutral"
        return {"score": round(score, 3), "label": label, "reason": "VADER fallback"}
    except Exception:
        return {"score": 0.0, "label": "neutral", "reason": "No sentiment available"}


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
        sent = compute_finbert_sentiment(title)
        headlines.append(
            Headline(
                ticker=ticker,
                title=title[:200],
                publisher=(content.get("provider") or {}).get("displayName", "") or item.get("publisher", ""),
                link=content.get("canonicalUrl", {}).get("url", "") or item.get("link", ""),
                sentiment_score=sent["score"],
                sentiment_label=sent["label"],
            )
        )
    return headlines