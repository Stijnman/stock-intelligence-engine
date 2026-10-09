# Future Improvements — Stock Intelligence Engine

**Last updated:** 2026-10-09  
**Current version baseline:** v2.56.1

**Audit 2026-10-09 (v2.56.1):** No open item below is present as a wired overlay (analyzer + CLI + config + dashboard) on `main` @ b5034313. Index reconstitution, Rule 606, alt-data provenance, target stance, primary credit, TRACE, ATM dilution, news materiality, and tokenized basis stay completed and off this list. Nothing removed this cycle.

**Completed 2026-10-08 (v2.56.0):** Index Reconstitution & Forced Passive-Flow Overlay — `sie/index_reconstitution.py`. Preferred columns shipped: `idx_event`, `idx_forced_usd`, `idx_boost`, `idx_reason`. Commit: https://github.com/Stijnman/stock-intelligence-engine/commit/76dd3af848a5126de874e83fb08fbc49690c3587.

**Audit 2026-10-08 (v2.55.1):** No open item below is present as a wired overlay (analyzer + CLI + config + dashboard) on `main` @ 4709c657. Rule 606, alt-data provenance, target stance, primary credit, TRACE, ATM dilution, news materiality, and tokenized basis stay completed and off this list. v2.54.1 roadmap items that were logged in CHANGELOG but missing from this file are restored at the bottom of their sections.

**Completed 2026-10-07 (v2.55.0):** Rule 606 Retail Options Routing & Execution-Quality Overlay — `sie/rule_606.py`. Preferred columns shipped: `r606_concentration`, `r606_exec_quality`, `r606_boost`, `r606_reason`. Commit: https://github.com/Stijnman/stock-intelligence-engine/commit/ac7d45952a624d4f29cf05a532342ea2040aa813.

This file is the single source of truth for the open roadmap.  
Items that are fully implemented and wired (analyzer + CLI + config + dashboard) are removed here and recorded in CHANGELOG.md + README Recent Edits.

**Completed 2026-10-01 (v2.48.0):** Cross-Venue Tokenized-Share Basis / On-Chain Equity Premium Overlay — `sie/tokenized_basis.py`.

**Completed 2026-10-02 (v2.49.0):** News Materiality / Predicted Next-Session Impact Score Overlay — `sie/news_materiality.py`. See CHANGELOG and the v2.49.0 commit on main.

**Completed 2026-10-02 (v2.50.0):** Secondary Offering / ATM Dilution Velocity Overlay — `sie/dilution_atm.py`.

**Audit 2026-10-03 (v2.50.1):** No open item below is present as a wired overlay. Tokenized basis, news materiality, and ATM dilution stay completed and off this list.

**Completed 2026-10-03 (v2.51.0):** TRACE Corporate-Bond Customer-Flow & Liquidity Shock Overlay — `sie/trace_flow.py`. See CHANGELOG and the v2.51.0 commit on main.

**Audit 2026-10-04 (v2.51.1):** No open item below is present as a wired overlay (analyzer + CLI + config + dashboard). TRACE, ATM dilution, news materiality, and tokenized basis stay completed and off this list.

**Completed 2026-10-04 (v2.52.0):** Primary Credit Issuance / New-Issue Concession & Supply Pressure Overlay — `sie/primary_credit.py`. Commit: https://github.com/Stijnman/stock-intelligence-engine/commit/d147faa739beb02203c95e3885a96a718196ffda. Preferred columns shipped: `pci_concession_bp`, `pci_supply_score`, `pci_boost`, `pci_reason`.

**Audit 2026-10-05 (v2.52.1):** No open item below is present as a wired overlay (analyzer + CLI + config + dashboard) on `main` @ 16a20ca. Primary credit, TRACE, ATM dilution, news materiality, and tokenized basis stay completed and off this list.

**Completed 2026-10-05 (v2.53.0):** Target-Specific Financial Stance & Narrative Specificity Overlay — `sie/target_stance.py`. Preferred columns shipped: `tsn_stance`, `tsn_specificity`, `tsn_qa_gap`, `tsn_boost`, `tsn_reason`. Commit: https://github.com/Stijnman/stock-intelligence-engine/commit/f03614fd13a9078c076042def5e92e446d9c90be.

**Completed 2026-10-06 (v2.54.0):** Alternative-Data Provenance & AI-Synthetic Contamination Confidence Overlay — `sie/alt_data_provenance.py`. Preferred columns shipped: `adp_provenance`, `adp_crosscheck`, `adp_boost`, `adp_reason`. Commit: https://github.com/Stijnman/stock-intelligence-engine/commit/b4710b4ccee1bdf2bfa3ba5fc33f9b8f7d015e59.

**Audit 2026-10-06 (v2.53.1):** No open item below is present as a wired overlay (analyzer + CLI + config + dashboard) on `main` @ c4c3bc5. Target stance, primary credit, TRACE, ATM dilution, news materiality, and tokenized basis stay completed and off this list.

---

## High Priority

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

- [ ] **Government Contract Award & Obligation Velocity Overlay**. Scores USAspending / FPDS award count and obligated-dollar delta as a public-demand nowcast, separate from congressional trading and lobbying. Soft boost when obligation velocity rises into a confirming narrative; caution on award cliffs or termination exposure. Preferred columns: `gov_obligation_delta`, `gov_award_count`, `gov_boost`, `gov_reason`.

- [ ] **ADR / Dual-Listing Premium vs Local Close Overlay**. Scores the ADR-versus-local close premium after FX, distinct from the tokenized-wrapper basis overlay. Soft boost when a liquid ADR trades rich into a confirming narrative; caution on a persistent discount with thin local liquidity. Preferred columns: `adr_premium_bps`, `adr_fx_gap`, `adr_boost`, `adr_reason`.

- [ ] **Options Skew Term-Structure & Risk-Reversal Dislocation Overlay**. Scores 25-delta risk reversal and skew term slope versus the name's own history. Complements IV rank, 0DTE and unusual-sweep overlays without duplicating them. Soft boost when put skew cheapens into a confirming narrative; caution on a steepening downside skew. Preferred columns: `skew_rr_25d`, `skew_term_slope`, `skew_boost`, `skew_reason`.

- [ ] **Lock-up / Resale-Registration Expiry Calendar Overlay**. Scores days to IPO, SPAC, or employee lock-up expiry and shares about to become freely tradable, distinct from Form 144 planned-sale windows and the already-wired ATM velocity overlay. Soft boost when the next expiry is distant and float is stable into a confirming narrative; caution inside a 15-day window with a large free-share print. Preferred columns: `lck_days_to_expiry`, `lck_shares_free`, `lck_boost`, `lck_reason`.

- [ ] **Convertible, Warrant & PIPE Dilution Overhang Overlay**. Scores conversion / warrant overhang as a percent of diluted shares and the gap between spot and the conversion price, distinct from ATM / 424B5 issuance velocity. Soft boost when overhang is small and the conversion price is far out of the money into a confirming narrative; caution when spot approaches conversion and the overhang is large. Preferred columns: `cvp_overhang_pct`, `cvp_conversion_gap`, `cvp_boost`, `cvp_reason`.

- [ ] **NHTSA / CPSC Recall & Complaint Velocity Overlay**. Scores open vehicle and consumer-product recalls plus complaint velocity as a demand and liability shock, distinct from app-store review sentiment and class-action filing counts. Soft boost when recall count is flat and complaint velocity is falling into a confirming narrative; caution when a new recall or complaint spike hits while social heat is still positive. Preferred columns: `rcl_recall_count`, `rcl_complaint_vel`, `rcl_boost`, `rcl_reason`.

- [ ] **Overnight / Extended-Hours Return Residual Overlay**. Scores the extended-hours move and the residual versus the next cash session, distinct from the ADR/local premium and the tokenized-wrapper basis. Soft boost when an overnight bid is confirmed by the cash open into a hot narrative; caution when the extended-hours move fades at the open. Preferred columns: `on_ext_return`, `on_cash_residual`, `on_boost`, `on_reason`.

- [ ] **Issuer MNPI Blackout & Buyback Window Calendar Overlay**. Scores whether the issuer is inside a pre-earnings MNPI blackout versus an open 10b5-1 trading window, distinct from the already-wired authorization-versus-execution overlay. Soft boost when the window is open and buyback capacity is unused into a confirming narrative; caution inside the blackout with elevated social heat. Preferred columns: `mnpi_blackout_flag`, `mnpi_days_to_window`, `mnpi_boost`, `mnpi_reason`.

- [ ] **Single-Stock / Levered ETF Rebalance Pressure Overlay**. Scores AUM in single-name and daily-reset levered products and the estimated end-of-day rebalance notional, distinct from the already-wired broad ETF creation/redemption overlay and from dealer GEX. Motivated by the 2026 expansion of single-stock leveraged ETFs, which options-flow and GEX dashboards still treat as a side channel. Soft boost when rebalance flow aligns with a confirming narrative and AUM is modest; caution when a large levered complex must buy or sell into the close against the narrative. Preferred columns: `ssetf_lev_aum`, `ssetf_rebalance_usd`, `ssetf_boost`, `ssetf_reason`.

- [ ] **Security-Based Swap / Equity TRS Large-Position Disclosure Overlay**. Scores disclosed security-based swap and total-return-swap notional and direction versus free float, distinct from 13F long ownership and Form 4 insider clusters. 2026 agent research stacks still underweight swap-equivalent exposure relative to listed options flow and EDGAR insider prints. Soft boost when disclosed swap interest is adding in the same direction as a confirming narrative; caution when a large short-equivalent TRS appears into crowded social heat. Preferred columns: `sbs_notional`, `sbs_direction`, `sbs_boost`, `sbs_reason`.

---

- [ ] **SEC Staff Comment-Letter & Filing-Review Velocity Overlay**. Scores open SEC staff comment letters, days since the last response, and amendment velocity on the latest 10-K / 10-Q. Distinct from 8-K cyber-incident velocity and from the already-wired target-specificity overlay. 2026 agent research desks still summarize filings without pricing unresolved staff review friction. Soft boost when the letter docket is clear into a confirming narrative; caution when an open comment letter ages while social heat is positive. Preferred columns: `cmt_open_letters`, `cmt_days_open`, `cmt_boost`, `cmt_reason`.

- [ ] **Rule 10b-18 Daily Volume-Cap Proximity Overlay**. Scores how much of the safe-harbor daily volume cap the issuer has already used and days left in the current buyback window. Distinct from the wired 10b5-1 authorization-versus-execution overlay and from the open MNPI blackout calendar. Soft boost when unused cap remains into a confirming narrative; caution when the cap is nearly exhausted into a crowded bid. Preferred columns: `b18_cap_used`, `b18_days_left`, `b18_boost`, `b18_reason`.

- [ ] **Treasury GC / Sponsored-Repo Funding-Stress Spillover Overlay**. Scores the general-collateral repo spread and the name's historical beta to dealer funding stress. Distinct from TRACE customer-flow and from the wired primary-credit concession overlay. Soft boost when funding is calm and the name is not a high funding-beta into a confirming narrative; caution when GC widens and the equity has historically sold off with dealer balance-sheet stress. Preferred columns: `repo_gc_spread`, `repo_equity_beta`, `repo_boost`, `repo_reason`.


- [ ] **CFTC Mention-Market / Named-Speaker Event-Contract Manipulation Overlay**. Scores open interest share in named-speaker or executive-mention event contracts and a manipulation flag when a thin contract leads the equity tape. Distinct from listed earnings event-contracts, KPI binaries, and prediction-market ETF overlap. Soft boost when mention-market positioning is diversified and agrees with a confirming narrative; caution when a thin contract's OI share spikes ahead of the stock. Preferred columns: `mmk_oi_share`, `mmk_manip_flag`, `mmk_boost`, `mmk_reason`.

- [ ] **Tokenized NMS Venue (TSV) AMM Pool Premium Overlay**. Scores the AMM pool premium of a tokenized NMS wrapper versus the listed share and LP depth, distinct from the already-wired cross-venue tokenized-share basis overlay. Soft boost when a deep pool trades modestly rich into a confirming narrative; caution on a wide premium with thin LP depth. Preferred columns: `tsv_pool_premium_bps`, `tsv_lp_depth`, `tsv_boost`, `tsv_reason`.

- [ ] **Prediction-Market ETF Event-Overlap Beta Overlay**. Scores the name's beta to filed prediction-market ETFs and the overlap between those event books and the issuer's own catalysts. Distinct from mention-market manipulation and from KPI binary vs street consensus. Soft boost when event-overlap beta confirms the narrative and the ETF book is liquid; caution when the equity is a high-beta passenger of an unrelated event book. Preferred columns: `pmetf_beta`, `pmetf_event_overlap`, `pmetf_boost`, `pmetf_reason`.

- [ ] **Cboe KPI Binary vs Street Consensus Divergence Overlay**. Scores the implied print on SEC-regulated Cboe KPI binary options (company metric / delivery / launch contracts listed with Robinhood from October 2026) against the street consensus for the same KPI. Distinct from the listed earnings event-contract vs whisper overlay and from prediction-market ETF event-overlap. Soft boost when the KPI binary and the street agree into a confirming narrative; caution when the binary implies a miss while narrative heat is still positive. Preferred columns: `kpi_implied`, `kpi_street_gap`, `kpi_boost`, `kpi_reason`.

- [ ] **Single-Name Event-Contract Jurisdiction Friction Overlay**. Scores equity-linked prediction-market volume and a flag for security-based-swap classification risk after the June 2026 SEC/CFTC request for comment on event-contract definitions. Distinct from disclosed equity TRS / SBS large-position filings and from mention-market manipulation. Soft boost when listed, SEC-regulated KPI binaries dominate and offshore single-stock event volume is small into a confirming narrative; caution when offshore single-name event volume is large relative to listed options open interest. Preferred columns: `ecj_event_vol`, `ecj_sbs_flag`, `ecj_boost`, `ecj_reason`.

- [ ] **LULD Band-Stress & Exchange-Halt Resume-Gap Overlay**. Scores limit-up/limit-down band hits and halt minutes, plus the cash gap on resume, as a microstructure stress check against narrative heat. Distinct from opening-auction imbalance and from overnight/extended-hours residual. Motivated by 2026 real-time dashboard practice that treats halt/LULD stress as a separate tape regime from sentiment. Soft boost when a confirming narrative prints without band stress; caution when repeated LULD hits or a halt-resume gap arrive into crowded social heat. Preferred columns: `luld_band_hits`, `luld_halt_min`, `luld_boost`, `luld_reason`.

## Medium Priority

- [ ] **Form 8-K Item 1.05 Cybersecurity Incident Velocity Overlay**. Preferred columns: `cyb_days_since`, `cyb_amend_vel`, `cyb_boost`, `cyb_reason`.

- [ ] **Long-form Newsletter / Substack Narrative Lead-Lag Overlay**. Preferred columns: `nl_lead_days`, `nl_authority`, `nl_boost`, `nl_reason`.

- [ ] **Guidance-vs-Delivery Promise Tracking Overlay**. Preferred columns: `gvd_open_promises`, `gvd_hit_rate`, `gvd_boost`, `gvd_reason`.

- [ ] **Board Interlock / Director-Network Centrality Overlay**. Preferred columns: `brd_interlock_n`, `brd_centrality`, `brd_boost`, `brd_reason`.

- [ ] **Thematic Narrative Taxonomy Exposure Overlay**. Preferred columns: `thm_pillar`, `thm_score`, `thm_boost`, `thm_reason`.

- [ ] **Point-in-Time Filing Freshness / Agent-Index Latency Overlay**. Preferred columns: `ptf_sec_lag_s`, `ptf_extract_lag_s`, `ptf_boost`, `ptf_reason`.

- [ ] **Expert-Call / Primary-Research Tone Overlay**. Preferred columns: `exp_tone`, `exp_revision_delta`, `exp_boost`, `exp_reason`.

- [ ] **Weather / Degree-Day Demand Shock Overlay**. Scores HDD/CDD z-score versus seasonal normal as a demand shock for retail, utilities, ag and logistics names. Soft boost when degree-day shock aligns with a confirming spend narrative; caution on adverse weather into weak traffic. Preferred columns: `wx_hdd_cdd_z`, `wx_demand_shock`, `wx_boost`, `wx_reason`.

- [ ] **Non-GAAP Bridge Drift / Adjusted-Earnings Quality Overlay**. Scores the GAAP-to-adjusted EPS bridge in basis points and the velocity of recurring add-backs (stock comp, restructuring, "one-time" items). Complements earnings-call sentiment and guidance tracking without duplicating them. Soft boost when the bridge is stable and shrinking into a confirming narrative; caution when add-backs accelerate while reported GAAP lags. Preferred columns: `ngaap_bridge_bps`, `ngaap_addback_vel`, `ngaap_boost`, `ngaap_reason`.

- [ ] **BNPL Delinquency & Consumer-Credit Spillover Overlay**. Scores buy-now-pay-later delinquency and late-stage consumer-credit stress as a demand spillover for discretionary retailers and card lenders, distinct from the aggregated card-spend nowcast. Soft boost when delinquency is falling into a confirming spend narrative; caution when DQ rates rise while traffic is still being reported as healthy. Preferred columns: `bnpl_dq_rate`, `bnpl_spillover`, `bnpl_boost`, `bnpl_reason`.

- [ ] **Customer Concentration / Top-Account Revenue Drift Overlay**. Scores disclosed top-customer or top-10 revenue share and quarter-over-quarter drift from 10-K / 10-Q concentration tables. Distinct from supply-chain CapEx and government-obligation velocity. Soft boost when concentration is stable or falling into a confirming narrative; caution when a single account's share jumps or a named customer is lost. Preferred columns: `ccn_top_share`, `ccn_drift`, `ccn_boost`, `ccn_reason`.

- [ ] **Search-Attention vs App-Download Divergence Overlay**. Scores the gap between Wikipedia / search attention momentum and app-download or digital-footprint momentum, distinct from either already-wired overlay alone. Retail dashboards in 2026 still publish those series side by side without a disagreement score. Soft boost when downloads confirm a search spike into a positive narrative; caution when search heat rises while downloads stall. Preferred columns: `sad_search_z`, `sad_download_z`, `sad_boost`, `sad_reason`.

- [ ] **Post-Quiet-Period Initiation Cluster Overlay**. Scores the count and direction of analyst initiations in the first window after an IPO or spin-off quiet period, distinct from the already-wired estimate-revision velocity overlay on seasoned names. Soft boost when initiations cluster bullish into a confirming narrative; caution on a bearish initiation cluster with thin float. Preferred columns: `pq_initiation_n`, `pq_bull_share`, `pq_boost`, `pq_reason`.

---

- [ ] **Channel Inventory Days & Working-Capital Fill Overlay**. Scores disclosed inventory days and the quarter-over-quarter fill delta from 10-Q working-capital tables. Distinct from the supplier bill-of-lading nowcast and from consumer-spend panels. Soft boost when inventory days are stable or falling into a confirming demand narrative; caution when channel fill rises while reported sell-through is still being described as healthy. Preferred columns: `inv_days`, `inv_fill_delta`, `inv_boost`, `inv_reason`.


- [ ] **XBRL Custom-Extension Tag Ratio Overlay**. Scores the share of custom extension tags in the latest 10-K / 10-Q XBRL and the count of tags new this period. Distinct from non-GAAP bridge drift and from staff comment-letter velocity. Soft boost when the extension ratio is stable and low into a confirming narrative; caution when new custom tags jump while reported GAAP lags. Preferred columns: `xbrl_ext_ratio`, `xbrl_new_tags`, `xbrl_boost`, `xbrl_reason`.

- [ ] **Opening Auction Imbalance vs Overnight Narrative Alignment Overlay**. Scores the NYSE/Nasdaq opening-auction imbalance notional and whether it confirms the overnight narrative. Distinct from the overnight / extended-hours return residual overlay. Soft boost when a large opening imbalance agrees with a confirming narrative and the cash open holds; caution when the imbalance fades or opposes the overnight story. Preferred columns: `auc_imbalance_usd`, `auc_narrative_align`, `auc_boost`, `auc_reason`.

- [ ] **FedNow / Same-Day ACH Corporate Receipt Velocity Overlay**. Scores same-day corporate receipt velocity and fail rate on FedNow and same-day ACH as a collections nowcast for payment, payroll, and B2B software names. Distinct from card authorization decline and chargeback velocity. Soft boost when receipt velocity rises and fails stay low into a confirming narrative; caution when fails spike while reported billings are still being described as healthy. Preferred columns: `fnw_receipt_vel`, `fnw_fail_rate`, `fnw_boost`, `fnw_reason`.

- [ ] **Delta 40-60 Directional Options Conviction Overlay**. Scores call-share and notional inside the delta 40-60 band (pure directional conviction, not lottery wings), distinct from unusual-options sweep-vs-block and from dealer GEX. Motivated by 2026 true-sentiment and options-flow desks that isolate this band rather than raw put/call volume. Soft boost when delta-band call dominance confirms the narrative; caution when put dominance in the same band fights a hot bid. Preferred columns: `d4060_call_share`, `d4060_notional`, `d4060_boost`, `d4060_reason`.
- [ ] **Issuer-Paid Research & Sponsored-Coverage Disclosure Velocity Overlay**. Scores the count and recency of issuer-sponsored or paid-for research disclosures versus independent sell-side notes. Distinct from news-authority and from KOL amplification. Soft boost when narrative heat is carried by independent coverage; caution when a spike in sponsored notes is the only support under the narrative. Preferred columns: `ipr_sponsored_n`, `ipr_independent_ratio`, `ipr_boost`, `ipr_reason`.

## Long-Term / Nice-to-Have

- [ ] **Class-Action / Multidistrict Litigation Filing Velocity Overlay**. Preferred columns: `lit_new_filings`, `lit_mdl_flag`, `lit_boost`, `lit_reason`.

- [ ] **Compute Waste-Heat / District-Heating Monetization Overlay**. Preferred columns: `heat_mw_offtake`, `heat_contract_flag`, `heat_boost`, `heat_reason`.

- [ ] **Parking-Lot / Satellite Occupancy Nowcast Overlay**. Preferred columns: `sat_occ_delta`, `sat_sample_n`, `sat_boost`, `sat_reason`.

- [ ] **Satellite Methane / Flare Intensity Energy Overlay**. Preferred columns: `ch4_intensity`, `flare_delta`, `ch4_boost`, `ch4_reason`.

- [ ] **Data-Center Interconnection Queue / Power-Availability Overlay**. Preferred columns: `dcq_mw_queued`, `dcq_wait_months`, `dcq_boost`, `dcq_reason`.

- [ ] **EU ETS / Carbon-Allowance Cost Pass-Through Overlay**. Preferred columns: `ets_cost_share`, `ets_price_mom`, `ets_boost`, `ets_reason`.

- [ ] **Private-Credit / BDC NAV Mark-Lag Overlay**. Scores BDC price-to-NAV discount and the lag between equity marks and private-credit portfolio marks. Soft boost when the discount narrows into a confirming credit narrative; caution on a widening discount with stale marks. Preferred columns: `bdc_nav_lag`, `bdc_discount`, `bdc_boost`, `bdc_reason`.

- [ ] **Podcast / Long-form Audio Mention Velocity Overlay**. Scores mention velocity and host authority on finance and company podcasts, distinct from newsletter lead-lag and short-form KOL amplification. Soft boost when authoritative long-form mentions lead a confirming narrative; caution on a spike in low-authority promotional episodes. Preferred columns: `pod_mention_vel`, `pod_authority`, `pod_boost`, `pod_reason`.

- [ ] **Autocallable Barrier Proximity & Observation-Calendar Hedge Overlay**. Scores distance to the nearest autocall / coupon barrier and days to the next shared observation date. Complements dealer GEX and pin-risk without duplicating listed-option gamma. Motivated by the 2026 expansion of laddered autocallable income ETFs and issuer hedge turnover around barriers. Soft boost when spot is comfortably above the barrier and the next observation is distant into a confirming narrative; caution inside a 5-day observation window with spot near the barrier. Preferred columns: `acb_barrier_gap`, `acb_obs_days`, `acb_boost`, `acb_reason`.

- [ ] **Contracted Power-Purchase vs Spot Power Spread Overlay**. Scores contracted data-center / industrial PPA price versus spot power and remaining tenor, distinct from the interconnection-queue overlay. Soft boost when a long cheap PPA covers rising load into a confirming narrative; caution when spot power blows out and contracted cover is short. Preferred columns: `ppa_spread`, `ppa_tenor_mo`, `ppa_boost`, `ppa_reason`.

- [ ] **State Incentive Clawback & Jobs-Credit Exposure Overlay**. Scores disclosed state and local incentive agreements, remaining jobs-credit headroom, and clawback exposure if hiring misses the covenant. Distinct from the government-obligation velocity overlay and from job-posting skill-mix. Soft boost when credits are intact and hiring is tracking the covenant into a confirming narrative; caution when a jobs gap opens a clawback window. Preferred columns: `inc_clawback_usd`, `inc_jobs_gap`, `inc_boost`, `inc_reason`.

- [ ] **Water-Rights / Basin Curtailment Exposure Overlay**. Scores disclosed basin curtailment flags and revenue share exposed to junior water rights. Distinct from the data-center interconnection queue and from contracted PPA vs spot power. Soft boost when curtailment risk is low and rights are senior into a confirming narrative; caution when a basin curtailment hits a material revenue share. Preferred columns: `wtr_curtail_flag`, `wtr_rev_share`, `wtr_boost`, `wtr_reason`.

- [ ] **Catastrophe-Bond / ILW Spread Spillover Overlay**. Scores catastrophe-bond and industry-loss-warranty spread widening and new issuance as a reinsurance-capacity shock for carriers and brokers. Distinct from EU ETS pass-through and from private-credit NAV mark-lag. Soft boost when cat spreads are tight and issuance is absorbed into a confirming underwriting narrative; caution when spreads blow out into a crowded equity bid. Preferred columns: `cat_spread`, `cat_issuance`, `cat_boost`, `cat_reason`.


- [ ] **CMS IRA Medicare Drug-Price Negotiation List Exposure Overlay**. Scores whether a product sits on the CMS Medicare Drug Price Negotiation list and the revenue share exposed to the negotiated price. Distinct from FDA milestone velocity and from government-obligation velocity. Soft boost when list exposure is immaterial into a confirming narrative; caution when a material franchise is selected or the negotiated price gaps the street model. Preferred columns: `ira_list_flag`, `ira_rev_share`, `ira_boost`, `ira_reason`.
