## [2.23.0] - 2026-08-26

### Added / Completed
* **Streamlit Fragment Live Dashboard Refresh** — fully implemented end-to-end in `app.py`.
  - `@st.fragment(run_every=...)` for independent live status metrics and signal table auto-refresh.
  - Honours existing `config.yaml` → `dashboard.refresh_interval` (seconds; 0 disables).
  - `@st.cache_data(ttl=300)` for expensive full analysis pipeline; Force Full Refresh button clears cache and forces re-run.
  - Improved column ordering, summary metrics (Buy/Hold/Caution counts), sidebar controls, and versioned title/caption.
  - No full-script reruns on timer ticks — selective fragment updates only.
  - Removed completed item from FUTURE-IMPROVEMENTS.md (marked done with date + version).

### Changed
* Autonomous feature implementation cycle (2026-08-26).
* Version bumped to **2.23.0** across CLI (`stock_intelligence_engine.py`), package (`sie/__init__.py`), dashboard (`app.py`), CHANGELOG, README and FUTURE-IMPROVEMENTS.

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
