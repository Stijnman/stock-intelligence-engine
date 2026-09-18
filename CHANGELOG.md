# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.35.0] - 2026-09-18

### Added / Completed
- **Social Trading Action Intent Classifier** (`sie/social_intent.py`).
  - Classifies social posts into buy_the_dip / fomo_chase / bag_holding / short_squeeze_call / take_profit / spam.
  - Soft +1 on rising high-intent authentic velocity; -1 on low-intent / spam-driven spikes.
  - Wired into `analyze_watchlist` / `run_report` (`include_social_intent`), CLI `--no-social-intent`, config `social_intent:`, Streamlit columns `sti_*`.
  - Deterministic synthetic proxy labeled `synthetic_proxy`.
  - Removed from FUTURE-IMPROVEMENTS.md High Priority.

### Version
- Aligned package, CLI, dashboard and docs to **2.35.0**.

### Notes
- Educational research tool only — not financial advice.

---

## [2.34.0] - 2026-09-18

### Added / Completed
- **Dealer Gamma Exposure (GEX) & Pin-Risk Overlay fully wired** (was High Priority open item).

### Version
- Aligned package, CLI, dashboard and docs to **2.34.0**.

See git history for earlier changelog entries.

*Educational research tool only — not financial advice.*
