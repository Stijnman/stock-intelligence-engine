# Stock Intelligence Engine

**Connect market narratives to your watchlist.**  
**Confirm with technicals.**  
**Explain every signal.**

**v2.35.0** — September 2026 · Social Trading Action Intent Classifier (fully wired) + Dealer GEX & Pin-Risk Overlay + Company Digital Footprint Momentum + Patent & IP Filing Momentum + Analyst Estimate Revision Velocity + Cross-Ticker Narrative Contagion + Borrow Fee & Short Squeeze Risk + Consumer Spend Nowcasting + Authenticity-Filtered Social Narrative Velocity + Supply-Chain CapEx + FINRA Short + Attention Momentum + Regime Adaptive Weighting + Confidence Calibration + Streamlit Fragment Live Dashboard + Thesis + Brief + Honesty + Hiring + EDGAR + 0DTE + IV + Dark Pool + Realtime + Congressional + 13F + Prediction Markets + Insider + Narrative Velocity + Backtesting

## Features

* Real-time signals with narrative intelligence
* **Social Trading Action Intent Classifier** — Classifies social posts into buy-the-dip, FOMO chase, bag-holding, short-squeeze call, take-profit, spam. Filters velocity to high-intent authentic posts; soft boost on rising high-intent authentic velocity, caution on spam/low-intent spikes. Synthetic proxy fully integrated into analyzer, CLI (`--no-social-intent`) and dashboard (`sti_*` columns).
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

* **v2.35.0 (2026-09-18)** : Fully implemented **Social Trading Action Intent Classifier** (`sie/social_intent.py`). Wired through analyzer (`include_social_intent`), CLI (`--no-social-intent`), config (`social_intent:`), Streamlit preferred columns (`sti_intent`, `sti_intent_share`, `sti_high_intent_velocity`, `sti_boost`, `sti_reason`). Extends authenticity layer. Removed from FUTURE-IMPROVEMENTS.md High Priority.
* **v2.34.0 (2026-09-18)** : Dealer GEX & Pin-Risk Overlay fully wired.
* **v2.33.3 (2026-09-17)** : Autonomous research & evolution cycle.

## Disclaimer

This is an educational research tool. Not financial advice. See DISCLAIMER.md.

v2.35.0
