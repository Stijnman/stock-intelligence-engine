# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.42.1] - 2026-09-26

### Research & Evolution
- Executed the full autonomous research & evolution cycle against `main` @ b85ac9a (2026-09-26).
- Code audit confirmed **Rule 10b5-1 / Buyback Authorization vs Execution** is fully wired (`sie/buyback_10b51.py`, analyzer `include_buyback_10b51`, CLI `--no-buyback-10b51`, config `buyback_10b51:`, dashboard `bb_*`). Removed the leftover checked item from FUTURE-IMPROVEMENTS.md High Priority.
- Confirmed ETF AP Flow, KOL amplification, whisper number, news authority, earnings-call, credit/CDS, social intent, GEX, digital footprint, patent momentum, estimate revision, contagion, borrow fee, consumer spend, authenticity, supply-chain, FINRA short, and attention overlays remain implemented; none of the remaining open High Priority items have matching `sie/` modules.
- 2026 research (sentiment APIs + MCP agents, SEC-filing AI platforms, news-impact engines, ChatGPT Financial Services / GPT-6 Astra, ECB LLM stability sentiment) added five net-new roadmap items not previously listed.

### Added (roadmap only)
- High: Tariff / Trade-Policy Exposure Overlay.
- High: AI Token-Cost / Inference-Price Deflation Overlay.
- High: Corporate Aviation / Executive Flight-Pattern Overlay.
- Medium: Form 8-K Item 1.05 Cybersecurity Incident Velocity Overlay.
- Long-Term: Class-Action / Multidistrict Litigation Filing Velocity Overlay.

### Version
- Package, CLI, dashboard and docs aligned to **2.42.1**.

### Notes
- Educational research tool only — not financial advice.

---

## [2.42.0] - 2026-09-25

### Added
- **Rule 10b5-1 / Buyback Authorization vs Execution Overlay** (`sie/buyback_10b51.py`).
  Clusters scheduled 10b5-1 plan adoptions/amendments and compares announced buyback authorizations against actual repurchase cadence.
  Soft +1 when execution runs ahead of authorization with supportive narrative; soft -1 on stalled buybacks into elevated social heat.
  Wired through analyzer (`include_buyback_10b51`), CLI (`--no-buyback-10b51`), config (`buyback_10b51:`), Streamlit preferred columns (`bb_util`, `bb_plan_delta`, `bb_auth_usd_bn`, `bb_exec_pace`, `bb_boost`, `bb_reason`).
  Deterministic synthetic proxy when live Form 10b5-1 / 8-K execution feeds are unavailable.

### Version
- Package, CLI, dashboard and docs aligned to **2.42.0**.

### Notes
- Educational research tool only — not financial advice.

---

## [2.41.1] - 2026-09-25

### Research & Evolution
- Executed the full autonomous research & evolution cycle against `main` @ 7e7df352.
- Code audit confirmed **ETF Creation / Redemption & Authorized-Participant Flow** is fully wired (`sie/etf_flow.py`, analyzer `include_etf_flow`, CLI `--no-etf-flow`, config `etf_flow:`). Removed from FUTURE-IMPROVEMENTS.md High Priority (implementation shipped in v2.41.0; roadmap was lagging).
- Dashboard `__version__` was still on 2.40.1 and omitted `etf_*` preferred columns — aligned to 2.41.1.
- Added five 2026 research items: CEO/CFO vocal-affect earnings audio (High), 13F amendment / late-filer velocity (High), hyperscaler interconnection-queue / AI power lead-time (Medium), dealer inventory vs GEX divergence (Medium), FOMC / central-bank vocal-stress (Long-Term).

### Version
- Package, CLI, dashboard and docs aligned to **2.41.1**.

### Notes
- Educational research tool only — not financial advice.

---

## [2.41.0] - 2026-09-24

### Added
- **ETF Creation / Redemption & Authorized-Participant Flow Overlay** (`sie/etf_flow.py`).

### Version
- Package, CLI, dashboard and docs aligned to **2.41.0**.

---

See git history for 2.40.1 and earlier releases.

*Educational research tool only — not financial advice.*
