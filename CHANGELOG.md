## [2.28.0] - 2026-08-30

### Added / Completed
* **Aggregated Consumer Transaction / Credit-Card Panel Spend Nowcasting Overlay** — `sie/consumer_spend.py`.
  - Deterministic synthetic panel-spend momentum proxy keyed by ticker + day-of-year.
  - Soft boost on rising spend momentum (leading demand confirmation); caution on contraction.
  - Surfaces `cs_momentum`, `cs_score`, `cs_boost`, `cs_confidence`, `cs_reason`, `cs_source`.
  - Source labeled `synthetic_panel_proxy` (live panel-provider hook left explicit).
  - Wired after authenticity / before thesis. CLI `--no-consumer-spend`.
  - Config section `consumer_spend.enabled` + thresholds.
  - Dashboard preferred columns include cs_momentum / cs_score / cs_boost.
  - Tests cover signature + CLI disable flag forwarding.

### Changed
* Autonomous feature implementation cycle (2026-08-30).
* Version bumped to **2.28.0** across package, CLI, dashboard, CHANGELOG, README and FUTURE-IMPROVEMENTS.

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
