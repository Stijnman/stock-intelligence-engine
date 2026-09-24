# Stock Intelligence Engine

**Connect market narratives to your watchlist.**  
**Confirm with technicals.**  
**Explain every signal.**

**v2.40.1** — September 2026 · KOL / Influencer Narrative Amplification (fully wired) + Whisper Number / Pre-Earnings Alt-Data Beat Probability (fully wired) + News-Source Authority Weighted Narrative (fully wired) + Earnings Call Transcript Sentiment & Guidance Drift Overlay + Corporate Credit Spread / CDS Momentum Overlay + Social Trading Action Intent Classifier + Dealer GEX & Pin-Risk Overlay + Company Digital Footprint Momentum + Patent & IP Filing Momentum + Analyst Estimate Revision Velocity + Cross-Ticker Narrative Contagion + Borrow Fee & Short Squeeze Risk + Consumer Spend Nowcasting + Authenticity-Filtered Social Narrative Velocity + Supply-Chain CapEx + FINRA Short + Attention Momentum + Regime Adaptive Weighting + Confidence Calibration + Streamlit Fragment Live Dashboard + Thesis + Brief + Honesty + Hiring + EDGAR + 0DTE + IV + Dark Pool + Realtime + Congressional + 13F + Prediction Markets + Insider + Narrative Velocity + Backtesting

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

* **v2.40.1 (2026-09-24)** : Autonomous research & evolution cycle. Code audit confirmed **KOL / Influencer Narrative Amplification** is fully wired (`sie/kol_amplification.py`) — removed from FUTURE-IMPROVEMENTS.md High Priority (implementation shipped in v2.40.0; roadmap lagged). Dashboard version string and `kol_*` preferred columns aligned. Fresh 2026 research (SentiSense/Adanos MCP sentiment, Rhea-AI impact scoring, ChatGPT for Financial Services, NorrisAI AlphaLens, CFTC COT crowding, FDA/PDUFA calendars, ADR basis, labor CBA, ADS-B exec travel). Added five new roadmap items: FDA / Clinical-Trial Milestone Velocity; CFTC COT Speculative Positioning; Labor-Action / CBA Expiry; Dual-Listed ADR / Ordinary Basis; Corporate-Jet / Executive-Travel Nowcast.
* **v2.40.0 (2026-09-23)** : Fully implemented **Key Opinion Leader (KOL) / Influencer Narrative Amplification Detector** (`sie/kol_amplification.py`). Wired through analyzer (`include_kol_amplification`), CLI (`--no-kol-amplification`), config (`kol_amplification:`), Streamlit preferred columns (`kol_score`, `kol_cascade`, `kol_amp_ratio`, `kol_auth`, `kol_boost`, `kol_reason`). Deterministic synthetic proxy. Removed from FUTURE-IMPROVEMENTS.md High Priority.
* **v2.39.2 (2026-09-23)** : Full [AUTONOMOUS RESEARCH & EVOLUTION CYCLE](AUTONOMOUS-RESEARCH-EVOLUTION-CYCLE.md). Exhaustive wiring audit of every open FUTURE-IMPROVEMENTS item against `sie/` modules found **no remaining roadmap item fully implemented** at that cut. Added five new overlays (index reconstitution, listed earnings event-contracts, working-capital DSO/DIO, SaaS status-page incidents, CAT-bond / ROL).
* **v2.39.1 (2026-09-22)** : Full autonomous research cycle. Added TRACE, primary credit issuance, target-specific stance, alt-data provenance, Rule 606 overlays.
* **v2.39.0 (2026-09-22)** : Fully implemented **Whisper Number / Pre-Earnings Alt-Data Beat Probability Overlay** (`sie/whisper_number.py`).
* **v2.38.1 (2026-09-22)** : Autonomous research cycle. Confirmed **News-Source Authority** fully wired. Added news materiality, ATM dilution, guidance-vs-delivered, activist velocity, cross-language lag.
* **v2.38.0 (2026-09-21)** : Fully implemented **News-Source Authority / Reliability Weighted Narrative Score** (`sie/news_authority.py`).
* **v2.37.0 (2026-09-20)** : Fully implemented **Earnings Call Transcript Real-Time Sentiment & Guidance Drift Detector** (`sie/earnings_call.py`).
* **v2.36.0 (2026-09-19)** : Fully implemented **Corporate Credit Spread / CDS Momentum Overlay** (`sie/credit_spread.py`).
* **v2.35.0 (2026-09-18)** : Fully implemented **Social Trading Action Intent Classifier** (`sie/social_intent.py`).
* **v2.34.0 (2026-09-18)** : Dealer GEX & Pin-Risk Overlay fully wired.

## Disclaimer

This is an educational research tool. Not financial advice. See DISCLAIMER.md.

v2.40.1

## Flagship integration

This project remains independently usable and is not deprecated. Its capabilities are also consumed by [SignalForge](https://github.com/Stijnman/SignalForge), where they are integrated with complementary repositories behind shared platform contracts. This repository remains the source of truth for its component-specific implementation.
