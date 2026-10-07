# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.54.1] - 2026-10-07

### Changed
* Autonomous research & evolution cycle against `main` @ ce6d39c (v2.54.0).
* Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard) beyond the v2.54.0 alt-data provenance overlay. Nothing removed from the roadmap.
* Version strings synchronized to **2.54.1** across package, CLI, dashboard and docs.

### Added
* Roadmap only (not yet implemented):
  * **CFTC Mention-Market / Named-Speaker Event-Contract Manipulation Overlay** (High Priority) — `mmk_oi_share`, `mmk_manip_flag`, `mmk_boost`, `mmk_reason`.
  * **Tokenized NMS Venue (TSV) AMM Pool Premium Overlay** (High Priority) — `tsv_pool_premium_bps`, `tsv_lp_depth`, `tsv_boost`, `tsv_reason`.
  * **Prediction-Market ETF Event-Overlap Beta Overlay** (High Priority) — `pmetf_beta`, `pmetf_event_overlap`, `pmetf_boost`, `pmetf_reason`.
  * **XBRL Custom-Extension Tag Ratio Overlay** (Medium Priority) — `xbrl_ext_ratio`, `xbrl_new_tags`, `xbrl_boost`, `xbrl_reason`.
  * **Water-Rights / Basin Curtailment Exposure Overlay** (Long-Term) — `wtr_curtail_flag`, `wtr_rev_share`, `wtr_boost`, `wtr_reason`.

---

See prior entries below. Full history through v2.47.1 is retained in git history if this summary is insufficient; the v2.54.0 entry follows.

## [2.54.0] - 2026-10-06

### Added
* Commit: https://github.com/Stijnman/stock-intelligence-engine/commit/b4710b4ccee1bdf2bfa3ba5fc33f9b8f7d015e59
* **Alternative-Data Provenance & AI-Synthetic Contamination Confidence Overlay** (`sie/alt_data_provenance.py`).
  Preferred columns: `adp_provenance`, `adp_crosscheck`, `adp_boost`, `adp_reason`.
  Soft +1 when attested provenance and an independent cross-check confirm a narrative; caution when narrative heat arrives on synthetic or uncorroborated alt-data.
  Wired through analyzer (`include_alt_data_provenance`), CLI (`--no-alt-data-provenance`), config (`alt_data_provenance:`), Streamlit preferred columns.
  Deterministic synthetic proxy; live vendor-attestation hook reserved.
* Dashboard chart: `assets/alt_data_provenance_v2.54.0.svg`.
* Unit tests: `tests/test_alt_data_provenance.py`.

### Changed
* Removed the completed Alternative-Data Provenance item from FUTURE-IMPROVEMENTS.md High Priority.
* Version strings synchronized to **2.54.0**.

---

## [2.53.1] - 2026-10-06

### Changed
* Autonomous research & evolution cycle against `main` @ c4c3bc5 (v2.53.0).
* Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard) beyond the v2.53.0 target-stance overlay. Nothing removed from the roadmap.
* Version strings synchronized to **2.53.1** across package, CLI, dashboard and docs.

### Added
* Roadmap only (not yet implemented):
  * **SEC Staff Comment-Letter & Filing-Review Velocity Overlay** (High Priority) — `cmt_open_letters`, `cmt_days_open`, `cmt_boost`, `cmt_reason`.
  * **Rule 10b-18 Daily Volume-Cap Proximity Overlay** (High Priority) — `b18_cap_used`, `b18_days_left`, `b18_boost`, `b18_reason`.
  * **Treasury GC / Sponsored-Repo Funding-Stress Spillover Overlay** (High Priority) — `repo_gc_spread`, `repo_equity_beta`, `repo_boost`, `repo_reason`.
  * **Channel Inventory Days & Working-Capital Fill Overlay** (Medium Priority) — `inv_days`, `inv_fill_delta`, `inv_boost`, `inv_reason`.
  * **State Incentive Clawback & Jobs-Credit Exposure Overlay** (Long-Term) — `inc_clawback_usd`, `inc_jobs_gap`, `inc_boost`, `inc_reason`.

---

Earlier releases (v2.53.0 through v2.47.1) are unchanged and remain in the previous CHANGELOG body on main before this cycle. See commit ce6d39c for the full pre-2.54.1 text.

*Educational research tool only — not financial advice.*
