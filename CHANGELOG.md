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
