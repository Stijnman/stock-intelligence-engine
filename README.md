# Stock Intelligence Engine

**Connect market narratives to your watchlist. Confirm with technicals. Explain every signal.**

**v2.10.1** — August 2026 · Institutional 13F Ownership Change Detector + Prediction Market Odds Overlay (Polymarket) + Insider Form 4 Clustering + Multi-source Narrative Velocity Forecasting + Backtesting + Real-time Dashboard + X narratives

## Features
- Real-time signals with narrative intelligence
- **Institutional 13F Ownership Change Detector** — Detects significant institutional ownership increases/decreases (yfinance + synthetic QoQ proxy) and applies soft confirmation/penalty as smart-money flow overlay; surfaces top holders delta, net shares change and confidence in dashboard & alerts
- **Prediction Market Odds Overlay (Polymarket)** — Ingests free Gamma API odds for company/sector events, detects divergence from narrative+technical signal, and applies soft boost/penalty; surfaces probability, best question, confidence and source in dashboard & alerts
- **Insider Form 4 Clustering & Confirmation Signals** — Detects clustered insider buying/selling (yfinance + proxy) within a 14-day window and applies confirmation boost/penalty to signals; surfaces cluster size, net shares, side and confidence in dashboard & alerts
- **Multi-source Narrative Velocity Forecasting** - Predicts 1-3 day narrative phase shifts (hype/dip/recovery) from X velocity + news sentiment using exponential smoothing; applies boost/penalty to signals
- **Backtesting Framework** - Validate historical performance with Sharpe ratios
- Streamlit dashboard with live updates & auto-refresh
- X/Twitter dominant narrative, velocity & crisis flags
- FinBERT + VADER news sentiment
- Telegram alerts

## Recent Edits & Version History
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
| 2.10.1 | Roadmap refresh + 5 new 2026 research items |
| 2.10.0 | Institutional 13F Ownership Change Detector |
| 2.9.1 | Roadmap refresh + 5 new 2026 research items |
| 2.9.0 | Prediction Market Odds Overlay (Polymarket) |
| 2.8.0 | Insider Form 4 Clustering & Confirmation Signals |
| 2.7.0 | Multi-source Narrative Velocity Forecasting |
| 2.6.0 | Backtesting Framework added |
| 2.5.0 | Real-time Streamlit auto-refresh |
| 2.4.0 | X narrative intelligence |

**Usage:** `python stock_intelligence_engine.py --backtest`  
**Dashboard:** `streamlit run app.py`
