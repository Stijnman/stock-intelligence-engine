## [2.20.1] - 2026-08-21

### Added
* **LLM-Generated Bull/Bear Thesis Pair Generator** fully wired end-to-end (completion of v2.20.0 surface).
  - `integrate_thesis_to_row` and `generate_thesis_pair` now called inside `analyze_watchlist` / `run_report`.
  - CLI `--no-thesis` flag respected; config.yaml `thesis:` section with sensible defaults.
  - Streamlit dashboard surfaces dedicated Bull/Bear Thesis table.
  - Version consistency across CLI, dashboard, package `__init__`, headers and docs.
* Five new high-value 2026 research-backed roadmap items to FUTURE-IMPROVEMENTS.md:
  - **Web Traffic / Company Site Visit Momentum Tracker** (High Priority)
  - **Earnings Call Transcript Tone & Guidance Revision Detector** (High Priority)
  - **Employee Outlook / Glassdoor Sentiment Overlay** (Medium Priority)
  - **App Download & Usage Momentum Tracker** (Medium Priority)
  - **Pre-Market Theme Rotation & AI Potential Stocks Scanner** (Medium Priority)

### Changed
* Autonomous research & evolution cycle (2026-08-21).
* Code audit confirmed thesis module was present but incompletely wired; completed the integration and marked roadmap item complete.
* Fresh 2026 research on AI stock tools (AltIndex, Nebula, NowNews, AlphaSense, Gate AI Potential Stocks), alternative data (web traffic, employee outlook, app usage), earnings transcript intelligence, and Streamlit real-time patterns.

## [2.19.2] - 2026-08-19

### Changed
* Autonomous research & evolution cycle (2026-08-19).
* Code audit of core modules (analyzer, hiring, edgar, options_0dte, options_iv, dark_pool, realtime, congressional, institutional, insider, prediction_markets, social, portfolio, CLI, dashboard, config) confirmed all previously marked-complete features remain fully implemented; no roadmap cleanups required.
* Fresh 2026 research on AI-powered stock analysis tools, narrative intelligence, alternative data (credit-card / transaction, satellite / foot traffic, social followers), options dealer positioning (GEX), LLM thesis generation, and Streamlit / agent tooling patterns.

### Added
* Five new high-value roadmap items to FUTURE-IMPROVEMENTS.md:
  - **Credit Card / Consumer Transaction Momentum Tracker** (High Priority)
  - **Options Gamma Exposure (GEX) / Dealer Positioning Overlay** (High Priority)
  - **Satellite / Foot-Traffic / Geolocation Demand Proxy** (Medium Priority)
  - **Social Follower Growth & Brand Momentum Tracker** (Medium Priority)
  - **LLM-Generated Bull/Bear Thesis Pair Generator** (Medium Priority)
* Version bump to **2.19.2** across CLI, dashboard, package `__init__`, headers and docs.
