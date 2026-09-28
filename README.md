# Stock Intelligence Engine

**Connect market narratives to your watchlist.**  
**Confirm with technicals.**  
**Explain every signal.**

**v2.44.1** — September 2026 · Employee Outlook / Glassdoor Business Sentiment (fully wired) + Unusual Options Sweep vs Block Confirmation (fully wired) + Rule 10b5-1 / Buyback Authorization vs Execution (fully wired) + ETF Creation / Redemption & AP Flow (fully wired) + KOL / Influencer Narrative Amplification (fully wired) + Whisper Number / Pre-Earnings Alt-Data Beat Probability (fully wired) + News-Source Authority Weighted Narrative + Earnings Call Transcript Sentiment & Guidance Drift Overlay + Corporate Credit Spread / CDS Momentum Overlay + Social Trading Action Intent Classifier + Dealer GEX & Pin-Risk Overlay + Company Digital Footprint Momentum + Patent & IP Filing Momentum + Analyst Estimate Revision Velocity + Cross-Ticker Narrative Contagion + Borrow Fee & Short Squeeze Risk + Consumer Spend Nowcasting + Authenticity-Filtered Social Narrative Velocity + Supply-Chain CapEx + FINRA Short + Attention Momentum + Regime Adaptive Weighting + Confidence Calibration + Streamlit Fragment Live Dashboard + Thesis + Brief + Honesty + Hiring + EDGAR + 0DTE + IV + Dark Pool + Realtime + Congressional + 13F + Prediction Markets + Insider + Narrative Velocity + Backtesting

## Features

* Real-time signals with narrative intelligence
* **Employee Outlook / Glassdoor Business Sentiment** — Scores employer-review outlook, CEO approval and complaint mix as a culture pulse orthogonal to hiring volume. Soft boost when rising outlook confirms narrative; caution when Glassdoor deteriorates into social heat. Fully integrated into analyzer, CLI (`--no-employee-outlook`) and dashboard (`eo_*` columns).
* **Unusual Options Sweep vs Block Confirmation** — Distinguishes aggressive sweep prints from passive blocks and scores confirmation vs fade against 0DTE / IV / GEX. Fully integrated into analyzer, CLI (`--no-unusual-options`) and dashboard (`uopt_*` columns).
* **Rule 10b5-1 / Buyback Authorization vs Execution** — Fully integrated into analyzer, CLI (`--no-buyback-10b51`) and dashboard (`bb_*` columns).
* **ETF Creation / Redemption & Authorized-Participant Flow** — Fully integrated into analyzer, CLI (`--no-etf-flow`) and dashboard (`etf_*` columns).
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

* **v2.44.1 (2026-09-28)** : Autonomous research & evolution cycle. Confirmed no open FUTURE-IMPROVEMENTS items were already shipped. Added five net-new roadmap items (implied-vs-realized news impact residual; corporate treasury stablecoin / on-chain cash; AIS port congestion; guidance-vs-delivery tracking; satellite parking occupancy).
* **v2.44.0 (2026-09-27)** : Fully implemented **Employee Outlook / Glassdoor Business Sentiment Overlay** (`sie/employee_outlook.py`). Wired through analyzer (`include_employee_outlook`), CLI (`--no-employee-outlook`), config (`employee_outlook:`), Streamlit preferred columns (`eo_outlook`, `eo_ceo`, `eo_review_velocity`, `eo_complaint_share`, `eo_boost`, `eo_reason`). Deterministic synthetic proxy. Removed from FUTURE-IMPROVEMENTS.md High Priority.
* **v2.43.1 (2026-09-27)** : Autonomous research & evolution cycle. Confirmed Unusual Options Sweep vs Block fully wired.
* **v2.43.0 (2026-09-26)** : Unusual Options Sweep vs Block Confirmation Overlay.
* **v2.42.0 (2026-09-25)** : Rule 10b5-1 / Buyback Authorization vs Execution Overlay.

## Disclaimer

This is an educational research tool. Not financial advice. See DISCLAIMER.md.

v2.44.1

## Flagship integration

This project remains independently usable and is not deprecated. Its capabilities are also consumed by [SignalForge](https://github.com/Stijnman/SignalForge), where they are integrated with complementary repositories behind shared platform contracts. This repository remains the source of truth for its component-specific implementation.
