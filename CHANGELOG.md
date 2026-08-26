## [2.22.0] - 2026-08-26

### Fixed / Completed
* **Narrative vs. Fundamentals Contradiction / Honesty Signal Detector** — fully wired end-to-end (was present as `sie/honesty.py` but missing from analyzer orchestration, CLI, config and dashboard).
  - `integrate_honesty_to_row` now called inside `analyze_watchlist` / `run_report` after brief.
  - `include_honesty` parameter added and respected by CLI `--no-honesty`.
  - `config.yaml` gains explicit `honesty:` section (enabled by default, with high/mid risk thresholds).
  - Streamlit dashboard receives honesty columns via the shared analysis path.
  - Version consistency restored across package `__init__`, CLI, dashboard, headers and docs.

### Changed
* Autonomous research & evolution cycle (2026-08-26).
* Code audit of core modules confirmed all other marked-complete features remain fully implemented; only the partial honesty implementation required cleanup and full wiring.
* Fresh 2026 research on AltIndex digital-footprint + social follower signals, OpenRouter-style AI token consumption / AI Premium factor (arXiv 2026), Earth Observation / satellite foot-traffic & parking data for finance, Rhea-AI dual impact+tone scoring, SentiSense / StockPulse stratified multi-agent reports, Streamlit 1.61 lazy dataframes + background cache refresh, and continued MCP / agent-native patterns.

### Added
* Five new high-value 2026 research-backed roadmap items to FUTURE-IMPROVEMENTS.md:
  - **Satellite Imagery / Geolocation Foot-Traffic & Parking Activity Overlay** (High Priority)
  - **AI Token Consumption / AI Premium Factor Overlay** (High Priority)
  - **Cross-Platform Social Follower Growth Momentum** (Medium Priority)
  - **Dual-Score News Impact vs Tone Detector** (Medium Priority)
  - **Stratified Multi-Agent Research Report Generator** (Medium Priority)
* Version bump to **2.22.0** across CLI, dashboard, package `__init__`, headers and docs.

## [2.21.0] - 2026-08-25

### Fixed / Completed
* **Self-Explaining AI Signal Brief Generator** — fully wired end-to-end (was present as `sie/brief.py` but missing from analyzer orchestration, CLI and config).
  - `integrate_brief_to_row` now called inside `analyze_watchlist` / `run_report` after thesis.
  - `include_brief` parameter added and respected by CLI `--no-brief`.
  - `config.yaml` gains explicit `brief:` section (enabled by default).
  - Streamlit dashboard receives brief columns via the shared analysis path.
  - Version consistency restored across package `__init__`, CLI, dashboard, headers and docs (previously split between 2.20.4 / 2.21.0).

### Changed
* Autonomous research & evolution cycle (2026-08-25).
* Code audit of core modules confirmed all other marked-complete features remain fully implemented; only the partial brief implementation required cleanup.
* Fresh 2026 research on AltIndex digital-footprint signals (web traffic, app downloads), NowNews honesty / narrative-data contradiction detection, SentiSense / Fiscal.ai MCP patterns, agentic multi-perspective debate, Streamlit 1.37+ fragments + 1.61 lazy dataframes / background cache refresh, and continued options/dealer surface work.

### Added
* Five new high-value 2026 research-backed roadmap items to FUTURE-IMPROVEMENTS.md:
  - **Narrative vs. Fundamentals Contradiction / Honesty Signal Detector** (High Priority)
  - **Company Digital Footprint Momentum Overlay (Web Traffic + App Downloads)** (High Priority)
  - **Agentic Multi-Perspective Signal Debate Layer** (Medium Priority)
  - **Streamlit Fragment Live Dashboard Refresh** (Medium Priority)
* Version bump to **2.21.0** across CLI, dashboard, package `__init__`, headers and docs.

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
