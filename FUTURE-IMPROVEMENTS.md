# Future Improvements — Stock Intelligence Engine

**Last updated:** 2026-10-11
**Current version baseline:** v2.58.1

This file is the single source of truth for the open roadmap.
Items that are fully implemented and wired (analyzer + CLI + config + dashboard) are removed here and recorded in CHANGELOG.md + README Recent Edits.

---

## High Priority

- [ ] **Domain-Tuned Financial LLM vs General LLM Sentiment Gap Overlay**.
  Preferred columns: `flm_sent`, `flm_gen_gap`, `flm_boost`, `flm_reason`.
  Soft boost when a domain-tuned financial LLM sentiment diverges constructively from a general LLM baseline into a confirming narrative; caution on adverse divergence.

- [ ] **Listed Event-Contract Book Depth vs Offshore Prediction-Market Basis Overlay**.
  Preferred columns: `lec_basis_bps`, `lec_listed_depth`, `lec_boost`, `lec_reason`.
  Soft boost when listed event-contract book depth supports a rich basis versus offshore prediction markets into a confirming narrative; caution on thin listed depth with adverse basis.

- [ ] **Satellite Imagery / Geospatial Physical Activity Overlay**.
  Preferred columns: `sat_fill`, `sat_delta`, `sat_boost`, `sat_reason`.
  Soft boost when rising physical activity proxies (parking-lot fill rates, oil-tank levels, night-light intensity, vessel counts) confirm a narrative; caution on sharp activity drops while narrative heat remains elevated. Synthetic proxy (live satellite feed reserved).

- [ ] **AIS Maritime Traffic & Port Congestion Overlay**.
  Preferred columns: `ais_congestion`, `ais_wait_hrs`, `ais_boost`, `ais_reason`.
  Soft boost when key-port congestion eases and vessel waiting times fall into a confirming narrative; caution on rising AIS congestion or extended wait hours. Synthetic proxy (live AIS feed reserved).

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

---

## Long-Term / Nice-to-Have

- [ ] **European Consolidated Tape Liquidity Visibility Overlay**.
  Preferred columns: `ect_liq`, `ect_spread`, `ect_boost`, `ect_reason`.
  Soft boost when improved European consolidated-tape visibility and tighter spreads confirm narrative; caution on fragmented liquidity. Synthetic proxy reserved.

---

## Completed (moved to CHANGELOG)

- [x] **Agentic Brokerage Account Flow & Penetration Overlay** (v2.58.0, 2026-10-10). Preferred columns: `agt_flow_share`, `agt_tool_intensity`, `agt_boost`, `agt_reason`.
