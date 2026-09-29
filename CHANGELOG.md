# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.45.1] - 2026-09-29

### Changed
* Autonomous research & evolution cycle. Code audit confirmed no FUTURE-IMPROVEMENTS items were fully wired (analyzer + CLI + config + dashboard) since v2.45.0; none removed.
* Roadmap expanded with five 2026 research-backed overlays: Form 144 planned-sale calendar, supplier invoice / freight BOL nowcast, activist 13D/13G accumulation velocity (High); board interlock / director-network centrality (Medium); satellite methane / flare intensity (Long-Term).
* Version bump to **2.45.1** across package, CLI, dashboard and docs.

---

## [2.45.0] - 2026-09-28

### Added
* **App-Store Review Sentiment & Complaint Velocity Overlay** (`sie/app_store_reviews.py`).
  Preferred columns: `asr_sentiment`, `asr_complaint_velocity`, `asr_rating`, `asr_boost`, `asr_reason`.
  Soft +1 when high sentiment + low complaint velocity confirm a hot narrative; caution when 1-star complaint velocity spikes into social heat.
  Wired through analyzer (`include_app_store_reviews`), CLI (`--no-app-store-reviews`), config (`app_store_reviews:`), Streamlit preferred columns.
  Deterministic synthetic proxy with live App Store / Play / Sensor Tower hook reserved.
* Also completed analyzer wiring for Employee Outlook and Unusual Options flags that CLI already exposed.

### Changed
* Version bump to **2.45.0** across package, CLI, dashboard and docs.

---

## [2.44.1] - 2026-09-28

See git history for 2.44.1 and earlier releases.

*Educational research tool only — not financial advice.*
