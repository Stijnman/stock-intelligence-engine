# Changelog

## v2.68.1 (2026-10-22)

- Autonomous research & evolution cycle against main (v2.68.0). Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard). Nothing removed from the roadmap. Added five new high-value overlays to FUTURE-IMPROVEMENTS.md High Priority (Tokenized Equity Continuous Pricing Premium vs Traditional Session Close Basis, Autonomous AI Agent Brokerage Order-Flow Share, Cross-Source Narrative Contradiction Density & Honesty Score, Physical Commodity Trade-Flow & Vessel Activity Equity Mapping, Prediction-Market Semantic Cluster Arbitrage Basis). Version strings synchronized to 2.68.1.

v2.68.0 (2026-10-21)

- Fully implemented **YouTube Financial Creator Transcript & Comment Sentiment Velocity Overlay** (`sie/youtube_creator_sentiment.py`).
  Columns: `ytc_vel`, `ytc_sent`, `ytc_boost`, `ytc_reason`.
  Soft boost when high-velocity authentic positive sentiment from financial YouTube creator transcripts and comments confirms a narrative into technical strength; caution when creator sentiment collapses or turns adversarial while human narrative heat remains elevated.
  Wired through analyzer, CLI (`--no-youtube-creator`), config, and Streamlit dashboard.
  Deterministic synthetic proxy (live YouTube transcript + comment feed reserved).
  Removed from FUTURE-IMPROVEMENTS.md High Priority.
  Asset: [youtube_creator_sentiment_v2.68.0.svg](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/youtube_creator_sentiment_v2.68.0.svg).

## v2.67.0 (2026-10-20)

- Fully implemented **RAG-Extracted Earnings Guidance Novelty & Hedge Density Overlay** (`sie/rag_earnings_guidance.py`).
  Columns: `rgn_novelty`, `rgn_hedge_density`, `rgn_boost`, `rgn_reason`.
  Soft boost when RAG-grounded extraction of earnings-call transcripts surfaces high-novelty guidance language with low hedge density into a confirming narrative; caution on boilerplate or heavily hedged guidance while narrative heat stays elevated.
  Wired through analyzer, CLI (`--no-rag-earnings-guidance`), config, and Streamlit dashboard.
  Deterministic synthetic proxy (live transcript RAG reserved).
  Removed from FUTURE-IMPROVEMENTS.md High Priority.
  Asset: [rag_earnings_guidance_v2.67.0.svg](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/rag_earnings_guidance_v2.67.0.svg).

## v2.66.2 (2026-10-20)

- Autonomous research & evolution cycle against main (v2.66.1). Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard). Nothing removed from the roadmap. Added four new high-value overlays to FUTURE-IMPROVEMENTS.md (Agentic MCP Tool-Call Chain Latency & Success Rate, Podcast Financial Narrative Velocity & Entity Sentiment, Sell-Side Broker Research Note Novelty & Recommendation Revision Velocity, Explainable AI Score Attribution Stability & Feature Drift). Version strings synchronized to 2.66.2.

## v2.66.1 (2026-10-19)

- Autonomous research & evolution cycle against main (v2.66.0). Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard). Nothing removed from the roadmap. Added five new high-value overlays to FUTURE-IMPROVEMENTS.md (Signed Options Flow Toxicity & Informed Trading Probability, Expert Network Call Novelty & Sentiment Velocity, Multi-Model Ensemble Sentiment Disagreement Rate, Supply-Chain Bill-of-Lading Anomaly & Delay Velocity, Decentralized Oracle Attested Alt-Data Provenance). Version strings synchronized to 2.66.1.

## v2.66.0 (2026-10-18)

- Fully implemented **Agentic Narrative Contagion Velocity Overlay** (`sie/agentic_narrative_contagion.py`).
  Columns: `anc_vel`, `anc_agent_share`, `anc_boost`, `anc_reason`.
  Soft boost when high-velocity narrative propagation through autonomous AI agents (agent-to-agent contagion, generative memo cascades) confirms a narrative into technical strength; caution when agent-driven contagion collapses or turns adversarial while human narrative heat remains elevated.
  Wired through analyzer, CLI, config, and Streamlit.
  Deterministic synthetic proxy (live agent-network monitor reserved).
  Removed from FUTURE-IMPROVEMENTS.md High Priority.
  Asset: [agentic_narrative_contagion_v2.66.0.svg](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/agentic_narrative_contagion_v2.66.0.svg).

## v2.65.1 (2026-10-18)

- Autonomous research & evolution cycle against main (v2.65.0). Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard). Nothing removed from the roadmap. Added five new high-value overlays to FUTURE-IMPROVEMENTS.md (Unified Real-Time Multi-Source Narrative Freshness, CFPB Consumer Complaint Topic Cluster & Sentiment Velocity, Short-Form Video Financial Creator Cascade Velocity, Cross-Agent Research Consensus Strength, Streamlit Multi-Fragment Parallel Refresh Health). Version strings synchronized to 2.65.1.

## v2.65.0 (2026-10-17)

- Fully implemented **SEC Filing Structured Extraction Latency & Completeness Overlay** (`sie/sec_filing_extraction.py`).
  Columns: `sec_latency_s`, `sec_completeness`, `sec_boost`, `sec_reason`.
  Soft boost when structured 10-K/10-Q/8-K extraction latency is low and completeness high into a confirming narrative; caution on delayed or incomplete agent-facing filing parses while narrative heat remains elevated.
  Wired through analyzer, CLI, config, and Streamlit.
  Deterministic synthetic proxy (live filing-monitor feed reserved).
  Removed from FUTURE-IMPROVEMENTS.md High Priority.
  Asset: [sec_filing_extraction_v2.65.0.svg](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/sec_filing_extraction_v2.65.0.svg).
