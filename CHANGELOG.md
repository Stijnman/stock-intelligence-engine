# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- This CHANGELOG file standardized for tracking changes
- `.github/` directory structure for GitHub configurations

---

## [2.33.0] - 2026-09-11

### Added
- **`SECURITY.md`**: Complete security policy with financial data handling, platform-specific warnings, developer responsibilities, user warnings, and incident response procedures
- **`CONTRIBUTING.md`**: Detailed contribution guidelines including how to add new features, testing requirements, PR templates, and review process
- **`TESTING.md`**: Comprehensive testing documentation with manual/automated testing guides, checklists, CI/CD pipeline
- **`SKILL.md`**: Repository-level documentation with platform overview, usage examples, and security summary
- **`CODE_OF_CONDUCT.md`**: Contributor Covenant code of conduct
- **`STATUS.md`**: Repository status tracking with quality metrics
- **`CONTRIBUTORS.md`**: Contributors list and recognition
- **`.github/workflows/test.yml`**: GitHub Actions CI/CD workflow with testing, linting, spellcheck, and security scanning
- **`.github/ISSUE_TEMPLATE/bug_report.yml`**: Bug report template with all required fields
- **`.github/ISSUE_TEMPLATE/feature_request.yml`**: Feature request template with categorized options
- **`.github/ISSUE_TEMPLATE/config.yml`**: Issue template configuration
- **`.github/PULL_REQUEST_TEMPLATE.md`**: Pull request template with comprehensive checklist
- **`.pre-commit-config.yaml`**: Pre-commit hooks configuration for code quality
- **`.markdownlint.json`**: Markdown lint configuration
- **`.gitignore`**: Updated with comprehensive exclusions
- **`.secrets.baseline`**: Secrets baseline for detect-secrets

### Changed
- **`CHANGELOG.md`**: Standardized format for consistency
- **`.gitignore`**: Enhanced with additional patterns for Python, testing, and financial data files

### Fixed
- All documentation now has consistent structure and cross-references
- All security warnings properly reference SECURITY.md

---

## [2.32.0] - 2026-09-10

### Added / Completed
- **Patent & Intellectual Property Filing Momentum Overlay fully implemented** (was High Priority open item).
  - New `sie/patent_momentum.py` synthetic proxy (ticker + day seeded) with AI/semi/biotech bias; tracks patent filing velocity, forward-citation velocity and grant ratio.
  - Soft +1 boost on accelerating high-quality patent activity (filing velocity + grant ratio + citation support); -1 caution on decelerating patent momentum.
  - Config section `patent_momentum:` with `enabled`, `boost_velocity`, `penalty_velocity`, `min_grant_ratio`, `min_confidence`.
  - CLI flag `--no-patent-momentum`.
  - Streamlit dashboard preferred columns now surface `pm_filing_velocity`, `pm_citation_velocity`, `pm_grant_ratio`, `pm_direction`, `pm_boost`, `pm_reason`.
  - Fully integrated into `analyze_watchlist` / `run_report` call path after estimate-revision layer.

### Version
- Bumped package, CLI, dashboard and docs to **2.32.0**.

### Notes
- Educational research tool only - not financial advice.

---

## [2.31.0] - 2026-09-09

### Added / Completed
- **Analyst Estimate Revision Velocity & Breadth Overlay fully implemented** (was High Priority open item).
  - New `sie/estimate_revision.py` synthetic proxy (ticker + day seeded) with AI/semi bias; tracks velocity, breadth and direction of consensus estimate revisions.
  - Soft +1 boost on rapid upward revisions with sufficient breadth (narrative durability confirmation); -1 caution on sharp downward revisions even when social heat is elevated.
  - Config section `estimate_revision:` with `enabled`, `boost_velocity`, `penalty_velocity`, `min_breadth`, `min_confidence`.
  - CLI flag `--no-estimate-revision`.
  - Streamlit dashboard preferred columns now surface `er_velocity`, `er_breadth`, `er_direction`, `er_boost`, `er_reason`.
  - Fully integrated into `analyze_watchlist` / `run_report` call path after contagion layer.

### Version
- Bumped package, CLI, dashboard and docs to **2.31.0**.

### Notes
- Educational research tool only - not financial advice.

---

*Changelog standardized: September 11, 2026*
*Educational research tool only - not financial advice.*
