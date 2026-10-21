# Future Improvements — Stock Intelligence Engine

**Last updated:** 2026-10-21
**Current version baseline:** v2.68.0

This file is the single source of truth for the open roadmap.
Items that are fully implemented and wired (analyzer + CLI + config + dashboard) are removed here and recorded in CHANGELOG.md + README Recent Edits.

---

## High Priority

- [ ] **Kalshi Regulated vs Polymarket Offshore Earnings Beat Probability Basis Overlay**.
  Preferred columns: `kpm_basis_bps`, `kpm_kalshi_prob`, `kpm_boost`, `kpm_reason`.
  Soft boost when regulated Kalshi earnings-beat probability shows a rich constructive basis versus offshore Polymarket into a confirming narrative; caution on adverse or collapsing basis while narrative heat remains elevated. Synthetic proxy (live Kalshi + Polymarket feed reserved).

- [ ] **Agent-Generated Research Memo Cascade Velocity Overlay**.
  Preferred columns: `agc_vel`, `agc_memo_share`, `agc_boost`, `agc_reason`.
  Soft boost when high-velocity cascade of agent-generated research memos (AlphaSense SuperAnalyst-style always-on workflows) confirms a narrative into technical strength; caution when cascade collapses or turns adversarial while human narrative heat remains elevated. Synthetic proxy (live agent-memo monitor reserved).

- [ ] **Unified Real-Time Multi-Source Narrative Freshness Overlay**.
  Preferred columns: `ums_fresh_s`, `ums_sources_ok`, `ums_boost`, `ums_reason`.
  Soft boost when unified multi-source (news, X cashtags, SEC filings, Form 4, congressional disclosures) remains fresh and constructively aligned into a confirming narrative; caution on stale sources or adverse clustering while narrative heat stays elevated. Synthetic proxy (live multi-source aggregator reserved).

- [ ] **Signed Options Flow Toxicity & Informed Trading Probability Overlay**.
  Preferred columns: `oft_toxicity`, `oft_informed_prob`, `oft_boost`, `oft_reason`.
  Soft boost when signed OPRA flow (customer buys/sells) shows low toxicity and constructive informed-trading probability into a confirming narrative; caution on elevated toxicity or adverse informed flow while narrative heat remains elevated. Synthetic proxy (live signed options-flow feed reserved).

- [ ] **Expert Network Call Novelty & Sentiment Velocity Overlay**.
  Preferred columns: `enc_novelty`, `enc_sent_vel`, `enc_boost`, `enc_reason`.
  Soft boost when high-novelty expert-network (Tegus/GLG-style) call transcripts exhibit constructive sentiment velocity confirming a narrative into technical strength; caution on low-novelty or adverse expert sentiment while narrative heat remains elevated. Synthetic proxy (live expert-network feed reserved).

- [ ] **Agentic MCP Tool-Call Chain Latency & Success Rate Overlay**.
  Preferred columns: `mcp_latency_ms`, `mcp_success_rate`, `mcp_boost`, `mcp_reason`.
  Soft boost when agentic research workflows show low tool-call latency and high success/completion rate against financial MCP servers (Distilla, Equibles, Alpha Vantage MCP, etc.) into a confirming narrative; caution on elevated latency, tool failures, or incomplete chains while narrative heat remains elevated. Synthetic proxy (live MCP telemetry reserved).

---

## Completed (moved to CHANGELOG)

- [x] **YouTube Financial Creator Transcript & Comment Sentiment Velocity Overlay** (v2.68.0, 2026-10-21). Preferred columns: `ytc_vel`, `ytc_sent`, `ytc_boost`, `ytc_reason`.

- [x] **RAG-Extracted Earnings Guidance Novelty & Hedge Density Overlay** (v2.67.0, 2026-10-20). Preferred columns: `rgn_novelty`, `rgn_hedge_density`, `rgn_boost`, `rgn_reason`.

- [x] **Agentic Narrative Contagion Velocity Overlay** (v2.66.0, 2026-10-18). Preferred columns: `anc_vel`, `anc_agent_share`, `anc_boost`, `anc_reason`.

- [x] **SEC Filing Structured Extraction Latency & Completeness Overlay** (v2.65.0, 2026-10-17). Preferred columns: `sec_latency_s`, `sec_completeness`, `sec_boost`, `sec_reason`.

- [x] **Listed Event-Contract Book Depth vs Offshore Prediction-Market Basis Overlay** (v2.64.0, 2026-10-16). Preferred columns: `lec_basis_bps`, `lec_listed_depth`, `lec_boost`, `lec_reason`.

- [x] **Multi-Agent Debate Consensus Strength Overlay** (v2.63.0, 2026-10-15). Preferred columns: `mad_consensus`, `mad_disagreement`, `mad_boost`, `mad_reason`.

- [x] **Always-On AI Agent Research Freshness & Workflow Completion Overlay** (v2.62.0, 2026-10-14). Preferred columns: `agt_fresh_s`, `agt_workflow_pct`, `agt_boost`, `agt_reason`.

- [x] **AIS Maritime Traffic & Port Congestion Overlay** (v2.61.0, 2026-10-13). Preferred columns: `ais_congestion`, `ais_wait_hrs`, `ais_boost`, `ais_reason`.
- [x] **Domain-Tuned Financial LLM vs General LLM Sentiment Gap Overlay** (v2.60.0, 2026-10-12). Preferred columns: `flm_sent`, `flm_gen_gap`, `flm_boost`, `flm_reason`.
- [x] **Satellite Imagery / Geospatial Physical Activity Overlay** (v2.59.0, 2026-10-11). Preferred columns: `sat_fill`, `sat_delta`, `sat_boost`, `sat_reason`.
- [x] **Agentic Brokerage Account Flow & Penetration Overlay** (v2.58.0, 2026-10-10). Preferred columns: `agt_flow_share`, `agt_tool_intensity`, `agt_boost`, `agt_reason`.
