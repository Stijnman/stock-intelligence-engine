# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.55.0] - 2026-10-07

### Added
* Commit: https://github.com/Stijnman/stock-intelligence-engine/commit/ac7d45952a624d4f29cf05a532342ea2040aa813
* **Rule 606 Retail Options Routing & Execution-Quality Overlay** (`sie/rule_606.py`).
  Preferred columns: `r606_concentration`, `r606_exec_quality`, `r606_boost`, `r606_reason`.
  Soft +1 when top-venue share is moderate and execution quality (price improvement / effective spread) confirms a narrative; caution when retail options flow is concentrated at one wholesaler with weak fills into social heat.
  Wired through analyzer (`include_rule_606`), CLI (`--no-rule-606`), config (`rule_606:`), Streamlit preferred columns.
  Deterministic synthetic proxy; live Rule 606 report parser reserved.
* Dashboard caption and preferred columns updated. Asset: `assets/rule_606_v2.55.0.svg`.

---

## [2.54.1] - 2026-10-07

### Changed
* Autonomous research & evolution cycle against `main` @ ce6d39c (v2.54.0).
* Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard) beyond the v2.54.0 alt-data provenance overlay. Nothing removed from the roadmap.
* Version strings synchronized to **2.54.1** across package, CLI, dashboard and docs.

### Added
* Roadmap only (not yet implemented):
  * **CFTC Mention-Market / Named-Speaker Event-Contract Manipulation Overlay** (High Priority) — `mmk_oi_share`, `mmk_manip_flag`, `mmk_boost`, `mmk_reason`.
  * **Tokenized NMS Venue (TSV) AMM Pool Premium Overlay** (High Priority) — `tsv_pool_premium_bps`, `tsv_lp_depth`, `tsv_boost`, `tsv_reason`.
  * **Prediction-Market ETF Event-Overlap Beta Overlay** (High Priority) — `pmetf_beta`, `pmetf_event_overlap`, `pmetf_boost`, `pmetf_reason`.
  * **XBRL Custom-Extension Tag Ratio Overlay** (Medium Priority) — `xbrl_ext_ratio`, `xbrl_new_tags`, `xbrl_boost`, `xbrl_reason`.
  * **Water-Rights / Basin Curtailment Exposure Overlay** (Long-Term) — `wtr_curtail_flag`, `wtr_rev_share`, `wtr_boost`, `wtr_reason`.

---

## [2.54.0] - 2026-10-06

### Added
* Commit: https://github.com/Stijnman/stock-intelligence-engine/commit/b4710b4ccee1bdf2bfa3ba5fc33f9b8f7d015e59
* **Alternative-Data Provenance & AI-Synthetic Contamination Confidence Overlay** (`sie/alt_data_provenance.py`).
  Preferred columns: `adp_provenance`, `adp_crosscheck`, `adp_boost`, `adp_reason`.
  Soft +1 when attested provenance and an independent cross-check confirm a narrative; caution when narrative heat arrives on synthetic or uncorroborated alt-data.
  Wired through analyzer (`include_alt_data_provenance`), CLI (`--no-alt-data-provenance`), config (`alt_data_provenance:`), Streamlit preferred columns.
  Deterministic synthetic proxy; live vendor-attestation hook reserved.
* Dashboard chart: `assets/alt_data_provenance_v2.54.0.svg`.
* Unit tests: `tests/test_alt_data_provenance.py`.

### Changed
* Removed the completed Alternative-Data Provenance item from FUTURE-IMPROVEMENTS.md High Priority.
* Version strings synchronized to **2.54.0**.

---

## [2.53.1] - 2026-10-06

### Changed
* Autonomous research & evolution cycle against `main` @ c4c3bc5 (v2.53.0).
* Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard) beyond the v2.53.0 target-stance overlay. Nothing removed from the roadmap.
* Version strings synchronized to **2.53.1** across package, CLI, dashboard and docs.

### Added
* Roadmap only (not yet implemented):
  * **SEC Staff Comment-Letter & Filing-Review Velocity Overlay** (High Priority) — `cmt_open_letters`, `cmt_days_open`, `cmt_boost`, `cmt_reason`.
  * **Rule 10b-18 Daily Volume-Cap Proximity Overlay** (High Priority) — `b18_cap_used`, `b18_days_left`, `b18_boost`, `b18_reason`.
  * **Treasury GC / Sponsored-Repo Funding-Stress Spillover Overlay** (High Priority) — `repo_gc_spread`, `repo_equity_beta`, `repo_boost`, `repo_reason`.
  * **Channel Inventory Days & Working-Capital Fill Overlay** (Medium Priority) — `inv_days`, `inv_fill_delta`, `inv_boost`, `inv_reason`.
  * **State Incentive Clawback & Jobs-Credit Exposure Overlay** (Long-Term) — `inc_clawback_usd`, `inc_jobs_gap`, `inc_boost`, `inc_reason`.

---

## [2.53.0] - 2026-10-05

### Added
* Commit: https://github.com/Stijnman/stock-intelligence-engine/commit/f03614fd13a9078c076042def5e92e446d9c90be
* **Target-Specific Financial Stance & Narrative Specificity Overlay** (`sie/target_stance.py`).
  Preferred columns: `tsn_stance`, `tsn_specificity`, `tsn_qa_gap`, `tsn_boost`, `tsn_reason`.
  Soft +1 when a constructive stance stays numerically specific through Q&A into a confirming narrative; caution when narrative heat arrives without target specificity or with a wide prepared-vs-Q&A gap.
  Wired through analyzer (`include_target_stance`), CLI (`--no-target-stance`), config (`target_stance:`), Streamlit preferred columns.
  Deterministic synthetic proxy; live transcript parser hook reserved.
* Dashboard chart: `assets/target_stance_v2.53.0.svg`.
* Unit tests: `tests/test_target_stance.py`.

### Changed
* Removed the completed item from FUTURE-IMPROVEMENTS.md High Priority.
* Version strings synchronized to **2.53.0**.

---

## [2.52.1] - 2026-10-05

### Changed
* Autonomous research & evolution cycle against `main` @ 16a20ca (v2.52.0).
* Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard) beyond the v2.52.0 primary-credit overlay. Nothing removed from the roadmap.
* Version strings synchronized to **2.52.1** across package, CLI, dashboard and docs.
* README footer version corrected from the stale v2.51.1 pin.

### Added
* Roadmap only (not yet implemented):
  * **Single-Stock / Levered ETF Rebalance Pressure Overlay** (High Priority) — `ssetf_lev_aum`, `ssetf_rebalance_usd`, `ssetf_boost`, `ssetf_reason`.
  * **Security-Based Swap / Equity TRS Large-Position Disclosure Overlay** (High Priority) — `sbs_notional`, `sbs_direction`, `sbs_boost`, `sbs_reason`.
  * **Search-Attention vs App-Download Divergence Overlay** (Medium Priority) — `sad_search_z`, `sad_download_z`, `sad_boost`, `sad_reason`.
  * **Post-Quiet-Period Initiation Cluster Overlay** (Medium Priority) — `pq_initiation_n`, `pq_bull_share`, `pq_boost`, `pq_reason`.
  * **Contracted Power-Purchase vs Spot Power Spread Overlay** (Long-Term) — `ppa_spread`, `ppa_tenor_mo`, `ppa_boost`, `ppa_reason`.

---

## [2.52.0] - 2026-10-04

### Added
* Commit: https://github.com/Stijnman/stock-intelligence-engine/commit/d147faa739beb02203c95e3885a96a718196ffda
* **Primary Credit Issuance / New-Issue Concession & Supply Pressure Overlay** (`sie/primary_credit.py`).
  Preferred columns: `pci_concession_bp`, `pci_supply_score`, `pci_boost`, `pci_reason`.
  Soft +1 when the new-issue concession is tight and primary supply is scarce into a confirming narrative; caution when a wide concession meets a crowded primary calendar.
  Wired through analyzer (`include_primary_credit`), CLI (`--no-primary-credit`), config (`primary_credit:`), Streamlit preferred columns.
  Deterministic synthetic proxy; live syndicate book / TRACE new-issue hook reserved.
* Dashboard chart: `assets/primary_credit_v2.52.0.svg`.
* Unit tests: `tests/test_primary_credit.py`.

### Changed
* Version bump to **2.52.0** across package, CLI, dashboard and docs.
* Removed the completed Primary Credit Issuance item from FUTURE-IMPROVEMENTS.md High Priority.

## [2.51.1] - 2026-10-04

### Changed
* Autonomous research & evolution cycle against `main` @ 995911f (v2.51.0).
* Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard) beyond the v2.51.0 TRACE customer-flow overlay. Nothing removed from the roadmap.
* Version strings synchronized to **2.51.1** across package, CLI, dashboard and docs.

### Added
* Roadmap only (not yet implemented):
  * **NHTSA / CPSC Recall & Complaint Velocity Overlay** (High Priority) — `rcl_recall_count`, `rcl_complaint_vel`, `rcl_boost`, `rcl_reason`.
  * **Overnight / Extended-Hours Return Residual Overlay** (High Priority) — `on_ext_return`, `on_cash_residual`, `on_boost`, `on_reason`.
  * **Issuer MNPI Blackout & Buyback Window Calendar Overlay** (High Priority) — `mnpi_blackout_flag`, `mnpi_days_to_window`, `mnpi_boost`, `mnpi_reason`.
  * **Customer Concentration / Top-Account Revenue Drift Overlay** (Medium Priority) — `ccn_top_share`, `ccn_drift`, `ccn_boost`, `ccn_reason`.
  * **Autocallable Barrier Proximity & Observation-Calendar Hedge Overlay** (Long-Term) — `acb_barrier_gap`, `acb_obs_days`, `acb_boost`, `acb_reason`.

---

## [2.51.0] - 2026-10-03

### Added
* **TRACE Corporate-Bond Customer-Flow & Liquidity Shock Overlay** (`sie/trace_flow.py`).
  Preferred columns: `trace_customer_flow`, `trace_liq_score`, `trace_boost`, `trace_reason`.
  Soft +1 when TRACE customer buying lands in a liquid print into a confirming narrative; caution when customer selling meets a liquidity shock.
  Wired through analyzer (`include_trace_flow`), CLI (`--no-trace-flow`), config (`trace_flow:`), Streamlit preferred columns.
  Deterministic synthetic proxy; live FINRA TRACE hook reserved.
* Dashboard chart: `assets/trace_flow_v2.51.0.svg`.
* Unit tests: `tests/test_trace_flow.py`.

### Changed
* Version bump to **2.51.0** across package, CLI, dashboard and docs.
* Removed the completed TRACE Corporate-Bond Customer-Flow item from FUTURE-IMPROVEMENTS.md High Priority.

## [2.50.1] - 2026-10-03

### Changed
* Autonomous research & evolution cycle against `main` @ 28864ab (v2.50.0).
* Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard) beyond the v2.50.0 ATM dilution overlay. Nothing removed from the roadmap.
* Version strings synchronized to **2.50.1** across package, CLI, dashboard and docs.

### Added
* Roadmap only (not yet implemented):
  * **Lock-up / Resale-Registration Expiry Calendar Overlay** (High Priority) — `lck_days_to_expiry`, `lck_shares_free`, `lck_boost`, `lck_reason`.
  * **Convertible, Warrant & PIPE Dilution Overhang Overlay** (High Priority) — `cvp_overhang_pct`, `cvp_conversion_gap`, `cvp_boost`, `cvp_reason`.
  * **Non-GAAP Bridge Drift / Adjusted-Earnings Quality Overlay** (Medium Priority) — `ngaap_bridge_bps`, `ngaap_addback_vel`, `ngaap_boost`, `ngaap_reason`.
  * **BNPL Delinquency & Consumer-Credit Spillover Overlay** (Medium Priority) — `bnpl_dq_rate`, `bnpl_spillover`, `bnpl_boost`, `bnpl_reason`.
  * **Podcast / Long-form Audio Mention Velocity Overlay** (Long-Term) — `pod_mention_vel`, `pod_authority`, `pod_boost`, `pod_reason`.

---

## [2.50.0] - 2026-10-02

### Added
* **Secondary Offering / ATM Dilution Velocity Overlay** (`sie/dilution_atm.py`).
  Preferred columns: `dil_atm_velocity`, `dil_share_delta`, `dil_boost`, `dil_reason`.
  Soft +1 when ATM issuance is paused and the share count is stable into a confirming narrative; caution when ATM velocity and share-count delta accelerate (secondary supply pressure).
  Wired through analyzer (`include_dilution_atm`), CLI (`--no-dilution-atm`), config (`dilution_atm:`), Streamlit preferred columns.
  Deterministic synthetic proxy; live EDGAR S-3 / 424B5 hook reserved.
* Dashboard chart: `assets/dilution_atm_v2.50.0.svg`.

### Changed
* Version bump to **2.50.0** across package, CLI, dashboard and docs.
* CLI parser sets `allow_abbrev=False` so prefixed flags do not collide.
* Removed the completed Secondary Offering / ATM Dilution item from FUTURE-IMPROVEMENTS.md High Priority.

---

## [2.49.0] - 2026-10-02

### Added
* **News Materiality / Predicted Next-Session Impact Score Overlay** (`sie/news_materiality.py`).
  Preferred columns: `nimp_score`, `nimp_vol_bucket`, `nimp_boost`, `nimp_reason`.
  Soft +1 when a high next-session impact score confirms a positive narrative with adequate authority; caution when a material adverse tape is likely.
  Wired through analyzer (`include_news_materiality`), CLI (`--no-news-materiality`), config (`news_materiality:`), Streamlit preferred columns.
  Deterministic synthetic proxy; live event-classifier / implied-move residual hook reserved.
* Dashboard chart: `assets/news_materiality_overlay.svg`.

### Changed
* Version bump to **2.49.0** across package, CLI, dashboard and docs.
* Removed the completed News Materiality item from FUTURE-IMPROVEMENTS.md High Priority.
* Config loader now merges `news_materiality`, `tokenized_basis`, and `hiring_skill_mix` blocks from `config.yaml`.

---

## [2.48.1] - 2026-10-02

### Changed
* Autonomous research & evolution cycle against `main` @ b0847bc (v2.48.0).
* Code audit: no FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard) beyond the v2.48.0 tokenized-basis overlay. Nothing removed from the roadmap.
* Version strings synchronized to **2.48.1** across package, CLI, dashboard and docs.

### Added
* Roadmap only (not yet implemented):
  * **Government Contract Award & Obligation Velocity Overlay** (High Priority) — `gov_obligation_delta`, `gov_award_count`, `gov_boost`, `gov_reason`.
  * **ADR / Dual-Listing Premium vs Local Close Overlay** (High Priority) — `adr_premium_bps`, `adr_fx_gap`, `adr_boost`, `adr_reason`.
  * **Options Skew Term-Structure & Risk-Reversal Dislocation Overlay** (High Priority) — `skew_rr_25d`, `skew_term_slope`, `skew_boost`, `skew_reason`.
  * **Weather / Degree-Day Demand Shock Overlay** (Medium Priority) — `wx_hdd_cdd_z`, `wx_demand_shock`, `wx_boost`, `wx_reason`.
  * **Private-Credit / BDC NAV Mark-Lag Overlay** (Long-Term) — `bdc_nav_lag`, `bdc_discount`, `bdc_boost`, `bdc_reason`.

---

## [2.48.0] - 2026-10-01

### Added
* **Cross-Venue Tokenized-Share Basis / On-Chain Equity Premium Overlay** (`sie/tokenized_basis.py`).
  Preferred columns: `tok_basis_bps`, `tok_venue_liq`, `tok_boost`, `tok_reason`.
  Soft +1 when a liquid tokenized wrapper trades rich vs the listed share into a hot narrative; caution when the wrapper trades at a deep discount on thin venue liquidity.
  Wired through analyzer (`include_tokenized_basis`), CLI (`--no-tokenized-basis`), config (`tokenized_basis:`), Streamlit preferred columns.
  Deterministic synthetic proxy with live Superstate / Backed / Dinari / Ondo hook reserved.
* Analyzer overlay dispatch table so new flags (`include_tokenized_basis`, `include_hiring_skill_mix`) flow through `run_report(**kwargs)`.

### Changed
* Version bump to **2.48.0** across package, CLI, dashboard and docs.
* Removed the completed Tokenized-Share Basis item from FUTURE-IMPROVEMENTS.md High Priority.

---

## [2.47.1] - 2026-10-01

### Changed
* Autonomous research & evolution cycle against `main` @ 5ba41fb.
* Version strings synchronized to **2.47.1** across package, CLI, dashboard and docs.

See git history for 2.47.0 and earlier releases.

*Educational research tool only — not financial advice.*
