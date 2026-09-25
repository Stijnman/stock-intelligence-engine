# Future Improvements — Stock Intelligence Engine

**Last updated:** 2026-09-25  
**Current version baseline:** v2.41.1

This file is the single source of truth for the open roadmap.  
Items that are fully implemented and wired (analyzer + CLI + config + dashboard) are removed here and recorded in CHANGELOG.md + README Recent Edits.

---

## High Priority

- [ ] **Rule 10b5-1 / Buyback Authorization vs Execution Overlay**. Cluster scheduled 10b5-1 plan adoptions/amendments and compare announced buyback authorizations against actual repurchase cadence. Soft boost when execution is running ahead of authorization with supportive narrative; caution on stalled buybacks. Preferred columns: `bb_util`, `bb_plan_delta`, `bb_boost`, `bb_reason`.

- [ ] **Unusual Options Sweep vs Block Confirmation Overlay**. Distinguish aggressive sweep prints from passive blocks on the options tape and score confirmation vs fade against existing 0DTE / IV / GEX layers. Soft boost when multi-strike sweeps align with narrative velocity and positive GEX; caution on large blocks into strength that look like distribution. Preferred columns: `uopt_sweep_score`, `uopt_block_ratio`, `uopt_boost`, `uopt_reason`. Synthetic proxy acceptable offline.

- [ ] **Employee Outlook / Glassdoor Business Sentiment Overlay**. Track employee business-outlook and CEO-approval deltas as an inside-the-firm leading indicator distinct from raw hiring-count momentum. Soft boost when outlook rises with hiring and digital-footprint velocity; caution on collapsing outlook while street estimates are still rising. Preferred columns: `eo_outlook`, `eo_ceo`, `eo_boost`, `eo_reason`.

- [ ] **App-Store Review Sentiment & Complaint Velocity Overlay**. Score App Store / Play Store review polarity, 1-star complaint velocity, and crash/outage language as a product-quality nowcast distinct from raw download counts in the digital-footprint layer. Soft boost when review sentiment rises with download velocity; caution on complaint spikes or outage clusters even when traffic is still high. Preferred columns: `asr_sentiment`, `asr_complaint_velocity`, `asr_boost`, `asr_reason`. Synthetic proxy acceptable offline.

- [ ] **Retail Brokerage Order-Flow Imbalance Overlay**. Track public retail-flow proxies (popularity lists, buy/sell imbalance prints, fractional-share heat) as a confirmation or fade against authenticity-filtered social intent. Soft boost when retail buy imbalance aligns with high-intent authentic velocity; caution on one-sided retail chase into weakening technicals. Preferred columns: `rflow_imbalance`, `rflow_heat`, `rflow_boost`, `rflow_reason`. Synthetic proxy acceptable offline.

- [ ] **Job-Posting Skill-Mix & Posted-Compensation Inflation Overlay**. Score not just hiring *count* but *what* is being hired (seniority mix, AI/infra skill tags) and posted salary bands vs last quarter. Soft boost when senior/AI-skill mix and posted-comp inflate with digital-footprint and patent velocity; caution on junior-only backfill or posted-comp compression while headline headcount still rises. Preferred columns: `hmix_senior_share`, `hmix_comp_delta`, `hmix_boost`, `hmix_reason`. Distinct from the existing hiring-count layer. Synthetic proxy acceptable offline.

- [ ] **Cross-Venue Tokenized-Share Basis / On-Chain Equity Premium Overlay**. Track premium/discount and liquidity between traditional listed shares and 2026 tokenized / on-chain equity venues as a new mechanical demand/arbitrage pulse. Soft boost when tokenized venue premium persists with rising authentic narrative; caution on widening discount or venue-outage language even when social heat is elevated. Preferred columns: `tok_basis_bps`, `tok_venue_liq`, `tok_boost`, `tok_reason`. Synthetic proxy acceptable offline.

- [ ] **News Materiality / Predicted Next-Session Impact Score Overlay**. Score each headline/filing for predicted next-session price impact and realized-volatility bucket (StockTitan Rhea-AI / news-analytics style) instead of polarity alone. Soft boost when high-authority + high-materiality prints align with narrative velocity; caution on high-velocity chatter that scores as low-materiality noise. Preferred columns: `nimp_score`, `nimp_vol_bucket`, `nimp_boost`, `nimp_reason`. Extends the shipped news-authority layer. Synthetic proxy acceptable offline.

- [ ] **Secondary Offering / ATM Dilution Velocity Overlay**. Track follow-on offerings, ATM prospectus tap activity, lock-up expiries and announced share-count growth as a supply pulse distinct from buyback execution. Soft caution when ATM / secondary velocity rises into elevated social heat; modest boost when dilution calendar is clean while buybacks are executing. Preferred columns: `dil_atm_velocity`, `dil_share_delta`, `dil_boost`, `dil_reason`. Synthetic proxy acceptable offline.

- [ ] **TRACE Corporate-Bond Customer-Flow & Liquidity Shock Overlay**. Use FINRA TRACE executed-trade price/yield/size plus customer-vs-interdealer volume structure to measure issuer-level fixed-income demand and liquidity stress separately from spread direction. Soft boost when customer demand and trade-quality/liquidity improve alongside constructive equity narrative; caution on customer selling pressure, price/yield dispersion or liquidity deterioration while equity sentiment stays hot. Preferred columns: `trace_customer_flow`, `trace_liq_score`, `trace_boost`, `trace_reason`. Deterministic synthetic proxy acceptable offline.

- [ ] **Primary Credit Issuance / New-Issue Concession & Supply Pressure Overlay**. Track issuer debt calendars, new-issue concession, oversubscription and clustered sector supply as a forward funding-pressure pulse distinct from the existing secondary-market credit-spread/CDS overlay. Soft boost when strong books and tight concessions confirm funding access; caution when repeated issuance needs widening concessions or sector supply overwhelms demand. Preferred columns: `pci_concession_bp`, `pci_supply_score`, `pci_boost`, `pci_reason`. Deterministic synthetic proxy acceptable offline.

- [ ] **Target-Specific Financial Stance & Narrative Specificity Overlay**. Parse 10-K MD&A and earnings-call language by explicit target (debt, EPS, sales/revenue and other configured KPIs), score specificity/novelty, and compare prepared remarks with Q&A stance. Soft boost when target-specific stance improves with high-specificity evidence and low presentation/Q&A divergence; caution when upbeat aggregate tone masks negative stance on a key target or specificity collapses. Preferred columns: `tsn_stance`, `tsn_specificity`, `tsn_qa_gap`, `tsn_boost`, `tsn_reason`. Deterministic synthetic proxy acceptable offline.

- [ ] **Alternative-Data Provenance & AI-Synthetic Contamination Confidence Overlay**. Score each alternative-data input for source provenance, raw-vs-derived lineage, freshness, independent corroboration and disclosed AI transformation so opaque/generated feeds cannot silently dominate the composite signal. Soft boost when independent traceable raw feeds corroborate; caution when apparent edge depends on low-provenance or AI-generated data with weak cross-checks. Preferred columns: `adp_provenance`, `adp_crosscheck`, `adp_boost`, `adp_reason`. Deterministic synthetic proxy acceptable offline.

- [ ] **Rule 606 Retail Options Routing & Execution-Quality Overlay**. Use public broker Rule 606 routing disclosures to score venue/consolidator concentration, payment-for-order-flow exposure and execution-quality trends for retail listed-options flow. This qualifies the existing/future retail-intent signal rather than duplicating directional buy/sell imbalance. Soft boost when retail activity broadens across venues with stable/improving execution quality; caution when chase activity concentrates through a narrow routing stack while execution quality deteriorates. Preferred columns: `r606_concentration`, `r606_exec_quality`, `r606_boost`, `r606_reason`. Deterministic synthetic proxy acceptable offline.

- [ ] **Index Reconstitution & Forced Passive-Flow Overlay**. Score scheduled S&P / Nasdaq / MSCI / Russell adds, deletes and weight-cap events plus estimated forced passive dollars as a mechanical demand pulse distinct from ETF AP creation/redemption. Soft boost when a confirmed add coincides with supportive authentic narrative and rising estimate revisions; caution when a delete or capping event hits into elevated social heat. Preferred columns: `idx_event`, `idx_forced_usd`, `idx_boost`, `idx_reason`. Deterministic synthetic proxy acceptable offline.

- [ ] **Listed Earnings Event-Contract vs Whisper / Street Divergence Overlay**. Compare Kalshi / Polymarket (and similar) listed beat/miss / EPS event-contract implied probabilities against street consensus and the shipped whisper-number alt-data cluster. Soft boost when event-contract odds and the whisper cluster agree against a stale street print; caution when listed event odds fade while social heat and street estimates stay elevated. Preferred columns: `eec_implied_beat`, `eec_whisper_gap`, `eec_boost`, `eec_reason`. Distinct from the generic prediction-markets overlay. Deterministic synthetic proxy acceptable offline.

- [ ] **FDA / Clinical-Trial Milestone & Protocol-Amendment Velocity Overlay**. Score PDUFA dates, Phase 2/3 readout calendars, protocol amendments, enrollment-pause language and CRL / complete-response density for biotech and device names. Soft boost when milestone cadence is clean and amendments shrink rather than expand; caution on clustered protocol changes, paused enrollment or accelerating CRL language even when social heat is elevated. Preferred columns: `fda_days_to_event`, `fda_amend_velocity`, `fda_boost`, `fda_reason`. Distinct from generic EDGAR 8-K volume. Deterministic synthetic proxy acceptable offline.

- [ ] **CFTC Commitment-of-Traders Speculative Positioning Overlay**. Map watchlist names and sector ETFs to related futures and score non-commercial net positioning, weekly position deltas and crowding vs the prior-year percentile. Soft boost when speculative positioning is rebuilding from a washed-out extreme alongside authentic narrative; caution when non-commercials are already at multi-year crowded longs while social intent is still chasing. Preferred columns: `cot_net_spec`, `cot_crowd_pct`, `cot_boost`, `cot_reason`. Deterministic synthetic proxy acceptable offline.

- [ ] **CEO / CFO Vocal-Affect & Earnings-Audio Hedge-Density Overlay**. Score earnings-call *audio* (not just transcript text) for vocal stress, pace, pitch variance and hedge-density in prepared remarks vs Q&A — MoodMetrics / Hume-style affect. Soft boost when vocal affect and transcript stance agree with rising whisper/event-contract odds; caution when upbeat text masks stressed affect or Q&A hedge spikes. Preferred columns: `va_affect`, `va_hedge_audio`, `va_boost`, `va_reason`. Distinct from `sie/earnings_call.py` text NLP. Deterministic synthetic proxy acceptable offline.

- [ ] **13F Amendment / Confidential-Treatment & Late-Filer Velocity Overlay**. Track 13F amendments, confidential-treatment requests and late-filer flags as a positioning-opacity pulse distinct from the shipped holdings snapshot. Soft boost when large holders file on time with rising active share; caution when amendment/late-filer velocity clusters into elevated social heat. Preferred columns: `f13_amend_vel`, `f13_late_share`, `f13_boost`, `f13_reason`. Deterministic synthetic proxy acceptable offline.

---

## Medium Priority

See prior roadmap items (ESG narrative, multi-agent thesis debate, long-form velocity, retail vs institutional options flow, expert-network aspects, MCP tool server, GPU/HBM lead-times, 10-K risk-factor delta, FOMC surprise, supplier-customer surprise graph).

- [ ] **Earnings Calendar Distance-Decay & Event-Risk Overlay**. Score days-to-next-print and historically implied event vol so overlays can auto-dampen or concentrate into the event window. Soft boost when pre-event alt-data cluster is aligned and IV is not already fully priced; caution when event is imminent and honesty / contradiction flags are elevated. Preferred columns: `ecd_days`, `ecd_event_vol`, `ecd_boost`, `ecd_reason`.

- [ ] **Macro Surprise vs Ticker-Beta Residual Overlay**. Compare same-session CPI / NFP / FOMC / PMI surprise prints against each ticker’s realized beta and isolate the residual move. Soft boost when the name outperforms a positive macro surprise on supportive narrative; caution when it underperforms a risk-on print. Preferred columns: `mx_surprise`, `mx_residual`, `mx_boost`, `mx_reason`.

- [ ] **Investor-Day / Conference Slide-Deck Guidance NLP Overlay**. Parse investor-day, analyst-day and conference slide text (or synthetic proxies) for incremental KPI targets vs last printed guidance. Soft boost when slide-deck targets step up with hiring / digital-footprint confirmation; caution on silent target cuts or weasel language. Preferred columns: `ideck_delta`, `ideck_tone`, `ideck_boost`, `ideck_reason`.

- [ ] **Physical Foot-Traffic vs Digital-Demand Divergence Overlay**. Compare geolocation / parking-lot / store-visit pulses against the existing digital-footprint (web + app) layer. Soft boost when physical and digital demand rise together; caution when stores empty while app/web traffic is still hot (or the reverse channel-shift). Preferred columns: `ft_phys_delta`, `ft_digital_gap`, `ft_boost`, `ft_reason`. Synthetic proxy acceptable offline.

- [ ] **SKU Shelf-Price / Promo-Intensity Nowcast Overlay**. Scrape or proxy on-shelf / e-commerce list prices, promo depth, and out-of-stock flags for key SKUs as a near-term margin and demand pulse distinct from card-panel spend. Soft boost when prices hold with low promo intensity and rising spend; caution on deepening discounting or stockouts into a supposedly strong narrative. Preferred columns: `sku_price_delta`, `sku_promo_intensity`, `sku_boost`, `sku_reason`. Synthetic proxy acceptable offline.

- [ ] **Multi-Quarter Guidance-vs-Delivered KPI Tracker Overlay**. Reconcile what management guided (revenue, margin, capex, unit KPIs) against subsequent printed results across trailing quarters — a delivery-score distinct from same-day transcript tone. Soft boost when delivery beats guidance for 2+ prints with supportive narrative; caution on serial misses or restated targets. Preferred columns: `gvd_hit_rate`, `gvd_slip`, `gvd_boost`, `gvd_reason`. Synthetic proxy acceptable offline.

- [ ] **Short-Seller Report / Activist Campaign Velocity Overlay**. Detect published short-seller reports, activist 13D/13G bursts, and rebuttal cadence as a distinct honesty / narrative-shock layer. Soft caution on fresh high-authority short reports or accelerating activist filings; modest boost when rebuttals land cleanly and credit spreads do not widen. Preferred columns: `act_report_flag`, `act_13d_velocity`, `act_boost`, `act_reason`. Synthetic proxy acceptable offline.

- [ ] **Working-Capital / DSO-DIO Drift Overlay**. Parse 10-Q / 10-K working-capital footnotes for days-sales-outstanding, days-inventory-outstanding and cash-conversion-cycle drift versus the prior four prints. Soft boost when CCC compresses alongside rising consumer-spend / digital-footprint nowcasts; caution when DSO/DIO silently expand while headline revenue and social narrative stay hot. Preferred columns: `wc_dso_delta`, `wc_ccc_delta`, `wc_boost`, `wc_reason`. Distinct from guidance-vs-delivered KPI tracking. Deterministic synthetic proxy acceptable offline.

- [ ] **Cloud / SaaS Status-Page Incident Velocity Overlay**. Ingest public vendor status pages, regional SRE incident banners and multi-hour degradation language as an operational nowcast for software / cloud names. Soft caution when incident velocity or duration spikes even while app-download and review layers look stable; modest boost when a high-severity incident clears cleanly with no residual complaint velocity. Preferred columns: `sts_incident_velocity`, `sts_mttr_hours`, `sts_boost`, `sts_reason`. Distinct from app-store complaint velocity. Deterministic synthetic proxy acceptable offline.

- [ ] **Labor-Action / Collective-Bargaining Expiry Overlay**. Score announced strikes, picket language, NLRB filings and major CBA expiry windows as an operational-disruption pulse for industrials, transport, healthcare and media names. Soft caution when strike probability and picket velocity rise into a thin inventory / high-demand narrative; modest boost when a contract clears without work stoppage. Preferred columns: `lab_expiry_days`, `lab_action_velocity`, `lab_boost`, `lab_reason`. Deterministic synthetic proxy acceptable offline.

- [ ] **Dual-Listed ADR / Ordinary-Share Basis Overlay**. Track premium/discount, borrow availability and session-lag between US ADRs and home-market ordinaries. Soft boost when the cheaper line is being accumulated with authentic narrative confirmation; caution when the ADR premium blows out on US social heat while the home print stays cold. Preferred columns: `adr_basis_bps`, `adr_lag`, `adr_boost`, `adr_reason`. Distinct from tokenized-share venue basis. Deterministic synthetic proxy acceptable offline.

- [ ] **Hyperscaler Interconnection-Queue & AI Power-Lead-Time Overlay**. Score data-center interconnection-queue depth, utility interconnection study delays and announced campus power MW as a capacity-constraint pulse for AI-exposed semiconductors, utilities and landlords. Soft boost when queue clearance accelerates with CapEx confirmation; caution when study delays lengthen while narrative stays hot. Preferred columns: `aiq_queue_months`, `aiq_mw_delta`, `aiq_boost`, `aiq_reason`. Distinct from generic supply-chain CapEx. Deterministic synthetic proxy acceptable offline.

- [ ] **Dealer Inventory / Market-Maker Hedging-Flow vs GEX Divergence Overlay**. Compare inferred MM inventory and hedging-flow direction against the shipped dealer GEX / pin-risk layer. Soft boost when hedging flow confirms GEX support under a constructive narrative; caution when inventory dump diverges from a still-positive GEX print. Preferred columns: `mmh_inv`, `mmh_gex_gap`, `mmh_boost`, `mmh_reason`. Deterministic synthetic proxy acceptable offline.

---

## Long-Term / Nice-to-Have

See prior roadmap items (event-driven webhooks, AIS/freight, data-center power, satellite night-lights, SAR activity, on-chain liquidity pulse).

- [ ] **SEC Comment Letter / Regulatory Docket Velocity Overlay**. Track incoming SEC comment letters, FDA/DoJ/FTC docket pulses, and reply cadence as a slow-burn legal-risk narrative. Soft caution on accelerating comment velocity or unanswered letters; modest boost when dockets close cleanly alongside supportive narrative. Preferred columns: `reg_docket_velocity`, `reg_unanswered`, `reg_boost`, `reg_reason`.

- [ ] **Physical Climate / Extreme-Weather Event Exposure Overlay**. Map watchlist names to facility / crop / coastal / grid exposure and score incoming extreme-weather events as a disruption pulse. Soft caution on high-severity events hitting concentrated assets; modest boost when events clear without operational impact while narrative stays constructive. Preferred columns: `wx_exposure`, `wx_event_score`, `wx_boost`, `wx_reason`.

- [ ] **Auditor-Change / Going-Concern Language Velocity Overlay**. Track auditor resignations, going-concern opinion language, and late-filer flags as a slow-burn accounting-quality risk distinct from EDGAR 8-K volume. Soft caution on auditor switches + going-concern language clustering; modest boost when filings stay clean while credit spreads tighten. Preferred columns: `aud_change`, `aud_gc_flag`, `aud_boost`, `aud_reason`.

- [ ] **Cross-Language / Offshore Narrative Lag Overlay**. Compare US X/Reddit narrative velocity against CN / KR / JP / TW board and search heat for dual-listed or supply-chain names. Soft boost when offshore heat leads US confirmation with authentic intent; caution when US social spikes while offshore venues stay cold (or vice versa). Preferred columns: `xl_us_vel`, `xl_offshore_lag`, `xl_boost`, `xl_reason`. Synthetic proxy acceptable offline.

- [ ] **CAT-Bond / Reinsurance Rate-on-Line Sector Stress Overlay**. Track catastrophe-bond issuance spreads and reinsurance rate-on-line resets as a slow-burn sector stress pulse for insurers, reinsurers and exposed industrials — distinct from the physical extreme-weather facility map. Soft caution when ROL / CAT spreads gap higher into a busy event season; modest boost when spreads compress after a clean season while credit and narrative stay constructive. Preferred columns: `cat_rol`, `cat_spread_delta`, `cat_boost`, `cat_reason`. Deterministic synthetic proxy acceptable offline.

- [ ] **Corporate-Jet / Executive-Travel Nowcast Overlay**. Use public ADS-B / flight-log proxies for C-suite and IR-roadshow aircraft as a slow-burn activity pulse (deal roadshows, site visits, unexpected multi-city bursts). Soft modest boost when travel clusters ahead of announced IR events with constructive narrative; caution when unexplained flight bursts coincide with honesty flags or widening credit. Preferred columns: `jet_activity`, `jet_burst`, `jet_boost`, `jet_reason`. Deterministic synthetic proxy acceptable offline.

- [ ] **Central-Bank Speech Vocal-Stress / FOMC Q&A Affect Overlay**. Score FOMC / ECB / BoJ press-conference audio affect and Q&A hedge density as an index-level regime pulse distinct from text surprise prints. Soft caution when hawkish affect arrives with rising hedge density even if the statement is unchanged; modest boost when dovish affect clears with compressed event vol. Preferred columns: `cb_affect`, `cb_qa_hedge`, `cb_boost`, `cb_reason`. Deterministic synthetic proxy acceptable offline.

---

## Completed this cycle

- [x] **ETF Creation / Redemption & Authorized-Participant Flow Overlay** — shipped in v2.41.0 (2026-09-24). Module `sie/etf_flow.py`, CLI `--no-etf-flow`, config `etf_flow:`, dashboard columns `etf_*`. Docs + dashboard version aligned in v2.41.1 (item was still listed open after the feature commit).
- [x] **Key Opinion Leader (KOL) / Influencer Narrative Amplification Detector** — shipped in v2.40.0 (2026-09-23). Module `sie/kol_amplification.py`, CLI `--no-kol-amplification`, config `kol_amplification:`, dashboard columns `kol_*`. Docs synced in v2.40.1 (item was still listed open after the feature commit).
- [x] **Whisper Number / Pre-Earnings Alt-Data Beat Probability Overlay** — shipped in v2.39.0 (2026-09-22). Module `sie/whisper_number.py`, CLI `--no-whisper-number`, config `whisper_number:`, dashboard columns `wn_*`.
- [x] **News-Source Authority / Reliability Weighted Narrative Score** — shipped in v2.38.0 (2026-09-21). Module `sie/news_authority.py`, CLI `--no-news-authority`, config `news_authority:`, dashboard columns `nsa_*`. Docs synced in v2.38.1.
- [x] **Earnings Call Transcript Real-Time Sentiment & Guidance Drift Detector** — shipped in v2.37.0 (2026-09-20). Module `sie/earnings_call.py`, CLI `--no-earnings-call`, config `earnings_call:`, dashboard columns `ect_*`.
- [x] **Corporate Credit Spread / CDS Momentum Overlay** — shipped in v2.36.0 (2026-09-19). Module `sie/credit_spread.py`, CLI `--no-credit-spread`, config `credit_spread:`, dashboard columns `cds_*`.

## Notes

- All new overlays must follow the established pattern: pure function in `sie/`, soft ±1 boost, config block, CLI disable flag, preferred columns in Streamlit, and a deterministic synthetic proxy when live data is unavailable.
- Educational research tool only — not financial advice.

*End of roadmap.*
