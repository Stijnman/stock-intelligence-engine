# Future Improvements — Stock Intelligence Engine

**Last updated:** 2026-09-27  
**Current version baseline:** v2.44.0

This file is the single source of truth for the open roadmap.  
Items that are fully implemented and wired (analyzer + CLI + config + dashboard) are removed here and recorded in CHANGELOG.md + README Recent Edits.

---

## High Priority

- [ ] **App-Store Review Sentiment & Complaint Velocity Overlay**. Preferred columns: `asr_sentiment`, `asr_complaint_velocity`, `asr_boost`, `asr_reason`.

- [ ] **Retail Brokerage Order-Flow Imbalance Overlay**. Preferred columns: `rflow_imbalance`, `rflow_heat`, `rflow_boost`, `rflow_reason`.

- [ ] **Job-Posting Skill-Mix & Posted-Compensation Inflation Overlay**. Preferred columns: `hmix_senior_share`, `hmix_comp_delta`, `hmix_boost`, `hmix_reason`.

- [ ] **Cross-Venue Tokenized-Share Basis / On-Chain Equity Premium Overlay**. Preferred columns: `tok_basis_bps`, `tok_venue_liq`, `tok_boost`, `tok_reason`.

- [ ] **News Materiality / Predicted Next-Session Impact Score Overlay**. Preferred columns: `nimp_score`, `nimp_vol_bucket`, `nimp_boost`, `nimp_reason`.

- [ ] **Secondary Offering / ATM Dilution Velocity Overlay**. Preferred columns: `dil_atm_velocity`, `dil_share_delta`, `dil_boost`, `dil_reason`.

- [ ] **TRACE Corporate-Bond Customer-Flow & Liquidity Shock Overlay**. Preferred columns: `trace_customer_flow`, `trace_liq_score`, `trace_boost`, `trace_reason`.

- [ ] **Primary Credit Issuance / New-Issue Concession & Supply Pressure Overlay**. Preferred columns: `pci_concession_bp`, `pci_supply_score`, `pci_boost`, `pci_reason`.

- [ ] **Target-Specific Financial Stance & Narrative Specificity Overlay**. Preferred columns: `tsn_stance`, `tsn_specificity`, `tsn_qa_gap`, `tsn_boost`, `tsn_reason`.

- [ ] **Alternative-Data Provenance & AI-Synthetic Contamination Confidence Overlay**. Preferred columns: `adp_provenance`, `adp_crosscheck`, `adp_boost`, `adp_reason`.

- [ ] **Rule 606 Retail Options Routing & Execution-Quality Overlay**. Preferred columns: `r606_concentration`, `r606_exec_quality`, `r606_boost`, `r606_reason`.

- [ ] **Index Reconstitution & Forced Passive-Flow Overlay**. Preferred columns: `idx_event`, `idx_forced_usd`, `idx_boost`, `idx_reason`.

- [ ] **Listed Earnings Event-Contract vs Whisper / Street Divergence Overlay**. Preferred columns: `eec_implied_beat`, `eec_whisper_gap`, `eec_boost`, `eec_reason`.

- [ ] **FDA / Clinical-Trial Milestone & Protocol-Amendment Velocity Overlay**. Preferred columns: `fda_days_to_event`, `fda_amend_velocity`, `fda_boost`, `fda_reason`.

- [ ] **CFTC Commitment-of-Traders Speculative Positioning Overlay**. Preferred columns: `cot_net_spec`, `cot_crowd_pct`, `cot_boost`, `cot_reason`.

- [ ] **CEO / CFO Vocal-Affect & Earnings-Audio Hedge-Density Overlay**. Preferred columns: `va_affect`, `va_hedge_audio`, `va_boost`, `va_reason`.

- [ ] **13F Amendment / Confidential-Treatment & Late-Filer Velocity Overlay**. Preferred columns: `f13_amend_vel`, `f13_late_share`, `f13_boost`, `f13_reason`.

- [ ] **Tariff / Trade-Policy Exposure Overlay**. Preferred columns: `trf_rev_share`, `trf_cogs_share`, `trf_shock`, `trf_boost`, `trf_reason`.

- [ ] **AI Token-Cost / Inference-Price Deflation Overlay**. Preferred columns: `tokc_price_idx`, `tokc_deflation_30d`, `tokc_usage_proxy`, `tokc_boost`, `tokc_reason`.

- [ ] **Corporate Aviation / Executive Flight-Pattern Overlay**. Preferred columns: `jet_ops_intensity`, `jet_hub_share`, `jet_boost`, `jet_reason`.

- [ ] **NSCC / CNS Fail-to-Deliver & Settlement-Stress Overlay**. Preferred columns: `ftd_shares`, `ftd_days`, `ftd_boost`, `ftd_reason`.

- [ ] **Behind-the-Meter Flexible-Load / Grid-Curtailment Overlay**. Preferred columns: `grid_curtail_mw`, `grid_scarcity_hrs`, `grid_boost`, `grid_reason`.

- [ ] **LLM Street-vs-Machine Estimate Divergence Overlay**. Preferred columns: `llm_est_gap`, `llm_lead_days`, `llm_boost`, `llm_reason`.

---

## Medium Priority

- [ ] **Form 8-K Item 1.05 Cybersecurity Incident Velocity Overlay**. Preferred columns: `cyb_days_since`, `cyb_amend_vel`, `cyb_boost`, `cyb_reason`.

- [ ] **Long-form Newsletter / Substack Narrative Lead-Lag Overlay**. Preferred columns: `nl_lead_days`, `nl_authority`, `nl_boost`, `nl_reason`.

---

## Long-Term / Nice-to-Have

- [ ] **Class-Action / Multidistrict Litigation Filing Velocity Overlay**. Preferred columns: `lit_new_filings`, `lit_mdl_flag`, `lit_boost`, `lit_reason`.

- [ ] **Compute Waste-Heat / District-Heating Monetization Overlay**. Preferred columns: `heat_mw_offtake`, `heat_contract_flag`, `heat_boost`, `heat_reason`.
