# Stock Intelligence Engine

**Connect market narratives to your watchlist.**  
**Confirm with technicals.**  
**Explain every signal.**

**v2.58.0** — October 2026 · Agentic Brokerage Account Flow & Penetration Overlay (fully wired) + Index Reconstitution & Forced Passive-Flow Overlay (fully wired) + Rule 606 Retail Options Routing Overlay (fully wired) + Alternative-Data Provenance Overlay (fully wired) + · Secondary Offering / ATM Dilution Velocity Overlay (fully wired) +  Cross-Venue Tokenized-Share Basis / On-Chain Equity Premium Overlay (fully wired through analyzer + CLI + dashboard) + Job-Posting Skill-Mix + Retail Brokerage Order-Flow + App-Store Review Sentiment + Employee Outlook + Unusual Options + Rule 10b5-1 / Buyback + ETF AP Flow + KOL + Whisper + News Authority + Earnings Call + CDS + Social Intent + GEX + Digital Footprint + Patent + Estimate Revision + Contagion + Borrow Fee + Consumer Spend + Authenticity + Supply-Chain + FINRA Short + Attention + Regime + Confidence + Thesis + Brief + Honesty + Hiring + EDGAR + 0DTE + IV + Dark Pool + Realtime + Congressional + 13F + Prediction Markets + Insider + Narrative Velocity + Backtesting

## Features

* Real-time signals with narrative intelligence
* **Agentic Brokerage Account Flow & Penetration Overlay** — Scores share of order flow from agentic / autonomous brokerage accounts and tool/API intensity. Soft boost when high agentic flow + elevated tool intensity confirms the narrative; caution when agentic accounts fade while narrative heat remains elevated. Fully integrated into analyzer (`include_agentic_flow`), CLI (`--no-agentic-flow`) and dashboard (`agt_*` columns).
* **Alternative-Data Provenance & AI-Synthetic Contamination Confidence Overlay** — Scores source-chain provenance and independent cross-check agreement. Soft boost when attested alt-data confirms a narrative; caution when narrative heat sits on synthetic or uncorroborated prints. Fully integrated into analyzer (`include_alt_data_provenance`), CLI (`--no-alt-data-provenance`) and dashboard (`adp_*` columns).
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

* **v2.58.0 (2026-10-10)** : Agentic Brokerage Account Flow & Penetration Overlay (`sie/agentic_flow.py`). Preferred columns: `agt_flow_share`, `agt_tool_intensity`, `agt_boost`, `agt_reason`. Soft boost when high agentic account flow share coincides with elevated tool intensity into a confirming narrative; caution when agentic accounts fade or tool intensity collapses while narrative heat remains elevated. Synthetic proxy (live brokerage agent-flow feed reserved). Wired through analyzer (`include_agentic_flow`), CLI (`--no-agentic-flow`), config (`agentic_flow:`), and Streamlit preferred columns. Removed from FUTURE-IMPROVEMENTS.md High Priority.
* **v2.57.1 (2026-10-10)** : Autonomous research & evolution cycle. Audit of main found no FUTURE-IMPROVEMENTS item fully wired since v2.57.0 earnings event-contract overlay. Nothing removed from the roadmap. New roadmap only: Agentic brokerage account flow & penetration, domain-tuned financial LLM vs general LLM sentiment gap, listed event-contract book depth vs offshore prediction-market basis, Reddit-ICE market insights conversation velocity, MCP data-feed freshness & attestation. Version bump across package, CLI, dashboard and docs.
* **v2.57.0 (2026-10-09)** : Listed Earnings Event-Contract vs Whisper / Street Divergence Overlay (`sie/earnings_event_contract.py`). Preferred columns: `eec_implied_beat`, `eec_whisper_gap`, `eec_boost`, `eec_reason`. Soft boost when a listed earnings contract prices a beat above whisper into a confirming narrative; caution when the contract implies a miss while narrative heat is still positive. Synthetic proxy (live exchange event-contract book reserved). Distinct from the whisper-number overlay and prediction-market ETF overlap. Wired through analyzer (`include_earnings_event_contract`), CLI (`--no-earnings-event-contract`), config (`earnings_event_contract:`), and Streamlit preferred columns. Removed from FUTURE-IMPROVEMENTS.md High Priority.

## Disclaimer

This is an educational research tool. Not financial advice. See DISCLAIMER.md.

v2.58.0

## Flagship integration

This project remains independently usable and is not deprecated. Its capabilities are also consumed by [SignalForge](https://github.com/Stijnman/SignalForge), where they are integrated with complementary repositories behind shared platform contracts. This repository remains the source of truth for its component-specific implementation.


![Agentic Flow Overlay](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/agentic_flow_v2.58.0.svg)
