# Stock Intelligence Engine

Connect market narratives to your watchlist, confirm with technicals, and explain every signal. A narrative-first equity signal engine: for each ticker on your watchlist, it detects the dominant market narrative, scores it against a configurable stack of alternative-data overlays, cross-checks the result with technical indicators, and emits a per-signal explanation of why the score moved.

Runs as a CLI (`stock_intelligence_engine.py`) and a Streamlit dashboard (`app.py`). Configuration lives in `config.yaml`: watchlist, overlay toggles, thresholds.

**Current version:** v2.63.1 (October 2026). See [CHANGELOG.md](CHANGELOG.md) for the full version history.

## How it works

1. **Narrative detection** — identifies the dominant narrative per ticker (viral signals, news impact, historical context).
2. **Overlay scoring** — a stack of alternative-data overlays each produce a `boost` (score adjustment) and a `reason` (human-readable explanation). Overlays are independently toggleable.
3. **Technical confirmation** — narrative signals are cross-checked against technicals before producing a buy/hold/caution output.
4. **Explanation** — every signal ships with the overlay reasons that moved it, so output is auditable rather than a black-box score.

## Overlay stack

Every overlay follows the same contract: wired through the analyzer (a `include_*` flag), the CLI (a `--no-*` flag), config.yaml, and the dashboard (`prefix_*` columns). Current overlays:

| Overlay | Columns | Purpose |
|---------|---------|---------|
| Multi-Agent Debate Consensus Strength | `mad_*` | Consensus/disagreement among specialized debate agents |
| Always-On Agent Research Freshness | `agt_fresh_s`, `agt_workflow_pct` | Freshness and completion of continuous agent research |
| AIS Maritime Traffic & Port Congestion | `ais_*` | Key-port congestion, vessel waiting times |
| Domain-Tuned vs General LLM Sentiment Gap | `flm_*` | FinBERT-style vs general-LLM divergence |
| Satellite Imagery / Geospatial Activity | `sat_*` | Parking-lot fill, oil-tank levels, night lights, vessel counts |
| Agentic Brokerage Account Flow | `agt_flow_share`, `agt_tool_intensity` | Share of order flow from autonomous accounts |
| Index Reconstitution & Forced Passive-Flow | — | Forced passive flow around index events |
| Rule 606 Retail Options Routing | — | Retail options routing patterns |
| Alternative-Data Provenance | — | Source-quality weighting |
| Secondary Offering / ATM Dilution Velocity | — | Dilution pressure |
| Cross-Venue Tokenized-Share Basis | — | On-chain equity premium |
| Job-Posting Skill-Mix | — | Hiring signals |
| Retail Brokerage Order-Flow | — | Retail positioning |
| App-Store Review Sentiment | `asr_*` | Complaint velocity for consumer-facing companies |
| Employee Outlook | — | Internal sentiment proxies |
| Unusual Options | — | Options-flow anomalies |
| Rule 10b5-1 / Buyback | — | Insider selling plans and buyback activity |
| ETF AP Flow | — | Creation/redemption pressure |

### Data status — read this before trusting a signal

Several of the newer overlays (multi-agent debate, agent research freshness, AIS maritime, Fin-LLM gap, satellite imagery, agentic brokerage flow) currently run on **deterministic synthetic proxies** — live feeds are stubbed and reserved for future wiring (see CHANGELOG entries). Their column shapes and boost logic are real; their input data is not yet. Treat signals from those overlays as pipeline validation, not tradable information. Check `config.yaml` and the CHANGELOG for which feeds are live before acting on any output.

## Quick start

```bash
pip install -r requirements.txt
cp .env.example .env   # add any API keys
python stock_intelligence_engine.py
streamlit run app.py
```

```config.yaml` holds the watchlist and per-overlay toggles. Every overlay can be disabled individually via config, CLI flag, or the dashboard.```

## Requirements

Python 3.10+. API keys optional depending on which overlays you enable — see `.env.example` for the supported providers.

## Version history

Moved to [CHANGELOG.md](CHANGELOG.md). The roadmap for unwired overlays lives in FUTURE-IMPROVEMENTS.md.
