## [2.7.1] - 2026-07-28

### Changed
- Autonomous research & evolution cycle (July 28, 2026). Full code audit confirmed no additional open FUTURE-IMPROVEMENTS items were implemented since v2.7.0. Roadmap remains accurate.
- Version bumped to 2.7.1 across documentation and entry-point headers for the roadmap refresh.

### Added
- Five new high-value improvements from fresh July 2026 research on AI stock tools, narrative intelligence, alternative data, prediction markets, insider activity, and agentic workflows:
  - **High Priority**: Insider Form 4 Clustering & Confirmation Signals
  - **Medium Priority**: Cross-Platform Narrative Convergence Score; Analyst Estimate Revision Momentum Tracker
  - **Long-Term**: Grok / xAI Agent Deep-Research Hook; Alternative Data Proxies (Hiring & Web Traffic)

## [2.7.0] - 2026-07-25

### Added
- **Multi-source Narrative Velocity Forecasting**: Lightweight exponential smoothing forecast combining X/Twitter sentiment_velocity + news FinBERT/VADER scores. Predicts short-term narrative phase (hype / dip / recovery / neutral) 1–3 days ahead. Applies forward-looking signal boost or penalty inside analyzer. Exposed in Streamlit dashboard with confidence and reason strings. Configurable via `forecast:` section in config.yaml (smoothing_alpha, horizon_days).
- New functions: `simple_exponential_smoothing`, `forecast_narrative_phase` in sie/social.py.

### Changed
- Version bumped to 2.7.0 across headers, app.py, stock_intelligence_engine.py, README, docs.
- Analyzer now always runs forecast after social + news integration and mutates signal accordingly.
- Dashboard displays predicted phase + confidence next to each ticker.

## [2.6.1] - 2026-07-25

### Changed
- Roadmap cleanup: Moved fully implemented items (Narrative Phase Labels via dominant_narrative, pytest coverage for RSI/MA, VADER fallback already present in news.py) from open High Priority into Completed section.
- Version bump to 2.6.1 across core files and documentation.

### Added
- Five new research-backed improvements (July 2026 scan of AI stock tools, narrative intelligence, options/dark-pool data, Streamlit 2026 patterns):
  - High: Multi-source Narrative Velocity Forecasting
  - Medium: Portfolio Correlation Heatmap & Risk Overlay; Streamlit Partial Reruns + Advanced Caching
  - Long-Term: SEC EDGAR 8-K NLP Alerts; Unusual Options Activity + Dark Pool Print Signals

## [2.6.0] - 2026-07-23

### Added
- **Backtesting Framework**: Historical signal backtesting with Sharpe ratio, returns metrics using yfinance data.
- Integration in CLI (`--backtest`), Streamlit dashboard (interactive button), and core analyzer.
- Config options for backtest periods.

### Changed
- Version bumped to 2.6.0 across files.
- Updated documentation, FUTURE-IMPROVEMENTS.md marked complete.

## [2.5.2] - 2026-07-23

### Added
- New high-value roadmap items from fresh research cycle.

# Previous
...
