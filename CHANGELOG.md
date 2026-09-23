# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.40.0] - 2026-09-23

### Added
- **Key Opinion Leader (KOL) / Influencer Narrative Amplification Detector** (`sie/kol_amplification.py`).
  Scores high-follower / high-engagement authentic accounts and amplification cascades across X / Reddit / YouTube proxies.
  Soft +1 when organic KOL-driven velocity confirms an authentic narrative; soft -1 on coordinated or low-authenticity amplification spikes.
  Wired through analyzer (`include_kol_amplification`), CLI (`--no-kol-amplification`), config (`kol_amplification:`), Streamlit preferred columns (`kol_score`, `kol_cascade`, `kol_amp_ratio`, `kol_auth`, `kol_boost`, `kol_reason`).
  Deterministic synthetic proxy when live follower-graph feeds are unavailable.

### Version
- Package, CLI, dashboard and docs aligned to **2.40.0**.

### Notes
- Educational research tool only — not financial advice.

---

## [2.39.2] - 2026-09-23

### Research & Evolution
- Executed the full `AUTONOMOUS-RESEARCH-EVOLUTION-CYCLE.md` against `main` @ 0a38a715.
- Verified every open `FUTURE-IMPROVEMENTS.md` concept against the current `sie/` module tree, analyzer imports/flags, CLI disable flags, config defaults and Streamlit preferred columns. **No open roadmap item satisfies the complete wiring gate**, so none was removed.
- Fresh 2026 research covered prediction-market event contracts (Kalshi / Polymarket / FMI event-risk TAM), passive index reconstitution flow, 10-Q working-capital quality, SaaS public status-page incident velocity, and CAT-bond / reinsurance rate-on-line as a sector stress pulse.
- Added five non-duplicate roadmap overlays:
  - **Index Reconstitution & Forced Passive-Flow Overlay** (High Priority)
  - **Listed Earnings Event-Contract vs Whisper / Street Divergence Overlay** (High Priority)
  - **Working-Capital / DSO-DIO Drift Overlay** (Medium Priority)
  - **Cloud / SaaS Status-Page Incident Velocity Overlay** (Medium Priority)
  - **CAT-Bond / Reinsurance Rate-on-Line Sector Stress Overlay** (Long-Term)

### Version
- Aligned package, CLI, dashboard and docs to **2.39.2**.
- Patch bump only: no runtime signal logic or dependency surface was changed by this research-cycle release.

### Notes
- Educational research tool only — not financial advice.

---

## [2.39.1] - 2026-09-22

### Research & Evolution
- Executed the full `AUTONOMOUS-RESEARCH-EVOLUTION-CYCLE.md` with research-first and safety gates.
- Exhaustively verified every open `FUTURE-IMPROVEMENTS.md` concept against the current `sie/` module tree.
- Added five non-duplicate roadmap overlays (TRACE, primary credit issuance, target-specific stance, alt-data provenance, Rule 606).

### Version
- Aligned package, CLI, dashboard and docs to **2.39.1**.

---

## [2.39.0] - 2026-09-22

### Added / Completed
- **Whisper Number / Pre-Earnings Alt-Data Beat Probability Overlay** (`sie/whisper_number.py`).

### Version
- Aligned package, CLI, dashboard and docs to **2.39.0**.

---

See git history for 2.38.x and earlier releases.

*Educational research tool only — not financial advice.*
