# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.44.0] - 2026-09-27

### Added
- **Employee Outlook / Glassdoor Business Sentiment Overlay** (`sie/employee_outlook.py`).
  Scores employer-review outlook, CEO approval and complaint-vs-praise mix as an operational-culture pulse orthogonal to hiring-volume and digital-footprint layers.
  Soft +1 when rising outlook / CEO approval confirms narrative velocity; soft -1 when deteriorating Glassdoor metrics print into elevated social heat.
  Wired through analyzer (`include_employee_outlook`), CLI (`--no-employee-outlook`), config (`employee_outlook:`), Streamlit preferred columns (`eo_outlook`, `eo_ceo`, `eo_review_velocity`, `eo_complaint_share`, `eo_boost`, `eo_reason`).
  Deterministic synthetic proxy when live Glassdoor / Indeed feeds are unavailable.

### Version
- Package, CLI, dashboard and docs aligned to **2.44.0**.

### Notes
- Educational research tool only — not financial advice.

---

## [2.43.1] - 2026-09-27

### Research & Evolution
- Executed the full autonomous research & evolution cycle against `main` @ f783f3ad (2026-09-27).
- Code audit confirmed **Unusual Options Sweep vs Block Confirmation** is fully wired (`sie/unusual_options.py`, analyzer `include_unusual_options`, CLI `--no-unusual-options`, config `unusual_options:`, dashboard `uopt_*`). Removed the leftover checked item from FUTURE-IMPROVEMENTS.md High Priority.
- Confirmed buyback 10b5-1, ETF AP flow, KOL amplification, whisper number, news authority, earnings-call, credit/CDS, social intent, GEX, digital footprint, patent momentum, estimate revision, contagion, borrow fee, consumer spend, authenticity, supply-chain, FINRA short, and attention overlays remain implemented; none of the remaining open High Priority items have matching `sie/` modules.
- 2026 research (SentiSense/Quiver/LangAlpha agent stacks, tokenized-equity DTCC/NYSE/Nasdaq rails, grid-flexible compute load, settlement fails, LLM vs street estimates, long-form newsletter lead-lag) added five net-new roadmap items not previously listed.

### Added (roadmap only)
- High: NSCC / CNS Fail-to-Deliver & Settlement-Stress Overlay.
- High: Behind-the-Meter Flexible-Load / Grid-Curtailment Overlay.
- High: LLM Street-vs-Machine Estimate Divergence Overlay.
- Medium: Long-form Newsletter / Substack Narrative Lead-Lag Overlay.
- Long-Term: Compute Waste-Heat / District-Heating Monetization Overlay.

### Version
- Package, CLI, dashboard and docs aligned to **2.43.1**.

### Notes
- Educational research tool only — not financial advice.

---

See git history for 2.43.0 and earlier releases.

*Educational research tool only — not financial advice.*
