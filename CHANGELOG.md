## [2.15.4] - 2026-08-12

### Changed
- Autonomous research & evolution cycle (August 12, 2026). Full code audit of all sie/ modules (options_iv, dark_pool, realtime, analyzer, congressional, institutional, prediction_markets, insider, social, portfolio, etc.), app.py, stock_intelligence_engine.py, config.yaml and supporting files confirmed **no additional open FUTURE-IMPROVEMENTS items** were newly implemented since v2.15.3. Roadmap remains accurate.
- Version bumped to **2.15.4** across stock_intelligence_engine.py, app.py, sie/__init__.py, README, CHANGELOG, FUTURE-IMPROVEMENTS and entry-point headers.

### Added
- Five new high-value improvements from fresh August 12 2026 research (NEXUS multi-modal news-price assimilation, MarketPsych trust indices, 2026 wash-trading risk dashboards, Streamlit + WebSocket production patterns, ICAART competing-narratives agent models):
  - **High Priority**: Delayed News-Price Assimilation Lag Detector; Social Trust / Narrative Credibility Index
  - **Medium Priority**: Suspicious Volume & Wash-Trading Risk Proxy; True Push-Style WebSocket Dashboard Updates
  - **Long-Term**: Competing-Narratives Agent-Based Stress Tester

## [2.15.3] - 2026-08-11

### Changed
- Autonomous research & evolution cycle (August 11, 2026). Full code audit of all sie/ modules (options_iv, dark_pool, realtime, analyzer, congressional, institutional, prediction_markets, insider, social, portfolio, etc.), app.py, stock_intelligence_engine.py, config.yaml and supporting files confirmed **no additional open FUTURE-IMPROVEMENTS items** were newly implemented since v2.15.2. Roadmap remains accurate.
- Version bumped to **2.15.3** across stock_intelligence_engine.py, app.py, sie/__init__.py, README, CHANGELOG, FUTURE-IMPROVEMENTS and entry-point headers.

### Added
- Five new high-value improvements from fresh August 11 2026 research (AltIndex multi-signal, STAX/TradeAlgo flow+sentiment fusion, ECB/QLoRA financial NLP advances, free CBOE/yfinance sweep detection patterns, Streamlit production hardening):
  - **High Priority**: Retail-Institutional Sentiment Divergence Overlay; Zero-Shot LLM Headline Materiality & Direction Classifier
  - **Medium Priority**: Options Sweep & Block Unusual Activity Proxy; Streamlit Fragment + Persistent Session Watchlist Hardening
  - **Long-Term**: Agentic Multi-Document Research Brief Generator

## [2.15.2] - 2026-08-09

### Changed
- Autonomous research & evolution cycle (August 9, 2026). Full code audit of sie/ modules (options_iv, dark_pool, realtime, analyzer, congressional, institutional, prediction_markets, insider, social, portfolio, etc.), app.py, stock_intelligence_engine.py, config.yaml confirmed **no additional open FUTURE-IMPROVEMENTS items** were newly implemented since v2.15.1. Roadmap remains accurate; restored complete FUTURE-IMPROVEMENTS.md and README.md that had been reduced to placeholders in prior cycle.
- Version bumped to **2.15.2** across stock_intelligence_engine.py, app.py, sie/__init__.py, README, CHANGELOG, FUTURE-IMPROVEMENTS and entry-point headers.

### Added
- Five new high-value improvements from fresh August 9 2026 research (Rolli authenticity scoring, ESG LLM-summary predictability papers, CBOE public delayed chains, event-surprise composites, dealer vanna exposure):
  - **High Priority**: Authenticity-Filtered Narrative Velocity; LLM ESG Summary Sentiment Overlay
  - **Medium Priority**: Event-Driven Surprise Composite; Free CBOE Delayed Options UOA Enhancer
  - **Long-Term**: Vanna Exposure (VEX) Proxy

## [2.15.1] - 2026-08-08

### Changed
- Autonomous research & evolution cycle (August 8, 2026). Full code audit of sie/ modules (options_iv, dark_pool, realtime, analyzer, congressional, institutional, prediction_markets, insider, social, portfolio, etc.), app.py, stock_intelligence_engine.py, config.yaml confirmed **no additional open FUTURE-IMPROVEMENTS items** were newly implemented since v2.15.0. Roadmap remains accurate.
- Version bumped to **2.15.1** across stock_intelligence_engine.py, app.py, sie/__init__.py, README, CHANGELOG, FUTURE-IMPROVEMENTS and entry-point headers.

### Added
- Five new high-value improvements from fresh August 8 2026 research (AltIndex hiring/web-traffic layers, NowNews honesty signals, MarketPsych scripted-vs-Q&A deltas, free options max-pain proxies, Streamlit 2026 patterns):
  - **High Priority**: Corporate Hiring & Headcount Momentum Tracker; Narrative-Data Honesty / Contradiction Detector
  - **Medium Priority**: Earnings Call Prepared Remarks vs Live Q&A Sentiment Delta; Company Website Traffic & Engagement Momentum Proxy
  - **Long-Term**: Max Pain & Simplified Dealer Positioning Overlay

## [2.15.0] - 2026-08-07

### Added
- **Options Implied Volatility Skew & Term Structure Overlay** fully promoted from roadmap to production (v2.15.0):
  - Module `sie/options_iv.py` already present and wired; now officially completed, version-synced and polished.
  - Pulls free yfinance options chains (nearest 1–3 expirations) or falls back to stable deterministic synthetic proxy.
  - Computes put/call IV skew and term-structure slope; applies soft signal boost/penalty on elevated fear skew or inversion.
  - Surfaces skew_ratio, term_slope, atm_iv, confidence, source, expirations and human-readable reason.
  - Fully integrated into analyzer (`include_options_iv`), CLI (`--no-options-iv`), Streamlit dashboard columns/captions, config.yaml (`options_iv:` section) and defaults in config.py.
- Five new high-value improvements from fresh August 7 2026 research (AltIndex, Adanos multi-source, CBOE/0DTE flow, FINRA short volume, EDGAR same-day filings, Streamlit fragments, Prospero/Danelfin-style composites):
  - **High Priority**: 0DTE Options Flow & Unusual Activity Proxy; Same-Day SEC EDGAR Material Filing Detector
  - **Medium Priority**: FINRA Short Volume Ratio & Squeeze Risk Overlay; Unified Multi-Platform Attention / Buzz Score
  - **Long-Term**: Gamma Exposure (GEX) Surface Proxy

### Changed
- Version bumped to **2.15.0** across stock_intelligence_engine.py, app.py, sie/__init__.py, README, CHANGELOG, FUTURE-IMPROVEMENTS and entry-point headers.
- FUTURE-IMPROVEMENTS.md: marked Options Implied Volatility Skew & Term Structure Overlay complete with date and version; added the five new research items at the bottoms of the correct priority sections.
- config.yaml + config.py defaults: added full `options_iv:` block (enabled, elevated_skew, boost_skew, penalty_skew, min_confidence, term_slope_threshold).
- CLI and analyzer flags made consistent for options_iv.
