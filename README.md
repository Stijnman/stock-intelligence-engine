# Stock Intelligence Engine

**Connect market narratives to your watchlist.**  
**Confirm with technicals.**  
**Explain every signal.**

**v2.29.2** — September 2026 · Securities Lending / Borrow Fee & Short Squeeze Risk Overlay + Aggregated Consumer Transaction / Credit-Card Panel Spend Nowcasting + Authenticity-Filtered Social Narrative Velocity + Supply-Chain CapEx + FINRA Short + Attention Momentum (fully wired) + Market Regime Adaptive Overlay Weighting + Signal Confidence Calibration & LLM Self-Critique + Streamlit Fragment Live Dashboard Refresh + LLM Bull/Bear Thesis + Self-Explaining AI Signal Brief + Honesty / Contradiction Detector + Corporate Hiring + Same-Day SEC EDGAR + 0DTE Options Flow + Options IV Skew + Dark Pool / ATS + Real-time Quotes + Congressional Trading + Portfolio Risk + Institutional 13F + Prediction Markets + Insider Form 4 + Narrative Velocity + Backtesting

## Features

* Real-time signals with narrative intelligence
* **Securities Lending / Borrow Fee & Short Squeeze Risk Overlay** — Deterministic borrow-fee / DTC / hard-to-borrow proxy; soft boost on elevated fees + covering + hot narrative (squeeze risk), caution on high fees vs cold narrative
* **Aggregated Consumer Transaction / Credit-Card Panel Spend Nowcasting Overlay** — Deterministic panel-spend momentum proxy as leading revenue nowcast; soft boost on rising spend vs narrative, caution on contraction
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

* **v2.29.2 (2026-09-03)** : Autonomous research & evolution cycle. Code audit confirmed no outstanding completed items needing cleanup; fixed version drift in `sie/__init__.py` (was 2.30.0). Fresh 2026 research on AI stock tools, BNPL/alternative credit, expert-network transcripts, data-center power intensity, cross-asset narrative contagion, analyst-note velocity, and Streamlit production patterns. Added five new high-value roadmap items (Expert Network Transcript Overlay, BNPL Credit Momentum, Cross-Asset Contagion, Analyst Note Velocity, Data-Center Power Intensity). Version alignment to 2.29.2.
* **v2.29.1 (2026-09-02)** : Autonomous research & evolution cycle. Code audit confirmed no outstanding completed items needing cleanup (Borrow Fee overlay and all prior features fully wired). Fresh 2026 research on AI stock tools, freight rate / logistics indices, job-posting AI-skill intensity, retail vs institutional options flow divergence, pre-earnings social/options leak scores, multi-channel alert routers, and Streamlit production patterns. Added five new high-value roadmap items (Freight Rate Overlay, AI-Skill Job Intensity, Retail/Institutional Options Divergence, Pre-Earnings Whisper Score, Multi-Channel Alert Router). Version alignment to 2.29.1.
* **v2.29.0 (2026-09-01)** : Autonomous feature implementation cycle. Fully implemented **Securities Lending / Borrow Fee & Short Squeeze Risk Overlay** (`sie/borrow_fee.py`, `--no-borrow-fee`). Deterministic synthetic borrow-fee / DTC / HTB proxy with soft boost on elevated fees + covering + hot narrative (squeeze risk) and caution on high fees vs cold narrative. Surfaces `bf_fee_pct`, `bf_dtc`, `bf_htb`, `bf_boost`, `bf_confidence`, `bf_reason`, `bf_source`. Wired into analyzer / CLI / config / dashboard preferred columns / tests. Marked completed in FUTURE-IMPROVEMENTS. Version alignment to 2.29.0.
* **v2.28.2 (2026-09-01)** : Autonomous research & evolution cycle. Code audit confirmed no outstanding completed items needing cleanup. Fresh 2026 research on AI stock tools, securities lending / borrow fees, GPU cloud utilization proxies, ETF flow theme rotation, earnings implied-move calibration, on-chain crypto-equity activity, and Streamlit production patterns. Added five new high-value roadmap items (Borrow Fee / Short Squeeze Risk, GPU Cloud Utilization Proxy, ETF Flow Theme Rotation, Earnings Implied-Move Calibration, On-Chain Crypto-Equity Overlay). Version alignment to 2.28.2.
* **v2.28.1 (2026-08-31)** : Autonomous research & evolution cycle. Code audit confirmed no outstanding completed items needing cleanup. Fresh 2026 research on AI stock tools, container/bill-of-lading trade flow, road/truck camera volume, dual institutional-vs-retail sentiment, AI-clustered news story impact, local open-weight LLM ticker mapping, and Streamlit production patterns. Added five new high-value roadmap items (Container Trade Flow, Truck Traffic Volume, Dual Sentiment Divergence, AI News Story Clustering, Local LLM Ticker Mapping). Version alignment to 2.28.1.
* **v2.28.0 (2026-08-30)** : Autonomous feature implementation cycle. Fully implemented **Aggregated Consumer Transaction / Credit-Card Panel Spend Nowcasting Overlay** (`sie/consumer_spend.py`, `--no-consumer-spend`). Deterministic synthetic panel-spend momentum proxy with soft boost/penalty; fields `cs_momentum`, `cs_score`, `cs_boost`, `cs_confidence`, `cs_reason`, `cs_source`. Wired into analyzer / CLI / config / dashboard preferred columns / tests. Marked completed in FUTURE-IMPROVEMENTS. Version alignment to 2.28.0.
* **v2.27.1 (2026-08-30)** : Autonomous research & evolution cycle. Code audit confirmed no outstanding completed items needing cleanup. Fresh 2026 research on AI stock tools, consumer transaction nowcasting, maritime AIS/port congestion, Substack/newsletter sentiment, analyst revision momentum, order-flow microstructure, and Streamlit production patterns. Added five new high-value roadmap items (Consumer Spend Nowcast, AIS/Port Congestion, Substack Sentiment, Analyst Revision Momentum, Order-Flow Imbalance). Version alignment to 2.27.1.
* **v2.27.0 (2026-08-29)** : Autonomous feature implementation cycle. Fully implemented **Authenticity-Filtered Social Narrative Velocity Overlay** (`sie/authenticity.py`, `--no-authenticity`). Deterministic authenticity score + filtered velocity proxy; soft boost on high-auth rising narrative, caution on low-auth elevated velocity (bot/spam risk). Wired into analyzer / CLI / config / dashboard preferred columns / tests. Marked completed in FUTURE-IMPROVEMENTS. Version alignment to 2.27.0.
* **v2.26.1 (2026-08-29)** : Autonomous research & evolution cycle. Code audit confirmed no outstanding completed items needing cleanup. Fresh 2026 research on AI stock tools, narrative authenticity scoring, earnings-call NLP divergence, dealer gamma exposure, and Streamlit production patterns. Added five new high-value roadmap items (Authenticity-Filtered Velocity, Q&A vs Prepared Divergence, GEX Overlay, Multi-User Persistent Watchlists, Cloud Deployment Profiles). Version alignment to 2.26.1.
* **v2.26.0 (2026-08-28)** : Autonomous implementation cycle. Shipped three overlays end-to-end: **Supply-Chain CapEx** (`sie/supply_chain.py`, `--no-supply-chain`), **FINRA Short Volume** (`sie/short_interest.py`, `--no-short-interest`), **Attention Momentum** (`sie/attention.py`, `--no-attention`). Wired into analyzer / CLI / config / dashboard / tests. Added DISCLAIMER.md and CONTRIBUTING.md. Marked completed items in FUTURE-IMPROVEMENTS. Version alignment to 2.26.0.
* **v2.25.0 (2026-08-28)** : Autonomous feature implementation cycle. Fully implemented **Market Regime Adaptive Overlay Weighting** (`sie/regime.py`) with live VIX/SPY detection, adaptive overlay group weights, soft signal bias and full wiring into analyzer / CLI (`--no-regime`) / dashboard / config. Removed completed item from FUTURE-IMPROVEMENTS. Version alignment to 2.25.0 across all files.
* **v2.24.0 (2026-08-28)** : Autonomous research & evolution cycle. Code audit discovered Signal Confidence Calibration & LLM Self-Critique was present (`sie/confidence.py` + config + CLI) but not wired into analyzer orchestration / dashboard; fully integrated `include_confidence` + `integrate_confidence_to_row`. Removed completed item from FUTURE-IMPROVEMENTS. Added five new high-value 2026 research-backed items. Version alignment to 2.24.0 across all files.
* **v2.23.0 (2026-08-26)** : Autonomous feature implementation cycle. Fully implemented **Streamlit Fragment Live Dashboard Refresh** in `app.py`.

## Disclaimer

This is an educational research tool. Not financial advice. See DISCLAIMER.md.

v2.29.2
