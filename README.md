# Stock Intelligence Engine

**Connect market narratives to your watchlist. Confirm with technicals. Explain every signal.**

**v2.15.4** — August 2026 · Options IV Skew & Term Structure + Dark Pool / ATS Flow + Real-time Quotes + Congressional Trading + Portfolio Risk Overlay + Institutional 13F + Prediction Markets (Polymarket) + Insider Form 4 Clustering + Multi-source Narrative Velocity + Backtesting + Real-time Dashboard + X narratives

## Features
- Real-time signals with narrative intelligence
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

**Usage:** `python stock_intelligence_engine.py --backtest`  
**Dashboard:** `streamlit run app.py`

See [FUTURE-IMPROVEMENTS.md](FUTURE-IMPROVEMENTS.md) for the full roadmap and [CHANGELOG.md](CHANGELOG.md) for detailed history.
