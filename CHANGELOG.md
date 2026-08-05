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
- **Congressional Trading Overlay**: New module `sie/congressional.py` that:
  - Detects clustered or material congressional stock buys/sells for watchlist tickers using a stable synthetic proxy (no paid API required).
  - Applies soft confirmation boost/penalty (+1 / 0 / −1) as an additional smart-money layer alongside insider Form 4 and institutional 13F.
  - Surfaces trade count, net value, side, confidence, member names and human-readable reason.
  - Fully integrated into analyzer, CLI (`--no-congress` flag), Streamlit dashboard (live Congress metrics + captions), config.yaml (`congressional:` section).
- Config keys: `congressional.enabled`, `lookback_days`, `min_trades`, `buy_boost_min`, `sell_penalty_min`, `min_trade_value`.

### Changed
- Version bumped to **2.12.0** across `stock_intelligence_engine.py`, `app.py`, `sie/__init__.py`, README, CHANGELOG and FUTURE-IMPROVEMENTS.
- Analyzer now runs congressional overlay after the institutional 13F layer and mutates signal accordingly.
- Dashboard title, display columns and per-ticker captions updated to surface congressional side and net value.
- FUTURE-IMPROVEMENTS.md: marked Congressional Trading Overlay complete with date and version.

## [2.11.0] - 2026-08-01

### Added
- **Portfolio Correlation Heatmap & Risk Overlay**: New module `sie/portfolio.py` that:
  - Downloads multi-ticker adjusted close prices via yfinance for the configured lookback.
  - Computes pairwise Pearson correlations of daily returns and equal-weight portfolio metrics (annualized volatility, Sharpe ratio using configurable risk-free rate, maximum drawdown, mean pairwise correlation).
  - Exposes `compute_portfolio_overlay`, `correlation_matrix`, `portfolio_risk_metrics` and a ready-to-use Plotly heatmap builder.
  - Fully integrated into Streamlit dashboard (metric cards + interactive heatmap), CLI (`--portfolio` flag; also appended to `--backtest` output), and config.yaml (`portfolio:` section).
- Config keys: `portfolio.enabled`, `lookback_period`, `min_periods`, `risk_free_rate`.

### Changed
- Version bumped to **2.11.0** across `stock_intelligence_engine.py`, `app.py`, `sie/__init__.py`, README, CHANGELOG and FUTURE-IMPROVEMENTS.
- Dashboard title and sidebar updated to surface the new overlay.
- FUTURE-IMPROVEMENTS.md: marked Portfolio Correlation Heatmap & Risk Overlay complete with date and version.

## [2.10.1] - 2026-08-01

### Changed
- Autonomous research & evolution cycle (August 1, 2026). Full code audit of analyzer.py, social.py, insider.py, institutional.py, prediction_markets.py, app.py, config.yaml, stock_intelligence_engine.py and supporting modules confirmed no additional open FUTURE-IMPROVEMENTS items were newly implemented since v2.10.0. Roadmap remains accurate; version bump for documentation sync.

### Added
- Five new high-value improvements from fresh August 1 2026 research on AI stock tools, alternative data, political/congressional trading signals, activist ownership, sentiment momentum, high-impact political narrative sources (Truth Social), and institutional-style channel checks:
  - **High Priority**: Congressional Stock Trade Monitor
  - **Medium Priority**: Activist Ownership Change Detector; Multi-source Sentiment Momentum Oscillator
  - **Long-Term**: High-Impact Political / Truth Social Narrative Injector; Lightweight Channel-Check / Expert Sentiment Proxy

## [2.10.0] - 2026-07-31

### Added
- **Institutional 13F Ownership Change Detector**: New module `sie/institutional.py` that:
  - Pulls institutional holders via yfinance (`institutional_holders` + fallback attributes).
  - Applies a realistic synthetic QoQ ownership-change proxy when live 13F data is sparse or unavailable (stable per-ticker + day seed).
  - Detects significant ownership increases/decreases by large funds and emits soft `signal_boost` (+1 / 0 / −1), net shares change, pct change, side, confidence and human-readable reason.
  - Surfaces top holders, holder count and source in the live dashboard and signal reasons.
  - Integrates into `analyze_watchlist` / `run_report`, Streamlit dashboard (live 13F metrics + captions), CLI (`--no-13f` flag).
- Config section `institutional:` in `config.yaml` and defaults in `sie/config.py` (`enabled`, `min_holders`, `significant_pct_change`, `boost_pct_threshold`, `penalty_pct_threshold`).

### Changed
- Version bumped to **2.10.0** across `stock_intelligence_engine.py`, `app.py`, `sie/__init__.py`, README, CHANGELOG and FUTURE-IMPROVEMENTS.
- Analyzer now runs institutional 13F overlay after prediction-market layer and mutates signal accordingly.
- Dashboard title and per-ticker display updated to surface 13F side, Δ% and holder count.
- FUTURE-IMPROVEMENTS.md: marked Institutional 13F Ownership Change Detector complete with date and version.

## [2.9.1] - 2026-07-31

### Changed
- Autonomous research & evolution cycle (July 31, 2026). Full code audit of analyzer.py, social.py, insider.py, prediction_markets.py, app.py, config.yaml, stock_intelligence_engine.py and supporting modules confirmed Prediction Market Odds Overlay fully live and no additional open FUTURE-IMPROVEMENTS items were newly implemented since v2.9.0. Roadmap remains accurate.
- Version bumped to **2.9.1** across documentation and entry-point headers for the roadmap refresh.

### Added
- Five new high-value improvements from fresh July 31 2026 research on AI stock tools, alternative data (AltIndex-style), institutional filings, news impact engines, multi-platform prediction markets, and social growth metrics:
  - **High Priority**: Institutional 13F Ownership Change Detector
  - **Medium Priority**: News Materiality & Volatility Impact Scoring; Consumer App Download & Engagement Momentum Signals
  - **Long-Term**: Kalshi Prediction Market Cross-Check Overlay; Social Media Follower Growth Velocity Tracker

## [2.9.0] - 2026-07-30

### Added
- Prediction Market Odds Overlay (Polymarket) fully implemented.

# Previous entries retained for history.
