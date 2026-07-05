# AUTONOMOUS RESEARCH & EVOLUTION CYCLE

**Stock Intelligence Engine – Reusable Maintenance Protocol**  
**Version:** 1.0 (July 2026)  
**Location:** Root of repo for easy future reference  

> **MANDATE:** Research-first. Safety-gated. Exhaustive. No simulation. Real execution only.

This file saves the full autonomous research & evolution process as a repeatable template. Run this cycle periodically (e.g. monthly or on trigger) to keep the project perfectly synchronized with 2026 reality, forward-looking, and production-grade.

---

## Safety Principles & Research-First Mandate (2026 Best Practices)

**Research First – Always:**
- Never propose or remove anything from FUTURE-IMPROVEMENTS.md without live verification against current code, docs, and running behavior.
- Use fresh external research (web, X, papers, tools) before adding new ideas. No hallucinated features.
- Verify "already implemented" claims by inspecting actual files, running tests/CI, and checking runtime output.

**Safety Gates (Non-Negotiable):**
- This cycle is **documentation + roadmap only**. It does **not** auto-edit core Python logic, add untested dependencies, or change runtime behavior without explicit separate PR + human review.
- Direct pushes to `main` are allowed **only** for verified roadmap/doc updates that do not break existing functionality.
- For any code-impacting change: Create a feature branch + PR. Require passing CI + at least one human review.
- Always run full lint + smoke tests (existing `.github/workflows/ci.yml`) before claiming "working".
- Version bumps only on confirmed, shipped changes. Patch for docs/roadmap cleanups; minor for new high-value features added to roadmap.
- Maintain full audit trail: Clear commit messages, SHA references, dates, and "what was actually verified" notes.
- If any verification fails or uncertainty exists → do **not** cleanup/remove from roadmap. Escalate in the entry instead.
- Respect repo ownership: Only push if you have authenticated write access via secure bridge/tooling. Never force or simulate.

**Exhaustive Execution:**
- Zero omissions. Every step below must be completed in order.
- Use live tools (repo inspection, code reading, external search) – no memory shortcuts or prior assumptions.
- After execution, produce concise summary + point to this file for next run.

**Good Place:** This file lives at repo root so it is the single source of truth for the process. Reference it in README.md "Recent Edits" and CONTRIBUTING.md.

---

## Full Exhaustive Cycle (Execute in Order)

### 1. Checkout & Verify Latest State
- Pull latest `main` branch.
- Confirm current version from `stock_intelligence_engine.py`, `app.py`, `README.md`, `CHANGELOG.md`.
- Record current commit SHA and date.

### 2. Read & Analyze All Core Documentation
- `README.md` (especially Recent Edits & Version History)
- `FUTURE-IMPROVEMENTS.md` (all sections, checkboxes, dates)
- `CHANGELOG.md` (top entries)
- `DISCLAIMER.md`, `CONTRIBUTING.md`, `COMPETITION.md`
- Any new docs added since last cycle.

### 3. Perform Thorough Code Audit
- Inspect core files: `stock_intelligence_engine.py`, `app.py`, `config.yaml`, `sie/*.py`, `.github/workflows/ci.yml`, `tests/`, `scripts/`.
- Run existing CI locally or note last successful run.
- **For every item in FUTURE-IMPROVEMENTS.md:**
  - Is it **fully implemented and working** in current code? (test it, read the functions, check dashboard output, run with --news etc.)
  - If yes → mark for cleanup (remove from FUTURE, add to CHANGELOG + README Recent Edits, bump version).
  - If partially or not at all → leave it. Add verification note if needed.
- Check for drift between docs and reality.

### 4. Perform Fresh Research (Research-First Step)
- AI-powered stock analysis tools & narrative intelligence (2026 state of FinBERT, hybrid models, LLM agents in finance).
- Real-time market monitoring dashboards & Streamlit 2026 best practices (session_state, data_editor, Plotly subplots, themes, auto-refresh, responsive).
- New data sources: X/Twitter API v2 usage in trading, Reddit, earnings transcripts, options flow, insider trading, viral signals.
- Backtesting & narrative-aware evaluation (vectorbt, Monte Carlo, walk-forward, phase attribution).
- Cloud deployment, Python tooling, security for automated agents.
- Use multiple sources: web search, X semantic search, papers, competitor analysis (COMPETITION.md), GitHub trending AI finance repos.

### 5. Identify 3–5 Genuinely New, High-Value Improvements
- Must **not** already exist in code or FUTURE-IMPROVEMENTS.md.
- Must be high-signal for narrative + technical stock intelligence edge in 2026.
- Prioritize: real data sources, measurable confidence boost, dashboard usability, backtesting rigor, deployment ease.

### 6. Categorize & Append Cleanly
- Place each new idea at the **very bottom** of the correct section in FUTURE-IMPROVEMENTS.md:
  - High Priority (v2.1)
  - Medium Priority (v2.2)
  - Long-Term / Nice-to-Have (v3.0+)
- Use exact same Markdown style: `- [ ] **Bold Title**. Clear one-paragraph description with config/runtime notes.`
- Update "Last updated: [today's date]" at bottom of FUTURE-IMPROVEMENTS.md.

### 7. Update All Affected Files
- FUTURE-IMPROVEMENTS.md (cleanup verified items + append new ones + date)
- README.md (add detailed entry to "Recent Edits & Version History" section with what was verified, new ideas, version bump reason)
- CHANGELOG.md (new top section with version, date, bullet summary of cleanups + additions)
- Version number bump in:
  - `stock_intelligence_engine.py` (__version__ + docstring)
  - `app.py`
  - `README.md` footer
  - Any other versioned files
- Bump rule: Patch (e.g. v2.0.1 → v2.0.2) for pure docs/roadmap cleanup. Minor for significant new roadmap value.

### 8. Commit & Push Immediately (Real Execution Only)
- Use authenticated GitHub tooling/bridge with write access.
- Commit message format (example):
  `docs(roadmap): vX.Y.Z autonomous research cycle — verified CI, added [new ideas summary], research-first safety audit`
- Push directly to `main`.
- Record the new commit SHA in your summary.
- If no write access or tool failure → output exact patch/diff + instructions for manual apply + commit.

---

## How to Trigger Next Time

Copy the content of this file (or the original prompt) into your AI session and say:

> "Execute the full AUTONOMOUS RESEARCH & EVOLUTION CYCLE from AUTONOMOUS-RESEARCH-EVOLUTION-CYCLE.md with expert precision. Research first, apply all safety gates, be exhaustive."

Future improvement: Turn this into a reusable skill / GitHub Action / agent workflow.

---

## Success Criteria for Each Cycle
- All implemented features from FUTURE-IMPROVEMENTS.md have been verified and cleaned up.
- 3–5 new high-value ideas added in correct sections.
- Version bumped correctly.
- Full audit trail in README + CHANGELOG.
- Real commit pushed (or clear manual instructions given).
- Project is measurably more current and forward-looking than before the cycle.

---

*This protocol keeps the Stock Intelligence Engine feral, accurate, and ahead of the 2026 narrative finance curve. Run it regularly. No shortcuts.*