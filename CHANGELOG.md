# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.47.1] - 2026-10-01

### Changed
* Autonomous research & evolution cycle against `main` @ 5ba41fb (docs claimed v2.47.0; README still on v2.46.1).
* Code audit: `sie/hiring_skill_mix.py` existed and dashboard preferred columns were present, but analyzer did not import or call the overlay and CLI had no `--no-hiring-skill-mix` flag. Wiring completed so the v2.47.0 claim is actually true.
* Removed the completed Job-Posting Skill-Mix item from FUTURE-IMPROVEMENTS.md.
* Version strings synchronized to **2.47.1** across package, CLI, dashboard and docs.

### Added (roadmap only)
* High: Cloud Committed-Use / Reserved-Instance Utilization Overlay.
* High: Payment-Network Authorization Decline & Chargeback Velocity Overlay.
* High: Critical-Mineral / Rare-Earth Export-Quota Exposure Overlay.
* Medium: Expert-Call / Primary-Research Tone Overlay.
* Long-Term: EU ETS / Carbon-Allowance Cost Pass-Through Overlay.

---

## [2.47.0] - 2026-09-30

### Added
* **Job-Posting Skill-Mix & Posted-Compensation Inflation Overlay** (`sie/hiring_skill_mix.py`).
  Preferred columns: `hmix_senior_share`, `hmix_comp_delta`, `hmix_boost`, `hmix_reason`.
  Soft +1 when senior/scarce skill mix and posted-comp inflation confirm labor demand into a hot narrative; caution when senior-share collapses with posted-comp deflation.
  Wired through analyzer (`include_hiring_skill_mix`), CLI (`--no-hiring-skill-mix`), config (`hiring_skill_mix:`), Streamlit preferred columns.
  Deterministic synthetic proxy with live Lightcast / Revelio / Indeed hook reserved.

### Changed
* Version bump to **2.47.0** across package, CLI, dashboard and docs.

---

## [2.46.1] - 2026-09-30

### Changed
* Autonomous research & evolution cycle against `main` @ a6230a64 (v2.46.0).
* Code audit confirmed no remaining FUTURE-IMPROVEMENTS items are fully wired (analyzer + CLI + config + dashboard). Retail flow remains the latest implemented overlay. None removed from the roadmap.
* 2026 research (realized AI-token consumption factors, multi-platform brand audience tracking, FTSE/MarketPsych thematic NLP indices, agent-native filing freshness, data-center interconnection queues) added five net-new roadmap items.
* Version bump to **2.46.1** across package, CLI, dashboard and docs.

### Added (roadmap only)
* High: Realized AI-Token Consumption Factor Beta Overlay.
* High: Multi-Platform Brand Audience / Short-Form Engagement Velocity Overlay.
* Medium: Thematic Narrative Taxonomy Exposure Overlay.
* Medium: Point-in-Time Filing Freshness / Agent-Index Latency Overlay.
* Long-Term: Data-Center Interconnection Queue / Power-Availability Overlay.

---

## [2.46.0] - 2026-09-29

### Added
* **Retail Brokerage Order-Flow Imbalance Overlay** (`sie/retail_flow.py`).
  Preferred columns: `rflow_imbalance`, `rflow_heat`, `rflow_boost`, `rflow_reason`.
  Soft +1 when retail buy-imbalance and heat confirm a hot narrative; caution when sell-imbalance hits elevated heat.
  Wired through analyzer (`include_retail_flow`), CLI (`--no-retail-flow`), config (`retail_flow:`), Streamlit preferred columns.
  Deterministic synthetic proxy with live FINRA ATS / brokerage-flow hook reserved.

### Changed
* Version bump to **2.46.0** across package, CLI, dashboard and docs.

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
