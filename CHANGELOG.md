# Changelog

## [2.2.0] - 2026-07-12

### Added
- **FinBERT / transformer-based sentiment scoring**: For news headlines per ticker. Adds sentiment_score (-1 to +1) and label to headlines. Config under `sentiment:`. Integrates into signals, boosts reasoning in CLI/Streamlit.
- New fields in reports: news sentiment per headline.
- Graceful fallback to VADER, lazy loading for transformers.
- Updated requirements.txt with `transformers`.
- Full integration in analyzer, news, dashboard, CLI.

### Changed
- Version bumped to v2.2.0 everywhere.
- Default include_news=True, enhanced report formatting.
- Marked FinBERT feature complete in FUTURE-IMPROVEMENTS.md.

## [2.1.0] - 2026-07-09
... (previous)