# Stock Intelligence Engine

**Connect market narratives to your watchlist.**  
**Confirm with technicals.**  
**Explain every signal.**

**v2.49.0** — October 2026 · Cross-Venue Tokenized-Share Basis / On-Chain Equity Premium Overlay (fully wired through analyzer + CLI + dashboard) + Job-Posting Skill-Mix + Retail Brokerage Order-Flow + App-Store Review Sentiment + Employee Outlook + Unusual Options + Rule 10b5-1 / Buyback + ETF AP Flow + KOL + Whisper + News Authority + Earnings Call + CDS + Social Intent + GEX + Digital Footprint + Patent + Estimate Revision + Contagion + Borrow Fee + Consumer Spend + Authenticity + Supply-Chain + FINRA Short + Attention + Regime + Confidence + Thesis + Brief + Honesty + Hiring + EDGAR + 0DTE + IV + Dark Pool + Realtime + Congressional + 13F + Prediction Markets + Insider + Narrative Velocity + Backtesting

## Features

* Real-time signals with narrative intelligence
* **News Materiality / Predicted Next-Session Impact Score Overlay** — Scores expected next-session news impact and a volatility bucket (`quiet` / `elevated` / `high` / `extreme`). Soft boost when high materiality confirms the narrative; caution on a material adverse tape. Fully integrated into analyzer (`include_news_materiality`), CLI (`--no-news-materiality`) and dashboard (`nimp_*` columns).
* **Cross-Venue Tokenized-Share Basis / On-Chain Equity Premium Overlay** — Scores listed-vs-tokenized wrapper basis (bps) and venue liquidity. Soft boost when a liquid wrapper trades rich into a confirming narrative; caution on deep discounts with thin venue liquidity. Fully integrated into analyzer (`include_tokenized_basis`), CLI (`--no-tokenized-basis`) and dashboard (`tok_*` columns).
* **Job-Posting Skill-Mix & Posted-Compensation Inflation Overlay** — Fully integrated into analyzer (`include_hiring_skill_mix`), CLI (`--no-hiring-skill-mix`) and dashboard (`hmix_*` columns).
* **Retail Brokerage Order-Flow Imbalance Overlay** — Fully integrated into analyzer, CLI (`--no-retail-flow`) and dashboard (`rflow_*` columns).
* **App-Store Review Sentiment & Complaint Velocity** — Fully integrated into analyzer, CLI (`--no-app-store-reviews`) and dashboard (`asr_*` columns).

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env   # add any API keys
python stock_intelligence_engine.py
streamlit run app.py
```

See config.yaml for watchlist and overlay toggles.

## Recent Edits & Version History

* **v2.49.0 (2026-10-02)** : Fully implemented **News Materiality / Predicted Next-Session Impact Score Overlay** (`sie/news_materiality.py`). Wired through analyzer (`include_news_materiality`), CLI (`--no-news-materiality`), config (`news_materiality:`), Streamlit preferred columns (`nimp_score`, `nimp_vol_bucket`, `nimp_boost`, `nimp_reason`). Deterministic synthetic proxy. Removed from FUTURE-IMPROVEMENTS.md High Priority.

![News materiality overlay](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/news_materiality_overlay.svg)
* **v2.48.1 (2026-10-02)** : Autonomous research & evolution cycle. Audit of `main` @ b0847bc found no FUTURE-IMPROVEMENTS item fully wired since v2.48.0. Roadmap additions only: government-contract obligation velocity, ADR/dual-listing premium, options skew term-structure, weather degree-day demand shock, private-credit / BDC NAV mark-lag. Version bump across package, CLI, dashboard and docs.
* **v2.48.0 (2026-10-01)** : Fully implemented **Cross-Venue Tokenized-Share Basis / On-Chain Equity Premium Overlay** (`sie/tokenized_basis.py`). Wired through analyzer (`include_tokenized_basis`), CLI (`--no-tokenized-basis`), config (`tokenized_basis:`), Streamlit preferred columns (`tok_basis_bps`, `tok_venue_liq`, `tok_boost`, `tok_reason`). Deterministic synthetic proxy. Removed from FUTURE-IMPROVEMENTS.md High Priority.
* **v2.47.1 (2026-10-01)** : Autonomous research & evolution cycle. Hiring skill-mix wiring completed.
* **v2.47.0 (2026-09-30)** : Job-Posting Skill-Mix & Posted-Compensation Inflation Overlay.
* **v2.46.0 (2026-09-29)** : Retail Brokerage Order-Flow Imbalance Overlay.
* **v2.45.0 (2026-09-28)** : App-Store Review Sentiment & Complaint Velocity Overlay.

## Disclaimer

This is an educational research tool. Not financial advice. See DISCLAIMER.md.

v2.49.0

## Flagship integration

This project remains independently usable and is not deprecated. Its capabilities are also consumed by [SignalForge](https://github.com/Stijnman/SignalForge), where they are integrated with complementary repositories behind shared platform contracts. This repository remains the source of truth for its component-specific implementation.
