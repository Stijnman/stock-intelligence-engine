# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.38.0] - 2026-09-21

### Added / Completed
- **News-Source Authority / Reliability Weighted Narrative Score** (`sie/news_authority.py`).
  - Weights news and social velocity by source authority (tier-1 share, unverified-source share, historical accuracy proxy) instead of treating all mentions equally.
  - Soft +1 when high-authority confirmed narrative aligns with velocity; -1 when velocity is driven by low-authority / unverified sources.
  - Wired into `analyze_watchlist` / `run_report` (`include_news_authority`), CLI `--no-news-authority`, config `news_authority:`, Streamlit columns `nsa_authority`, `nsa_weighted_vel`, `nsa_tier1_share`, `nsa_unverified_share`, `nsa_boost`, `nsa_reason`.
  - Deterministic synthetic proxy labeled `synthetic_proxy`.
  - Removed from FUTURE-IMPROVEMENTS.md High Priority.

### Version
- Aligned package, CLI, dashboard and docs to **2.38.0**.

### Notes
- Educational research tool only — not financial advice.

---

## [2.37.1] - 2026-09-21

See git history for the 2.37.1 research-cycle notes and earlier releases.

*Educational research tool only — not financial advice.*
