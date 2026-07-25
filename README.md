# Stock Intelligence Engine

**Connect market narratives to your watchlist. Confirm with technicals. Explain every signal.**

**v2.6.1** — July 2026 · Backtesting Framework + Real-time Dashboard + X narratives + Roadmap Sync

## Features
- Real-time signals with narrative intelligence
- **Backtesting Framework** - Validate historical performance with Sharpe ratios
- Streamlit dashboard with live updates & auto-refresh
- X/Twitter dominant narrative, velocity & crisis flags
- FinBERT + VADER news sentiment
- Telegram alerts

## Recent Edits & Version History
- **v2.6.1 (2026-07-25)**: Autonomous research cycle — cleaned completed roadmap items (narrative phases already in social.py, pytest present, VADER fallback covered). Added 5 new high-value 2026 improvements (narrative velocity forecasting, portfolio risk heatmap, Streamlit fragments/caching, SEC 8-K NLP, unusual options/dark-pool). Docs & version sync.
- **v2.6.0 (2026-07-23)**: Implemented Backtesting Framework. CLI `--backtest`, dashboard button, integrated metrics. [Commit](https://github.com/Stijnman/stock-intelligence-engine/commit/ead6af1db28485a90c302f5169dfbaf118101320)

## Version highlights

| Version | Notes |
|---------|--------|
| 2.6.1 | Roadmap cleanup + fresh 2026 research items |
| 2.6.0 | Backtesting Framework added |
| 2.5.2 | Fresh research-driven roadmap updates |
| 2.5.0 | Real-time Streamlit auto-refresh |
| 2.4.0 | X narrative intelligence |

**Usage:** `python stock_intelligence_engine.py --backtest`  
**Dashboard:** `streamlit run app.py`
