# Stock Intelligence Engine

Connect market narratives to your watchlist, confirm with technicals, and explain every signal. A narrative-first equity signal engine: for each ticker on your watchlist, it detects the dominant market narrative, scores it against a configurable stack of alternative-data overlays, cross-checks the result with technical indicators, and emits a per-signal explanation of why the score moved.

Runs as a CLI (`stock_intelligence_engine.py`) and a Streamlit dashboard (`app.py`). Configuration lives in `config.yaml`: watchlist, overlay toggles, thresholds.

**Current version:** v2.73.1 (October 2026). See [CHANGELOG.md](CHANGELOG.md) for the full version history.

## How it works

1. **Narrative detection** — identifies the dominant narrative per ticker (viral signals, news impact, historical context).
2. **Overlay scoring** — a stack of alternative-data overlays each produce a `boost` (score adjustment) and a `reason` (human-readable explanation). Overlays are independently toggleable.
3. **Technical confirmation** — narrative signals are cross-checked against technicals before producing a buy/hold/caution output.
4. **Explanation** — every signal ships with the overlay reasons that moved it, so output is auditable rather than a black-box score.

## Overlay stack

Every overlay follows the same contract: wired through the analyzer (a `include_*` flag), the CLI (a `--no-*` flag), config.yaml, and the dashboard (`prefix_*` columns). Current overlays:

| Overlay | Columns | Purpose |
|---------|---------|---------|
| Expert Network Call Novelty & Sentiment Velocity | `enc_*` | Novelty and constructive sentiment velocity from expert-network call transcripts |
| Signed Options Flow Toxicity & Informed Trading Probability | `oft_*` | Low toxicity + constructive informed-trading probability from signed OPRA flow |
| Unified Real-Time Multi-Source Narrative Freshness | `ums_*` | Freshness and constructive alignment across news, X, SEC, Form 4, congressional |
| Agent-Generated Research Memo Cascade Velocity | `agc_*` | Velocity and share of agent-generated research memo cascades |
| Kalshi Regulated vs Polymarket Offshore Earnings Beat Probability Basis | `kpm_*` | Basis between regulated Kalshi and offshore Polymarket earnings-beat probabilities |
| YouTube Financial Creator Transcript & Comment Sentiment Velocity | `ytc_*` | Velocity and sentiment of financial YouTube creator transcripts and comments |
| RAG-Extracted Earnings Guidance Novelty & Hedge Density | `rgn_*` | Novelty and hedge density of RAG-extracted earnings guidance |
| Agentic Narrative Contagion Velocity | `anc_*` | Velocity and agent share of narrative propagation through autonomous AI agents |
| SEC Filing Structured Extraction Latency & Completeness | `sec_*` | Latency and completeness of structured 10-K/10-Q/8-K extraction for agent consumption |
| Listed Event-Contract Book Depth vs Offshore Basis | `lec_*` | Listed event-contract depth and basis versus offshore prediction markets |
| Multi-Agent Debate Consensus Strength | `mad_*` | Consensus/disagreement among specialized debate agents |
| Always-On Agent Research Freshness | `agt_fresh_s`, `agt_workflow_pct` | Freshness and completion of continuous agent research |
| AIS Maritime Traffic & Port Congestion | `ais_*` | Key-port congestion, vessel waiting times |
| Domain-Tuned vs General LLM Sentiment Gap | `flm_*` | FinBERT-style vs general-LLM divergence |
| Satellite Imagery / Geospatial Activity | `sat_*` | Parking-lot fill, oil-tank levels, night lights, vessel counts |
| Agentic Brokerage Account Flow | `agt_flow_share`, `agt_tool_intensity` | Share of order flow from autonomous accounts |

### Data status — read this before trusting a signal

Several of the newer overlays (Expert Network Call Novelty, Signed Options Flow Toxicity, Unified Multi-Source Narrative Freshness, Agent-Generated Memo Cascade, Kalshi vs Polymarket basis, YouTube creator sentiment, RAG earnings guidance, listed event-contract basis, multi-agent debate, agent research freshness, AIS maritime, Fin-LLM gap, satellite imagery, agentic brokerage flow) currently run on **deterministic synthetic proxies** — live feeds are stubbed and reserved for future wiring (see CHANGELOG entries). Their column shapes and boost logic are real; their input data is not yet. Treat signals from those overlays as pipeline validation, not tradable information. Check `config.yaml` and the CHANGELOG for which feeds are live before acting on any output.

## Quick start

```bash
pip install -r requirements.txt
cp .env.example .env   # add any API keys
python stock_intelligence_engine.py
streamlit run app.py
```

`config.yaml` holds the watchlist and per-overlay toggles. Every overlay can be disabled individually via config, CLI flag, or the dashboard.

## Requirements

Python 3.10+. API keys optional depending on which overlays you enable — see `.env.example` for the supported providers.

## Version history

Moved to [CHANGELOG.md](CHANGELOG.md). The roadmap for unwired overlays lives in FUTURE-IMPROVEMENTS.md.

## Recent Edits & Version History

- **v2.73.1 (2026-10-27)**: Autonomous research & evolution cycle. Code audit confirmed no open FUTURE-IMPROVEMENTS items fully wired (analyzer + CLI + config + dashboard). Nothing removed from the roadmap. Added four new high-value overlays to FUTURE-IMPROVEMENTS.md (one High Priority: AI Multi-Model Council Forecast vs Prediction Market Probability Basis Overlay; two Medium Priority: Equibles MCP Full-Text Filing & Transcript Extraction Completeness & Latency Overlay, Graded AI Verdict Hit-Rate Cascade on Prediction Markets Overlay; one Long-Term: Sports Prediction Market Official Data Partnership Spillover Narrative Contagion Overlay). Version bump.

- **v2.73.0 (2026-10-26)**: Fully implemented Expert Network Call Novelty & Sentiment Velocity Overlay (`sie/expert_network_call_novelty.py`). Columns: `enc_novelty`, `enc_sent_vel`, `enc_boost`, `enc_reason`. Soft boost when high-novelty expert-network (Tegus/GLG-style) call transcripts exhibit constructive sentiment velocity confirming a narrative into technical strength; caution on low-novelty or adverse expert sentiment while narrative heat remains elevated. Wired through analyzer, CLI (`--no-expert-network-call-novelty`), config, and Streamlit dashboard. Deterministic synthetic proxy. Asset: ![ENC](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/expert_network_call_novelty_v2.73.0.svg)

- **v2.72.1 (2026-10-26)**: Autonomous research & evolution cycle. Code audit confirmed no open FUTURE-IMPROVEMENTS items fully wired. Added four new high-value overlays to the roadmap (Hiring Velocity & Employee Outlook Sentiment and Short Interest & Fails-to-Deliver Squeeze Pressure to High Priority; App Download & Consumer Engagement Velocity and Prediction-Market Agent Signal Cascade Velocity to Medium Priority). Version bump.

- **v2.72.0 (2026-10-25)**: Fully implemented Signed Options Flow Toxicity & Informed Trading Probability Overlay (`sie/signed_options_flow_toxicity.py`). Columns: `oft_toxicity`, `oft_informed_prob`, `oft_boost`, `oft_reason`. Soft boost when signed OPRA flow shows low toxicity and constructive informed-trading probability into a confirming narrative; caution on elevated toxicity or adverse informed flow while narrative heat remains elevated. Wired through analyzer, CLI (`--no-signed-options-flow-toxicity`), config, and Streamlit dashboard. Deterministic synthetic proxy. Asset: ![OFT](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/signed_options_flow_toxicity_v2.72.0.svg)

- **v2.71.1 (2026-10-25)**: Autonomous research & evolution cycle. Code audit confirmed no open FUTURE-IMPROVEMENTS items fully wired. Added four new high-value overlays to the roadmap (Truth Social Influential Political Account Narrative Velocity and Adanos Unified Social + Prediction-Market Buzz Velocity to High Priority; Multi-LLM Ensemble Financial Headline Sentiment Divergence and Streamlit st.fragment Live Market Pulse Auto-Refresh to Medium Priority). Version bump.

- **v2.71.0 (2026-10-24)**: Fully implemented Unified Real-Time Multi-Source Narrative Freshness Overlay (`sie/unified_multi_source_narrative_freshness.py`). Columns: `ums_fresh_s`, `ums_sources_ok`, `ums_boost`, `ums_reason`. Soft boost on fresh, constructively aligned multi-source narrative (news, X cashtags, SEC filings, Form 4, congressional disclosures); caution on stale sources or adverse clustering while narrative heat remains elevated. Wired through analyzer, CLI (`--no-unified-multi-source-narrative-freshness`), config, and Streamlit dashboard. Deterministic synthetic proxy. Asset: ![UMS](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/unified_multi_source_narrative_freshness_v2.71.0.svg)

- **v2.70.1 (2026-10-24)**: Autonomous research & evolution cycle. Code audit confirmed no open FUTURE-IMPROVEMENTS items fully wired. Added five new high-value overlays to the roadmap (Dark Pool / Off-Exchange Institutional Block Print Intensity & Informed Flow, Real-Time Earnings Call Transcript Sentiment Velocity vs Pre-Call Narrative, Gamma Exposure (GEX) Regime & Dealer Hedging Pressure to High Priority; Congressional Trade Disclosure Clustering & Timing Alpha, Web Traffic & App Engagement Velocity as Leading Demand Proxy to Medium Priority). Version bump.

- **v2.70.0 (2026-10-23)**: Fully implemented Agent-Generated Research Memo Cascade Velocity Overlay (`sie/agent_generated_memo_cascade.py`). Columns: `agc_vel`, `agc_memo_share`, `agc_boost`, `agc_reason`. Soft boost on high-velocity agent-generated research memo cascade into confirming narrative; caution on collapse or adversarial turn while human narrative heat remains elevated. Wired through analyzer, CLI (`--no-agent-generated-memo-cascade`), config, and Streamlit dashboard. Deterministic synthetic proxy. Asset: ![AGC](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/agent_generated_memo_cascade_v2.70.0.svg)
