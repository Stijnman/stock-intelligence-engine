# Stock Intelligence Engine

**Connect market narratives to your watchlist.**  
**Confirm with technicals.**  
**Explain every signal.**

**v2.31.0** — September 2026 · Analyst Estimate Revision Velocity & Breadth Overlay (fully wired) + Cross-Ticker Narrative Contagion Detector + Securities Lending / Borrow Fee & Short Squeeze Risk Overlay + Aggregated Consumer Transaction / Credit-Card Panel Spend Nowcasting + Authenticity-Filtered Social Narrative Velocity + Supply-Chain CapEx + FINRA Short + Attention Momentum + Market Regime Adaptive Overlay Weighting + Signal Confidence Calibration & LLM Self-Critique + Streamlit Fragment Live Dashboard Refresh + LLM Bull/Bear Thesis + Self-Explaining AI Signal Brief + Honesty / Contradiction Detector + Corporate Hiring + Same-Day SEC EDGAR + 0DTE Options Flow + Options IV Skew + Dark Pool / ATS + Real-time Quotes + Congressional Trading + Portfolio Risk + Institutional 13F + Prediction Markets + Insider Form 4 + Narrative Velocity + Backtesting

## Features

* Real-time signals with narrative intelligence
* **Analyst Estimate Revision Velocity & Breadth Overlay** — Tracks speed, direction and coverage-breadth of consensus EPS/revenue estimate revisions; soft boost on rapid upward revisions + rising breadth (narrative durability), caution on sharp downward revisions. Synthetic proxy fully integrated into analyzer, CLI and dashboard.
* **Cross-Ticker Narrative Contagion Detector** — Measures rapid transfer of narrative velocity between thematic peers (AI/semiconductor, consumer, energy, meme clusters); soft boost on inbound contagion confirmation, caution on reverse flow. Synthetic cluster proxy fully integrated into analyzer, CLI and dashboard.
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

* **v2.31.0 (2026-09-09)** : Fully implemented **Analyst Estimate Revision Velocity & Breadth Overlay**. New `sie/estimate_revision.py` synthetic proxy (ticker+day seeded, AI/semi bias) tracks consensus revision velocity, breadth and direction. Soft +1 boost on rapid upward revisions with sufficient breadth; -1 caution on sharp downward revisions. Wired into `analyze_watchlist` / `run_report`, added `estimate_revision:` config block, CLI `--no-estimate-revision` flag, and preferred dashboard columns (`er_velocity`, `er_breadth`, `er_direction`, `er_boost`, `er_reason`). Marked roadmap item complete. Version alignment to **2.31.0** across package, CLI, dashboard and docs.
* **v2.30.1 (2026-09-09)** : Autonomous research & evolution cycle. Code audit confirmed all prior overlays (including Cross-Ticker Narrative Contagion Detector) remain fully wired in analyzer / CLI / config / dashboard; no completed roadmap items required removal this cycle. Fresh 2026 research on AI stock tools (SentiSense, Fiscal.ai, Prospero, Marvin Labs, AlphaSense, NowNews, Adanos, Financial Datasets, Danelfin, AltIndex), narrative/sentiment MCP surfaces, alternative data (patent/IP momentum, maritime AIS/port congestion, corporate CDS/credit spreads, analyst estimate revision velocity, long-form YouTube/podcast narrative), Streamlit production patterns and cloud connectors. Added five new high-value roadmap items (Analyst Estimate Revision Velocity & Breadth, Patent & IP Filing Momentum, Maritime AIS / Port Congestion, Corporate Credit Spread / CDS Momentum, YouTube / Podcast / Long-Form Content Narrative Velocity). Version alignment to **2.30.1** across package, CLI, dashboard and docs.
* **v2.30.0 (2026-09-08)** : Fully implemented **Cross-Ticker Narrative Contagion Detector**. Wired existing `sie/contagion.py` synthetic cluster proxy into `analyze_watchlist` / `run_report`, added `contagion:` config block, CLI `--no-contagion` flag, and preferred columns (`ct_score`, `ct_velocity_transfer`, `ct_boost`, `ct_peers`, `ct_reason`) on the Streamlit dashboard. Also fixed dashboard row extraction from `run_report` result dict. Marked roadmap item complete. Version alignment to **2.30.0** across package, CLI, dashboard and docs.
* **v2.29.5 (2026-09-08)** : Autonomous research & evolution cycle. Code audit confirmed no outstanding completed items needing cleanup (all prior overlays fully wired; contagion module exists but not fully integrated). Fresh 2026 research on AI stock tools (AltIndex, SentiSense, Fiscal.ai, Prospero, Marvin Labs, AlphaSense, NowNews, Adanos, Financial Datasets), alt-data categories (freight rates / logistics indices, job-posting AI-skill intensity, retail vs institutional options flow divergence, expert-network transcripts, data-center power intensity), near-instant XBRL, and Streamlit / cloud patterns. Added five new high-value roadmap items (Freight Rate Overlay, AI-Skill Job Intensity, Retail/Institutional Options Divergence, Expert Network Transcript, Data-Center Power Intensity). Version alignment to **2.29.5** across CLI, package, dashboard and docs.

## Disclaimer

This is an educational research tool. Not financial advice. See DISCLAIMER.md.

v2.31.0
