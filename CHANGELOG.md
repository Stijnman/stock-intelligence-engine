# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.48.0] - 2026-10-01

### Added
* **Cross-Venue Tokenized-Share Basis / On-Chain Equity Premium Overlay** (`sie/tokenized_basis.py`).
  Preferred columns: `tok_basis_bps`, `tok_venue_liq`, `tok_boost`, `tok_reason`.
  Soft +1 when a liquid tokenized wrapper trades rich vs the listed share into a hot narrative; caution when the wrapper trades at a deep discount on thin venue liquidity.
  Wired through analyzer (`include_tokenized_basis`), CLI (`--no-tokenized-basis`), config (`tokenized_basis:`), Streamlit preferred columns.
  Deterministic synthetic proxy with live Superstate / Backed / Dinari / Ondo hook reserved.
* Analyzer overlay dispatch table so new flags (`include_tokenized_basis`, `include_hiring_skill_mix`) flow through `run_report(**kwargs)`.

### Changed
* Version bump to **2.48.0** across package, CLI, dashboard and docs.
* Removed the completed Tokenized-Share Basis item from FUTURE-IMPROVEMENTS.md High Priority.

---

## [2.47.1] - 2026-10-01

### Changed
* Autonomous research & evolution cycle against `main` @ 5ba41fb.
* Version strings synchronized to **2.47.1** across package, CLI, dashboard and docs.

See git history for 2.47.0 and earlier releases.

*Educational research tool only — not financial advice.*
