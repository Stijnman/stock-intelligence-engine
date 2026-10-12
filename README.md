# Stock Intelligence Engine

**Connect market narratives to your watchlist.**  
**Confirm with technicals.**  
**Explain every signal.**

**v2.59.1** — October 2026 · Autonomous research cycle (roadmap expansion) + Satellite Imagery / Geospatial Physical Activity Overlay (fully wired) + Agentic Brokerage Account Flow & Penetration Overlay (fully wired) + Index Reconstitution & Forced Passive-Flow Overlay (fully wired) + Rule 606 Retail Options Routing Overlay (fully wired) + Alternative-Data Provenance Overlay (fully wired) + Secondary Offering / ATM Dilution Velocity Overlay (fully wired) + Cross-Venue Tokenized-Share Basis / On-Chain Equity Premium Overlay (fully wired) + Job-Posting Skill-Mix + Retail Brokerage Order-Flow + App-Store Review Sentiment + Employee Outlook + Unusual Options + Rule 10b5-1 / Buyback + ETF AP Flow.

## Features

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

- **v2.59.1 (2026-10-12)**: Autonomous research & evolution cycle against main (v2.59.0). Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard). Nothing removed from the roadmap. Added five new high-value overlays to FUTURE-IMPROVEMENTS.md (Always-On AI Agent Research Freshness, SEC Filing Structured Extraction Latency, Cross-Platform Retail Sentiment Divergence, Social Narrative Authenticity Scoring, WebSocket Streaming Latency Attribution). Version strings synchronized to **2.59.1**.
- **v2.59.0 (2026-10-11)**: Fully implemented **Satellite Imagery / Geospatial Physical Activity Overlay** (`sie/satellite_imagery.py`). Preferred columns: `sat_fill`, `sat_delta`, `sat_boost`, `sat_reason`. Wired through analyzer, CLI, config, and Streamlit. Deterministic synthetic proxy (live satellite feed reserved). Removed from FUTURE-IMPROVEMENTS.md High Priority.
- **v2.58.0 (2026-10-10)**: Fully implemented **Agentic Brokerage Account Flow & Penetration Overlay** (`sie/agentic_flow.py`). Preferred columns: `agt_flow_share`, `agt_tool_intensity`, `agt_boost`, `agt_reason`. Wired through analyzer, CLI, config, and Streamlit. Deterministic synthetic proxy (live brokerage agent-flow feed reserved).
