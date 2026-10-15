# Stock Intelligence Engine

**Connect market narratives to your watchlist.**  
**Confirm with technicals.**  
**Explain every signal.**

**v2.63.0** — October 2026 · Multi-Agent Debate Consensus Strength Overlay (fully wired) + Always-On AI Agent Research Freshness & Workflow Completion Overlay (fully wired) + AIS Maritime Traffic & Port Congestion Overlay (fully wired) + Domain-Tuned Financial LLM vs General LLM Sentiment Gap Overlay (fully wired) + Satellite Imagery / Geospatial Physical Activity Overlay (fully wired) + Agentic Brokerage Account Flow & Penetration Overlay (fully wired) + Index Reconstitution & Forced Passive-Flow Overlay (fully wired) + Rule 606 Retail Options Routing Overlay (fully wired) + Alternative-Data Provenance Overlay (fully wired) + Secondary Offering / ATM Dilution Velocity Overlay (fully wired) + Cross-Venue Tokenized-Share Basis / On-Chain Equity Premium Overlay (fully wired) + Job-Posting Skill-Mix + Retail Brokerage Order-Flow + App-Store Review Sentiment + Employee Outlook + Unusual Options + Rule 10b5-1 / Buyback + ETF AP Flow.

## Features

- **Multi-Agent Debate Consensus Strength Overlay** — Scores consensus strength and disagreement among specialized multi-agent debates (fundamental, narrative, options-flow agents). Soft boost when high consensus confirms a narrative; caution on high disagreement or rapid flip-flops. Fully integrated into analyzer (`include_multi_agent_debate`), CLI (`--no-multi-agent-debate`) and dashboard (`mad_*` columns).

- **Always-On AI Agent Research Freshness & Workflow Completion Overlay** — Scores freshness of always-on agent research (memo age, workflow completion %) from SuperAnalyst-style continuous workflow proxies. Soft boost when research is fresh and high-completion into a confirming narrative; caution when workflows stall or research age spikes. Fully integrated into analyzer (`include_agent_research_freshness`), CLI (`--no-agent-research-freshness`) and dashboard (`agt_*` columns).

- **AIS Maritime Traffic & Port Congestion Overlay** — Scores key-port congestion and vessel waiting times from AIS maritime traffic proxies. Soft boost when congestion eases and waiting times fall into a confirming narrative; caution on rising congestion or extended wait hours. Fully integrated into analyzer (`include_ais_maritime`), CLI (`--no-ais-maritime`) and dashboard (`ais_*` columns).

- **Domain-Tuned Financial LLM vs General LLM Sentiment Gap Overlay** — Scores divergence between domain-tuned financial LLM (FinBERT-style) and general LLM baseline. Soft boost on constructive gap into confirming narrative; caution on adverse gap. Fully integrated into analyzer (`include_fin_llm_gap`), CLI (`--no-fin-llm-gap`) and dashboard (`flm_*` columns).

- Real-time signals with narrative intelligence
- **Satellite Imagery / Geospatial Physical Activity Overlay** — Scores parking-lot fill, oil-tank levels, night-light intensity, vessel counts. Soft boost when rising physical activity confirms a narrative; caution on sharp drops. Fully integrated into analyzer (`include_satellite_imagery`), CLI (`--no-satellite-imagery`) and dashboard (`sat_*` columns).
- **Agentic Brokerage Account Flow & Penetration Overlay** — Scores share of order flow from agentic / autonomous brokerage accounts and tool/API intensity. Soft boost when high agentic flow + elevated tool intensity confirms the narrative; caution when agentic accounts fade while narrative heat remains elevated. Fully integrated into analyzer (`include_agentic_flow`), CLI (`--no-agentic-flow`) and dashboard (`agt_*` columns).
- **App-Store Review Sentiment & Complaint Velocity** — Fully integrated into analyzer, CLI (`--no-app-store-reviews`) and dashboard (`asr_*` columns).

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env   # add any API keys
python stock_intelligence_engine.py
streamlit run app.py
```

See config.yaml for watchlist and overlay toggles.

## Recent Edits & Version History

- **v2.63.0 (2026-10-15)**: Fully implemented **Multi-Agent Debate Consensus Strength Overlay** (`sie/multi_agent_debate.py`). Preferred columns: `mad_consensus`, `mad_disagreement`, `mad_boost`, `mad_reason`. Soft boost when specialized multi-agent debate reaches high consensus into a confirming narrative; caution on high disagreement or rapid flip-flops while narrative heat remains elevated. Wired through analyzer, CLI, config, and Streamlit. Deterministic synthetic proxy (live multi-agent orchestrator reserved). Removed from FUTURE-IMPROVEMENTS.md High Priority.

- **v2.62.1 (2026-10-15)**: Autonomous research & evolution cycle against main (v2.62.0). Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard). Nothing removed from the roadmap. Added five new high-value overlays to FUTURE-IMPROVEMENTS.md (Multi-Agent Debate Consensus Strength, Live Macro Event Narrative Spillover Velocity, Cross-Exchange Tokenized Equity Order-Book Depth, Streamlit Session-State Persistence & Crash Recovery, Earnings Call Speaker Sentiment Divergence). Version strings synchronized to **2.62.1**.

- **v2.62.0 (2026-10-14)**: Fully implemented **Always-On AI Agent Research Freshness & Workflow Completion Overlay** (`sie/agent_research_freshness.py`). Preferred columns: `agt_fresh_s`, `agt_workflow_pct`, `agt_boost`, `agt_reason`. Soft boost when always-on agent research is fresh and high workflow completion into a confirming narrative; caution when agent workflows stall or research age spikes while narrative heat remains elevated. Wired through analyzer, CLI, config, and Streamlit. Deterministic synthetic proxy (live agent-monitor feed reserved). Removed from FUTURE-IMPROVEMENTS.md High Priority.

- **v2.61.1 (2026-10-14)**: Autonomous research & evolution cycle against main (v2.61.0). Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard). Nothing removed from the roadmap. Added five new high-value overlays to FUTURE-IMPROVEMENTS.md (Agentic Narrative Contagion Velocity, RAG-Extracted Earnings Guidance Novelty & Hedge Density, Prediction-Market vs Options-Implied Probability Basis, Narrative Gravity Divergence from Fundamental Valuation, Streamlit Fragment Refresh Health & Staleness Attribution). Version strings synchronized to **2.61.1**.

- **v2.61.0 (2026-10-13)**: Fully implemented **AIS Maritime Traffic & Port Congestion Overlay** (`sie/ais_maritime.py`). Preferred columns: `ais_congestion`, `ais_wait_hrs`, `ais_boost`, `ais_reason`. Soft boost when key-port congestion eases and vessel waiting times fall into a confirming narrative; caution on rising congestion or extended waits. Wired through analyzer, CLI, config, and Streamlit. Deterministic synthetic proxy (live AIS feed reserved). Removed from FUTURE-IMPROVEMENTS.md High Priority.

- **v2.60.0 (2026-10-12)**: Domain-Tuned Financial LLM vs General LLM Sentiment Gap Overlay (`sie/fin_llm_gap.py`). Preferred columns: `flm_sent`, `flm_gen_gap`, `flm_boost`, `flm_reason`. Soft boost when domain-tuned model diverges constructively from general baseline into confirming narrative; caution on adverse gap. Wired through analyzer, CLI, config, and Streamlit. Restored core analyzer/CLI after placeholder. Synthetic proxy (live dual-LLM reserved).

- **v2.59.1 (2026-10-12)**: Autonomous research & evolution cycle against main (v2.59.0). Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard). Nothing removed from the roadmap. Added five new high-value overlays to FUTURE-IMPROVEMENTS.md (Always-On AI Agent Research Freshness, SEC Filing Structured Extraction Latency, Cross-Platform Retail Sentiment Divergence, Social Narrative Authenticity Scoring, WebSocket Streaming Latency Attribution). Version strings synchronized to **2.59.1**.
- **v2.59.0 (2026-10-11)**: Fully implemented **Satellite Imagery / Geospatial Physical Activity Overlay** (`sie/satellite_imagery.py`). Preferred columns: `sat_fill`, `sat_delta`, `sat_boost`, `sat_reason`. Wired through analyzer, CLI, config, and Streamlit. Deterministic synthetic proxy (live satellite feed reserved). Removed from FUTURE-IMPROVEMENTS.md High Priority.
- **v2.58.0 (2026-10-10)**: Fully implemented **Agentic Brokerage Account Flow & Penetration Overlay** (`sie/agentic_flow.py`). Preferred columns: `agt_flow_share`, `agt_tool_intensity`, `agt_boost`, `agt_reason`. Wired through analyzer, CLI, config, and Streamlit. Deterministic synthetic proxy (live brokerage agent-flow feed reserved).
