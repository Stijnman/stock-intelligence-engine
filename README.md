# Stock Intelligence Engine

**Connect market narratives to your watchlist.**  
**Confirm with technicals.**  
**Explain every signal.**

**v2.37.0** — September 2026 · Earnings Call Transcript Sentiment & Guidance Drift Overlay (fully wired) + Corporate Credit Spread / CDS Momentum Overlay + Social Trading Action Intent Classifier + Dealer GEX & Pin-Risk Overlay + Company Digital Footprint Momentum + Patent & IP Filing Momentum + Analyst Estimate Revision Velocity + Cross-Ticker Narrative Contagion + Borrow Fee & Short Squeeze Risk + Consumer Spend Nowcasting + Authenticity-Filtered Social Narrative Velocity + Supply-Chain CapEx + FINRA Short + Attention Momentum + Regime Adaptive Weighting + Confidence Calibration + Streamlit Fragment Live Dashboard + Thesis + Brief + Honesty + Hiring + EDGAR + 0DTE + IV + Dark Pool + Realtime + Congressional + 13F + Prediction Markets + Insider + Narrative Velocity + Backtesting

## Features

* Real-time signals with narrative intelligence
* **Earnings Call Transcript Sentiment & Guidance Drift** — Management tone, guidance language drift vs the prior print, and hedging density from same-day / near-real-time transcripts (synthetic proxy offline). Soft boost when guidance tone + narrative velocity align upward; caution on soft-pedaled guidance or hedge language that diverges from social heat. Fully integrated into analyzer, CLI (`--no-earnings-call`) and dashboard (`ect_*` columns).
* **Corporate Credit Spread / CDS Momentum Overlay** — Relative CDS / credit-spread tightening vs widening as a leading fundamental stress / relief signal. Soft boost on tightening + rising narrative; caution on rapid widening even when social heat is elevated. Synthetic proxy fully integrated into analyzer, CLI (`--no-credit-spread`) and dashboard (`cds_*` columns).
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

* **v2.37.0 (2026-09-20)** : Fully implemented **Earnings Call Transcript Real-Time Sentiment & Guidance Drift Detector** (`sie/earnings_call.py`). Wired through analyzer (`include_earnings_call`), CLI (`--no-earnings-call`), config (`earnings_call:`), Streamlit preferred columns (`ect_sentiment`, `ect_guidance_drift`, `ect_hedge_density`, `ect_direction`, `ect_boost`, `ect_reason`). Deterministic synthetic proxy. Removed from FUTURE-IMPROVEMENTS.md High Priority.
* **v2.36.1 (2026-09-20)** : Autonomous research & evolution cycle. Code audit confirmed no High Priority FUTURE items are fully implemented and wired (earnings-call transcripts, news-source authority, whisper-number cluster, KOL amplification, ETF AP flow, 10b5-1 / buyback execution, unusual options sweep-vs-block, employee outlook). Nothing removed from FUTURE-IMPROVEMENTS.md. Fresh 2026 research (AltIndex alt-data + app-store rankings, Stock Companion FinBERT news sentiment, TradeAlgo / Unusual Whales AI options scanners, Prospero.ai signal stack, SentiSense publisher reliability + MCP, StockTools.ai workspace, Earnings Trader event cards). Added five new roadmap items: App-Store Review Sentiment & Complaint Velocity, Retail Brokerage Order-Flow Imbalance, Macro Surprise vs Ticker-Beta Residual, Investor-Day / Slide-Deck Guidance NLP, Physical Climate / Extreme-Weather Event Exposure.
* **v2.36.0 (2026-09-19)** : Fully implemented **Corporate Credit Spread / CDS Momentum Overlay** (`sie/credit_spread.py`). Wired through analyzer (`include_credit_spread`), CLI (`--no-credit-spread`), config (`credit_spread:`), Streamlit preferred columns (`cds_spread_bp`, `cds_delta_bp`, `cds_direction`, `cds_boost`, `cds_reason`). Deterministic synthetic proxy. Removed from FUTURE-IMPROVEMENTS.md High Priority.
* **v2.35.1 (2026-09-19)** : Autonomous research & evolution cycle. Code audit confirmed no High Priority FUTURE items were fully implemented and wired; nothing removed from FUTURE-IMPROVEMENTS.md. Fresh 2026 research (AltIndex employee-outlook / AI Score API, SentiSense MCP sentiment, TickerDesk sweep/block options flow, StockTools / Stock Companion news+insider workspaces, Trade Ideas HOLLY). Added four new roadmap items: Unusual Options Sweep-vs-Block Confirmation, Employee Outlook / Glassdoor Business Sentiment, Earnings Calendar Distance-Decay & Event-Risk, SEC Comment-Letter / Regulatory Docket Velocity.
* **v2.35.0 (2026-09-18)** : Fully implemented **Social Trading Action Intent Classifier** (`sie/social_intent.py`). Wired through analyzer (`include_social_intent`), CLI (`--no-social-intent`), config (`social_intent:`), Streamlit preferred columns (`sti_intent`, `sti_intent_share`, `sti_high_intent_velocity`, `sti_boost`, `sti_reason`). Extends authenticity layer. Removed from FUTURE-IMPROVEMENTS.md High Priority.
* **v2.34.0 (2026-09-18)** : Dealer GEX & Pin-Risk Overlay fully wired.
* **v2.33.3 (2026-09-17)** : Autonomous research & evolution cycle.

## Disclaimer

This is an educational research tool. Not financial advice. See DISCLAIMER.md.

v2.37.0
