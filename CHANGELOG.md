# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.41.0] - 2026-09-24

### Added
- **ETF Creation / Redemption & Authorized-Participant Flow Overlay** (`sie/etf_flow.py`).
  Tracks net creation/redemption and premium/discount vs NAV for thematically relevant ETFs as a mechanical demand pulse into underlying names.
  Soft +1 on multi-session creation streaks confirming narrative; soft -1 on redemption streaks or persistent NAV discount while social heat is elevated.
  Wired through analyzer (`include_etf_flow`), CLI (`--no-etf-flow`), config (`etf_flow:`), Streamlit preferred columns (`etf_flow_score`, `etf_prem_disc`, `etf_create_streak`, `etf_theme`, `etf_boost`, `etf_reason`).
  Deterministic synthetic proxy when live AP / iNAV feeds are unavailable.

### Version
- Package, CLI, dashboard and docs aligned to **2.41.0**.

### Notes
- Educational research tool only — not financial advice.

---

## [2.40.1] - 2026-09-24

### Research & Evolution
- Executed the full autonomous research & evolution cycle against `main` @ 404b8c09 / follow-on version bump commit.
- Code audit confirmed **KOL / Influencer Narrative Amplification** is fully wired (`sie/kol_amplification.py`, analyzer `include_kol_amplification`, CLI `--no-kol-amplification`, config `kol_amplification:`). Removed from FUTURE-IMPROVEMENTS.md High Priority (implementation shipped in v2.40.0; roadmap was lagging).
- Dashboard `__version__` and preferred-column list were still on 2.39.2 and omitted `kol_*` — aligned to 2.40.1.

### Version
- Aligned package, CLI, dashboard and docs to **2.40.1**.

### Notes
- Educational research tool only — not financial advice.

---

## [2.40.0] - 2026-09-23

### Added
- **Key Opinion Leader (KOL) / Influencer Narrative Amplification Detector** (`sie/kol_amplification.py`).

### Version
- Package, CLI, dashboard and docs aligned to **2.40.0**.

---

See git history for 2.39.2 and earlier releases.

*Educational research tool only — not financial advice.*
