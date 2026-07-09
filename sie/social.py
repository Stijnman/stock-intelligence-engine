"""X/Twitter viral & sentiment scanner for watchlist tickers."""
from __future__ import annotations

import tweepy
from datetime import datetime, timedelta
from typing import Any, Dict
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from sie.config import load_config

analyzer = SentimentIntensityAnalyzer()

def get_twitter_client(cfg: dict | None = None):
    cfg = cfg or load_config()
    twitter_cfg = cfg.get("twitter", {})
    bearer = twitter_cfg.get("bearer_token") or ""
    if not bearer:
        # Fallback mock for demo
        return None
    return tweepy.Client(bearer_token=bearer)

def scan_viral_sentiment(ticker: str, cfg: dict | None = None) -> Dict[str, Any]:
    """Scan X for mentions, compute buzz_score and sentiment."""
    cfg = cfg or load_config()
    twitter_cfg = cfg.get("twitter", {})
    if not twitter_cfg.get("enabled", True):
        return {"buzz_score": 0.0, "sentiment": 0.0, "mention_count": 0, "reason": "Twitter scanner disabled"}

    client = get_twitter_client(cfg)
    if client is None:
        # Mock data for local testing/demo
        import random
        mention_count = random.randint(5, 50)
        sentiment = random.uniform(-0.5, 0.8)
        buzz = min(1.0, mention_count / 20.0 + abs(sentiment))
        return {
            "buzz_score": round(buzz, 2),
            "sentiment": round(sentiment, 2),
            "mention_count": mention_count,
            "reason": "Mock X data (add bearer_token for real)",
            "recent_posts": ["Mock post about $TICKER AI hype."]
        }

    # Real implementation
    try:
        query = f"${ticker} OR {ticker} lang:en -is:retweet"
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=twitter_cfg.get("lookback_hours", 24))
        response = client.search_recent_tweets(
            query=query,
            max_results=twitter_cfg.get("search_limit", 50),
            start_time=start_time,
            end_time=end_time,
        )
        tweets = response.data or []
        mention_count = len(tweets)
        if mention_count == 0:
            return {"buzz_score": 0.0, "sentiment": 0.0, "mention_count": 0, "reason": "No recent mentions"}

        sentiments = [analyzer.polarity_scores(t.text)["compound"] for t in tweets]
        avg_sentiment = sum(sentiments) / len(sentiments)
        buzz_score = min(1.0, (mention_count / 30.0) + (avg_sentiment * 0.5 if avg_sentiment > 0 else 0))

        return {
            "buzz_score": round(buzz_score, 2),
            "sentiment": round(avg_sentiment, 2),
            "mention_count": mention_count,
            "reason": f"{mention_count} mentions, avg sentiment {avg_sentiment:.2f}",
            "recent_posts": [t.text[:100] + "..." for t in tweets[:3]]
        }
    except Exception as e:
        return {"buzz_score": 0.0, "sentiment": 0.0, "mention_count": 0, "reason": f"Error: {str(e)}"}

def integrate_social_to_row(row: dict, cfg: dict | None = None):
    """Add social metrics to analysis row."""
    social = scan_viral_sentiment(row["ticker"], cfg)
    row.update({
        "buzz_score": social["buzz_score"],
        "twitter_sentiment": social["sentiment"],
        "mention_count": social["mention_count"],
        "social_reason": social["reason"],
    })
    return row