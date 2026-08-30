## [2.27.1] - 2026-08-30

### Research / Roadmap
* Autonomous research & evolution cycle (2026-08-30).
* Code audit confirmed all previously completed High/Medium Priority items remain correctly marked [x] with full wiring present in analyzer / CLI / dashboard / config / tests; no cleanup required this cycle.
* Fresh 2026 research across AI stock analysis platforms (AltIndex, Prospero, StockTitan/Rhea-AI, AlphaSense, SentiSense, Hebbia), narrative authenticity, consumer transaction nowcasting, maritime AIS/port congestion alternative data, Substack/newsletter sentiment, analyst revision velocity, order-flow microstructure, and Streamlit 1.58–1.62 production patterns (parallel fragments, multi-user session isolation).
* Added five genuinely new high-value roadmap items not previously present:
  - **Aggregated Consumer Transaction / Credit-Card Panel Spend Nowcasting Overlay** (High Priority)
  - **Maritime AIS / Port Congestion & Vessel Activity Overlay** (High Priority)
  - **Substack & Independent Research Newsletter Sentiment Overlay** (Medium Priority)
  - **Analyst Estimate Revision Momentum & Surprise Probability Overlay** (Medium Priority)
  - **Order-Flow / Level-2 Imbalance Soft Overlay** (Medium Priority)
* Version bumped to **2.27.1** across package, CLI, dashboard, CHANGELOG, README and FUTURE-IMPROVEMENTS.

## [2.27.0] - 2026-08-29

### Added / Completed
* **Authenticity-Filtered Social Narrative Velocity Overlay** — `sie/authenticity.py`.
  - Deterministic authenticity score (0–1) + filtered velocity proxy keyed by ticker + day.
  - High-auth + rising narrative → soft boost; elevated velocity with low-auth (bot/spam risk) → caution.
  - Surfaces `auth_score`, `auth_filtered_velocity`, `auth_boost`, `auth_confidence`, `auth_reason`, `auth_source`.
  - Source labeled `synthetic_proxy` / `synthetic_proxy_high_auth` / `synthetic_proxy_low_auth` (live bot-classifier hook left explicit).
  - Wired after attention / before thesis. CLI `--no-authenticity`.
  - Config section `authenticity.enabled` + thresholds.
  - Dashboard preferred columns include auth_score / auth_filtered_velocity / auth_boost.
  - Tests cover signature + CLI disable flag forwarding.

### Changed
* Autonomous feature implementation cycle (2026-08-29).
* Version bumped to **2.27.0** across package, CLI, dashboard, CHANGELOG, README and FUTURE-IMPROVEMENTS.

## [2.26.1] - 2026-08-29

### Research / Roadmap
* Autonomous research & evolution cycle (2026-08-29).
* Code audit confirmed all previously completed High/Medium Priority items remain correctly marked [x] with wiring present; no cleanup required this cycle.
* Fresh 2026 research across AI stock analysis platforms (AltIndex, Nebula, SentiSense, StockTitan/Rhea-AI, Prospero, AlphaSense), narrative intelligence, authenticity scoring, earnings NLP, options dealer positioning, and Streamlit production/deployment patterns.
* Added five genuinely new high-value roadmap items not previously present:
  - **Authenticity-Filtered Social Narrative Velocity Overlay** (High Priority)
  - **Earnings Call Q&A vs Prepared Remarks Sentiment & Guidance Divergence Detector** (High Priority)
  - **Dealer Gamma Exposure (GEX) Real-Time Overlay** (Medium Priority)
  - **Multi-User Persistent Watchlist & Session Sync for Streamlit** (Medium Priority)
  - **Cloud Deployment Profiles & Production Auth Templates** (Medium Priority)
* Version bumped to **2.26.1** across package, CLI, dashboard, CHANGELOG, README and FUTURE-IMPROVEMENTS.

## [2.26.0] - 2026-08-28

### Added / Completed
* **Semiconductor / AI Supply-Chain CapEx Momentum Tracker** — `sie/supply_chain.py`.
  - Seeded proxy plus optional yfinance peek on ASML / AMAT / LRCX / KLAC / TSM.
  - Surfaces `sc_capex_score`, `sc_side`, `sc_boost`, `sc_confidence`, `sc_reason`, `sc_source`.
  - Soft boost/penalty; source labeled `public_yfinance` or `synthetic_proxy`.
  - Wired after hiring / before thesis. CLI `--no-supply-chain`.
* **FINRA Short Volume / Short Interest Momentum Overlay** — `sie/short_interest.py`.
  - Deterministic short-volume ratio + change proxy.
  - Elevated short volume vs rising narrative → caution; covering + rising narrative → boost.
  - Fields `si_ratio`, `si_change`, `si_boost`, `si_confidence`, `si_reason`, `si_source`.
  - CLI `--no-short-interest`. Live FINRA CSV left as an explicit future hook (no invented API).
* **Wikipedia / Google Trends Attention Momentum Tracker** — `sie/attention.py`.
  - Optional stdlib Wikimedia pageview WoW momentum; fallback synthetic proxy.
  - Fields `attn_momentum`, `attn_boost`, `attn_confidence`, `attn_reason`, `attn_source`.
  - CLI `--no-attention`.
* Tests cover signature + `run_report` forwarding + CLI disable flags for the three overlays.
* Added missing `DISCLAIMER.md` and `CONTRIBUTING.md` (README already linked them).

### Changed
* Autonomous implementation cycle (2026-08-28). Honest batch of 3 overlays.
* Version bumped to **2.26.0** across package, CLI, dashboard, CHANGELOG, README and FUTURE-IMPROVEMENTS.

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

### Added
* Five new high-value 2026 research-backed roadmap items to FUTURE-IMPROVEMENTS.md:
  - **Market Regime Adaptive Overlay Weighting** (High Priority)
  - **Semiconductor / AI Supply-Chain CapEx Momentum Tracker** (High Priority)
  - **Earnings Call Audio Tone & Prosody Sentiment Layer** (Medium Priority)
  - **Vision-Model Chart Pattern & Anomaly Detector** (Medium Priority)
  - **Open-Source Factor Risk Decomposition Overlay** (Medium Priority)
