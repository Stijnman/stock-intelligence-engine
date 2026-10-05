# Stock Intelligence Engine

**Connect market narratives to your watchlist.**  
**Confirm with technicals.**  
**Explain every signal.**

**v2.53.0** — October 2026 · Secondary Offering / ATM Dilution Velocity Overlay (fully wired) +  Cross-Venue Tokenized-Share Basis / On-Chain Equity Premium Overlay (fully wired through analyzer + CLI + dashboard) + Job-Posting Skill-Mix + Retail Brokerage Order-Flow + App-Store Review Sentiment + Employee Outlook + Unusual Options + Rule 10b5-1 / Buyback + ETF AP Flow + KOL + Whisper + News Authority + Earnings Call + CDS + Social Intent + GEX + Digital Footprint + Patent + Estimate Revision + Contagion + Borrow Fee + Consumer Spend + Authenticity + Supply-Chain + FINRA Short + Attention + Regime + Confidence + Thesis + Brief + Honesty + Hiring + EDGAR + 0DTE + IV + Dark Pool + Realtime + Congressional + 13F + Prediction Markets + Insider + Narrative Velocity + Backtesting

## Features

* Real-time signals with narrative intelligence
* **Target-Specific Financial Stance & Narrative Specificity Overlay** — Scores management/street stance, numeric target specificity, and the prepared-remarks vs Q&A gap. Soft boost when constructive numeric targets hold through Q&A into a confirming narrative; caution when narrative heat arrives without specificity or with a wide Q&A gap. Fully integrated into analyzer (`include_target_stance`), CLI (`--no-target-stance`) and dashboard (`tsn_*` columns).
* **Primary Credit Issuance / New-Issue Concession & Supply Pressure Overlay** — Scores new-issue concession (bps) and primary calendar supply. Soft boost when concession is tight and the book is scarce into a confirming narrative; caution when a wide concession meets crowded primary supply. Fully integrated into analyzer (`include_primary_credit`), CLI (`--no-primary-credit`) and dashboard (`pci_*` columns).
* **Secondary Offering / ATM Dilution Velocity Overlay** — Scores ATM / secondary issuance velocity and share-count delta. Soft boost when issuance is paused into a confirming narrative; caution when ATM velocity accelerates. Fully integrated into analyzer (`include_dilution_atm`), CLI (`--no-dilution-atm`) and dashboard (`dil_*` columns).
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

* **v2.53.0 (2026-10-05)** : Fully implemented **Target-Specific Financial Stance & Narrative Specificity Overlay** (`sie/target_stance.py`). Wired through analyzer (`include_target_stance`), CLI (`--no-target-stance`), config (`target_stance:`), Streamlit preferred columns (`tsn_stance`, `tsn_specificity`, `tsn_qa_gap`, `tsn_boost`, `tsn_reason`). Deterministic synthetic proxy (live transcript parser hook reserved). Removed from FUTURE-IMPROVEMENTS.md High Priority. Commit: https://github.com/Stijnman/stock-intelligence-engine/commit/f03614fd13a9078c076042def5e92e446d9c90be.

![Target-specific financial stance overlay](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/target_stance_v2.53.0.svg)
* **v2.52.1 (2026-10-05)** : Autonomous research & evolution cycle. Audit of `main` @ 16a20ca found no FUTURE-IMPROVEMENTS item fully wired since v2.52.0 primary-credit overlay. Roadmap additions only: single-stock levered ETF rebalance pressure, security-based swap / equity TRS disclosure, search-vs-download divergence, post-quiet-period initiation cluster, contracted PPA vs spot power. Version bump across package, CLI, dashboard and docs.
* **v2.52.0 (2026-10-04)** : Fully implemented **Primary Credit Issuance / New-Issue Concession & Supply Pressure Overlay** (`sie/primary_credit.py`). Wired through analyzer (`include_primary_credit`), CLI (`--no-primary-credit`), config (`primary_credit:`), Streamlit preferred columns (`pci_concession_bp`, `pci_supply_score`, `pci_boost`, `pci_reason`). Deterministic synthetic proxy (live syndicate / new-issue TRACE hook reserved). Removed from FUTURE-IMPROVEMENTS.md High Priority. Commit: https://github.com/Stijnman/stock-intelligence-engine/commit/d147faa739beb02203c95e3885a96a718196ffda.

![Primary credit issuance overlay](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/primary_credit_v2.52.0.svg)
* **v2.51.1 (2026-10-04)** : Autonomous research & evolution cycle. Audit of `main` @ 995911f found no FUTURE-IMPROVEMENTS item fully wired since v2.51.0 TRACE overlay. Roadmap additions only: NHTSA/CPSC recall velocity, overnight/extended-hours residual, issuer MNPI blackout calendar, customer-concentration drift, autocallable barrier proximity. Version bump across package, CLI, dashboard and docs.
* **v2.51.0 (2026-10-03)** : Fully implemented **TRACE Corporate-Bond Customer-Flow & Liquidity Shock Overlay** (`sie/trace_flow.py`). Wired through analyzer (`include_trace_flow`), CLI (`--no-trace-flow`), config (`trace_flow:`), Streamlit preferred columns (`trace_customer_flow`, `trace_liq_score`, `trace_boost`, `trace_reason`). Deterministic synthetic proxy (live FINRA TRACE hook reserved). Removed from FUTURE-IMPROVEMENTS.md High Priority. Commit: https://github.com/Stijnman/stock-intelligence-engine/commit/f03614fd13a9078c076042def5e92e446d9c90be.

![TRACE customer-flow overlay](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/trace_flow_v2.51.0.svg)
* **v2.50.0 (2026-10-02)** : Fully implemented **Secondary Offering / ATM Dilution Velocity Overlay** (`sie/dilution_atm.py`). Wired through analyzer (`include_dilution_atm`), CLI (`--no-dilution-atm`), config (`dilution_atm:`), Streamlit preferred columns (`dil_atm_velocity`, `dil_share_delta`, `dil_boost`, `dil_reason`). Deterministic synthetic proxy. Removed from FUTURE-IMPROVEMENTS.md High Priority. Commit: https://github.com/Stijnman/stock-intelligence-engine/commit/f03614fd13a9078c076042def5e92e446d9c90be.

![ATM dilution overlay](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/dilution_atm_v2.50.0.svg)
* **v2.49.0 (2026-10-02)** : Fully implemented **News Materiality / Predicted Next-Session Impact Score Overlay** (`sie/news_materiality.py`). Wired through analyzer (`include_news_materiality`), CLI (`--no-news-materiality`), config (`news_materiality:`), Streamlit preferred columns (`nimp_score`, `nimp_vol_bucket`, `nimp_boost`, `nimp_reason`). Deterministic synthetic proxy. Removed from FUTURE-IMPROVEMENTS.md High Priority. Commit: https://github.com/Stijnman/stock-intelligence-engine/commit/f03614fd13a9078c076042def5e92e446d9c90be.

![News materiality overlay](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/news_materiality_overlay.svg)
* **v2.48.1 (2026-10-02)** : Autonomous research & evolution cycle. Audit of `main` @ b0847bc found no FUTURE-IMPROVEMENTS item fully wired since v2.48.0. Roadmap additions only: government-contract obligation velocity, ADR/dual-listing premium, options skew term-structure, weather degree-day demand shock, private-credit / BDC NAV mark-lag. Version bump across package, CLI, dashboard and docs.
* **v2.48.0 (2026-10-01)** : Fully implemented **Cross-Venue Tokenized-Share Basis / On-Chain Equity Premium Overlay** (`sie/tokenized_basis.py`). Wired through analyzer (`include_tokenized_basis`), CLI (`--no-tokenized-basis`), config (`tokenized_basis:`), Streamlit preferred columns (`tok_basis_bps`, `tok_venue_liq`, `tok_boost`, `tok_reason`). Deterministic synthetic proxy. Removed from FUTURE-IMPROVEMENTS.md High Priority. Commit: https://github.com/Stijnman/stock-intelligence-engine/commit/f03614fd13a9078c076042def5e92e446d9c90be.
* **v2.47.1 (2026-10-01)** : Autonomous research & evolution cycle. Hiring skill-mix wiring completed.
* **v2.47.0 (2026-09-30)** : Job-Posting Skill-Mix & Posted-Compensation Inflation Overlay.
* **v2.46.0 (2026-09-29)** : Retail Brokerage Order-Flow Imbalance Overlay.
* **v2.45.0 (2026-09-28)** : App-Store Review Sentiment & Complaint Velocity Overlay.

## Disclaimer

This is an educational research tool. Not financial advice. See DISCLAIMER.md.

v2.53.0

## Flagship integration

This project remains independently usable and is not deprecated. Its capabilities are also consumed by [SignalForge](https://github.com/Stijnman/SignalForge), where they are integrated with complementary repositories behind shared platform contracts. This repository remains the source of truth for its component-specific implementation.
