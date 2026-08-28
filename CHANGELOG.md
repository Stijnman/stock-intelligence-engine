## [2.25.0] - 2026-08-28

### Added / Completed
* **Market Regime Adaptive Overlay Weighting** — fully implemented end-to-end.
  - New module `sie/regime.py` detects regime via VIX level, SPY trend vs MA20 and 20-day realized volatility.
  - Classifies into high_vol_stress / elevated_vol / low_vol_bull / low_vol_calm / balanced / etc.
  - Produces adaptive weights for narrative / technical / flow / fundamental overlay groups.
  - Soft signal bias applied only at high confidence; always surfaces transparent regime reason.
  - Wired into `analyze_watchlist` / `run_report` via `include_regime` (CLI `--no-regime`).
  - Dashboard receives `market_regime`, `regime_confidence` columns in preferred order.
  - Config section `regime.enabled` added.
  - Removed completed item from FUTURE-IMPROVEMENTS.md (marked done with date + version).

### Changed
* Autonomous feature implementation cycle (2026-08-28).
* Version bumped to **2.25.0** across CLI (`stock_intelligence_engine.py`), package (`sie/__init__.py`), dashboard (`app.py`), CHANGELOG, README and FUTURE-IMPROVEMENTS.

## [2.24.0] - 2026-08-28

### Fixed / Completed
* **Signal Confidence Calibration & LLM Self-Critique Layer** — fully wired end-to-end (was present as `sie/confidence.py` + config + CLI flag but missing from analyzer orchestration and dashboard path).
  - `integrate_confidence_to_row` now called inside `analyze_watchlist` / `run_report` after honesty.
  - `include_confidence` parameter added and respected by CLI `--no-confidence`.
  - Dashboard receives confidence_score / confidence_label columns and surfaces them in preferred order.
  - Version consistency restored across package `__init__`, CLI, dashboard, headers and docs.

### Changed
* Autonomous research & evolution cycle (2026-08-28).
* Code audit confirmed all other marked-complete features remain fully implemented; only the partial confidence implementation required cleanup and full wiring.
* Fresh 2026 research on Fiscal.ai MCP patterns, MoatScan AI-impact scoring, Rhea-AI dual impact+tone, satellite/EO foot-traffic, AI token consumption / AI-premium factors, Streamlit fragment + background patterns, earnings-call narrative morphing (arXiv), and supply-chain CapEx leading indicators.

### Added
* Five new high-value 2026 research-backed roadmap items to FUTURE-IMPROVEMENTS.md:
  - **Market Regime Adaptive Overlay Weighting** (High Priority)
  - **Semiconductor / AI Supply-Chain CapEx Momentum Tracker** (High Priority)
  - **Earnings Call Audio Tone & Prosody Sentiment Layer** (Medium Priority)
  - **Vision-Model Chart Pattern & Anomaly Detector** (Medium Priority)
  - **Open-Source Factor Risk Decomposition Overlay** (Medium Priority)
* Version bump to **2.24.0** across CLI, dashboard, package `__init__`, headers and docs.
