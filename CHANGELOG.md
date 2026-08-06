## [2.14.1] - 2026-08-06

### Changed
- Autonomous research & evolution cycle (August 6, 2026). Full code audit of sie/dark_pool.py, realtime.py, analyzer.py, app.py, stock_intelligence_engine.py, portfolio.py, congressional.py, institutional.py, prediction_markets.py, insider.py, social.py, config.yaml and supporting modules confirmed no additional open FUTURE-IMPROVEMENTS items were newly implemented since v2.14.0. Roadmap remains accurate.
- Version bumped to **2.14.1** across documentation and entry-point headers for the roadmap refresh + new research items.

### Added
- Four new high-value improvements from fresh August 6 2026 research on AI stock platforms (Prospero, Zen Ratings, Fiscal.ai, Danelfin, AlphaSense), narrative/sentiment advances (ECB FinBERT/GPT, HBS AI-summary market reaction study), alternative data (AltIndex, Adanos multi-source, Truth Social API), and agentic fundamentals (as-reported data):
  - **High Priority**: Truth Social / Official Political Narrative Overlay
  - **Medium Priority**: Retail Whisper Number vs Consensus Divergence Tracker; As-Reported Fundamentals Preference & Restatement Alert Layer
  - **Long-Term**: AI News Summary Engagement Multiplier

## [2.14.0] - 2026-08-05

### Added
- **Dark Pool / ATS Off-Exchange Flow Overlay**: New module `sie/dark_pool.py` that:
  - Detects elevated off-exchange / ATS volume relative to average daily volume using a stable synthetic daily proxy (FINRA ATS transparency style) as the free default, with clean extension points for live FINRA weekly data.
  - Infers institutional accumulation or distribution and applies soft confirmation boost/penalty (+1 / 0 / −1) as an additional smart-money layer alongside 13F, insider Form 4 and congressional overlays.
  - Surfaces relative volume ratio, ATS volume, ADV, side, confidence, top venues and human-readable reason.
  - Fully integrated into analyzer, CLI (`--no-dark-pool` flag), Streamlit dashboard (live ATS columns + captions), config.yaml (`dark_pool:` section).
- Config keys: `dark_pool.enabled`, `elevated_ratio`, `boost_ratio`, `penalty_ratio`, `min_confidence`.
- Also wired the previously missing `include_realtime` path through `analyze_watchlist` / `run_report` for full consistency with CLI and dashboard flags.

### Changed
- Version set to **2.14.0** across `stock_intelligence_engine.py`, `app.py`, `sie/__init__.py`, README, CHANGELOG and FUTURE-IMPROVEMENTS.
- Analyzer now runs dark-pool overlay after the realtime layer and mutates signal accordingly.
- Dashboard title, display columns and per-ticker captions updated to surface dark-pool side and relative ratio.
- FUTURE-IMPROVEMENTS.md: marked Dark Pool / ATS Off-Exchange Flow Overlay complete with date and version.

## [2.13.1] - 2026-08-05

### Changed
- Autonomous research & evolution cycle (August 5, 2026). Full code audit of sie/realtime.py, analyzer.py, app.py, stock_intelligence_engine.py, portfolio.py, congressional.py, institutional.py, prediction_markets.py, insider.py, social.py, config.yaml and supporting modules confirmed **Real-time WebSocket Price & Quote Feeds** fully implemented (synthetic low-latency proxy + extension points) and live in CLI/dashboard since the v2.13.0 code path. Roadmap cleaned accordingly.
- Version bumped to **2.13.1** across documentation and entry-point headers for the roadmap refresh + new research items.

### Added
- Five new high-value improvements from fresh August 5 2026 research on AI stock analysis platforms (Prospero, Danelfin, Zen Ratings, Fiscal.ai, FinSMART, AlphaSense, ECB sentiment methods, agentic narrative finance):
  - **High Priority**: Options Implied Volatility Skew & Term Structure Overlay
  - **Medium Priority**: Multi-Factor Composite AI Score (0–100); Earnings Surprise Magnitude & Post-Drift Context
  - **Long-Term**: Narrative Contagion Rate Tracker; Prompt-Based Financial-Stability Sentiment Filter

## [2.13.0] - 2026-08-05

### Added
- **Real-time WebSocket Price & Quote Feeds**: New module `sie/realtime.py` providing low-latency quotes via stable synthetic tick generator (deterministic per-minute) as free default, with clean hooks for real WebSocket providers (Polygon, Massive, Finnhub). Surfaces price, bid/ask, change %, volume, source, latency_ms. Integrated into analyzer row enrichment, CLI (`--no-realtime`), Streamlit dashboard captions and columns.

### Changed
- Version set to **2.13.0** in stock_intelligence_engine.py, app.py, sie/__init__.py.

## [2.12.1] - 2026-08-04

### Changed
- Autonomous research & evolution cycle (August 4, 2026). Full code audit of analyzer.py, social.py, insider.py, institutional.py, prediction_markets.py, congressional.py, portfolio.py, app.py, config.yaml, stock_intelligence_engine.py and supporting modules confirmed no additional open FUTURE-IMPROVEMENTS items were newly implemented since v2.12.0. Roadmap remains accurate.
- Version bumped to **2.12.1** across documentation and entry-point headers for the roadmap refresh.

### Added
- Five new high-value improvements from fresh August 4 2026 research on AI stock tools, dark-pool/ATS flow, technical pattern AI, correlation shocks, market-aligned sentiment (FinSMART-style), and free-tier options proxies:
  - **High Priority**: Dark Pool / ATS Off-Exchange Flow Overlay
  - **Medium Priority**: AI Technical Pattern Confirmation Layer; Cross-Asset Correlation Shock Detector
  - **Long-Term**: Market-Outcome-Aligned Sentiment Refiner; Free-Tier Unusual Options Activity Proxy

## [2.12.0] - 2026-08-02

### Added
- Congressional Trading Overlay fully implemented.

# Previous entries retained for history.
