# Stock Intelligence Engine

**Connect market narratives to your watchlist.**  
**Confirm with technicals.**  
**Explain every signal.**

**v2.29.4** — September 2026 · Securities Lending / Borrow Fee & Short Squeeze Risk Overlay + Aggregated Consumer Transaction / Credit-Card Panel Spend Nowcasting + Authenticity-Filtered Social Narrative Velocity + Supply-Chain CapEx + FINRA Short + Attention Momentum (fully wired) + Market Regime Adaptive Overlay Weighting + Signal Confidence Calibration & LLM Self-Critique + Streamlit Fragment Live Dashboard Refresh + LLM Bull/Bear Thesis + Self-Explaining AI Signal Brief + Honesty / Contradiction Detector + Corporate Hiring + Same-Day SEC EDGAR + 0DTE Options Flow + Options IV Skew + Dark Pool / ATS + Real-time Quotes + Congressional Trading + Portfolio Risk + Institutional 13F + Prediction Markets + Insider Form 4 + Narrative Velocity + Backtesting

## Features

* Real-time signals with narrative intelligence
* **Securities Lending / Borrow Fee & Short Squeeze Risk Overlay** — Deterministic borrow-fee / DTC / hard-to-borrow proxy; soft boost on elevated fees + covering + hot narrative (squeeze risk), caution on high fees vs cold narrative
* **Aggregated Consumer Transaction / Credit-Card Panel Spend Nowcasting Overlay** — Deterministic panel-spend momentum proxy as leading revenue nowcast; soft boost on rising spend vs narrative, caution on contraction
* **Authenticity-Filtered Social Narrative Velocity Overlay** — Scores social heat for authenticity / bot-likelihood before aggregating velocity; soft boost on high-auth rising narratives, caution on low-auth (bot/spam) elevated velocity
* **Semiconductor / AI Supply-Chain CapEx Momentum Tracker** — Supplier momentum (ASML / AMAT / LRCX / KLAC / TSM) as a leading inference-demand proxy; yfinance peek when available, otherwise labeled synthetic proxy
* **FINRA Short Volume / Short Interest Momentum Overlay** — Elevated short volume vs rising narrative = caution; covering + hot narrative = soft boost
* **Wikipedia / Search Attention Momentum Tracker** — Wikimedia pageview WoW when reachable, else seeded proxy
* **Market Regime Adaptive Overlay Weighting** — Dynamically re-weights narrative / technical / flow / fundamental overlays by current regime
* **Signal Confidence Calibration & LLM Self-Critique Layer** — Consistency scoring across overlays with calibrated confidence
* **Streamlit Fragment Live Dashboard Refresh**
* LLM Bull/Bear Thesis + Self-Explaining AI Signal Brief + Honesty / Contradiction Detector
* Corporate Hiring + Same-Day SEC EDGAR + 0DTE Options Flow + Options IV Skew + Dark Pool / ATS + Real-time Quotes
* Congressional Trading + Portfolio Risk + Institutional 13F + Prediction Markets + Insider Form 4 + Narrative Velocity + Backtesting

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env   # add any API keys
python stock_intelligence_engine.py
streamlit run app.py
```

See config.yaml for watchlist and overlay toggles.

## Recent Edits & Version History

* **v2.29.4 (2026-09-07)** : Autonomous research & evolution cycle. Restored empty core docs (README, FUTURE-IMPROVEMENTS, app.py) from prior good state. Code audit: all previously shipped overlays remain fully wired; completed [x] roadmap items cleaned from FUTURE-IMPROVEMENTS.md (9 items removed). Fresh 2026 research on AI stock tools (AltIndex, SentiSense, Fiscal.ai, Prospero, MoatScan), narrative/sentiment MCP surfaces, near-instant XBRL, options liquidity pools, Streamlit production (Parquet/offline), and cloud data connectors. Added five new high-value roadmap items (Near-Instant XBRL Filing Diff & Consensus Surprise, Options Liquidity-Ranked Setup Pool & Outcome Tracker, Streamlit Parquet State + Offline Demo, Multi-Provider Sentiment Aggregation with MCP, Cloud Data Marketplace Connectors). Version alignment to **2.29.4** across CLI, package, dashboard and docs.
* **v2.29.2 (2026-09-03)** : Autonomous research & evolution cycle. Code audit confirmed no outstanding completed items needing cleanup; fixed version drift in `sie/__init__.py` (was 2.30.0). Fresh 2026 research on AI stock tools, BNPL/alternative credit, expert-network transcripts, data-center power intensity, cross-asset narrative contagion, analyst-note velocity, and Streamlit production patterns. Added five new high-value roadmap items (Expert Network Transcript Overlay, BNPL Credit Momentum, Cross-Asset Contagion, Analyst Note Velocity, Data-Center Power Intensity). Version alignment to 2.29.2.

## Disclaimer

This is an educational research tool. Not financial advice. See DISCLAIMER.md.

v2.29.4
