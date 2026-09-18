# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.34.0] - 2026-09-18

### Added / Completed
- **Dealer Gamma Exposure (GEX) & Pin-Risk Overlay fully wired** (was High Priority open item).
  - Module `sie/gex.py` already existed with live yfinance-chain attempt + deterministic synthetic proxy.
  - CLI already exposed `--no-gex` / `include_gex`, but `analyze_watchlist` / `run_report` did not accept the flag and did not call `integrate_gex_to_row` — passing `include_gex` would have raised TypeError.
  - Now imported and integrated after the digital-footprint layer; `run_report` forwards `include_gex`.
  - Streamlit preferred columns: `gex_score`, `pin_level`, `gex_boost`, `gex_reason`, `gex_net`, `gex_flip`.
  - Default `gex:` block added to `sie/config.py`.
  - Removed from FUTURE-IMPROVEMENTS.md High Priority.

### Research & Evolution
- Autonomous research & evolution cycle executed (2026-09-18).
- Code audit confirmed prior overlays remain wired; GEX was the only completed-but-unwired overlay.
- Fresh 2026 research: AltIndex AI Score + developer API, NowNews / AlphaSense / Hebbia / Fintool / Signals.ai, NorrisAI AlphaLens, Massive MCP market-data server, ChatGPT for Financial Services (GPT-6 Astra), ETF creation/redemption flow, month-end rebalancing predictability.

### Added (Roadmap)
- **ETF Creation / Redemption & Authorized-Participant Flow Overlay** (High Priority) — new.
- **Rule 10b5-1 / Buyback Authorization vs Execution Overlay** (High Priority) — new.
- **FOMC / Central-Bank Speech Surprise Score** (Medium Priority) — new.
- **Supplier–Customer Earnings Surprise Propagation Graph** (Medium Priority) — new.
- **On-Chain Stablecoin / Tokenized-Treasury Liquidity Pulse** (Long-Term) — new.

### Version
- Aligned package, CLI, dashboard and docs to **2.34.0**.

### Notes
- Educational research tool only — not financial advice.

---

## [2.33.3] - 2026-09-17

### Research & Evolution
- Autonomous research & evolution cycle executed (2026-09-17).
- Prior overlays confirmed fully wired. Five roadmap items added (Whisper Number, KOL Amplification, GPU/HBM Lead-Time, 10-K Risk Factor Delta, SAR Activity).

### Version
- **2.33.3**

---

See git history for earlier changelog entries (2.33.2 through 2.31.0).

*Educational research tool only — not financial advice.*
