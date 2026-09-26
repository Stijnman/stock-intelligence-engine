# Stock Intelligence Engine

**Connect market narratives to your watchlist.**  
**Confirm with technicals.**  
**Explain every signal.**

**v2.43.0** — September 2026 · Unusual Options Sweep vs Block Confirmation (fully wired) + Rule 10b5-1 / Buyback Authorization vs Execution (fully wired) + ETF Creation / Redemption & AP Flow (fully wired) + KOL / Influencer Narrative Amplification (fully wired) + Whisper Number / Pre-Earnings Alt-Data Beat Probability (fully wired) + News-Source Authority Weighted Narrative + Earnings Call Transcript Sentiment & Guidance Drift Overlay + Corporate Credit Spread / CDS Momentum Overlay + Social Trading Action Intent Classifier + Dealer GEX & Pin-Risk Overlay + Company Digital Footprint Momentum + Patent & IP Filing Momentum + Analyst Estimate Revision Velocity + Cross-Ticker Narrative Contagion + Borrow Fee & Short Squeeze Risk + Consumer Spend Nowcasting + Authenticity-Filtered Social Narrative Velocity + Supply-Chain CapEx + FINRA Short + Attention Momentum + Regime Adaptive Weighting + Confidence Calibration + Streamlit Fragment Live Dashboard + Thesis + Brief + Honesty + Hiring + EDGAR + 0DTE + IV + Dark Pool + Realtime + Congressional + 13F + Prediction Markets + Insider + Narrative Velocity + Backtesting

## Features

* Real-time signals with narrative intelligence
* **Unusual Options Sweep vs Block Confirmation** — Distinguishes aggressive sweep prints from passive blocks and scores confirmation vs fade against 0DTE / IV / GEX. Soft boost on sweep-led call tape confirming narrative; caution on passive blocks into social heat. Fully integrated into analyzer, CLI (`--no-unusual-options`) and dashboard (`uopt_*` columns).
* **Rule 10b5-1 / Buyback Authorization vs Execution** — Clusters scheduled 10b5-1 plan adoptions/amendments and compares announced buyback authorizations against actual repurchase cadence. Soft boost when execution runs ahead of authorization with supportive narrative; caution on stalled buybacks. Fully integrated into analyzer, CLI (`--no-buyback-10b51`) and dashboard (`bb_*` columns).
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

* **v2.43.0 (2026-09-26)** : Fully implemented **Unusual Options Sweep vs Block Confirmation Overlay** (`sie/unusual_options.py`). Wired through analyzer (`include_unusual_options`), CLI (`--no-unusual-options`), config (`unusual_options:`), Streamlit preferred columns (`uopt_sweep_score`, `uopt_block_ratio`, `uopt_call_put`, `uopt_premium_usd_m`, `uopt_boost`, `uopt_reason`). Deterministic synthetic proxy. Removed from FUTURE-IMPROVEMENTS.md High Priority.
* **v2.42.1 (2026-09-26)** : Autonomous research & evolution cycle against `main` @ b85ac9a. Removed leftover checked **Rule 10b5-1 / Buyback** item from FUTURE-IMPROVEMENTS.md (shipped in v2.42.0). Added five 2026 research items: tariff/trade-policy exposure (High), AI token-cost / inference-price deflation (High), corporate aviation / executive flight-pattern (High), 8-K Item 1.05 cyber incident velocity (Medium), class-action / MDL filing velocity (Long-Term). Docs, CLI and dashboard aligned to 2.42.1.
* **v2.42.0 (2026-09-25)** : Fully implemented **Rule 10b5-1 / Buyback Authorization vs Execution Overlay** (`sie/buyback_10b51.py`). Wired through analyzer (`include_buyback_10b51`), CLI (`--no-buyback-10b51`), config (`buyback_10b51:`), Streamlit preferred columns (`bb_util`, `bb_plan_delta`, `bb_auth_usd_bn`, `bb_exec_pace`, `bb_boost`, `bb_reason`). Deterministic synthetic proxy. Removed from FUTURE-IMPROVEMENTS.md High Priority.
* **v2.41.1 (2026-09-25)** : Autonomous research & evolution cycle against `main` @ 7e7df35. Code audit confirmed **ETF Creation / Redemption & AP Flow** is fully wired (`sie/etf_flow.py`, analyzer `include_etf_flow`, CLI `--no-etf-flow`, config `etf_flow:`). Removed from FUTURE-IMPROVEMENTS.md High Priority (implementation shipped in v2.41.0; roadmap and dashboard were lagging). Aligned `app.py` `__version__` and preferred columns (`etf_*`). Added five 2026 research items to the roadmap (vocal-affect earnings audio, 13F amendment velocity, hyperscaler interconnection queue, dealer inventory vs GEX divergence, FOMC vocal-stress).
* **v2.41.0 (2026-09-24)** : Fully implemented **ETF Creation / Redemption & Authorized-Participant Flow Overlay** (`sie/etf_flow.py`). Wired through analyzer (`include_etf_flow`), CLI (`--no-etf-flow`), config (`etf_flow:`), Streamlit preferred columns (`etf_flow_score`, `etf_prem_disc`, `etf_create_streak`, `etf_theme`, `etf_boost`, `etf_reason`). Deterministic synthetic proxy. Removed from FUTURE-IMPROVEMENTS.md High Priority.
* **v2.40.1 (2026-09-24)** : Autonomous research & evolution cycle. Confirmed KOL amplification fully wired.
* **v2.40.0 (2026-09-23)** : Fully implemented **Key Opinion Leader (KOL) / Influencer Narrative Amplification Detector** (`sie/kol_amplification.py`).

## Disclaimer

This is an educational research tool. Not financial advice. See DISCLAIMER.md.

v2.43.0

## Flagship integration

This project remains independently usable and is not deprecated. Its capabilities are also consumed by [SignalForge](https://github.com/Stijnman/SignalForge), where they are integrated with complementary repositories behind shared platform contracts. This repository remains the source of truth for its component-specific implementation.
