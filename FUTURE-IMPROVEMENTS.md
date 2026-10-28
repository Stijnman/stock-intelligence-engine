# Future Improvements — Stock Intelligence Engine

**Last updated:** 2026-10-28
**Current version baseline:** v2.74.1

This file is the single source of truth for the open roadmap.
Items that are fully implemented and wired (analyzer + CLI + config + dashboard) are removed here and recorded in CHANGELOG.md + README Recent Edits.

---

## High Priority

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

- [ ] **Truth Social Influential Political Account Narrative Velocity Overlay**.
  Preferred columns: `ts_vel`, `ts_impact`, `ts_boost`, `ts_reason`.
  Soft boost when high-velocity posts from market-moving Truth Social accounts (via Truth API or equivalent) confirm a constructive narrative into technical strength; caution on adverse or collapsing velocity while narrative heat remains elevated. Synthetic proxy (live Truth Social feed reserved).

- [ ] **Adanos Unified Social + Prediction-Market Buzz Velocity Overlay**.
  Preferred columns: `ads_buzz_vel`, `ads_mention_share`, `ads_boost`, `ads_reason`.
  Soft boost when high-velocity constructive buzz aggregated from Reddit, X, and Polymarket via unified APIs confirms a narrative into technical strength; caution when buzz collapses or turns adversarial while narrative heat remains elevated. Synthetic proxy (live Adanos-style multi-source feed reserved).

- [ ] **Hiring Velocity & Employee Outlook Sentiment Overlay**.
  Preferred columns: `hiv_vel`, `hiv_outlook`, `hiv_boost`, `hiv_reason`.
  Soft boost when rising open job postings and constructive employee business outlook (Glassdoor-style) velocity confirm operational confidence into a narrative into technical strength; caution on collapsing hiring or adverse employee outlook while narrative heat remains elevated. Synthetic proxy (live hiring/employee-outlook feed reserved).

- [ ] **Short Interest & Fails-to-Deliver Squeeze Pressure Overlay**.
  Preferred columns: `sis_short_int`, `sis_squeeze_score`, `sis_boost`, `sis_reason`.
  Soft boost when declining short interest, elevated fails-to-deliver, or rising squeeze score from off-exchange volume aligns constructively with narrative into technical strength; caution on rising short interest or collapsing squeeze pressure while narrative heat remains elevated. Synthetic proxy (live short-interest / FTD feed reserved).

- [ ] **AI Multi-Model Council Forecast vs Prediction Market Probability Basis Overlay**.
  Preferred columns: `aic_basis_bps`, `aic_council_prob`, `aic_boost`, `aic_reason`.
  Soft boost when multi-model AI council (Grok, Claude, GPT, Gemini ensemble) sealed forecasts show a rich constructive basis versus Kalshi/Polymarket implied probabilities into a confirming narrative; caution on adverse or collapsing basis while narrative heat remains elevated. Synthetic proxy (live AI-council + prediction-market feed reserved).

- [ ] **Agentic Prediction-Market Trade Execution Latency & Fill Quality Overlay**.
  Preferred columns: `apm_latency_ms`, `apm_fill_quality`, `apm_boost`, `apm_reason`.
  Soft boost when autonomous AI agents executing trades on prediction markets (Unhedged-style MCP servers, Octagon agents) show low execution latency and high fill quality into a confirming narrative; caution on elevated latency, poor fills, or incomplete agent workflows while narrative heat remains elevated. Synthetic proxy (live agentic prediction-market execution telemetry reserved).

- [ ] **Crowdsourced Earnings Estimate Revision Cascade Velocity Overlay**.
  Preferred columns: `cee_rev_vel`, `cee_consensus_div`, `cee_boost`, `cee_reason`.
  Soft boost when high-velocity constructive revisions from crowdsourced estimate platforms (Estimize-style) produce a rich positive divergence versus street consensus into a confirming narrative; caution on adverse revisions, collapsing velocity, or consensus convergence while narrative heat remains elevated. Synthetic proxy (live crowdsourced estimate feed reserved).

---

## Medium Priority

- [ ] **Congressional Trade Disclosure Clustering & Timing Alpha Overlay**.
  Preferred columns: `cong_cluster`, `cong_timing`, `cong_boost`, `cong_reason`.
  Soft boost when clustered congressional disclosure trades show constructive timing alpha aligning with narrative; caution on adverse clusters or poor timing while narrative heat remains elevated. Synthetic proxy (live congressional disclosure feed reserved).

- [ ] **Web Traffic & App Engagement Velocity as Leading Demand Proxy Overlay**.
  Preferred columns: `web_vel`, `app_engagement`, `web_boost`, `web_reason`.
  Soft boost when rising web traffic and app engagement velocity for consumer-facing issuers confirms operational demand into a narrative; caution on collapsing engagement while narrative heat remains elevated. Synthetic proxy (live web/app analytics feed reserved).

- [ ] **Multi-LLM Ensemble Financial Headline Sentiment Divergence Overlay**.
  Preferred columns: `mle_divergence`, `mle_consensus`, `mle_boost`, `mle_reason`.
  Soft boost when low divergence across FinBERT, general LLM, and specialized models (Vicuna-style) produces high consensus confirming a narrative; caution on rising ensemble divergence while narrative heat remains elevated. Synthetic proxy (live multi-LLM sentiment ensemble reserved).

- [ ] **Streamlit st.fragment Live Market Pulse Auto-Refresh Overlay**.
  Preferred columns: `stf_refresh_ms`, `stf_freshness`, `stf_boost`, `stf_reason`.
  Soft boost when Streamlit fragment-based live market pulse maintains sub-second freshness and constructive data alignment into a confirming narrative dashboard view; caution on stale fragments or elevated refresh latency while narrative heat remains elevated. Synthetic proxy (live Streamlit fragment telemetry reserved).

- [ ] **App Download & Consumer Engagement Velocity Overlay**.
  Preferred columns: `app_dl_vel`, `app_engagement`, `app_boost`, `app_reason`.
  Soft boost when rising app download velocity and constructive consumer engagement metrics for consumer-facing issuers confirm leading demand into a narrative into technical strength; caution on collapsing downloads or adverse engagement while narrative heat remains elevated. Synthetic proxy (live app-download analytics feed reserved).

- [ ] **Prediction-Market Agent Signal Cascade Velocity Overlay**.
  Preferred columns: `pma_vel`, `pma_agent_share`, `pma_boost`, `pma_reason`.
  Soft boost when high-velocity cascade of AI-agent signals derived from prediction-market probabilities (Public.com-style agentic brokerage triggers) confirms a narrative into technical strength; caution when cascade collapses or turns adversarial while narrative heat remains elevated. Synthetic proxy (live prediction-market agent telemetry reserved).

- [ ] **Equibles MCP Full-Text Filing & Transcript Extraction Completeness & Latency Overlay**.
  Preferred columns: `eqm_latency_ms`, `eqm_completeness`, `eqm_boost`, `eqm_reason`.
  Soft boost when Equibles-style MCP tool-calls for full-text SEC filings, speaker-labeled transcripts and Form 4 clusters show low latency and high completeness/citation density confirming a narrative; caution on elevated latency or incomplete extraction while narrative heat remains elevated. Synthetic proxy (live Equibles MCP telemetry reserved).

- [ ] **Graded AI Verdict Hit-Rate Cascade on Prediction Markets Overlay**.
  Preferred columns: `gav_hit_rate`, `gav_cascade_vel`, `gav_boost`, `gav_reason`.
  Soft boost when high historical hit-rate cascade of graded AI verdicts (OddsShift-style) on related prediction-market contracts confirms a narrative into technical strength; caution when hit-rate collapses or cascade turns adversarial while narrative heat remains elevated. Synthetic proxy (live graded-verdict tracker reserved).

- [ ] **Finance Podcast & Long-Form Audio Transcript Sentiment Velocity Overlay**.
  Preferred columns: `fpt_sent_vel`, `fpt_novelty`, `fpt_boost`, `fpt_reason`.
  Soft boost when finance podcasts, earnings deep-dive audio, and long-form expert interviews exhibit constructive sentiment velocity and high novelty confirming a narrative into technical strength; caution on adverse sentiment, low novelty, or collapsing audio attention while narrative heat remains elevated. Synthetic proxy (live podcast/audio transcript feed reserved).

- [ ] **On-Chain Tokenized Equity Smart-Money Wallet Clustering Overlay**.
  Preferred columns: `ote_cluster_strength`, `ote_flow_share`, `ote_boost`, `ote_reason`.
  Soft boost when clustered on-chain wallets (known smart-money / institutional addresses) show constructive accumulation share in tokenized equities into a confirming narrative; caution on distribution, weak clustering, or adverse flow while narrative heat remains elevated. Synthetic proxy (live on-chain tokenized equity wallet clustering reserved).

---

## Long-Term / Nice-to-Have

- [ ] **Sports Prediction Market Official Data Partnership Spillover Narrative Contagion Overlay**.
  Preferred columns: `spm_spillover`, `spm_contagion_vel`, `spm_boost`, `spm_reason`.
  Soft boost when official league partnerships (NBA-Kalshi/Polymarket style) and live event-contract volume create constructive spillover narrative contagion to related public equities; caution on adverse spillover or volume collapse while narrative heat remains elevated. Synthetic proxy (live sports-prediction spillover feed reserved).

---

## Completed (moved to CHANGELOG)

- [x] **Agentic MCP Tool-Call Chain Latency & Success Rate Overlay** (v2.74.0, 2026-10-27). Preferred columns: `mcp_latency_ms`, `mcp_success_rate`, `mcp_boost`, `mcp_reason`.

- [x] **Expert Network Call Novelty & Sentiment Velocity Overlay** (v2.73.0, 2026-10-26). Preferred columns: `enc_novelty`, `enc_sent_vel`, `enc_boost`, `enc_reason`.

- [x] **Signed Options Flow Toxicity & Informed Trading Probability Overlay** (v2.72.0, 2026-10-25). Preferred columns: `oft_toxicity`, `oft_informed_prob`, `oft_boost`, `oft_reason`.

- [x] **Unified Real-Time Multi-Source Narrative Freshness Overlay** (v2.71.0, 2026-10-24). Preferred columns: `ums_fresh_s`, `ums_sources_ok`, `ums_boost`, `ums_reason`.

- [x] **Agent-Generated Research Memo Cascade Velocity Overlay** (v2.70.0, 2026-10-23). Preferred columns: `agc_vel`, `agc_memo_share`, `agc_boost`, `agc_reason`.
