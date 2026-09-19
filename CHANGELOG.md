# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.36.0] - 2026-09-19

### Added / Completed
- **Corporate Credit Spread / CDS Momentum Overlay** (`sie/credit_spread.py`).
  - Tracks synthetic CDS / credit-spread level and session delta as a fundamental stress / relief pulse.
  - Soft +1 when spreads tighten with rising narrative velocity; -1 on rapid widening even if social heat is elevated.
  - Wired into `analyze_watchlist` / `run_report` (`include_credit_spread`), CLI `--no-credit-spread`, config `credit_spread:`, Streamlit columns `cds_spread_bp`, `cds_delta_bp`, `cds_direction`, `cds_boost`, `cds_reason`.
  - Deterministic synthetic proxy labeled `synthetic_proxy`.
  - Removed from FUTURE-IMPROVEMENTS.md High Priority.

### Version
- Aligned package, CLI, dashboard and docs to **2.36.0**.

### Notes
- Educational research tool only — not financial advice.

---

## [2.35.1] - 2026-09-19

### Research & Evolution
- Autonomous research & evolution cycle executed (2026-09-19).
- Code audit of `sie/` overlays, CLI flags, Streamlit preferred columns, and FUTURE-IMPROVEMENTS.md.
- **Cleanup:** none. High Priority items (CDS, earnings-call transcripts, news-source authority, whisper-number cluster, KOL amplification, ETF AP flow, Rule 10b5-1 / buyback execution) are still roadmap-only — no matching fully wired modules.
- Fresh 2026 research: AltIndex AI Score + employee outlook / Glassdoor, SentiSense MCP + publisher reliability, TickerDesk unusual options sweeps/blocks, StockTools.ai / Stock Companion news+insider workspaces, Trade Ideas HOLLY session signals.

### Added (Roadmap)
- **Unusual Options Sweep vs Block Confirmation Overlay** (High Priority) — new.
- **Employee Outlook / Glassdoor Business Sentiment Overlay** (High Priority) — new.
- **Earnings Calendar Distance-Decay & Event-Risk Overlay** (Medium Priority) — new.
- **SEC Comment Letter / Regulatory Docket Velocity Overlay** (Long-Term / Nice-to-Have) — new.

### Version
- Aligned package, CLI, dashboard and docs to **2.35.1**.

### Notes
- Educational research tool only — not financial advice.

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
