# Future Improvements \u2014 Stock Intelligence Engine

**Last updated:** 2026-10-24
**Current version baseline:** v2.71.0

This file is the single source of truth for the open roadmap.
Items that are fully implemented and wired (analyzer + CLI + config + dashboard) are removed here and recorded in CHANGELOG.md + README Recent Edits.

---

## High Priority

- [ ] **Signed Options Flow Toxicity & Informed Trading Probability Overlay**.
  Preferred columns: `oft_toxicity`, `oft_informed_prob`, `oft_boost`, `oft_reason`.
  Soft boost when signed OPRA flow (customer buys/sells) shows low toxicity and constructive informed-trading probability into a confirming narrative; caution on elevated toxicity or adverse informed flow while narrative heat remains elevated. Synthetic proxy (live signed options-flow feed reserved).

- [ ] **Expert Network Call Novelty & Sentiment Velocity Overlay**.
  Preferred columns: `enc_novelty`, `enc_sent_vel`, `enc_boost`, `enc_reason`.
  Soft boost when high-novelty expert-network (Tegus/GLG-style) call transcripts exhibit constructive sentiment velocity confirming a narrative into technical strength; caution on low-novelty or adverse expert sentiment while narrative heat remains elevated. Synthetic proxy (live expert-network feed reserved).

- [ ] **Agentic MCP Tool-Call Chain Latency & Success Rate Overlay**.
  Preferred columns: `mcp_latency_ms`, `mcp_success_rate`, `mcp_boost`, `mcp_reason`.
  Soft boost when agentic research workflows show low tool-call latency and high success/completion rate against financial MCP servers (Distilla, Equibles, Alpha Vantage MCP, etc.) into a confirming narrative; caution on elevated latency, tool failures, or incomplete chains while narrative heat remains elevated. Synthetic proxy (live MCP telemetry reserved).

- [ ] **Tokenized Equity Continuous Pricing Premium vs Traditional Session Close Basis Overlay**.
  Preferred columns: `tep_basis_bps`, `tep_24_5_vol_share`, `tep_boost`, `tep_reason`.
  Soft boost when on-chain/tokenized equity continuous pricing (Robinhood, Ondo, MarketVector 24/5 indexes, etc.) shows a rich constructive premium and elevated 24/5 volume share into a confirming narrative; caution on adverse or collapsing continuous basis while narrative heat remains elevated. Synthetic proxy (live tokenized equity feed reserved).

- [ ] **Autonomous AI Agent Brokerage Order-Flow Share Overlay**.
  Preferred columns: `aaf_share`, `aaf_intensity`, `aaf_boost`, `aaf_reason`.
  Soft boost when the share of order flow originating from autonomous AI agents (Robinhood Agents, broker MCP-connected agents, eToro agents) rises constructively into a confirming narrative; caution when agent-driven flow collapses or turns adverse while human narrative heat stays elevated. Synthetic proxy (live agent-brokerage telemetry reserved).

- [ ] **Cross-Source Narrative Contradiction Density & Honesty Score Overlay**.
  Preferred columns: `ncd_density`, `ncd_honesty`, `ncd_boost`, `ncd_reason`.
  Soft boost when low contradiction density across news, X, filings, expert notes and agent memos produces a high honesty score confirming a narrative; caution on rising contradiction density or low honesty while narrative heat remains elevated. Synthetic proxy (live multi-source contradiction detector reserved).

- [ ] **Physical Commodity Trade-Flow & Vessel Activity Equity Mapping Overlay**.
  Preferred columns: `ctf_activity`, `ctf_delta`, `ctf_boost`, `ctf_reason`.
  Soft boost when elevated or improving physical commodity trade flows / vessel activity (Kpler-style mapping to public equities) confirms operational strength into a narrative; caution on deteriorating physical activity while narrative heat remains elevated. Synthetic proxy (live commodity trade-flow feed reserved).

- [ ] **Prediction-Market Semantic Cluster Arbitrage Basis Overlay**.
  Preferred columns: `pmc_basis_bps`, `pmc_cluster_strength`, `pmc_boost`, `pmc_reason`.
  Soft boost when agentic semantic clustering of related prediction-market contracts reveals a rich constructive arbitrage basis into a confirming narrative; caution on collapsing basis or weak cluster consistency while narrative heat remains elevated. Synthetic proxy (live prediction-market semantic graph reserved).

- [ ] **Reddit WallStreetBets & Financial Subreddit Mention Cascade Velocity Overlay**.
  Preferred columns: `rws_vel`, `rws_mention_share`, `rws_boost`, `rws_reason`.
  Soft boost when high-velocity constructive mention cascades on r/wallstreetbets, r/stocks and related financial subreddits confirm a narrative into technical strength; caution when cascade collapses or turns adversarial while narrative heat remains elevated. Synthetic proxy (live Reddit API / PRAW feed reserved).

- [ ] **Prediction-Market Firm-Level KPI Probability vs Analyst Consensus Basis Overlay**.
  Preferred columns: `kpi_basis_bps`, `kpi_market_prob`, `kpi_boost`, `kpi_reason`.
  Soft boost when Kalshi/Polymarket-style prediction-market implied probabilities for firm KPIs (revenue growth, margin, beat probability) show a rich constructive basis versus street consensus into a confirming narrative; caution on adverse or collapsing basis while narrative heat remains elevated. Synthetic proxy (live KPI-market feed reserved).

- [ ] **Live Insider Trading Cluster Significance & Direct Ownership Overlay**.
  Preferred columns: `ins_cluster_sig`, `ins_direct_pct`, `ins_boost`, `ins_reason`.
  Soft boost when high-significance cluster of direct open-market insider purchases (Form 4) aligns constructively with narrative into technical strength; caution on cluster selling or low direct ownership while narrative heat remains elevated. Synthetic proxy (live EDGAR Form 4 cluster detector reserved).

- [ ] **Agentic Research Citation Density & Source Authenticity Overlay**.
  Preferred columns: `arc_density`, `arc_authenticity`, `arc_boost`, `arc_reason`.
  Soft boost when agent-generated research memos and workflows exhibit high citation density to primary sources with strong authenticity scores confirming a narrative; caution on low citation density or synthetic/contaminated sources while narrative heat remains elevated. Synthetic proxy (live agent-citation monitor reserved).

- [ ] **Dark Pool / Off-Exchange Institutional Block Print Intensity & Informed Flow Overlay**.
  Preferred columns: `dp_intensity`, `dp_informed_bias`, `dp_boost`, `dp_reason`.
  Soft boost when elevated off-exchange block print intensity shows constructive informed institutional bias into a confirming narrative; caution on adverse or collapsing dark-pool intensity while narrative heat remains elevated. Synthetic proxy (live dark-pool / ATS feed reserved).

- [ ] **Real-Time Earnings Call Transcript Sentiment Velocity vs Pre-Call Narrative Overlay**.
  Preferred columns: `ect_sent_vel`, `ect_divergence`, `ect_boost`, `ect_reason`.
  Soft boost when live earnings-call transcript sentiment velocity diverges constructively from pre-call narrative heat into technical strength; caution on adverse divergence or sentiment collapse while narrative heat remains elevated. Synthetic proxy (live transcript feed reserved).

- [ ] **Gamma Exposure (GEX) Regime & Dealer Hedging Pressure Overlay**.
  Preferred columns: `gex_regime`, `gex_pressure`, `gex_boost`, `gex_reason`.
  Soft boost when gamma exposure regime indicates constructive dealer hedging pressure confirming a narrative; caution on adverse GEX regime or hedging pressure while narrative heat remains elevated. Synthetic proxy (live GEX / options positioning feed reserved).

---

## Medium Priority

- [ ] **Congressional Trade Disclosure Clustering & Timing Alpha Overlay**.
  Preferred columns: `cong_cluster`, `cong_timing`, `cong_boost`, `cong_reason`.
  Soft boost when clustered congressional disclosure trades show constructive timing alpha aligning with narrative; caution on adverse clusters or poor timing while narrative heat remains elevated. Synthetic proxy (live congressional disclosure feed reserved).

- [ ] **Web Traffic & App Engagement Velocity as Leading Demand Proxy Overlay**.
  Preferred columns: `web_vel`, `app_engagement`, `web_boost`, `web_reason`.
  Soft boost when rising web traffic and app engagement velocity for consumer-facing issuers confirms operational demand into a narrative; caution on collapsing engagement while narrative heat remains elevated. Synthetic proxy (live web/app analytics feed reserved).

---

## Completed (moved to CHANGELOG)

- [x] **Unified Real-Time Multi-Source Narrative Freshness Overlay** (v2.71.0, 2026-10-24). Preferred columns: `ums_fresh_s`, `ums_sources_ok`, `ums_boost`, `ums_reason`.

- [x] **Agent-Generated Research Memo Cascade Velocity Overlay** (v2.70.0, 2026-10-23). Preferred columns: `agc_vel`, `agc_memo_share`, `agc_boost`, `agc_reason`.

- [x] **Kalshi Regulated vs Polymarket Offshore Earnings Beat Probability Basis Overlay** (v2.69.0, 2026-10-22). Preferred columns: `kpm_basis_bps`, `kpm_kalshi_prob`, `kpm_boost`, `kpm_reason`.

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
