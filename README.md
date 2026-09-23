# Stock Intelligence Engine

**Connect market narratives to your watchlist.**  
**Confirm with technicals.**  
**Explain every signal.**

**v2.40.0** — September 2026 · KOL / Influencer Narrative Amplification + Whisper Number / Pre-Earnings Alt-Data Beat Probability (fully wired) + News-Source Authority Weighted Narrative (fully wired) + Earnings Call Transcript Sentiment & Guidance Drift Overlay + Corporate Credit Spread / CDS Momentum Overlay + Social Trading Action Intent Classifier + Dealer GEX & Pin-Risk Overlay + Company Digital Footprint Momentum + Patent & IP Filing Momentum + Analyst Estimate Revision Velocity + Cross-Ticker Narrative Contagion + Borrow Fee & Short Squeeze Risk + Consumer Spend Nowcasting + Authenticity-Filtered Social Narrative Velocity + Supply-Chain CapEx + FINRA Short + Attention Momentum + Regime Adaptive Weighting + Confidence Calibration + Streamlit Fragment Live Dashboard + Thesis + Brief + Honesty + Hiring + EDGAR + 0DTE + IV + Dark Pool + Realtime + Congressional + 13F + Prediction Markets + Insider + Narrative Velocity + Backtesting

## Features

* Real-time signals with narrative intelligence
* **KOL / Influencer Narrative Amplification** — Scores high-follower / high-engagement authentic accounts and amplification cascades on X / Reddit / YouTube. Soft boost on organic KOL-driven velocity confirmation; caution on coordinated or low-authenticity spikes. Fully integrated into analyzer, CLI (`--no-kol-amplification`) and dashboard (`kol_*` columns).
* **Whisper Number / Pre-Earnings Alt-Data Beat Probability** — Fuses consumer-spend, digital-footprint, hiring, attention and supply-chain nowcasts into a probabilistic whisper beat/miss estimate ahead of earnings. Soft boost when the alt-data cluster implies a high beat probability; caution on a deteriorating cluster even when street consensus is stable. Fully integrated into analyzer, CLI (`--no-whisper-number`) and dashboard (`wn_*` columns).
* **News-Source Authority / Reliability Weighted Narrative** — Weights news and social velocity by source authority (tier-1 share, unverified-source share) instead of treating all mentions equally. Soft boost on high-authority confirmed narrative; caution on low-authority / unverified spikes. Fully integrated into analyzer, CLI (`--no-news-authority`) and dashboard (`nsa_*` columns).
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

* **v2.40.0 (2026-09-23)** : Fully implemented **Key Opinion Leader (KOL) / Influencer Narrative Amplification Detector** (`sie/kol_amplification.py`). Wired through analyzer (`include_kol_amplification`), CLI (`--no-kol-amplification`), config (`kol_amplification:`), Streamlit preferred columns (`kol_score`, `kol_cascade`, `kol_amp_ratio`, `kol_auth`, `kol_boost`, `kol_reason`). Deterministic synthetic proxy. Removed from FUTURE-IMPROVEMENTS.md High Priority.
* **v2.39.2 (2026-09-23)** : Full [AUTONOMOUS RESEARCH & EVOLUTION CYCLE](AUTONOMOUS-RESEARCH-EVOLUTION-CYCLE.md). Exhaustive wiring audit of every open FUTURE-IMPROVEMENTS item against `sie/` modules, analyzer flags, CLI disable switches, config blocks and Streamlit preferred columns found **no remaining roadmap item fully implemented**, so none was removed. Fresh 2026 research (prediction-market event contracts vs street/whisper, passive index forced flow, 10-Q working-capital drift, SaaS status-page incident velocity, CAT-bond / reinsurance sector stress) added five genuinely new overlays. Patch release: roadmap/docs/version metadata only; runtime signal behavior unchanged.
* **v2.39.1 (2026-09-22)** : Full [AUTONOMOUS RESEARCH & EVOLUTION CYCLE](AUTONOMOUS-RESEARCH-EVOLUTION-CYCLE.md). Exhaustive code/wiring audit found **no remaining FUTURE-IMPROVEMENTS item fully implemented across module + analyzer + CLI + config + Streamlit**, so no roadmap item was incorrectly removed. Fresh 2026 research across narrative NLP, alternative-data quality, options/retail routing and corporate credit added five genuinely new overlays: TRACE Corporate-Bond Customer-Flow & Liquidity Shock; Primary Credit Issuance / New-Issue Concession & Supply Pressure; Target-Specific Financial Stance & Narrative Specificity; Alternative-Data Provenance & AI-Synthetic Contamination Confidence; Rule 606 Retail Options Routing & Execution Quality. Patch release: roadmap/docs/version metadata only; runtime signal behavior unchanged.
* **v2.39.0 (2026-09-22)** : Fully implemented **Whisper Number / Pre-Earnings Alt-Data Beat Probability Overlay** (`sie/whisper_number.py`). Wired through analyzer (`include_whisper_number`), CLI (`--no-whisper-number`), config (`whisper_number:`), Streamlit preferred columns (`wn_beat_prob`, `wn_cluster_score`, `wn_days_to_print`, `wn_consensus_gap`, `wn_boost`, `wn_reason`). Deterministic synthetic proxy. Removed from FUTURE-IMPROVEMENTS.md High Priority.
* **v2.38.1 (2026-09-22)** : Autonomous research & evolution cycle. Code audit confirmed **News-Source Authority** is fully wired (`sie/news_authority.py`) — removed from FUTURE-IMPROVEMENTS.md High Priority (implementation shipped in v2.38.0; docs were lagging). Fresh 2026 research (StockTitan Rhea-AI impact scoring, OpenAI ChatGPT for Financial Services, SentiSense MCP + publisher reliability, Adanos sentiment APIs, NorrisAI AlphaLens, Marvin Labs guidance-vs-delivered). Added five new roadmap items: News Materiality / Predicted Next-Session Impact Score, Secondary Offering / ATM Dilution Velocity, Multi-Quarter Guidance-vs-Delivered KPI Tracker, Short-Seller Report / Activist Campaign Velocity, Cross-Language / Offshore Narrative Lag.
* **v2.38.0 (2026-09-21)** : Fully implemented **News-Source Authority / Reliability Weighted Narrative Score** (`sie/news_authority.py`). Wired through analyzer (`include_news_authority`), CLI (`--no-news-authority`), config (`news_authority:`), Streamlit preferred columns (`nsa_authority`, `nsa_weighted_vel`, `nsa_tier1_share`, `nsa_unverified_share`, `nsa_boost`, `nsa_reason`). Deterministic synthetic proxy.
* **v2.37.1 (2026-09-21)** : Autonomous research & evolution cycle. Code audit confirmed no remaining High Priority FUTURE items are fully implemented and wired (news-source authority was still listed; subsequent cycle shipped it). Added five new roadmap items: Job-Posting Skill-Mix & Posted-Compensation Inflation, Cross-Venue Tokenized-Share Basis, Physical Foot-Traffic vs Digital-Demand Divergence, SKU Shelf-Price / Promo-Intensity Nowcast, Auditor-Change / Going-Concern Language Velocity.
* **v2.37.0 (2026-09-20)** : Fully implemented **Earnings Call Transcript Real-Time Sentiment & Guidance Drift Detector** (`sie/earnings_call.py`). Wired through analyzer (`include_earnings_call`), CLI (`--no-earnings-call`), config (`earnings_call:`), Streamlit preferred columns (`ect_sentiment`, `ect_guidance_drift`, `ect_hedge_density`, `ect_direction`, `ect_boost`, `ect_reason`). Deterministic synthetic proxy. Removed from FUTURE-IMPROVEMENTS.md High Priority.
* **v2.36.1 (2026-09-20)** : Autonomous research & evolution cycle.
* **v2.36.0 (2026-09-19)** : Fully implemented **Corporate Credit Spread / CDS Momentum Overlay** (`sie/credit_spread.py`).
* **v2.35.1 (2026-09-19)** : Autonomous research & evolution cycle.
* **v2.35.0 (2026-09-18)** : Fully implemented **Social Trading Action Intent Classifier** (`sie/social_intent.py`).
* **v2.34.0 (2026-09-18)** : Dealer GEX & Pin-Risk Overlay fully wired.
* **v2.33.3 (2026-09-17)** : Autonomous research & evolution cycle.

## Disclaimer

This is an educational research tool. Not financial advice. See DISCLAIMER.md.

v2.40.0

## Flagship integration

This project remains independently usable and is not deprecated. Its capabilities are also consumed by [SignalForge](https://github.com/Stijnman/SignalForge), where they are integrated with complementary repositories behind shared platform contracts. This repository remains the source of truth for its component-specific implementation.
