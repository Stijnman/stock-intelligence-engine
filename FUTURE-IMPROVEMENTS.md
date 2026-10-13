# Future Improvements — Stock Intelligence Engine

**Last updated:** 2026-10-13
**Current version baseline:** v2.61.0

This file is the single source of truth for the open roadmap.
Items that are fully implemented and wired (analyzer + CLI + config + dashboard) are removed here and recorded in CHANGELOG.md + README Recent Edits.

---

## High Priority

- [ ] **Listed Event-Contract Book Depth vs Offshore Prediction-Market Basis Overlay**.
  Preferred columns: `lec_basis_bps`, `lec_listed_depth`, `lec_boost`, `lec_reason`.
  Soft boost when listed event-contract book depth supports a rich basis versus offshore prediction markets into a confirming narrative; caution on thin listed depth with adverse basis.

- [ ] **Always-On AI Agent Research Freshness & Workflow Completion Overlay**.
  Preferred columns: `agt_fresh_s`, `agt_workflow_pct`, `agt_boost`, `agt_reason`.
  Soft boost when always-on agent research (SuperAnalyst-style continuous workflow execution, memo refresh, evidence reconciliation) is fresh and high-completion into a confirming narrative; caution when agent workflows stall or research age spikes while narrative heat remains elevated. Synthetic proxy (live agent-monitor feed reserved).

- [ ] **SEC Filing Structured Extraction Latency & Completeness Overlay**.
  Preferred columns: `sec_latency_s`, `sec_completeness`, `sec_boost`, `sec_reason`.
  Soft boost when structured 10-K/10-Q/8-K extraction latency is low and completeness high into a confirming narrative; caution on delayed or incomplete agent-facing filing parses. Synthetic proxy (live filing-monitor feed reserved).

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

---

## Long-Term / Nice-to-Have

- [ ] **European Consolidated Tape Liquidity Visibility Overlay**.
  Preferred columns: `ect_liq`, `ect_spread`, `ect_boost`, `ect_reason`.
  Soft boost when improved European consolidated-tape visibility and tighter spreads confirm narrative; caution on fragmented liquidity. Synthetic proxy reserved.

- [ ] **WebSocket Streaming Latency Attribution vs Polling Overlay**.
  Preferred columns: `ws_latency_ms`, `poll_delta_ms`, `ws_boost`, `ws_reason`.
  Soft boost when WebSocket streaming latency is materially lower than polling and supports real-time narrative confirmation; caution on persistent high streaming latency or fallback to polling. Synthetic proxy (live dashboard telemetry reserved).

---

## Completed (moved to CHANGELOG)

- [x] **AIS Maritime Traffic & Port Congestion Overlay** (v2.61.0, 2026-10-13). Preferred columns: `ais_congestion`, `ais_wait_hrs`, `ais_boost`, `ais_reason`.
- [x] **Domain-Tuned Financial LLM vs General LLM Sentiment Gap Overlay** (v2.60.0, 2026-10-12). Preferred columns: `flm_sent`, `flm_gen_gap`, `flm_boost`, `flm_reason`.
- [x] **Satellite Imagery / Geospatial Physical Activity Overlay** (v2.59.0, 2026-10-11). Preferred columns: `sat_fill`, `sat_delta`, `sat_boost`, `sat_reason`.
- [x] **Agentic Brokerage Account Flow & Penetration Overlay** (v2.58.0, 2026-10-10). Preferred columns: `agt_flow_share`, `agt_tool_intensity`, `agt_boost`, `agt_reason`.
