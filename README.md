**Stock Intelligence Engine**  
*Connect market narratives to your watchlist. Confirm with technicals. Explain every signal.*

**v2.0.2** — July 2026

An open-source Python tool that maps narrative themes from config.yaml to tickers, confirms with RSI(14), MA50/MA200, 52-week drawdown via yfinance, and outputs transparent `strong_buy` / `buy` / `hold` / `caution` signals with human-readable reasons. Optional news headlines, CSV export, email alerts, daemon mode, Docker support, and a Streamlit dashboard with Plotly charts.

## Recent Edits & Version History

- **2026-07-05 (v2.0.2)**: Second autonomous research & evolution cycle executed per AUTONOMOUS-RESEARCH-EVOLUTION-CYCLE.md protocol. Verified latest main (v2.0.1 state): no items from FUTURE-IMPROVEMENTS.md are implemented yet in core code (stock_intelligence_engine.py remains narrative + technical + yfinance only; no FinBERT, X API, options flow, backtesting, or Streamlit upgrades present). Added 5 new high-value improvements from fresh July 2026 research on narrative intelligence, social sentiment, earnings transcripts, news impact, and multi-source fusion. Appended cleanly to v2.1 / v2.2 / v3.0+ sections in FUTURE-IMPROVEMENTS.md. Updated CHANGELOG.md with full audit trail. Bumped version to **v2.0.2** across docs and Python entry points for the roadmap refresh. Research-first safety gates followed; no code logic changes.
- **2026-07-05 (v2.0.1)**: Autonomous research & evolution cycle. Full code audit confirmed **GitHub Actions CI** (`.github/workflows/ci.yml`) is fully implemented and working (multi-Python matrix, flake8, smoke tests + artifacts). Removed it from FUTURE-IMPROVEMENTS.md v2.1. Added detailed entry to CHANGELOG.md. Bumped version to **v2.0.1** in all files (stock_intelligence_engine.py, app.py, docs). Added 5 new high-value improvements from fresh July 2026 research (FinBERT sentiment scoring, X/Twitter v2 viral scanner, options flow detector, Streamlit 2026 UX overhaul with data_editor + themes, vectorbt/Monte Carlo narrative backtester). Categorized into existing priority sections. Roadmap now current and forward-looking.

## What it does

... (rest of original README content remains unchanged) ...