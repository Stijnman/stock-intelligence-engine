# Future Improvements — Stock Intelligence Engine

**Last updated:** 2026-10-17
**Current version baseline:** v2.65.0

This file is the single source of truth for the open roadmap.
Items that are fully implemented and wired (analyzer + CLI + config + dashboard) are removed here and recorded in CHANGELOG.md + README Recent Edits.

---

## High Priority

- [ ] **Agentic Narrative Contagion Velocity Overlay**.
  Preferred columns: `anc_vel`, `anc_agent_share`, `anc_boost`, `anc_reason`.
  Soft boost when high-velocity narrative propagation through autonomous AI agents (agent-to-agent contagion, generative memo cascades) confirms a narrative into technical strength; caution when agent-driven contagion collapses or turns adversarial while human narrative heat remains elevated. Synthetic proxy (live agent-network monitor reserved).

- [ ] **RAG-Extracted Earnings Guidance Novelty & Hedge Density Overlay**.
  Preferred columns: `rgn_novelty`, `rgn_hedge_density`, `rgn_boost`, `rgn_reason`.
  Soft boost when RAG-grounded extraction of earnings-call transcripts surfaces high-novelty guidance language with low hedge density into a confirming narrative; caution on boilerplate or heavily hedged guidance while narrative heat stays elevated. Synthetic proxy (live transcript RAG reserved).

- [ ] **YouTube Financial Creator Transcript & Comment Sentiment Velocity Overlay**.
  Preferred columns: `ytc_vel`, `ytc_sent`, `ytc_boost`, `ytc_reason`.
  Soft boost when high-velocity authentic sentiment from financial YouTube creator transcripts and comments confirms a narrative into technical strength; caution when creator sentiment collapses or turns adversarial while human narrative heat remains elevated. Synthetic proxy (live YouTube transcript + comment feed reserved).

- [ ] **Kalshi Regulated vs Polymarket Offshore Earnings Beat Probability Basis Overlay**.
  Preferred columns: `kpm_basis_bps`, `kpm_kalshi_prob`, `kpm_boost`, `kpm_reason`.
  Soft boost when regulated Kalshi earnings-beat probability shows a rich constructive basis versus offshore Polymarket into a confirming narrative; caution on adverse or collapsing basis while narrative heat remains elevated. Synthetic proxy (live Kalshi + Polymarket feed reserved).

- [ ] **Agent-Generated Research Memo Cascade Velocity Overlay**.
  Preferred columns: `agc_vel`, `agc_memo_share`, `agc_boost`, `agc_reason`.
  Soft boost when high-velocity cascade of agent-generated research memos (AlphaSense SuperAnalyst-style always-on workflows) confirms a narrative into technical strength; caution when cascade collapses or turns adversarial while human narrative heat remains elevated. Synthetic proxy (live agent-memo monitor reserved).

---

## Medium Priority

- [ ] **Reddit-ICE Market Insights Conversation Velocity Overlay**.
  Preferred columns: `rdt_vel`, `rdt_theme_align`, `rdt_boost`, `rdt_reason`.

- [ ] **MCP Data-Feed Freshness & Attestation Overlay**.
  Preferred columns: `mcp_age_s`, `mcp_attested`, `mcp_boost`, `mcp_reason`.

- [ ] **Real-Time X/Twitter Cashtag Firehose Velocity with Bot Filter Overlay**.
  Preferred columns: `xtw_vel`, `xtw_auth`, `xtw_boost`, `xtw_reason`.
  Soft boost when high-velocity authentic cashtag volume confirms narrative; caution when bot-filtered velocity collapses while narrative heat stays elevated. Synthetic proxy (live X API v2 firehose reserved).

- [ ] **Multi-Venue Options Flow Sweep Aggregation & Dark-Pool Cross-Confirmation Overlay**.
  Preferred columns: `mvo_sweep`, `mvo_dark_conf`, `mvo_boost`, `mvo_reason`.
  Soft boost when multi-venue sweep aggregation is confirmed by dark-pool prints into a confirming narrative; caution on unconfirmed or conflicting flow. Synthetic proxy (live multi-venue feed reserved).

- [ ] **Cross-Platform Retail Sentiment Divergence (X + Reddit + StockTwits) Overlay**.
  Preferred columns: `xrs_div`, `xrs_align`, `xrs_boost`, `xrs_reason`.
  Soft boost when cross-platform retail sentiment (X, Reddit, StockTwits) aligns constructively into a confirming narrative; caution on sharp divergence while narrative heat remains elevated. Synthetic proxy (live multi-platform feed reserved).

- [ ] **Social Narrative Authenticity Scoring & Cluster Confidence Overlay**.
  Preferred columns: `sna_auth`, `sna_cluster_conf`, `sna_boost`, `sna_reason`.
  Soft boost when high-authenticity narrative clusters (bot-filtered, source-attested) confirm a narrative; caution on low-authenticity or fragmented clusters while narrative heat stays elevated. Synthetic proxy (live authenticity scorer reserved).

- [ ] **Prediction-Market (Polymarket) vs Options-Implied Probability Basis Overlay**.
  Preferred columns: `pmo_basis_bps`, `pmo_poly_prob`, `pmo_boost`, `pmo_reason`.
  Soft boost when Polymarket (or equivalent real-money prediction market) implied probability shows a rich constructive basis versus options-implied probability into a confirming narrative; caution on adverse or collapsing basis while narrative heat remains elevated. Synthetic proxy (live Polymarket + options feed reserved).

- [ ] **Narrative Gravity Divergence from Fundamental Valuation Overlay**.
  Preferred columns: `ngd_gravity`, `ngd_fund_gap`, `ngd_boost`, `ngd_reason`.
  Soft boost when measured narrative gravity (viral story pull on price) remains constructively aligned with or below fundamental valuation anchors into a confirming narrative; caution when narrative gravity sharply diverges from fundamentals while heat stays elevated. Synthetic proxy (live narrative-gravity scorer reserved).

- [ ] **Live Macro Event Narrative Spillover Velocity Overlay**.
  Preferred columns: `lms_spillover`, `lms_macro_align`, `lms_boost`, `lms_reason`.
  Soft boost when live macro events (Fed speakers, CPI, geopolitics) produce constructive narrative spillover into the ticker; caution on adverse or lagged spillover while narrative heat stays elevated. Synthetic proxy (live macro-event monitor reserved).

- [ ] **Cross-Exchange Tokenized Equity Order-Book Depth Overlay**.
  Preferred columns: `cto_depth`, `cto_basis_bps`, `cto_boost`, `cto_reason`.
  Soft boost when cross-exchange tokenized equity order-book depth supports tight basis into a confirming narrative; caution on thin depth or adverse basis. Synthetic proxy (live tokenized venue feed reserved).

- [ ] **LLM Source-Grounding Confidence & Hallucination Rate Overlay**.
  Preferred columns: `lgc_ground`, `lgc_halluc`, `lgc_boost`, `lgc_reason`.
  Soft boost when narrative extraction shows high source-grounding confidence and low hallucination rate into a confirming narrative; caution on elevated hallucination or weak grounding while narrative heat remains elevated. Synthetic proxy (live dual-LLM + citation scorer reserved).

- [ ] **Insider Cluster Buying Acceleration & Timing Overlay**.
  Preferred columns: `icb_accel`, `icb_cluster_size`, `icb_boost`, `icb_reason`.
  Soft boost when accelerating cluster buying by multiple insiders with constructive timing confirms a narrative; caution on cluster selling or stalled acceleration while narrative heat stays elevated. Synthetic proxy (live Form 4 cluster monitor reserved).

- [ ] **ICE Reddit Signals Institutional Sentiment Freshness Overlay**.
  Preferred columns: `irs_fresh_s`, `irs_sent`, `irs_boost`, `irs_reason`.
  Soft boost when ICE-distributed Reddit Signals & Sentiment feed remains fresh and constructively aligned into a confirming narrative; caution on stale or adverse institutional Reddit signal while narrative heat stays elevated. Synthetic proxy (live ICE Reddit feed reserved).

- [ ] **Substack Financial Author Narrative Velocity & Authenticity Overlay**.
  Preferred columns: `ssa_vel`, `ssa_auth`, `ssa_boost`, `ssa_reason`.
  Soft boost when high-velocity authentic sentiment from Substack financial authors and newsletters confirms a narrative into technical strength; caution when author sentiment collapses or low authenticity while narrative heat remains elevated. Synthetic proxy (live Substack feed reserved).

---

## Long-Term / Nice-to-Have

- [ ] **European Consolidated Tape Liquidity Visibility Overlay**.
  Preferred columns: `ect_liq`, `ect_spread`, `ect_boost`, `ect_reason`.
  Soft boost when improved European consolidated-tape visibility and tighter spreads confirm narrative; caution on fragmented liquidity. Synthetic proxy reserved.

- [ ] **WebSocket Streaming Latency Attribution vs Polling Overlay**.
  Preferred columns: `ws_latency_ms`, `poll_delta_ms`, `ws_boost`, `ws_reason`.
  Soft boost when WebSocket streaming latency is materially lower than polling and supports real-time narrative confirmation; caution on persistent high streaming latency or fallback to polling. Synthetic proxy (live dashboard telemetry reserved).

- [ ] **Streamlit Fragment Refresh Health & Staleness Attribution Overlay**.
  Preferred columns: `sfr_age_s`, `sfr_fragment_ok`, `sfr_boost`, `sfr_reason`.
  Soft boost when Streamlit `st.fragment` incremental refresh cycles remain healthy and low-staleness for live market panels; caution on fragment failures, excessive age, or fallback to full-app reruns. Synthetic proxy (live dashboard telemetry reserved).

- [ ] **Streamlit Session-State Persistence & Crash Recovery Overlay**.
  Preferred columns: `ssp_persist_ok`, `ssp_recovery_ms`, `ssp_boost`, `ssp_reason`.
  Soft boost when Streamlit session-state persistence remains healthy and recovery is fast after fragment or full-app restarts; caution on persistence failures or slow recovery. Synthetic proxy (live dashboard telemetry reserved).

- [ ] **Earnings Call Speaker Sentiment Divergence Overlay**.
  Preferred columns: `ecs_div`, `ecs_ceo_tone`, `ecs_boost`, `ecs_reason`.
  Soft boost when CEO vs CFO (or key speakers) sentiment divergence remains constructive or low into a confirming narrative; caution on sharp adverse divergence while narrative heat stays elevated. Synthetic proxy (live transcript speaker-level scorer reserved).

- [ ] **Cross-Asset (Equity-Crypto) Narrative Contagion Velocity Overlay**.
  Preferred columns: `cac_vel`, `cac_crypto_align`, `cac_boost`, `cac_reason`.
  Soft boost when high-velocity narrative contagion from related crypto or tokenized assets confirms an equity narrative; caution when cross-asset contagion collapses or turns adversarial while equity narrative heat remains elevated. Synthetic proxy (live cross-asset monitor reserved).

- [ ] **Real-Time WebSocket Multi-Source Sentiment Aggregation Latency Overlay**.
  Preferred columns: `wms_latency_ms`, `wms_sources_ok`, `wms_boost`, `wms_reason`.
  Soft boost when WebSocket multi-source sentiment aggregation latency remains low and sources healthy into a confirming narrative; caution on high latency, source dropouts, or fallback to polling. Synthetic proxy (live dashboard telemetry reserved).

- [ ] **Cross-Venue Prediction Market Liquidity Depth Overlay**.
  Preferred columns: `cpd_depth`, `cpd_basis_bps`, `cpd_boost`, `cpd_reason`.
  Soft boost when cross-venue (Kalshi + Polymarket) prediction-market liquidity depth supports tight basis into a confirming narrative; caution on thin depth or adverse basis. Synthetic proxy (live multi-venue prediction-market feed reserved).

---

## Completed (moved to CHANGELOG)

- [x] **SEC Filing Structured Extraction Latency & Completeness Overlay** (v2.65.0, 2026-10-17). Preferred columns: `sec_latency_s`, `sec_completeness`, `sec_boost`, `sec_reason`.

- [x] **Listed Event-Contract Book Depth vs Offshore Prediction-Market Basis Overlay** (v2.64.0, 2026-10-16). Preferred columns: `lec_basis_bps`, `lec_listed_depth`, `lec_boost`, `lec_reason`.

- [x] **Multi-Agent Debate Consensus Strength Overlay** (v2.63.0, 2026-10-15). Preferred columns: `mad_consensus`, `mad_disagreement`, `mad_boost`, `mad_reason`.

- [x] **Always-On AI Agent Research Freshness & Workflow Completion Overlay** (v2.62.0, 2026-10-14). Preferred columns: `agt_fresh_s`, `agt_workflow_pct`, `agt_boost`, `agt_reason`.

- [x] **AIS Maritime Traffic & Port Congestion Overlay** (v2.61.0, 2026-10-13). Preferred columns: `ais_congestion`, `ais_wait_hrs`, `ais_boost`, `ais_reason`.
- [x] **Domain-Tuned Financial LLM vs General LLM Sentiment Gap Overlay** (v2.60.0, 2026-10-12). Preferred columns: `flm_sent`, `flm_gen_gap`, `flm_boost`, `flm_reason`.
- [x] **Satellite Imagery / Geospatial Physical Activity Overlay** (v2.59.0, 2026-10-11). Preferred columns: `sat_fill`, `sat_delta`, `sat_boost`, `sat_reason`.
- [x] **Agentic Brokerage Account Flow & Penetration Overlay** (v2.58.0, 2026-10-10). Preferred columns: `agt_flow_share`, `agt_tool_intensity`, `agt_boost`, `agt_reason`.
