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

# Changelog

All notable changes to the Stock Intelligence Engine are documented in this file.

## [2.19.1] - 2026-08-18

### Changed
* Autonomous research & evolution cycle (2026-08-18).
* Code audit confirmed all previously marked-complete features remain fully implemented; no roadmap cleanups required.
* Fresh 2026 research on AI stock analysis, narrative intelligence, options flow, agent/MCP tooling, Streamlit patterns, and alternative data sources.

### Added
* Five new high-value roadmap items to FUTURE-IMPROVEMENTS.md:
  - **Short Interest & Securities Lending Squeeze Risk Overlay** (High Priority)
  - **Analyst Rating & Price Target Revision Velocity** (High Priority)
  - **AI News Story Clustering & Multi-Perspective Impact Scoring** (High Priority)
  - **MCP / Agent Tool Surface for Stock Intelligence Engine** (Medium Priority)
  - **Reddit Subreddit-Specific Momentum & WSB Cluster Detector** (Medium Priority)
* Version bump to **2.19.1** across CLI, dashboard, package `__init__`, headers and docs.

## [2.19.0] - 2026-08-17

### Added
* **Corporate Hiring & Headcount Momentum Tracker** fully integrated end-to-end.
  - New module `sie/hiring.py` (`detect_hiring_momentum` + `integrate_hiring_to_row`).
  - Soft boost/penalty on hiring acceleration or contraction as forward-looking demand proxy (AltIndex-style).
  - Surfaces job growth %, headcount delta, open-roles estimate, side, confidence, reason and source.
  - Wired into `analyze_watchlist` / `run_report`, CLI (`--no-hiring`), Streamlit dashboard (dedicated Hiring table), config.yaml (`hiring:` section) and public API.
  - Deterministic synthetic proxy (seeded) with mild bullish bias for AI / semiconductor names; ready for live job-board hooks.

### Changed
* Version bump to **2.19.0** across CLI, dashboard, package `__init__`, headers and docs.
* Updated FUTURE-IMPROVEMENTS.md: marked Corporate Hiring & Headcount Momentum Tracker complete with date.
* Analyzer docstring and parameter surface updated for `include_hiring`.
* Config loader and YAML now include `hiring:` section with sensible defaults.

## [2.18.1] - 2026-08-17

### Changed
* Autonomous research & evolution cycle (August 17, 2026). Full audit of core modules, analyzer, CLI, dashboard, config and docs confirmed all previously marked FUTURE-IMPROVEMENTS items remain accurately completed; no additional open items were found already implemented.
* Version consistency fix: aligned package `__init__.py` version reference with 2.18.x line.
* Five genuinely new high-value improvements from fresh 2026 research (earnings transcript guidance shifts, YouTube/influencer narrative velocity, web traffic & app download momentum, employee/Glassdoor outlook proxy, unusual options percentile/sweep ranking) added to FUTURE-IMPROVEMENTS.md under High and Medium Priority.

### Added
* Roadmap entries for Earnings Call Transcript Sentiment & Guidance Shift Detector, Finance YouTube / Influencer Narrative Velocity Overlay, Web Traffic & App Download Momentum Tracker (High Priority); Employee Outlook / Glassdoor Sentiment Proxy and Unusual Options Flow Percentile Ranking & Sweep Detector (Medium Priority).

## [2.18.0] - 2026-08-16

### Added
* **Same-Day SEC EDGAR Material Filing Detector** fully integrated end-to-end.
  - Module `sie/edgar.py` (live EDGAR probe + deterministic synthetic fallback).
  - Soft boost/penalty on material positive/negative filings (8-K items, etc.).
  - Surfaces form, description, tone, materiality score, confidence, reason and link.
  - Wired into `analyze_watchlist` / `run_report`, CLI (`--no-edgar`), Streamlit dashboard (dedicated EDGAR table), config.yaml (`edgar:` section) and public API.
* Confirmed and hardened **0DTE Options Flow & Unusual Activity Proxy** configuration and integration (options_0dte section, defaults, loader).

### Changed
* Version bump to **2.18.0** across CLI, dashboard, package `__init__`, headers and docs.
* Restored production README.md and CHANGELOG.md (previously placeholders).
* Updated FUTURE-IMPROVEMENTS.md: marked 0DTE and EDGAR complete with dates.
* Analyzer docstring and parameter surface updated for include_edgar.
* Config loader now merges `options_0dte` and `edgar` sections with sensible defaults.

### Fixed
* Incomplete wiring of EDGAR detector into the main analysis pipeline.
* Missing configuration defaults and YAML sections for recent overlays.

## [2.17.0] - 2026-08-15

### Changed
* Intermediate evolution cycle preparing EDGAR and 0DTE surfaces.
* Version references updated in headers.

## [2.16.2] - 2026-08-14

### Changed
* Replaced permissive CI smoke checks with blocking lint, test-suite, repository-hygiene, and CLI validation across Python 3.10–3.12.
* Added pytest.ini.
* Documented setup and structure.

## [2.16.1] - 2026-08-14

### Fixed
* Repaired the package public API by replacing stale imports and exports.

## [2.15.5] - 2026-08-13

### Changed
* Autonomous research & evolution cycle. Roadmap audit and five new high-value research items added to FUTURE-IMPROVEMENTS.

## Earlier versions
See git history for v2.4.0 through v2.15.0 feature introductions (X narrative, velocity forecasting, insider Form 4, Polymarket, 13F, congressional, realtime, dark-pool, options IV skew, portfolio risk, backtesting, Streamlit dashboard).
