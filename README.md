# Stock Intelligence Engine

**Connect market narratives to your watchlist.**  
**Confirm with technicals.**  
**Explain every signal.**

**v2.27.0** — August 2026 · Authenticity-Filtered Social Narrative Velocity + Supply-Chain CapEx + FINRA Short + Attention Momentum (fully wired) + Market Regime Adaptive Overlay Weighting + Signal Confidence Calibration & LLM Self-Critique + Streamlit Fragment Live Dashboard Refresh + LLM Bull/Bear Thesis + Self-Explaining AI Signal Brief + Honesty / Contradiction Detector + Corporate Hiring + Same-Day SEC EDGAR + 0DTE Options Flow + Options IV Skew + Dark Pool / ATS + Real-time Quotes + Congressional Trading + Portfolio Risk + Institutional 13F + Prediction Markets + Insider Form 4 + Narrative Velocity + Backtesting

## Features

* Real-time signals with narrative intelligence
* **Authenticity-Filtered Social Narrative Velocity Overlay** — Scores social heat for authenticity / bot-likelihood before aggregating velocity; soft boost on high-auth rising narratives, caution on low-auth (bot/spam) elevated velocity
* **Semiconductor / AI Supply-Chain CapEx Momentum Tracker** — Supplier momentum (ASML / AMAT / LRCX / KLAC / TSM) as a leading inference-demand proxy; yfinance peek when available, otherwise labeled synthetic proxy
* **FINRA Short Volume / Short Interest Momentum Overlay** — Elevated short volume vs rising narrative = caution; covering + hot narrative = soft boost
* **Wikipedia / Search Attention Momentum Tracker** — Wikimedia pageview WoW when reachable, else seeded proxy
* **Market Regime Adaptive Overlay Weighting** — Dynamically re-weights narrative / technical / flow / fundamental overlays by current regime
* **Signal Confidence Calibration & LLM Self-Critique Layer** — Consistency scoring across overlays with calibrated confidence and self-critique
* **LLM-Generated Bull/Bear Thesis Pair Generator**
* **Self-Explaining AI Signal Brief Generator**
* **Narrative vs. Fundamentals Contradiction / Honesty Signal Detector**
* **Corporate Hiring & Headcount Momentum Tracker**
* **Same-Day SEC EDGAR Material Filing Detector**
* **0DTE Options Flow & Unusual Activity Proxy**
* Options Implied Volatility Skew & Term Structure Overlay
* Dark Pool / ATS Off-Exchange Flow Overlay
* Real-time WebSocket Price & Quote Feeds
* Congressional Trading Overlay
* Portfolio Correlation Heatmap & Risk Overlay
* Institutional 13F Ownership Change Detector
* Prediction Market Odds Overlay (Polymarket)
* Insider Form 4 Clustering & Confirmation Signals
* Multi-source Narrative Velocity Forecasting
* Backtesting framework
* **Streamlit Fragment Live Dashboard Refresh**
* Streamlit real-time dashboard

## Quick Start

```bash
git clone https://github.com/Stijnman/stock-intelligence-engine.git
cd stock-intelligence-engine
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env        # optional: add X bearer token, Telegram, etc.
python stock_intelligence_engine.py
streamlit run app.py
```

## Recent Edits & Version History

* **v2.27.0 (2026-08-29)** : Autonomous feature implementation cycle. Fully implemented **Authenticity-Filtered Social Narrative Velocity Overlay** (`sie/authenticity.py`, `--no-authenticity`). Deterministic authenticity score + filtered velocity proxy; soft boost on high-auth rising narrative, caution on low-auth elevated velocity (bot/spam risk). Wired into analyzer / CLI / config / dashboard preferred columns / tests. Marked completed in FUTURE-IMPROVEMENTS. Version alignment to 2.27.0.
* **v2.26.1 (2026-08-29)** : Autonomous research & evolution cycle. Code audit confirmed no outstanding completed items needing cleanup. Fresh 2026 research on AI stock tools, narrative authenticity scoring, earnings-call NLP divergence, dealer gamma exposure, and Streamlit production patterns. Added five new high-value roadmap items (Authenticity-Filtered Velocity, Q&A vs Prepared Divergence, GEX Overlay, Multi-User Persistent Watchlists, Cloud Deployment Profiles). Version alignment to 2.26.1.
* **v2.26.0 (2026-08-28)** : Autonomous implementation cycle. Shipped three overlays end-to-end: **Supply-Chain CapEx** (`sie/supply_chain.py`, `--no-supply-chain`), **FINRA Short Volume** (`sie/short_interest.py`, `--no-short-interest`), **Attention Momentum** (`sie/attention.py`, `--no-attention`). Wired into analyzer / CLI / config / dashboard / tests. Added DISCLAIMER.md and CONTRIBUTING.md. Marked completed items in FUTURE-IMPROVEMENTS. Version alignment to 2.26.0.
* **v2.25.0 (2026-08-28)** : Autonomous feature implementation cycle. Fully implemented **Market Regime Adaptive Overlay Weighting** (`sie/regime.py`) with live VIX/SPY detection, adaptive overlay group weights, soft signal bias and full wiring into analyzer / CLI (`--no-regime`) / dashboard / config. Removed completed item from FUTURE-IMPROVEMENTS. Version alignment to 2.25.0 across all files.
* **v2.24.0 (2026-08-28)** : Autonomous research & evolution cycle. Code audit discovered Signal Confidence Calibration & LLM Self-Critique was present (`sie/confidence.py` + config + CLI) but not wired into analyzer orchestration / dashboard; fully integrated `include_confidence` + `integrate_confidence_to_row`. Removed completed item from FUTURE-IMPROVEMENTS. Added five new high-value 2026 research-backed items. Version alignment to 2.24.0 across all files.
* **v2.23.0 (2026-08-26)** : Autonomous feature implementation cycle. Fully implemented **Streamlit Fragment Live Dashboard Refresh** in `app.py`.

## Disclaimer

This is an educational research tool. Not financial advice. See DISCLAIMER.md.

v2.27.0
