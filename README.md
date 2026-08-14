# Stock Intelligence Engine

**Connect market narratives to your watchlist. Confirm with technicals. Explain every signal.**

**v2.16.2** — August 2026 · 0DTE Options Flow + Options IV Skew & Term Structure + Dark Pool / ATS Flow + Real-time Quotes + Congressional Trading + Portfolio Risk Overlay + Institutional 13F + Prediction Markets (Polymarket) + Insider Form 4 Clustering + Multi-source Narrative Velocity + Backtesting + Real-time Dashboard + X narratives

## Features
- Real-time signals with narrative intelligence
- **0DTE Options Flow Overlay** — Same-day options activity proxy integrated into report generation and the CLI feature toggle
- **Options Implied Volatility Skew & Term Structure Overlay** — Free yfinance (or synthetic) options chains → put/call IV skew + term-structure slope; soft boost/penalty on fear skew or inversion
- **Dark Pool / ATS Off-Exchange Flow Overlay** — Elevated dark-pool volume ratios and prints as institutional flow confirmation
- **Real-time WebSocket Price & Quote Feeds** — Low-latency quotes with stable fallback
- **Congressional Trading Overlay** — Clustered or large congressional buys/sells as smart-money layer
- **Portfolio Correlation Heatmap & Risk Overlay** — Pairwise correlations, max drawdown, volatility, Sharpe of watchlist basket
- **Institutional 13F Ownership Change Detector** — Significant institutional ownership increases/decreases (yfinance + synthetic QoQ proxy)
- **Prediction Market Odds Overlay (Polymarket)** — Free Gamma API odds for company/sector events; divergence from narrative+technical signal
- **Insider Form 4 Clustering & Confirmation Signals** — Clustered insider buying/selling within 14-day window
- **Multi-source Narrative Velocity Forecasting** — 1-3 day narrative phase shifts (hype/dip/recovery) from X velocity + news sentiment
- **Backtesting Framework** — Historical performance with Sharpe ratios
- Streamlit dashboard with live updates & auto-refresh
- X/Twitter dominant narrative, velocity & crisis flags
- FinBERT + VADER news sentiment
- Telegram alerts (optional)

## Recent Edits & Version History
- **v2.16.2 (2026-08-14)**: Streamlined the project layout documentation, added a standard pytest configuration, and converted continuous integration from permissive smoke checks to blocking lint, test, hygiene, and CLI validation.
- **v2.16.1 (2026-08-14)**: Repaired stale package exports and dashboard interfaces, connected the implemented 0DTE overlay through the analysis and CLI paths, restored the advertised CSV export command, and added regression tests for these public interfaces.
- **v2.15.5 (2026-08-13)**: Autonomous research & evolution cycle. Full code audit of all sie/ modules, app.py, stock_intelligence_engine.py, config.yaml confirmed no additional open FUTURE-IMPROVEMENTS items newly implemented since v2.15.4. Added 5 new high-value 2026 research items (Narrative Momentum Acceleration Detector, Unified Smart-Money Consensus Score, Sector vs Idiosyncratic Narrative Attribution, Intraday Volume Profile Anomaly Detector, Automated Natural-Language Signal Explanation Generator). Version bump and docs sync.
- **v2.15.4 (2026-08-12)**: Autonomous research & evolution cycle. Full code audit of all sie/ modules, app.py, stock_intelligence_engine.py, config.yaml confirmed no additional open FUTURE-IMPROVEMENTS items newly implemented since v2.15.3. Added 5 new high-value 2026 research items (Delayed News-Price Assimilation Lag Detector, Social Trust / Narrative Credibility Index, Suspicious Volume & Wash-Trading Risk Proxy, True Push-Style WebSocket Dashboard Updates, Competing-Narratives Agent-Based Stress Tester). Version bump and docs sync.
- **v2.15.3 (2026-08-11)**: Autonomous research & evolution cycle. Full code audit of all sie/ modules, app.py, stock_intelligence_engine.py, config.yaml confirmed no additional open FUTURE-IMPROVEMENTS items newly implemented since v2.15.2. Added 5 new high-value 2026 research items (Retail-Institutional Sentiment Divergence Overlay, Zero-Shot LLM Headline Materiality & Direction Classifier, Options Sweep & Block Unusual Activity Proxy, Streamlit Fragment + Persistent Session Watchlist Hardening, Agentic Multi-Document Research Brief Generator). Version bump and docs sync.
- **v2.15.2 (2026-08-09)**: Autonomous research & evolution cycle. Full code audit of all sie/ modules, app.py, stock_intelligence_engine.py, config.yaml confirmed no additional open FUTURE-IMPROVEMENTS items newly implemented since v2.15.1. Restored complete FUTURE-IMPROVEMENTS.md and README from prior cycle state. Added 5 new high-value 2026 research items (Authenticity-Filtered Narrative Velocity, LLM ESG Summary Sentiment Overlay, Event-Driven Surprise Composite, Free CBOE Delayed Options UOA Enhancer, Vanna Exposure (VEX) Proxy). Version bump and docs sync.
- **v2.15.1 (2026-08-08)**: Autonomous research & evolution cycle. Full code audit confirmed no new implementations. Added 5 high-value improvements (Corporate Hiring & Headcount Momentum Tracker, Narrative-Data Honesty / Contradiction Detector, Earnings Call Prepared Remarks vs Live Q&A Sentiment Delta, Company Website Traffic & Engagement Momentum Proxy, Max Pain & Simplified Dealer Positioning Overlay).
- **v2.15.0 (2026-08-07)**: Implemented **Options Implied Volatility Skew & Term Structure Overlay**. Module sie/options_iv.py polished and fully wired. Added 5 new research items (0DTE Options Flow, Same-Day SEC EDGAR, FINRA Short Volume, Unified Multi-Platform Attention / Buzz Score, Gamma Exposure GEX).
- **v2.14.0**: Dark Pool / ATS Off-Exchange Flow Overlay.
- **v2.13.0**: Real-time WebSocket Price & Quote Feeds.
- **v2.12.0**: Congressional Trading Overlay.
- **v2.11.0**: Portfolio Correlation Heatmap & Risk Overlay.
- **v2.10.0**: Institutional 13F Ownership Change Detector.
- **v2.9.0**: Prediction Market Odds Overlay (Polymarket).
- **v2.8.0**: Insider Form 4 Clustering & Confirmation Signals.
- **v2.7.0**: Multi-source Narrative Velocity Forecasting.
- **v2.6.0**: Backtesting Framework.

## Version highlights

| Version | Notes |
|---------|--------|
| 2.16.2 | Release-ready CI, test configuration, and repository-structure documentation |
| 2.16.1 | Public API, dashboard, 0DTE toggle, and CSV export compatibility repair |
| 2.15.5 | Roadmap refresh + 5 new 2026 research items (Narrative Momentum Acceleration, Smart-Money Consensus, Sector Attribution, Volume Profile Anomaly, NL Signal Explainer) |
| 2.15.4 | Roadmap refresh + 5 new 2026 research items (Assimilation Lag Detector, Social Trust Index, Wash-Trading Proxy, WebSocket Push Updates, Competing-Narratives Stress Tester) |
| 2.15.3 | Roadmap refresh + 5 new 2026 research items (Retail-Institutional Divergence, Zero-Shot LLM Materiality, Options Sweep/Block, Streamlit Fragment Hardening, Agentic Briefs) |
| 2.15.2 | Roadmap restore + 5 new 2026 research items (Authenticity filter, LLM ESG, Event Surprise, CBOE UOA, VEX) |
| 2.15.1 | Roadmap refresh + 5 new 2026 research items |
| 2.15.0 | Options IV Skew & Term Structure Overlay |
| 2.14.0 | Dark Pool / ATS Off-Exchange Flow Overlay |
| 2.13.0 | Real-time WebSocket Price & Quote Feeds |
| 2.12.0 | Congressional Trading Overlay |
| 2.11.0 | Portfolio Correlation Heatmap & Risk Overlay |
| 2.10.0 | Institutional 13F Ownership Change Detector |
| 2.9.0  | Prediction Market Odds Overlay (Polymarket) |
| 2.8.0  | Insider Form 4 Clustering |
| 2.7.0  | Multi-source Narrative Velocity Forecasting |
| 2.6.0  | Backtesting Framework |

## Quick start

Install the project dependencies, inspect the available options, and run the desired interface.

```bash
python -m pip install -r requirements.txt
python stock_intelligence_engine.py --help
python stock_intelligence_engine.py --export
streamlit run app.py
```

The primary runtime settings, ticker universe, and optional integrations are defined in [`config.yaml`](config.yaml). Copy [`.env.example`](.env.example) to `.env` before configuring optional notification credentials.

## Project structure

| Path | Purpose |
|---|---|
| `sie/` | Core analysis, data overlays, reporting, and integration modules. |
| `tests/` | Automated regression tests for technical indicators and public interfaces. |
| `scripts/check_repo.py` | Repository hygiene check used locally and in continuous integration. |
| `app.py` | Streamlit dashboard entry point. |
| `stock_intelligence_engine.py` | Command-line entry point for reports, exports, and feature toggles. |
| `config.yaml` | Watchlist, scoring thresholds, and runtime configuration. |
| `.github/workflows/ci.yml` | Python-version matrix for linting, tests, hygiene checks, and CLI validation. |

## Quality checks

Run the same core checks used by continuous integration before opening a pull request.

```bash
python -m pytest -q
python scripts/check_repo.py
python stock_intelligence_engine.py --help
```

See [FUTURE-IMPROVEMENTS.md](FUTURE-IMPROVEMENTS.md) for the full roadmap and [CHANGELOG.md](CHANGELOG.md) for detailed history.
