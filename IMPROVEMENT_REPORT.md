**2026-10-04 — v2.52.0** Primary Credit Issuance / New-Issue Concession & Supply Pressure Overlay implemented and wired (analyzer, CLI, config, dashboard, tests). Prior notes below.

# Improvement Report

**2026-10-02 — v2.49.0** News Materiality / Predicted Next-Session Impact Score Overlay implemented and wired (analyzer, CLI, config, dashboard). Prior notes below.

# Improvement Report

## Baseline
Portfolio audit score: **80.0/100**.

## Changes in this pass
- Added a single-command Makefile for install, lint, tests, coverage, local run, dashboard, and Docker lifecycle.
- Added Dependabot for Python and GitHub Actions dependencies.
- Added CodeQL static analysis.
- Added Trivy container vulnerability scanning.

## Existing strengths verified
- Python CI across 3.10, 3.11, and 3.12.
- pytest coverage workflow and Codecov upload.
- Dockerfile with health check.
- Docker Compose for CLI and Streamlit dashboard.
- .env.example and security policy.
- Secret scanning via TruffleHog.

## Remaining gaps
- Coverage percentage should be measured from a fresh CI run before claiming a numeric target.
- Existing CI is Linux-only; cross-platform validation should be added only after confirming all dependencies support Windows/macOS.
- README needs a compact architecture diagram and an operations/troubleshooting section.
- Runtime health for the Streamlit service is container-level rather than a dedicated HTTP health API.

## Provisional post-change score
**84/100**, pending green CI and measured coverage.
