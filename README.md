# Stock Intelligence Engine

**Connect market narratives to your watchlist.**  
**Confirm with technicals.**  
**Explain every signal.**

**v2.34.0** — September 2026 · Dealer GEX & Pin-Risk Overlay (fully wired) + Autonomous Research & Evolution Cycle + Company Digital Footprint Momentum Overlay (fully wired) + Patent & Intellectual Property Filing Momentum Overlay + Analyst Estimate Revision Velocity & Breadth Overlay + Cross-Ticker Narrative Contagion Detector + Securities Lending / Borrow Fee & Short Squeeze Risk Overlay + Aggregated Consumer Transaction / Credit-Card Panel Spend Nowcasting + Authenticity-Filtered Social Narrative Velocity + Supply-Chain CapEx + FINRA Short + Attention Momentum + Market Regime Adaptive Overlay Weighting + Signal Confidence Calibration & LLM Self-Critique + Streamlit Fragment Live Dashboard Refresh + LLM Bull/Bear Thesis + Self-Explaining AI Signal Brief + Honesty / Contradiction Detector + Corporate Hiring + Same-Day SEC EDGAR + 0DTE Options Flow + Options IV Skew + Dark Pool / ATS + Real-time Quotes + Congressional Trading + Portfolio Risk + Institutional 13F + Prediction Markets + Insider Form 4 + Narrative Velocity + Backtesting

## Features

* Real-time signals with narrative intelligence
* **Dealer Gamma Exposure (GEX) & Pin-Risk Overlay** — Approximate dealer gamma + pin-risk from live yfinance options chains when available, otherwise a labeled synthetic proxy. Soft +1 near high positive-GEX pins; -1 on large negative GEX + elevated 0DTE. Fully wired into analyzer, CLI (`--no-gex`) and dashboard.
* **Company Digital Footprint Momentum Overlay** — Tracks web traffic velocity + app download / engagement momentum as a forward demand / narrative-durability proxy (AltIndex-style); soft boost on accelerating high-engagement footprint, caution on sharp deceleration. Synthetic proxy fully integrated into analyzer, CLI and dashboard.
* **Patent & Intellectual Property Filing Momentum Overlay** — Tracks USPTO/EPO-style patent filing velocity, forward-citation velocity and grant ratio as a forward-looking innovation / economic-moat signal; soft boost on accelerating high-quality patent activity (esp. AI/semi/biotech), caution on deceleration. Synthetic proxy fully integrated into analyzer, CLI and dashboard.
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

* **v2.34.0 (2026-09-18)** : Autonomous research & evolution cycle. Completed full wiring of **Dealer Gamma Exposure (GEX) & Pin-Risk Overlay** (`sie/gex.py`) — module + CLI flag already existed but analyzer `analyze_watchlist` / `run_report` signature, import chain and Streamlit preferred columns were incomplete; `include_gex` would have TypeError'd. Now fully integrated. Removed GEX from FUTURE-IMPROVEMENTS.md. Fresh 2026 research on AI stock tools (AltIndex Developer API, Signals.ai, NorrisAI AlphaLens, Massive MCP, ChatGPT for Financial Services / GPT-6 Astra, NowNews, AlphaSense, Hebbia, Fintool), ETF creation/redemption as mechanical demand, 10b5-1/buyback execution, FOMC surprise scoring, supplier-customer surprise graphs, on-chain stablecoin/tokenized-treasury liquidity. Added five new roadmap items (ETF AP Flow, 10b5-1/Buyback Execution, FOMC Surprise, Supplier–Customer Surprise Graph, On-Chain Liquidity Pulse). Version alignment to **2.34.0** across package, CLI, dashboard and docs.
* **v2.33.3 (2026-09-17)** : Autonomous research & evolution cycle. Code audit confirmed every previously completed overlay (Digital Footprint, Patent Momentum, Estimate Revision, Contagion, Borrow Fee, Consumer Spend, Authenticity, Supply-Chain CapEx, Short Interest, Attention, Regime, Confidence, Honesty, Thesis, Brief and earlier layers) remains fully wired in analyzer / CLI / config / dashboard; no FUTURE items required removal. Fresh 2026 research on AI stock tools (NowNews, Fiscal.ai, Marvin Labs, AlphaSense, Prospero, Danelfin, Webull Vega, Barebone AI), narrative advances (KOL amplification graphs, whisper-number alt-data fusion, risk-factor delta detection), alternative data (SAR industrial activity, GPU/HBM lead-times, foot-traffic proxies), MCP agent surfaces and production Streamlit patterns. Added five new high-value roadmap items (Whisper Number / Pre-Earnings Alt-Data Beat Probability, KOL / Influencer Narrative Amplification, GPU / AI Accelerator Supply-Chain & Lead-Time, 10-K/10-Q Risk Factor Delta & Hidden Liability, SAR Industrial & Commodity Activity Proxy). Version alignment to **2.33.3** across package, CLI, dashboard and docs.
* **v2.33.2 (2026-09-16)** : Autonomous research & evolution cycle. Completed full wiring of **Company Digital Footprint Momentum Overlay** (`sie/digital_footprint.py`) — module + CLI flag already existed but analyzer import chain, `run_report` signature and Streamlit preferred columns were incomplete; now fully integrated. Code audit confirmed all prior overlays remain wired. Fresh 2026 research on AI stock tools (NowNews, Fiscal.ai, Marvin Labs, AlphaSense, Prospero, Danelfin, MoneySense AI, SentiSense, Adanos, Optionomics), earnings-call guidance drift detection, source-authority weighting, expert-network aspect extraction, MCP agent surfaces, and geospatial activity proxies. Added five new high-value roadmap items (Earnings Call Transcript Sentiment & Guidance Drift, News-Source Authority Weighting, Expert Network Aspect Extraction, MCP / Agent Tool Server Surface, Satellite / Night-Lights Activity Proxy). Version alignment to **2.33.2** across package, CLI, dashboard and docs.
* **v2.33.1 (2026-09-14)** : Autonomous research & evolution cycle. Restored `FUTURE-IMPROVEMENTS.md` (previously reduced to a stub). Code audit confirmed all prior overlays remain fully wired. Version alignment to **2.33.1**.
* **v2.32.1 (2026-09-13)** : Autonomous research & evolution cycle. Version alignment to **2.32.1**.
* **v2.32.0 (2026-09-10)** : Fully implemented **Patent & Intellectual Property Filing Momentum Overlay**.
* **v2.31.0 (2026-09-09)** : Fully implemented **Analyst Estimate Revision Velocity & Breadth Overlay**.
* **v2.30.0 (2026-09-08)** : Fully implemented **Cross-Ticker Narrative Contagion Detector**.

## Disclaimer

This is an educational research tool. Not financial advice. See DISCLAIMER.md.

v2.34.0
