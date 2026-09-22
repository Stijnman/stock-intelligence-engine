# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.39.0] - 2026-09-22

### Added / Completed
- **Whisper Number / Pre-Earnings Alt-Data Beat Probability Overlay** (`sie/whisper_number.py`).
  - Fuses consumer-spend, digital-footprint, hiring, attention and supply-chain nowcast layers into a probabilistic whisper beat/miss estimate ahead of earnings.
  - Soft +1 when the multi-signal alt-data cluster implies high beat probability inside the event window; -1 when the cluster deteriorates even if street consensus looks stable.
  - Wired into `analyze_watchlist` / `run_report` (`include_whisper_number`), CLI `--no-whisper-number`, config `whisper_number:`, Streamlit columns `wn_beat_prob`, `wn_cluster_score`, `wn_days_to_print`, `wn_consensus_gap`, `wn_boost`, `wn_reason`.
  - Deterministic synthetic proxy labeled `synthetic_proxy`.
  - Removed from FUTURE-IMPROVEMENTS.md High Priority.

### Version
- Aligned package, CLI, dashboard and docs to **2.39.0**.

### Notes
- Educational research tool only — not financial advice.

---

## [2.38.1] - 2026-09-22

### Research & Evolution
- Autonomous research & evolution cycle executed (2026-09-22).
- Code audit confirmed **News-Source Authority / Reliability Weighted Narrative Score** is fully implemented and wired (`sie/news_authority.py`, analyzer `include_news_authority`, CLI `--no-news-authority`, dashboard `nsa_*` columns). Removed from FUTURE-IMPROVEMENTS.md High Priority (implementation already recorded in [2.38.0]).
- Remaining High Priority items (whisper-number cluster, KOL amplification, ETF AP flow, 10b5-1 / buyback execution, unusual options sweep-vs-block, employee outlook, app-store reviews, retail flow, job-posting skill-mix, tokenized-share basis) remain roadmap-only.
- Fresh 2026 research: StockTitan Rhea-AI news impact scoring, OpenAI ChatGPT for Financial Services + Daloopa/LSEG transcripts, SentiSense publisher reliability + MCP, Adanos multi-source sentiment APIs, NorrisAI AlphaLens 15-framework live filings, Marvin Labs guidance-vs-delivered tracking, equity-research platform stack (AlphaSense / Hebbia).
- Added five new roadmap items: News Materiality / Predicted Next-Session Impact Score; Secondary Offering / ATM Dilution Velocity; Multi-Quarter Guidance-vs-Delivered KPI Tracker; Short-Seller Report / Activist Campaign Velocity; Cross-Language / Offshore Narrative Lag.

### Version
- Aligned package, CLI, dashboard and docs to **2.38.1**.

### Notes
- Educational research tool only — not financial advice.

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
