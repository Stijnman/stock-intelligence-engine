# Changelog

## [2.1.0] - 2026-07-09

### Added
- **X/Twitter viral & sentiment scanner**: Real-time buzz_score, sentiment, mention tracking for watchlist using tweepy (official API) with graceful mock fallback and VADER integration.
- New columns in reports/dashboards: buzz_score, twitter_sentiment, mention_count.
- Config options under twitter: bearer_token, enabled, etc.
- Full integration in CLI (--social flag), analyzer, Streamlit app.py.
- Updated requirements.txt with tweepy and vaderSentiment.

### Changed
- Version bumped to v2.1.0 everywhere.
- Analyzer and report formatting enhanced for social metrics.
- Marked feature complete in FUTURE-IMPROVEMENTS.md.

## [2.0.2] - 2026-07-05
... (previous)