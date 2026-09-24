# Stock Intelligence Engine

**Connect market narratives to your watchlist.**  
**Confirm with technicals.**  
**Explain every signal.**

**v2.41.0** — September 2026 · ETF Creation / Redemption & AP Flow (fully wired) + KOL / Influencer Narrative Amplification (fully wired) + Whisper Number / Pre-Earnings Alt-Data Beat Probability (fully wired) + News-Source Authority Weighted Narrative + Earnings Call Transcript Sentiment & Guidance Drift Overlay + Corporate Credit Spread / CDS Momentum Overlay + Social Trading Action Intent Classifier + Dealer GEX & Pin-Risk Overlay + Company Digital Footprint Momentum + Patent & IP Filing Momentum + Analyst Estimate Revision Velocity + Cross-Ticker Narrative Contagion + Borrow Fee & Short Squeeze Risk + Consumer Spend Nowcasting + Authenticity-Filtered Social Narrative Velocity + Supply-Chain CapEx + FINRA Short + Attention Momentum + Regime Adaptive Weighting + Confidence Calibration + Streamlit Fragment Live Dashboard + Thesis + Brief + Honesty + Hiring + EDGAR + 0DTE + IV + Dark Pool + Realtime + Congressional + 13F + Prediction Markets + Insider + Narrative Velocity + Backtesting

## Features

* Real-time signals with narrative intelligence
* **ETF Creation / Redemption & Authorized-Participant Flow** — Tracks net creation/redemption and premium/discount vs NAV for theme ETFs as a mechanical demand pulse into underlying names. Soft boost on multi-session creation streaks confirming narrative; caution on redemption streaks or persistent discount while social heat is elevated. Fully integrated into analyzer, CLI (`--no-etf-flow`) and dashboard (`etf_*` columns).
* **KOL / Influencer Narrative Amplification** — Scores high-follower / high-engagement authentic accounts and amplification cascades on X / Reddit / YouTube. Soft boost on organic KOL-driven velocity confirmation; caution on coordinated or low-authenticity spikes. Fully integrated into analyzer, CLI (`--no-kol-amplification`) and dashboard (`kol_*` columns).
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

* **v2.41.0 (2026-09-24)** : Fully implemented **ETF Creation / Redemption & Authorized-Participant Flow Overlay** (`sie/etf_flow.py`). Wired through analyzer (`include_etf_flow`), CLI (`--no-etf-flow`), config (`etf_flow:`), Streamlit preferred columns (`etf_flow_score`, `etf_prem_disc`, `etf_create_streak`, `etf_theme`, `etf_boost`, `etf_reason`). Deterministic synthetic proxy. Removed from FUTURE-IMPROVEMENTS.md High Priority.
* **v2.40.1 (2026-09-24)** : Autonomous research & evolution cycle. Confirmed KOL amplification fully wired.
* **v2.40.0 (2026-09-23)** : Fully implemented **Key Opinion Leader (KOL) / Influencer Narrative Amplification Detector** (`sie/kol_amplification.py`).

## Disclaimer

This is an educational research tool. Not financial advice. See DISCLAIMER.md.

v2.41.0

## Flagship integration

This project remains independently usable and is not deprecated. Its capabilities are also consumed by [SignalForge](https://github.com/Stijnman/SignalForge), where they are integrated with complementary repositories behind shared platform contracts. This repository remains the source of truth for its component-specific implementation.
