## [2.8.1] - 2026-07-30

### Changed
- Autonomous research & evolution cycle (July 30, 2026). Full code audit of analyzer.py, social.py, insider.py, app.py, config.yaml, stock_intelligence_engine.py and supporting modules confirmed no additional open FUTURE-IMPROVEMENTS items were implemented since v2.8.0. Roadmap remains accurate.
- Version bumped to **2.8.1** across documentation and entry-point headers for the roadmap refresh.

### Added
- Five new high-value improvements from fresh July 30 2026 research on AI stock tools, prediction markets, short interest, congressional trading, earnings whispers, and multi-LLM ensembles:
  - **High Priority**: Prediction Market Odds Overlay (Polymarket)
  - **Medium Priority**: Short Interest & Squeeze Risk Monitor; Congressional Trading Overlay
  - **Long-Term**: Earnings Whisper vs Actual Surprise Integration; Multi-LLM Ensemble Narrative Extractor

## [2.8.0] - 2026-07-29

### Added
- **Insider Form 4 Clustering & Confirmation Signals**: New module `sie/insider.py` that:
  - Pulls recent insider transactions via yfinance (`insider_transactions` / fallback attributes).
  - Applies a realistic synthetic proxy when live Form-4 data is unavailable (stable per-ticker seed).
  - Detects buy/sell clusters inside a configurable lookback window (default 14 days).
  - Emits `signal_boost` (+1 / 0 / −1), cluster size, net shares, net value, side, confidence and human-readable reason.
  - Integrates into `analyze_watchlist` / `run_report`, Streamlit dashboard (live metrics + captions), CLI (`--no-insider` flag) and Telegram path.
- Config section `insider:` in `config.yaml` and defaults in `sie/config.py` (`enabled`, `lookback_days`, `min_cluster_size`, `buy_boost_min`, `sell_penalty_min`).

### Changed
- Version bumped to **2.8.0** across `stock_intelligence_engine.py`, `app.py`, `sie/__init__.py`, README, CHANGELOG and FUTURE-IMPROVEMENTS.
- Analyzer now runs insider clustering after narrative-velocity forecast and mutates signal accordingly.
- Dashboard title and per-ticker display updated to surface insider cluster side, size and net shares.
- FUTURE-IMPROVEMENTS.md: marked Insider Form 4 item complete with date and version.

## [2.7.2] - 2026-07-29

### Changed
- Autonomous research & evolution cycle (July 29, 2026). Full code audit of analyzer.py, social.py, app.py, config.yaml, and supporting modules confirmed no additional open FUTURE-IMPROVEMENTS items were implemented since v2.7.1. Roadmap remains accurate.
- Version bumped to 2.7.2 across documentation and entry-point headers for the roadmap refresh.

### Added
- Five new high-value improvements from fresh July 29 2026 research on AI stock tools, real-time feeds, alternative media, employee sentiment, regime detection, and MCP agent tooling:
  - **High Priority**: Real-time WebSocket Price & Quote Feeds
  - **Medium Priority**: Podcast & Alternative Media Sentiment Layer; Employee Outlook & Glassdoor Sentiment Signals
  - **Long-Term**: HMM / Regime Detection Filter; MCP-Native Agent Data Hooks

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
