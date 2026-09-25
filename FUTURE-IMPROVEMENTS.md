# Future Improvements — Stock Intelligence Engine

**Last updated:** 2026-09-25  
**Current version baseline:** v2.42.0

This file is the single source of truth for the open roadmap.  
Items that are fully implemented and wired (analyzer + CLI + config + dashboard) are removed here and recorded in CHANGELOG.md + README Recent Edits.

---

## High Priority

- [x] **Rule 10b5-1 / Buyback Authorization vs Execution Overlay** — shipped in v2.42.0 (2026-09-25). See CHANGELOG / commit on main.

- [ ] **Unusual Options Sweep vs Block Confirmation Overlay**. Distinguish aggressive sweep prints from passive blocks on the options tape and score confirmation vs fade against existing 0DTE / IV / GEX layers. Preferred columns: `uopt_sweep_score`, `uopt_block_ratio`, `uopt_boost`, `uopt_reason`. Synthetic proxy acceptable offline.

- [ ] **Employee Outlook / Glassdoor Business Sentiment Overlay**. Preferred columns: `eo_outlook`, `eo_ceo`, `eo_boost`, `eo_reason`.

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

---

## Medium Priority

See prior roadmap items (ESG narrative, multi-agent thesis debate, long-form velocity, retail vs institutional options flow, expert-network aspects, MCP tool server, GPU/HBM lead-times, 10-K risk-factor delta, FOMC surprise, supplier-customer surprise graph, earnings calendar distance-decay, macro surprise residual, investor-day slide NLP, foot-traffic vs digital demand, SKU promo intensity, multi-quarter guidance-vs-delivered, activist/short-seller velocity, working-capital DSO-DIO, status-page incidents, labor-action expiry, ADR basis, hyperscaler interconnection queue, dealer inventory vs GEX).

---

## Long-Term / Nice-to-Have

See prior roadmap items (event-driven webhooks, AIS/freight, data-center power, satellite night-lights, SAR activity, on-chain liquidity pulse, SEC comment letters, climate exposure, auditor-change / going-concern language).
