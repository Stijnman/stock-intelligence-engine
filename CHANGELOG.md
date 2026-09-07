# Changelog

## [2.29.4] — 2026-09-07

### Research & Maintenance
- Autonomous research & evolution cycle.
- Restored empty core documentation files (README.md, FUTURE-IMPROVEMENTS.md, app.py) from last known good commit state.
- Code audit: no additional completed FUTURE-IMPROVEMENTS items required cleanup beyond the 9 previously marked [x] items which were removed from the active roadmap; all shipped overlays remain fully wired in analyzer / CLI / config / dashboard.
- Fresh 2026 research covering AI-powered stock analysis tools (AltIndex, SentiSense, Fiscal.ai, Prospero.ai, MoatScan, Stock Companion), narrative intelligence & multi-provider sentiment with MCP surfaces, near-instant XBRL structured filing intelligence, options liquidity-ranked pools with historical outcome tracking, Streamlit production patterns (Parquet state compression, offline demo mode), and cloud data marketplace connectors.
- Added five new high-value roadmap items:
  - **High**: Near-Instant XBRL Structured Filing Diff & Consensus Surprise Overlay
  - **High**: Options Liquidity-Ranked Setup Pool & Historical Outcome Tracker
  - **Medium**: Production Streamlit Parquet State Compression + Offline Demo Mode
  - **Medium**: Multi-Provider Sentiment Aggregation Layer with MCP Tool Surface
  - **Long-Term**: Cloud Data Marketplace Native Connectors (Snowflake / similar)

### Notes
- Research-only cycle; no new overlay implementations this release.
- Educational research tool only — not financial advice.

## [2.29.3] — 2026-09-05

### Research & Maintenance
- Autonomous research & evolution cycle.
- Code audit: no completed FUTURE-IMPROVEMENTS items remaining unchecked; all previously shipped overlays remain fully wired.
- Fixed version drift: `sie/__init__.py` and CLI entrypoint were at 2.30.0 while README and `app.py` reported 2.29.2. Aligned everything to **2.29.3**.
- Fresh 2026 research covering AI-powered stock tools, narrative/sentiment providers with MCP surfaces, near-instant XBRL filing intelligence, options liquidity-ranked pools with historical outcomes, Streamlit production patterns (Parquet state compression, offline demo mode), and cloud data marketplace connectors.
- Added five new roadmap items:
  - **High**: Near-Instant XBRL Structured Filing Diff & Consensus Surprise Overlay
  - **High**: Options Liquidity-Ranked Setup Pool & Historical Outcome Tracker
  - **Medium**: Production Streamlit Parquet State Compression + Offline Demo Mode
  - **Medium**: Multi-Provider Sentiment Aggregation Layer with MCP Tool Surface
  - **Long-Term**: Cloud Data Marketplace Native Connectors (Snowflake / similar)

### Notes
- Research-only cycle; no new overlay implementations this release.
- Educational research tool only — not financial advice.
