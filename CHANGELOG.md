# Changelog

## [2.32.0] — 2026-09-10

### Added / Completed
- **Patent & Intellectual Property Filing Momentum Overlay fully implemented** (was High Priority open item).
  - New `sie/patent_momentum.py` synthetic proxy (ticker + day seeded) with AI/semi/biotech bias; tracks patent filing velocity, forward-citation velocity and grant ratio.
  - Soft +1 boost on accelerating high-quality patent activity (filing velocity + grant ratio + citation support); -1 caution on decelerating patent momentum.
  - Config section `patent_momentum:` with `enabled`, `boost_velocity`, `penalty_velocity`, `min_grant_ratio`, `min_confidence`.
  - CLI flag `--no-patent-momentum`.
  - Streamlit dashboard preferred columns now surface `pm_filing_velocity`, `pm_citation_velocity`, `pm_grant_ratio`, `pm_direction`, `pm_boost`, `pm_reason`.
  - Fully integrated into `analyze_watchlist` / `run_report` call path after estimate-revision layer.

### Version
- Bumped package, CLI, dashboard and docs to **2.32.0**.

### Notes
- Educational research tool only — not financial advice.

## [2.31.0] — 2026-09-09

### Added / Completed
- **Analyst Estimate Revision Velocity & Breadth Overlay fully implemented** (was High Priority open item).
  - New `sie/estimate_revision.py` synthetic proxy (ticker + day seeded) with AI/semi bias; tracks velocity, breadth and direction of consensus estimate revisions.
  - Soft +1 boost on rapid upward revisions with sufficient breadth (narrative durability confirmation); -1 caution on sharp downward revisions even when social heat is elevated.
  - Config section `estimate_revision:` with `enabled`, `boost_velocity`, `penalty_velocity`, `min_breadth`, `min_confidence`.
  - CLI flag `--no-estimate-revision`.
  - Streamlit dashboard preferred columns now surface `er_velocity`, `er_breadth`, `er_direction`, `er_boost`, `er_reason`.
  - Fully integrated into `analyze_watchlist` / `run_report` call path after contagion layer.

### Version
- Bumped package, CLI, dashboard and docs to **2.31.0**.

### Notes
- Educational research tool only — not financial advice.

## [2.30.1] — 2026-09-09

### Research & Maintenance
- Autonomous research & evolution cycle.
- Code audit: all previously shipped overlays remain fully wired in analyzer / CLI / config / dashboard (Cross-Ticker Narrative Contagion Detector completed and integrated in v2.30.0; Borrow Fee, Consumer Spend, Authenticity, Supply-Chain CapEx, Short Interest, Attention, Regime, Confidence, Honesty, Thesis, Brief, Hiring, EDGAR, 0DTE, Options IV, Dark Pool, Realtime, Congressional, 13F, Prediction Markets, Insider, Narrative Velocity all confirmed present and called). No outstanding completed FUTURE-IMPROVEMENTS items required removal this cycle.
- Fresh 2026 research covering AI-powered stock analysis platforms (SentiSense, Fiscal.ai / FinChat, Prospero.ai, Marvin Labs, AlphaSense, NowNews, Adanos, Financial Datasets, Danelfin, AltIndex), narrative intelligence & multi-provider sentiment with MCP surfaces, alternative data categories (patent/IP filings, maritime AIS / port congestion, corporate CDS / credit spreads, analyst estimate revision velocity, long-form YouTube/podcast narrative), near-instant structured filings, options liquidity & flow, Streamlit production patterns (Parquet state, caching, offline modes), and cloud data connectors.
- Added five genuinely new high-value roadmap items not previously present:
  - **High**: Analyst Estimate Revision Velocity & Breadth Overlay
  - **High**: Patent & Intellectual Property Filing Momentum Overlay
  - **Medium**: Maritime AIS / Port Congestion & Vessel Activity Overlay
  - **Medium**: Corporate Credit Spread / CDS Momentum Overlay
  - **Long-Term**: YouTube / Podcast / Long-Form Content Narrative Velocity Overlay

### Version
- Bumped package, CLI, dashboard and docs to **2.30.1**.

### Notes
- Research-only cycle; no new overlay implementations this release.
- Educational research tool only — not financial advice.

## [2.30.0] — 2026-09-08

### Added / Completed
- **Cross-Ticker Narrative Contagion Detector fully wired** (was Medium Priority open item).
  - `sie/contagion.py` synthetic cluster-contagion proxy (AI / consumer / energy / meme thematic adjacency) now called from `analyze_watchlist` after authenticity / borrow-fee layers.
  - Config section `contagion:` with `enabled`, `boost_transfer`, `penalty_transfer`, `min_confidence`.
  - CLI flag `--no-contagion`.
  - Streamlit dashboard preferred columns now surface `ct_score`, `ct_velocity_transfer`, `ct_boost`, `ct_peers`, `ct_reason`.
  - Soft signal boost on inbound narrative transfer from peers; caution on reverse / outbound contagion.
  - Fixed `app.py` to correctly unpack `run_report()` result dict (`result["report"]["rows"]`) so the live table renders.

### Version
- Bumped package, CLI, dashboard and docs to **2.30.0**.

### Notes
- Educational research tool only — not financial advice.
