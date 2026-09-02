## [2.29.1] - 2026-09-02

### Research / Roadmap
* Autonomous research & evolution cycle (2026-09-02).
* Code audit confirmed all previously completed High/Medium Priority items remain correctly marked [x] with full wiring present in analyzer / CLI / dashboard / config / tests (including Securities Lending / Borrow Fee overlay from v2.29.0); no cleanup required this cycle.
* Fresh 2026 research across AI stock analysis platforms (AltIndex, Prospero.ai, StockTitan/Rhea-AI, AlphaSense, MoneySense AI, Adanos, NowNews, GammaRips, Unusual Whales), alternative data (freight indices, job-skill intensity, retail vs institutional options flow, pre-earnings social/options leaks, multi-channel alerting), narrative intelligence, prediction-market cross-checks, and Streamlit production patterns.
* Added five genuinely new high-value roadmap items not previously present:
  - **Freight Rate & Logistics Cost Index Momentum Overlay** (High Priority)
  - **Job Posting AI-Skill Intensity & Role-Mix Shift Overlay** (High Priority)
  - **Retail vs Institutional Options Flow Divergence Gauge** (Medium Priority)
  - **Pre-Earnings Social Whisper & Options Leak Probability Score** (Medium Priority)
  - **Webhook / Multi-Channel Alert Router with Overlay Threshold Triggers** (Medium Priority)
* Version bumped to **2.29.1** across package, CLI, dashboard, CHANGELOG, README and FUTURE-IMPROVEMENTS.

## [2.29.0] - 2026-09-01

### Added / Completed
* **Securities Lending / Borrow Fee & Short Squeeze Risk Overlay** — `sie/borrow_fee.py`.
  - Deterministic synthetic borrow-fee / days-to-cover / hard-to-borrow proxy keyed by ticker + day-of-year.
  - Soft boost when elevated borrow costs coincide with rising narrative velocity and short-interest covering (squeeze-risk confirmation).
  - Caution when very high fees + expanding DTC meet cold narrative.
  - Surfaces `bf_fee_pct`, `bf_dtc`, `bf_htb`, `bf_dtc_change`, `bf_boost`, `bf_confidence`, `bf_reason`, `bf_source`.
  - Source labeled `synthetic_proxy` (live securities-lending feed hook left explicit).
  - Wired after consumer_spend / before thesis. CLI `--no-borrow-fee`.
  - Config section `borrow_fee.enabled` + thresholds.
  - Dashboard preferred columns include bf_fee_pct / bf_dtc / bf_htb / bf_boost.
  - Tests cover signature + CLI disable flag forwarding.

### Changed
* Autonomous feature implementation cycle (2026-09-01).
* Version bumped to **2.29.0** across package, CLI, dashboard, CHANGELOG, README and FUTURE-IMPROVEMENTS.

## [2.28.2] - 2026-09-01

### Research / Roadmap
* Autonomous research & evolution cycle (2026-09-01).
* Code audit confirmed all previously completed High/Medium Priority items remain correctly marked [x] with full wiring present in analyzer / CLI / dashboard / config / tests; no cleanup required this cycle.
* Fresh 2026 research across AI stock analysis platforms (AltIndex, Nebula/Hidden Systems, StockTitan/Rhea-AI, AlphaSense, SentiSense, Adanos, OpenGamma, GammaRips), alternative data (securities lending / borrow fees, GPU cloud utilization, ETF flows, earnings implied-move calibration, on-chain crypto-equity activity), narrative intelligence, GEX/dealer positioning, and Streamlit 2026 multi-user / production patterns.
* Added five genuinely new high-value roadmap items not previously present:
  - **Securities Lending / Borrow Fee & Short Squeeze Risk Overlay** (High Priority)
  - **GPU Cloud Utilization & Inference Capacity Pricing Proxy** (High Priority)
  - **ETF & Mutual Fund Flow Theme Rotation Overlay** (Medium Priority)
  - **Earnings Implied-Move Calibration & Post-Event Surprise Tracker** (Medium Priority)
  - **On-Chain Wallet & Exchange Flow Overlay for Crypto-Equity Names** (Medium Priority)
* Version bumped to **2.28.2** across package, CLI, dashboard, CHANGELOG, README and FUTURE-IMPROVEMENTS.

## [2.28.1] - 2026-08-31

### Research / Roadmap
* Autonomous research & evolution cycle (2026-08-31).
* Code audit confirmed all previously completed High/Medium Priority items remain correctly marked [x] with full wiring present in analyzer / CLI / dashboard / config / tests; no cleanup required this cycle.
* Fresh 2026 research across AI stock analysis platforms (AltIndex, Prospero, StockTitan/Rhea-AI, AlphaSense, SentiSense, Hebbia, Stock Companion), alternative data (container/bill-of-lading trade flow, road/truck camera volume, satellite + AIS), AI token consumption / AI premium factor literature, dual institutional-vs-retail sentiment, AI-clustered news story impact scoring, local open-weight LLM ticker mapping, and Streamlit 2026 multi-user / production patterns.
* Added five genuinely new high-value roadmap items not previously present:
  - **Container / Bill-of-Lading Trade Flow Momentum Overlay** (High Priority)
  - **Road / Truck Traffic Camera Volume Overlay** (High Priority)
  - **Dual Institutional vs Retail Sentiment Divergence Gauge** (Medium Priority)
  - **AI-Clustered News Story Impact & Multi-Perspective Overlay** (Medium Priority)
  - **Local Open-Weight LLM Ticker Mapping Layer** (Medium Priority)
* Version bumped to **2.28.1** across package, CLI, dashboard, CHANGELOG, README and FUTURE-IMPROVEMENTS.

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
