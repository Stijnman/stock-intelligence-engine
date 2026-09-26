# Future Improvements — Stock Intelligence Engine

**Last updated:** 2026-09-26  
**Current version baseline:** v2.43.0

This file is the single source of truth for the open roadmap.  
Items that are fully implemented and wired (analyzer + CLI + config + dashboard) are removed here and recorded in CHANGELOG.md + README Recent Edits.

---

## High Priority

- [x] **Unusual Options Sweep vs Block Confirmation Overlay** — DONE 2026-09-26 in v2.43.0 (`sie/unusual_options.py`, CLI `--no-unusual-options`, dashboard `uopt_*`). See CHANGELOG.

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

- [ ] **Tariff / Trade-Policy Exposure Overlay**. Scores issuer revenue and COGS exposure to announced or rumored tariff schedules, Section 301/232 actions, and customs-unit value shocks. Soft boost when narrative heat is high but trade-policy exposure is low or declining; caution when policy risk is rising into a crowded theme. Preferred columns: `trf_rev_share`, `trf_cogs_share`, `trf_shock`, `trf_boost`, `trf_reason`. Synthetic proxy acceptable offline.

- [ ] **AI Token-Cost / Inference-Price Deflation Overlay**. Tracks published API token prices, open-weight serving costs, and hyperscaler inference list-price changes as a margin and demand pulse for semis, networking, and AI software names. Soft boost when falling token costs expand usage faster than ASP compression; caution when price wars outrun volume. Preferred columns: `tokc_price_idx`, `tokc_deflation_30d`, `tokc_usage_proxy`, `tokc_boost`, `tokc_reason`.

- [ ] **Corporate Aviation / Executive Flight-Pattern Overlay**. Uses public ADS-B / corporate-jet tail mappings as a leading activity proxy around plants, customer sites, M&A destinations, and capital-markets hubs. Soft boost on rising multi-site operational flight intensity confirming hiring/CapEx narrative; caution on unexplained hub-to-hub banker-route spikes into quiet periods. Preferred columns: `jet_ops_intensity`, `jet_hub_share`, `jet_boost`, `jet_reason`.

---

## Medium Priority

See prior roadmap items (ESG narrative, multi-agent thesis debate, long-form velocity, retail vs institutional options flow, expert-network aspects, MCP tool server, GPU/HBM lead-times, 10-K risk-factor delta, FOMC surprise, supplier-customer surprise graph, earnings calendar distance-decay, macro surprise residual, investor-day slide NLP, foot-traffic vs digital demand, SKU promo intensity, multi-quarter guidance-vs-delivered, activist/short-seller velocity, working-capital DSO-DIO, status-page incidents, labor-action expiry, ADR basis, hyperscaler interconnection queue, dealer inventory vs GEX).

- [ ] **Form 8-K Item 1.05 Cybersecurity Incident Velocity Overlay**. Times material cyber 8-Ks, amendment cadence, and subsequent guidance/insurance language against social and credit-spread overlays. Soft caution on clustered Item 1.05 + widening CDS; fade isolated low-specificity filings. Preferred columns: `cyb_days_since`, `cyb_amend_vel`, `cyb_boost`, `cyb_reason`.

---

## Long-Term / Nice-to-Have

See prior roadmap items (event-driven webhooks, AIS/freight, data-center power, satellite night-lights, SAR activity, on-chain liquidity pulse, SEC comment letters, climate exposure, auditor-change / going-concern language).

- [ ] **Class-Action / Multidistrict Litigation Filing Velocity Overlay**. Tracks new securities and consumer class complaints, lead-plaintiff races, and MDL centralization as a legal-overhang score orthogonal to honesty/EDGAR layers. Preferred columns: `lit_new_filings`, `lit_mdl_flag`, `lit_boost`, `lit_reason`.
