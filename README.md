# Stock Intelligence Engine

**Connect market narratives to your watchlist.**  
**Confirm with technicals.**  
**Explain every signal.**

**v2.46.1** — September 2026 · Retail Brokerage Order-Flow Imbalance (fully wired) + App-Store Review Sentiment & Complaint Velocity (fully wired) + Employee Outlook / Glassdoor Business Sentiment (fully wired) + Unusual Options Sweep vs Block Confirmation (fully wired) + Rule 10b5-1 / Buyback Authorization vs Execution (fully wired) + ETF Creation / Redemption & AP Flow (fully wired) + KOL / Influencer Narrative Amplification (fully wired) + Whisper Number / Pre-Earnings Alt-Data Beat Probability (fully wired) + News-Source Authority Weighted Narrative + Earnings Call Transcript Sentiment & Guidance Drift Overlay + Corporate Credit Spread / CDS Momentum Overlay + Social Trading Action Intent Classifier + Dealer GEX & Pin-Risk Overlay + Company Digital Footprint Momentum + Patent & IP Filing Momentum + Analyst Estimate Revision Velocity + Cross-Ticker Narrative Contagion + Borrow Fee & Short Squeeze Risk + Consumer Spend Nowcasting + Authenticity-Filtered Social Narrative Velocity + Supply-Chain CapEx + FINRA Short + Attention Momentum + Regime Adaptive Weighting + Confidence Calibration + Streamlit Fragment Live Dashboard + Thesis + Brief + Honesty + Hiring + EDGAR + 0DTE + IV + Dark Pool + Realtime + Congressional + 13F + Prediction Markets + Insider + Narrative Velocity + Backtesting

## Features

* Real-time signals with narrative intelligence
* **Retail Brokerage Order-Flow Imbalance Overlay** — Scores retail buy/sell imbalance and heat as a confirmation layer next to dark-pool and unusual-options. Soft boost on buy-imbalance + heat into a confirming narrative; caution on sell-imbalance into elevated heat. Fully integrated into analyzer, CLI (`--no-retail-flow`) and dashboard (`rflow_*` columns).
* **App-Store Review Sentiment & Complaint Velocity** — Scores consumer app-store sentiment and 1-star complaint velocity as a product-quality pulse. Soft boost when ratings hold and complaints fade into a confirming narrative; caution on complaint spikes into social heat. Fully integrated into analyzer, CLI (`--no-app-store-reviews`) and dashboard (`asr_*` columns).
* **Employee Outlook / Glassdoor Business Sentiment** — Fully integrated into analyzer, CLI (`--no-employee-outlook`) and dashboard (`eo_*` columns).
* **Unusual Options Sweep vs Block Confirmation** — Fully integrated into analyzer, CLI (`--no-unusual-options`) and dashboard (`uopt_*` columns).
* **Rule 10b5-1 / Buyback Authorization vs Execution** — Fully integrated into analyzer, CLI (`--no-buyback-10b51`) and dashboard (`bb_*` columns).
* Dealer GEX & Pin-Risk, Digital Footprint, Patent Momentum, Estimate Revision, Contagion, Borrow Fee, Consumer Spend, Authenticity Filter, Supply-Chain CapEx, FINRA Short, Attention, Regime, Confidence, Thesis, Brief, Honesty, Hiring, EDGAR, 0DTE, IV, Dark Pool, Realtime, Congressional, 13F, Prediction Markets, Insider, Narrative Velocity, Backtesting

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env   # add any API keys
python stock_intelligence_engine.py
streamlit run app.py
```

See config.yaml for watchlist and overlay toggles.

## Recent Edits & Version History

* **v2.46.1 (2026-09-30)** : Autonomous research & evolution cycle. Code audit found no FUTURE-IMPROVEMENTS items fully wired since v2.46.0. Added five new roadmap overlays (realized AI-token consumption factor beta, multi-platform brand audience / short-form engagement velocity, thematic narrative taxonomy exposure, point-in-time filing freshness / agent-index latency, data-center interconnection queue / power availability). Version bump across package, CLI, dashboard and docs.
* **v2.46.0 (2026-09-29)** : Fully implemented **Retail Brokerage Order-Flow Imbalance Overlay** (`sie/retail_flow.py`). Wired through analyzer (`include_retail_flow`), CLI (`--no-retail-flow`), config (`retail_flow:`), Streamlit preferred columns (`rflow_imbalance`, `rflow_heat`, `rflow_boost`, `rflow_reason`). Deterministic synthetic proxy. Removed from FUTURE-IMPROVEMENTS.md High Priority.
* **v2.45.1 (2026-09-29)** : Autonomous research & evolution cycle. Code audit found no FUTURE-IMPROVEMENTS items fully wired since v2.45.0. Added five new roadmap overlays (Form 144 planned-sale calendar, freight BOL nowcast, activist 13D/13G accumulation, board interlock centrality, satellite methane / flare intensity). Version bump across package, CLI, dashboard and docs.
* **v2.45.0 (2026-09-28)** : Fully implemented **App-Store Review Sentiment & Complaint Velocity Overlay** (`sie/app_store_reviews.py`). Wired through analyzer (`include_app_store_reviews`), CLI (`--no-app-store-reviews`), config (`app_store_reviews:`), Streamlit preferred columns (`asr_sentiment`, `asr_complaint_velocity`, `asr_rating`, `asr_boost`, `asr_reason`). Deterministic synthetic proxy. Removed from FUTURE-IMPROVEMENTS.md High Priority.
* **v2.44.1 (2026-09-28)** : Autonomous research & evolution cycle.
* **v2.44.0 (2026-09-27)** : Employee Outlook / Glassdoor Business Sentiment Overlay.
* **v2.43.1 (2026-09-27)** : Autonomous research & evolution cycle.
* **v2.43.0 (2026-09-26)** : Unusual Options Sweep vs Block Confirmation Overlay.

## Disclaimer

This is an educational research tool. Not financial advice. See DISCLAIMER.md.

v2.46.1

## Flagship integration

This project remains independently usable and is not deprecated. Its capabilities are also consumed by [SignalForge](https://github.com/Stijnman/SignalForge), where they are integrated with complementary repositories behind shared platform contracts. This repository remains the source of truth for its component-specific implementation.
