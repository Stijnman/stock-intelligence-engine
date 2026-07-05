# Changelog

## [2.0.2] - 2026-07-05

### Added
- 5 new high-value roadmap items from fresh July 2026 research into narrative intelligence tools, social sentiment overlays, earnings transcript analysis, news impact classification, and multi-source data fusion:
  - High Priority (v2.1): Narrative contradiction detection engine + Retail social sentiment overlay (Reddit + Stocktwits).
  - Medium Priority (v2.2): Earnings transcript narrative fit scoring + Automated news impact classification feed.
  - Long-Term (v3.0+): Multi-source narrative conviction fusion engine.
- Full execution of the reusable AUTONOMOUS-RESEARCH-EVOLUTION-CYCLE.md protocol with research-first verification and safety gates.

### Changed
- Documentation and roadmap refreshed to stay synchronized with 2026 AI finance trends. No features qualified for cleanup (none of the v2.1+ items are implemented in current code).
- Version bumped to **v2.0.2** for the significant roadmap value added.

## [2.0.1] - 2026-07-05

### Changed
- **Cleanup**: Removed "GitHub Actions CI" from FUTURE-IMPROVEMENTS.md (it was already fully implemented in `.github/workflows/ci.yml` with multi-Python 3.10-3.12 matrix, flake8 linting, smoke tests on import + --export, and artifact uploads on push/PR to main).
- Bumped version to **v2.0.1** across the project (Python `__version__`, Streamlit hero, all documentation).

### Added
- Comprehensive "Recent Edits & Version History" section to README.md documenting the autonomous cycle.
- 5 new high-value roadmap items to FUTURE-IMPROVEMENTS.md based on July 2026 research into AI finance tools, narrative intelligence, real-time monitoring, options data, and modern Streamlit patterns:
  - High Priority: FinBERT/transformer sentiment scoring + X/Twitter v2 real-time viral & sentiment scanner with buzz_score.
  - Medium Priority: Unusual options activity detector & overlay + Streamlit 2026 best practices upgrade (session_state, data_editor, themes, auto-refresh, responsive).
  - Long-Term: Enhanced narrative-aware backtester with vectorbt, Monte Carlo, walk-forward optimization and phase-based attribution.

### Fixed
- Documentation now accurately reflects implemented features (CI was live but undocumented in roadmap/CHANGELOG).

## [2.0.0] - 2026-06-24

### Added
- `sie/` package: technical analysis, news, export, alerts, config, i18n
- RSI(14), MA50, MA200, 52-week drawdown calculations
- Rule-based signals with explicit reason strings
- Working `--news`, `--export`, `--email`, `--refresh` CLI flags
- `config.yaml` driven watchlist and technical thresholds
- Streamlit dashboard with signal table and headlines
- `COMPETITION.md` competitive analysis and feature brainstorm
- `pyyaml` dependency

### Fixed
- README aligned with actual implementation (was marketing-only in v1.0)

## [1.0.0] - 2026-05-23

### Added
- Initial public release (price-only prototype)
- Docker scaffold, disclaimers, branding