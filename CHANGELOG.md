## v2.74.1 (2026-10-28)

- Autonomous research & evolution cycle against main (v2.74.0). Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard). Nothing removed from the roadmap. Added four new high-value overlays to FUTURE-IMPROVEMENTS.md (two High Priority: Agentic Prediction-Market Trade Execution Latency & Fill Quality Overlay, Crowdsourced Earnings Estimate Revision Cascade Velocity Overlay; two Medium Priority: Finance Podcast & Long-Form Audio Transcript Sentiment Velocity Overlay, On-Chain Tokenized Equity Smart-Money Wallet Clustering Overlay). Version strings synchronized to 2.74.1.

## v2.74.0 (2026-10-27)

- Fully implemented **Agentic MCP Tool-Call Chain Latency & Success Rate Overlay** (`sie/agentic_mcp_tool_call_latency.py`).
  Columns: `mcp_latency_ms`, `mcp_success_rate`, `mcp_boost`, `mcp_reason`.
  Soft boost when agentic research workflows show low tool-call latency and high success/completion rate against financial MCP servers (Distilla, Equibles, Alpha Vantage MCP, etc.) into a confirming narrative; caution on elevated latency, tool failures, or incomplete chains while narrative heat remains elevated.
  Wired through analyzer, CLI (`--no-agentic-mcp-tool-call-latency`), config, and Streamlit dashboard.
  Deterministic synthetic proxy (live MCP telemetry reserved).
  Removed from FUTURE-IMPROVEMENTS.md High Priority.
  Asset: [agentic_mcp_tool_call_latency_v2.74.0.svg](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/agentic_mcp_tool_call_latency_v2.74.0.svg).

## v2.73.1 (2026-10-27)

- Autonomous research & evolution cycle against main (v2.73.0). Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard). Nothing removed from the roadmap. Added four new high-value overlays to FUTURE-IMPROVEMENTS.md (one High Priority: AI Multi-Model Council Forecast vs Prediction Market Probability Basis Overlay; two Medium Priority: Equibles MCP Full-Text Filing & Transcript Extraction Completeness & Latency Overlay, Graded AI Verdict Hit-Rate Cascade on Prediction Markets Overlay; one Long-Term: Sports Prediction Market Official Data Partnership Spillover Narrative Contagion Overlay). Version strings synchronized to 2.73.1.

## v2.73.0 (2026-10-26)

- Fully implemented **Expert Network Call Novelty & Sentiment Velocity Overlay** (`sie/expert_network_call_novelty.py`).
  Columns: `enc_novelty`, `enc_sent_vel`, `enc_boost`, `enc_reason`.
  Soft boost when high-novelty expert-network (Tegus/GLG-style) call transcripts exhibit constructive sentiment velocity confirming a narrative into technical strength; caution on low-novelty or adverse expert sentiment while narrative heat remains elevated.
  Wired through analyzer, CLI (`--no-expert-network-call-novelty`), config, and Streamlit dashboard.
  Deterministic synthetic proxy (live expert-network feed reserved).
  Removed from FUTURE-IMPROVEMENTS.md High Priority.
  Asset: [expert_network_call_novelty_v2.73.0.svg](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/expert_network_call_novelty_v2.73.0.svg).

## v2.72.1 (2026-10-26)

- Autonomous research & evolution cycle against main (v2.72.0). Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard). Nothing removed from the roadmap. Added four new high-value overlays to FUTURE-IMPROVEMENTS.md (two High Priority: Hiring Velocity & Employee Outlook Sentiment Overlay, Short Interest & Fails-to-Deliver Squeeze Pressure Overlay; two Medium Priority: App Download & Consumer Engagement Velocity Overlay, Prediction-Market Agent Signal Cascade Velocity Overlay). Version strings synchronized to 2.72.1.

## v2.72.0 (2026-10-25)

- Fully implemented **Signed Options Flow Toxicity & Informed Trading Probability Overlay** (`sie/signed_options_flow_toxicity.py`).
  Columns: `oft_toxicity`, `oft_informed_prob`, `oft_boost`, `oft_reason`.
  Soft boost when signed OPRA flow (customer buys/sells) shows low toxicity and constructive informed-trading probability into a confirming narrative; caution on elevated toxicity or adverse informed flow while narrative heat stays elevated.
  Wired through analyzer, CLI (`--no-signed-options-flow-toxicity`), config, and Streamlit dashboard.
  Deterministic synthetic proxy (live signed options-flow feed reserved).
  Removed from FUTURE-IMPROVEMENTS.md High Priority.
  Asset: [signed_options_flow_toxicity_v2.72.0.svg](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/signed_options_flow_toxicity_v2.72.0.svg).

## v2.71.1 (2026-10-25)

- Autonomous research & evolution cycle against main (v2.71.0). Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard). Nothing removed from the roadmap. Added four new high-value overlays to FUTURE-IMPROVEMENTS.md (two High Priority: Truth Social Influential Political Account Narrative Velocity Overlay, Adanos Unified Social + Prediction-Market Buzz Velocity Overlay; two Medium Priority: Multi-LLM Ensemble Financial Headline Sentiment Divergence Overlay, Streamlit st.fragment Live Market Pulse Auto-Refresh Overlay). Version strings synchronized to 2.71.1.

## v2.71.0 (2026-10-24)

- Fully implemented **Unified Real-Time Multi-Source Narrative Freshness Overlay** (`sie/unified_multi_source_narrative_freshness.py`).
  Columns: `ums_fresh_s`, `ums_sources_ok`, `ums_boost`, `ums_reason`.
  Soft boost when unified multi-source (news, X cashtags, SEC filings, Form 4, congressional disclosures) remains fresh and constructively aligned into a confirming narrative; caution on stale sources or adverse clustering while narrative heat stays elevated.
  Wired through analyzer, CLI (`--no-unified-multi-source-narrative-freshness`), config, and Streamlit dashboard.
  Deterministic synthetic proxy (live multi-source aggregator reserved).
  Removed from FUTURE-IMPROVEMENTS.md High Priority.
  Asset: [unified_multi_source_narrative_freshness_v2.71.0.svg](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/unified_multi_source_narrative_freshness_v2.71.0.svg).

## v2.70.1 (2026-10-24)

- Autonomous research & evolution cycle against main (v2.70.0). Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard). Nothing removed from the roadmap. Added five new high-value overlays to FUTURE-IMPROVEMENTS.md (three High Priority: Dark Pool / Off-Exchange Institutional Block Print Intensity & Informed Flow Overlay, Real-Time Earnings Call Transcript Sentiment Velocity vs Pre-Call Narrative Overlay, Gamma Exposure (GEX) Regime & Dealer Hedging Pressure Overlay; two Medium Priority: Congressional Trade Disclosure Clustering & Timing Alpha Overlay, Web Traffic & App Engagement Velocity as Leading Demand Proxy Overlay). Version strings synchronized to 2.70.1.

## v2.70.0 (2026-10-23)

- Fully implemented **Agent-Generated Research Memo Cascade Velocity Overlay** (`sie/agent_generated_memo_cascade.py`).
  Columns: `agc_vel`, `agc_memo_share`, `agc_boost`, `agc_reason`.
  Soft boost when high-velocity cascade of agent-generated research memos (AlphaSense SuperAnalyst-style always-on workflows) confirms a narrative into technical strength; caution when cascade collapses or turns adversarial while human narrative heat remains elevated.
  Wired through analyzer, CLI (`--no-agent-generated-memo-cascade`), config, and Streamlit dashboard.
  Deterministic synthetic proxy (live agent-memo monitor reserved).
  Removed from FUTURE-IMPROVEMENTS.md High Priority.
  Asset: [agent_generated_memo_cascade_v2.70.0.svg](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/agent_generated_memo_cascade_v2.70.0.svg).
