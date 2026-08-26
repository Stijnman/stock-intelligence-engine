# Stock Intelligence Engine

**Connect market narratives to your watchlist.**  
**Confirm with technicals.**  
**Explain every signal.**

**v2.22.0** — August 2026 · LLM Bull/Bear Thesis (fully wired) + Self-Explaining AI Signal Brief (fully wired) + Narrative vs. Fundamentals Honesty / Contradiction Detector (fully wired) + Corporate Hiring & Headcount Momentum Tracker + Same-Day SEC EDGAR Material Filing Detector + 0DTE Options Flow & Unusual Activity Proxy + Options IV Skew & Term Structure + Dark Pool / ATS Flow + Real-time Quotes + Congressional Trading + Portfolio Risk Overlay + Institutional 13F + Prediction Markets (Polymarket) + Insider Form 4 Clustering + Multi-source Narrative Velocity + Backtesting + Real-time Dashboard + X narratives

## Features

* Real-time signals with narrative intelligence
* **LLM-Generated Bull/Bear Thesis Pair Generator** — Balanced, evidence-grounded bull and bear paragraphs for every ticker (deterministic structured generator, LLM-swappable)
* **Self-Explaining AI Signal Brief Generator** — One-click / auto-generated 4–6 sentence plain-English brief that cites every active overlay with confidence and "what would change my mind"
* **Narrative vs. Fundamentals Contradiction / Honesty Signal Detector** — Flags pure-narrative risk when social/velocity heat diverges from hard overlays (13F, hiring, EDGAR, technicals); applies soft penalty on high honesty risk
* **Corporate Hiring & Headcount Momentum Tracker** — Forward-looking demand proxy via open-role / headcount growth (soft boost on acceleration)
* **Same-Day SEC EDGAR Material Filing Detector** — Fresh 8-K / material filings with tone & materiality soft boost/penalty
* **0DTE Options Flow & Unusual Activity Proxy** — Near-expiry volume/OI spikes as short-horizon event / dealer-hedging signals
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

* **v2.22.0 (2026-08-26)** : Autonomous research & evolution cycle. Code audit discovered Narrative vs. Fundamentals Honesty Signal Detector was present (`sie/honesty.py`) but not wired into analyzer orchestration / CLI / config / dashboard; fully integrated `include_honesty` + `integrate_honesty_to_row`. Removed completed item from FUTURE-IMPROVEMENTS. Added five new high-value 2026 research-backed items (Satellite Imagery / Foot-Traffic Overlay, AI Token Consumption / AI Premium Factor, Cross-Platform Social Follower Growth, Dual-Score News Impact vs Tone, Stratified Multi-Agent Research Report Generator). Version alignment to 2.22.0 across all files.
* **v2.21.0 (2026-08-25)** : Autonomous research & evolution cycle. Code audit discovered Self-Explaining AI Signal Brief Generator was present (`sie/brief.py`) but not wired into analyzer orchestration / CLI / config; fully integrated `include_brief` + `integrate_brief_to_row`. Removed completed item from FUTURE-IMPROVEMENTS. Added four new high-value 2026 research-backed items (Narrative vs. Fundamentals Contradiction / Honesty Signal Detector, Company Digital Footprint Momentum Overlay, Agentic Multi-Perspective Signal Debate Layer, Streamlit Fragment Live Dashboard Refresh). Version alignment to 2.21.0 across all files.
* **v2.20.4 (2026-08-24)** : Autonomous research & evolution cycle. Code audit confirmed all previously marked-complete features remain fully implemented (thesis fully wired, hiring, EDGAR, 0DTE, IV skew, dark pool, realtime, congressional, 13F, Polymarket, insider, narrative velocity). Added five new high-value 2026 research-backed items to FUTURE-IMPROVEMENTS: Earnings Call Transcript Diff & Guidance Change Detector, Native MCP Server for Agent Integration, FINRA Short Volume / Short Interest Momentum Overlay, YouTube Finance Creator Sentiment Overlay, Employee Glassdoor / Outlook Sentiment Tracker.
* **v2.20.3 (2026-08-23)** : Autonomous research & evolution cycle. Added Wikipedia/Google Trends Attention, Patent/IP Momentum, Government Contract/Lobbying, Options Vanna/Charm/DEX, Signal Confidence Calibration & LLM Self-Critique.
* **v2.20.2 (2026-08-22)** : Autonomous research & evolution cycle. Code audit discovered LLM Thesis was claimed complete but missing from analyzer orchestration; fully wired include_thesis + integrate_thesis_to_row into analyze_watchlist / run_report, CLI, dashboard data path and config. Added five new high-value 2026 research-backed items to FUTURE-IMPROVEMENTS (Narrative Graph / Conversation Network Intelligence, Self-Explaining AI Signal Brief Generator, Options Max Pain & OI Wall Detector, Pre-Market Theme Rotation & Volume Surge Scanner, Cross-Ticker Narrative Contagion Detector).

## Disclaimer

This is an educational research tool. Not financial advice. See DISCLAIMER.md.

v2.22.0
