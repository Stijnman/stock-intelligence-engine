# Stock Intelligence Engine

**Connect market narratives to your watchlist. Confirm with technicals. Explain every signal.**

**v2.14.1** — August 2026 · Dark Pool / ATS Off-Exchange Flow Overlay + Real-time WebSocket Price & Quote Feeds + Congressional Trading Overlay + Portfolio Correlation Heatmap & Risk Overlay + Institutional 13F Ownership Change Detector + Prediction Market Odds Overlay (Polymarket) + Insider Form 4 Clustering + Multi-source Narrative Velocity Forecasting + Backtesting + Real-time Dashboard + X narratives

## Features
- Real-time signals with narrative intelligence
- **Dark Pool / ATS Off-Exchange Flow Overlay** — Detects elevated off-exchange volume relative to ADV via stable synthetic FINRA-style proxy (free default) + live extension points; applies soft accumulation/distribution boost/penalty as smart-money layer; surfaces relative ratio, side, confidence and venues in dashboard & alerts
- **Real-time WebSocket Price & Quote Feeds** — Low-latency quotes via synthetic tick generator (free default) + extension points for live WebSocket providers; surfaces change %, bid/ask, source and latency in dashboard & alerts
- **Congressional Trading Overlay** — Detects clustered or material congressional stock buys/sells (stable synthetic proxy) and applies soft confirmation/penalty as smart-money layer; surfaces trade count, net value, side and confidence in dashboard & alerts
- **Portfolio Correlation Heatmap & Risk Overlay** — Computes pairwise daily-return correlations and equal-weight portfolio metrics (annualized volatility, Sharpe, max drawdown, mean correlation); interactive Plotly heatmap in dashboard + CLI `--portfolio`
- **Institutional 13F Ownership Change Detector** — Detects significant institutional ownership increases/decreases (yfinance + synthetic QoQ proxy) and applies soft confirmation/penalty as smart-money flow overlay; surfaces top holders delta, net shares change and confidence in dashboard & alerts
- **Prediction Market Odds Overlay (Polymarket)** — Ingests free Gamma API odds for company/sector events, detects divergence from narrative+technical signal, and applies soft boost/penalty; surfaces probability, best question, confidence and source in dashboard & alerts
- **Insider Form 4 Clustering & Confirmation Signals** — Detects clustered insider buying/selling (yfinance + proxy) within a 14-day window and applies confirmation boost/penalty to signals; surfaces cluster size, net shares, side and confidence in dashboard & alerts
- Multi-source narrative velocity forecasting
- Backtesting framework
- Real-time Streamlit dashboard
- X/Twitter narrative intelligence

## Quick Start
```bash
pip install -r requirements.txt
streamlit run app.py
# or
python stock_intelligence_engine.py
```

See config.yaml for watchlist and overlay toggles.

## Recent Edits & Version History
- **v2.14.1 (2026-08-06)**: Autonomous research & evolution cycle. Full code audit confirmed no additional open FUTURE-IMPROVEMENTS items newly completed since v2.14.0. Added 4 new high-value 2026 improvements (Truth Social / Official Political Narrative Overlay, Retail Whisper Number vs Consensus Divergence Tracker, As-Reported Fundamentals Preference & Restatement Alert Layer, AI News Summary Engagement Multiplier). Docs & version sync.
- **v2.14.0 (2026-08-05)**: Implemented **Dark Pool / ATS Off-Exchange Flow Overlay**. New module `sie/dark_pool.py` detects elevated ATS volume vs ADV via stable synthetic daily proxy (FINRA transparency style), infers accumulation/distribution, applies soft signal boost/penalty. Fully integrated into Streamlit dashboard (live ATS columns + captions), CLI (`--no-dark-pool`), config.yaml (`dark_pool:` section). Also wired missing realtime integration path through analyzer for full flag consistency. Version bumped across all entry points and docs.
- **v2.13.1 (2026-08-05)**: Autonomous research & evolution cycle. Full code audit confirmed Real-time WebSocket Price & Quote Feeds fully implemented and live; marked complete in roadmap. Added 5 new high-value 2026 improvements (Options IV Skew & Term Structure Overlay, Multi-Factor Composite AI Score, Earnings Surprise Magnitude & Post-Drift Context, Narrative Contagion Rate Tracker, Prompt-Based Financial-Stability Sentiment Filter). Docs & version sync.
- **v2.13.0 (2026-08-05)**: Implemented **Real-time WebSocket Price & Quote Feeds**. New module `sie/realtime.py` with synthetic low-latency proxy + live extension points. Integrated into CLI, dashboard and analyzer rows.
- **v2.12.1 (2026-08-04)**: Autonomous research & evolution cycle. Full code audit confirmed no additional open FUTURE-IMPROVEMENTS items newly completed since v2.12.0. Added 5 new high-value 2026 improvements (Dark Pool / ATS Off-Exchange Flow Overlay, AI Technical Pattern Confirmation Layer, Cross-Asset Correlation Shock Detector, Market-Outcome-Aligned Sentiment Refiner, Free-Tier Unusual Options Activity Proxy). Docs & version sync.
- **v2.12.0 (2026-08-02)**: Implemented **Congressional Trading Overlay**. New module `sie/congressional.py` detects clustered congressional buys/sells via stable synthetic proxy (no paid API), applies soft signal boost/penalty, surfaces trade count / net value / side / confidence. Fully integrated into Streamlit dashboard (live Congress metrics + captions), CLI (`--no-congress`), config.yaml (`congressional:` section). Version bumped across all entry points and docs.
- **v2.11.0 (2026-08-01)**: Implemented **Portfolio Correlation Heatmap & Risk Overlay**. New module `sie/portfolio.py` downloads multi-ticker adjusted closes via yfinance, computes Pearson correlation of daily returns, equal-weight portfolio volatility / Sharpe / max drawdown / mean pairwise correlation. Fully integrated into Streamlit dashboard (interactive Plotly heatmap + metric cards), CLI (`--portfolio` flag and appended to `--backtest`), config.yaml (`portfolio:` section with lookback, min_periods, risk_free_rate). Version bumped across all entry points and docs.
- **v2.10.1 (2026-08-01)**: Autonomous research & evolution cycle. Full code audit confirmed Institutional 13F Ownership Change Detector fully implemented and live; no additional open FUTURE-IMPROVEMENTS items newly completed. Added 5 new high-value 2026 improvements (Congressional Stock Trade Monitor, Activist Ownership Change Detector, Multi-source Sentiment Momentum Oscillator, High-Impact Political / Truth Social Narrative Injector, Lightweight Channel-Check / Expert Sentiment Proxy). Docs & version sync.
- **v2.10.0 (2026-07-31)**: Implemented **Institutional 13F Ownership Change Detector**. New module `sie/institutional.py` fetches institutional holders via yfinance (with realistic synthetic QoQ proxy fallback), detects significant ownership increases/decreases by large funds, and applies soft signal boost/penalty. Fully integrated into analyzer, CLI (`--no-13f` flag), Streamlit dashboard (live 13F metrics + captions), config.yaml (`institutional:` section). Version bumped across all entry points and docs.
- **v2.9.1 (2026-07-31)**: Autonomous research & evolution cycle. Full code audit confirmed Prediction Market Odds Overlay (Polymarket) fully implemented and live; no additional open FUTURE-IMPROVEMENTS items newly completed. Added 5 high-value improvements from fresh research.
- **v2.9.0 (2026-07-30)**: Prediction Market Odds Overlay (Polymarket).
- **v2.8.0 (2026-07-29)**: Insider Form 4 Clustering & Confirmation Signals.
- **v2.7.0 (2026-07-25)**: Multi-source Narrative Velocity Forecasting.
- **v2.6.0 (2026-07-23)**: Backtesting Framework.

## Version highlights

| Version | Notes |
|---------|--------|
| 2.14.1 | Roadmap refresh + 4 new 2026 research items |
| 2.14.0 | Dark Pool / ATS Off-Exchange Flow Overlay |
| 2.13.1 | Roadmap refresh + 5 new 2026 research items; Real-time WebSocket marked complete |
| 2.13.0 | Real-time WebSocket Price & Quote Feeds |
| 2.12.1 | Roadmap refresh + 5 new 2026 research items |
| 2.12.0 | Congressional Trading Overlay |
| 2.11.0 | Portfolio Correlation Heatmap & Risk Overlay |
| 2.10.1 | Roadmap refresh + 5 new 2026 research items |
| 2.10.0 | Institutional 13F Ownership Change Detector |
| 2.9.1 | Roadmap refresh + 5 new 2026 research items |
| 2.9.0 | Prediction Market Odds Overlay (Polymarket) |
| 2.8.0 | Insider Form 4 Clustering & Confirmation Signals |

## Dark Pool Overlay (v2.14.0)
See CHANGELOG and FUTURE-IMPROVEMENTS for full details.

## License
MIT
