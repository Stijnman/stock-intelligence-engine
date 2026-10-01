# Future Improvements — Stock Intelligence Engine

**Last updated:** 2026-10-01  
**Current version baseline:** v2.47.1

This file is the single source of truth for the open roadmap.  
Items that are fully implemented and wired (analyzer + CLI + config + dashboard) are removed here and recorded in CHANGELOG.md + README Recent Edits.

---

## High Priority

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

- [ ] **Implied-vs-Realized News Impact Residual Overlay**. Preferred columns: `ivr_pred`, `ivr_realized`, `ivr_residual`, `ivr_boost`, `ivr_reason`.

- [ ] **Corporate Treasury Stablecoin / On-Chain Cash Overlay**. Preferred columns: `tsc_onchain_usd`, `tsc_share_cash`, `tsc_boost`, `tsc_reason`.

- [ ] **Port / AIS Shipping Congestion & Lead-Time Overlay**. Preferred columns: `ais_dwell_hrs`, `ais_lead_delta`, `ais_boost`, `ais_reason`.

- [ ] **SEC Form 144 Planned-Sale Calendar Overlay**. Preferred columns: `f144_shares`, `f144_days_to_window`, `f144_boost`, `f144_reason`.

- [ ] **Supplier Invoice / Freight Bill-of-Lading Nowcast Overlay**. Preferred columns: `bol_volume_delta`, `bol_lead_days`, `bol_boost`, `bol_reason`.

- [ ] **Activist 13D/13G Accumulation Velocity Overlay**. Preferred columns: `act_stake_delta`, `act_filer_count`, `act_boost`, `act_reason`.

- [ ] **Realized AI-Token Consumption Factor Beta Overlay**. Preferred columns: `aib_beta`, `aib_token_mom`, `aib_boost`, `aib_reason`.

- [ ] **Multi-Platform Brand Audience / Short-Form Engagement Velocity Overlay**. Preferred columns: `aud_follower_delta`, `aud_shortform_vel`, `aud_boost`, `aud_reason`.

- [ ] **Cloud Committed-Use / Reserved-Instance Utilization Overlay**. Preferred columns: `ccu_util`, `ccu_discount_bps`, `ccu_boost`, `ccu_reason`.

- [ ] **Payment-Network Authorization Decline & Chargeback Velocity Overlay**. Preferred columns: `pay_auth_decline`, `pay_chargeback_vel`, `pay_boost`, `pay_reason`.

- [ ] **Critical-Mineral / Rare-Earth Export-Quota Exposure Overlay**. Preferred columns: `crm_quota_tight`, `crm_rev_share`, `crm_boost`, `crm_reason`.

---

## Medium Priority

- [ ] **Form 8-K Item 1.05 Cybersecurity Incident Velocity Overlay**. Preferred columns: `cyb_days_since`, `cyb_amend_vel`, `cyb_boost`, `cyb_reason`.

- [ ] **Long-form Newsletter / Substack Narrative Lead-Lag Overlay**. Preferred columns: `nl_lead_days`, `nl_authority`, `nl_boost`, `nl_reason`.

- [ ] **Guidance-vs-Delivery Promise Tracking Overlay**. Preferred columns: `gvd_open_promises`, `gvd_hit_rate`, `gvd_boost`, `gvd_reason`.

- [ ] **Board Interlock / Director-Network Centrality Overlay**. Preferred columns: `brd_interlock_n`, `brd_centrality`, `brd_boost`, `brd_reason`.

- [ ] **Thematic Narrative Taxonomy Exposure Overlay**. Preferred columns: `thm_pillar`, `thm_score`, `thm_boost`, `thm_reason`.

- [ ] **Point-in-Time Filing Freshness / Agent-Index Latency Overlay**. Preferred columns: `ptf_sec_lag_s`, `ptf_extract_lag_s`, `ptf_boost`, `ptf_reason`.

- [ ] **Expert-Call / Primary-Research Tone Overlay**. Preferred columns: `exp_tone`, `exp_revision_delta`, `exp_boost`, `exp_reason`.

---

## Long-Term / Nice-to-Have

- [ ] **Class-Action / Multidistrict Litigation Filing Velocity Overlay**. Preferred columns: `lit_new_filings`, `lit_mdl_flag`, `lit_boost`, `lit_reason`.

- [ ] **Compute Waste-Heat / District-Heating Monetization Overlay**. Preferred columns: `heat_mw_offtake`, `heat_contract_flag`, `heat_boost`, `heat_reason`.

- [ ] **Parking-Lot / Satellite Occupancy Nowcast Overlay**. Preferred columns: `sat_occ_delta`, `sat_sample_n`, `sat_boost`, `sat_reason`.

- [ ] **Satellite Methane / Flare Intensity Energy Overlay**. Preferred columns: `ch4_intensity`, `flare_delta`, `ch4_boost`, `ch4_reason`.

- [ ] **Data-Center Interconnection Queue / Power-Availability Overlay**. Preferred columns: `dcq_mw_queued`, `dcq_wait_months`, `dcq_boost`, `dcq_reason`.

- [ ] **EU ETS / Carbon-Allowance Cost Pass-Through Overlay**. Preferred columns: `ets_cost_share`, `ets_price_mom`, `ets_boost`, `ets_reason`.
