## [2.20.4] - 2026-08-24

### Changed
* Autonomous research & evolution cycle (2026-08-24).
* Code audit of core modules (analyzer, hiring, edgar, options_*, dark_pool, realtime, congressional, institutional, insider, prediction_markets, social, portfolio, thesis, CLI, dashboard, config) confirmed all marked-complete features remain fully implemented; no roadmap cleanups required.
* Fresh 2026 research on SentiSense Earnings Analysis API / transcript diffs, AlphaSense guidance indices, FINRA short volume feeds, YouTube-as-first-class sentiment (SentiSense), Glassdoor/employee outlook (AltIndex), MCP servers for agent-native finance tools, Streamlit 1.61+ lazy dataframes & background cache refresh, Nebula narrative graphs, and Truth Social high-influence feeds.

### Added
* Five new high-value 2026 research-backed roadmap items to FUTURE-IMPROVEMENTS.md:
  - **Earnings Call Transcript Diff & Guidance Change Detector** (High Priority)
  - **Native MCP Server for Agent Integration** (High Priority)
  - **FINRA Short Volume / Short Interest Momentum Overlay** (Medium Priority)
  - **YouTube Finance Creator Sentiment Overlay** (Medium Priority)
  - **Employee Glassdoor / Outlook Sentiment Tracker** (Medium Priority)
* Version bump to **2.20.4** across CLI, dashboard, package `__init__`, headers and docs.

## [2.20.3] - 2026-08-23

### Changed
* Autonomous research & evolution cycle (2026-08-23).
* Code audit of core modules (analyzer, hiring, edgar, options_*, dark_pool, realtime, congressional, institutional, insider, prediction_markets, social, portfolio, thesis, CLI, dashboard, config) confirmed all marked-complete features remain fully implemented; no roadmap cleanups required.
* Fresh 2026 research on AltIndex / QuiverQuantitative alt-data (Wikipedia/pageview attention, patents, government contracts), FlashAlpha / SpotGamma extended dealer surfaces (vanna/charm/DEX), Nebula narrative graphs, SentiSense story clustering & YouTube, agentic self-critique / confidence calibration patterns, and Streamlit 2026 fragment best practices.

### Added
* Five new high-value 2026 research-backed roadmap items to FUTURE-IMPROVEMENTS.md:
  - **Wikipedia / Google Trends Attention Momentum Tracker** (Medium Priority)
  - **Patent Filing & IP Momentum Overlay** (Medium Priority)
  - **Government Contract & Lobbying Activity Overlay** (Medium Priority)
  - **Options Vanna / Charm / DEX Exposure Overlay** (High Priority)
  - **Signal Confidence Calibration & LLM Self-Critique Layer** (High Priority)
* Version bump to **2.20.3** across CLI, dashboard, package `__init__`, headers and docs.

## [2.20.2] - 2026-08-22

### Fixed / Completed
* **LLM-Generated Bull/Bear Thesis Pair Generator** — fully wired end-to-end (was claimed complete in 2.20.0/2.20.1 but missing from analyzer orchestration).
  - `integrate_thesis_to_row` now called inside `analyze_watchlist` / `run_report` after all overlays.
  - `include_thesis` parameter added to both functions and respected by CLI `--no-thesis`.
  - Streamlit dashboard already surfaced thesis columns; now receives real data.
  - `config.yaml` + defaults gain explicit `thesis:` section.
  - Version consistency across package `__init__`, CLI, dashboard, headers and docs.

### Added
* Five new high-value 2026 research-backed roadmap items to FUTURE-IMPROVEMENTS.md:
  - **Narrative Graph / Conversation Network Intelligence** (High Priority)
  - **Self-Explaining AI Signal Brief Generator** (High Priority)
  - **Options Max Pain & Open-Interest Wall Detector** (Medium Priority)
  - **Pre-Market Theme Rotation & Volume Surge Scanner** (Medium Priority)
  - **Cross-Ticker Narrative Contagion Detector** (Medium Priority)

### Changed
* Autonomous research & evolution cycle (2026-08-22).
* Fresh 2026 research on Nebula / Hidden Systems narrative graphs, NowNews honesty signals, AlphaSense transcript indices, FlashAlpha / Unusual Whales dealer positioning, AltIndex alt-data, Streamlit `@st.fragment` real-time patterns, and multi-source sentiment APIs.
* Code audit confirmed thesis was the only incomplete claimed feature; all other marked-complete items remain fully implemented.
