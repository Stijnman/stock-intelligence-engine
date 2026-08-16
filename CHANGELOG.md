# Changelog

All notable changes to the Stock Intelligence Engine are documented in this file.

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
