# Stock Intelligence Engine

**Connect market narratives to your watchlist.**  
**Confirm with technicals.**  
**Explain every signal.**

**v2.25.0** — August 2026 · Market Regime Adaptive Overlay Weighting (fully wired) + Signal Confidence Calibration & LLM Self-Critique (fully wired) + Streamlit Fragment Live Dashboard Refresh (fully wired) + LLM Bull/Bear Thesis (fully wired) + Self-Explaining AI Signal Brief (fully wired) + Narrative vs. Fundamentals Honesty / Contradiction Detector (fully wired) + Corporate Hiring & Headcount Momentum Tracker + Same-Day SEC EDGAR Material Filing Detector + 0DTE Options Flow & Unusual Activity Proxy + Options IV Skew & Term Structure + Dark Pool / ATS Flow + Real-time Quotes + Congressional Trading + Portfolio Risk Overlay + Institutional 13F + Prediction Markets (Polymarket) + Insider Form 4 Clustering + Multi-source Narrative Velocity + Backtesting + Real-time Dashboard + X narratives

## Features

* Real-time signals with narrative intelligence
* **Market Regime Adaptive Overlay Weighting** — Dynamically re-weights narrative / technical / flow / fundamental overlays by current regime (VIX terciles + SPY trend + realized vol); cuts narrative weight in high-vol stress and boosts flow/technical when trends are strong
* **Signal Confidence Calibration & LLM Self-Critique Layer** — Post-signal consistency scoring across all overlays; surfaces calibrated confidence (0-1), conflict list, and plain-English self-critique with "what would change my mind"
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
* **Streamlit Fragment Live Dashboard Refresh** — Selective auto-refresh of status metrics and signal table via `@st.fragment(run_every=...)` (config-driven interval, cached analysis, Force Full Refresh)
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

* **v2.25.0 (2026-08-28)** : Autonomous feature implementation cycle. Fully implemented **Market Regime Adaptive Overlay Weighting** (`sie/regime.py`) with live VIX/SPY detection, adaptive overlay group weights, soft signal bias and full wiring into analyzer / CLI (`--no-regime`) / dashboard / config. Removed completed item from FUTURE-IMPROVEMENTS. Version alignment to 2.25.0 across all files.
* **v2.24.0 (2026-08-28)** : Autonomous research & evolution cycle. Code audit discovered Signal Confidence Calibration & LLM Self-Critique was present (`sie/confidence.py` + config + CLI) but not wired into analyzer orchestration / dashboard; fully integrated `include_confidence` + `integrate_confidence_to_row`. Removed completed item from FUTURE-IMPROVEMENTS. Added five new high-value 2026 research-backed items (Market Regime Adaptive Overlay Weighting, Semiconductor / AI Supply-Chain CapEx Momentum Tracker, Earnings Call Audio Tone & Prosody Sentiment Layer, Vision-Model Chart Pattern & Anomaly Detector, Open-Source Factor Risk Decomposition Overlay). Version alignment to 2.24.0 across all files.
* **v2.23.0 (2026-08-26)** : Autonomous feature implementation cycle. Fully implemented **Streamlit Fragment Live Dashboard Refresh** in `app.py` using `@st.fragment(run_every=...)` for selective live status + signal table updates (config-driven `dashboard.refresh_interval`, cached analysis with 5 min TTL, Force Full Refresh button). Removed completed item from FUTURE-IMPROVEMENTS. Version alignment to 2.23.0 across all files.

## Disclaimer

This is an educational research tool. Not financial advice. See DISCLAIMER.md.

v2.25.0
