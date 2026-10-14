## [2.62.0] - 2026-10-14

### Added
* **Always-On AI Agent Research Freshness & Workflow Completion Overlay** (`sie/agent_research_freshness.py`).
  Preferred columns: `agt_fresh_s`, `agt_workflow_pct`, `agt_boost`, `agt_reason`.
  Soft +1 when always-on agent research is fresh and high workflow completion into a confirming narrative; caution when agent workflows stall or research age spikes while narrative heat remains elevated.
  Wired through analyzer (`include_agent_research_freshness`), CLI (`--no-agent-research-freshness`), config (`agent_research_freshness:`), Streamlit preferred columns.
  Deterministic synthetic proxy; live agent-monitor feed reserved.

### Changed
* Version bump to **2.62.0** across package, CLI, dashboard and docs.
* Removed completed Always-On AI Agent Research Freshness item from FUTURE-IMPROVEMENTS.md High Priority.

---

## [2.61.1] - 2026-10-14

### Changed
* Autonomous research & evolution cycle against main (v2.61.0).
* Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard). Nothing removed from the roadmap.
* Version strings synchronized to **2.61.1** across package, CLI, dashboard and docs.

### Added
* Roadmap only (not yet implemented):
  * **Agentic Narrative Contagion Velocity Overlay** (High Priority) — `anc_vel`, `anc_agent_share`, `anc_boost`, `anc_reason`.
  * **RAG-Extracted Earnings Guidance Novelty & Hedge Density Overlay** (High Priority) — `rgn_novelty`, `rgn_hedge_density`, `rgn_boost`, `rgn_reason`.
  * **Prediction-Market (Polymarket) vs Options-Implied Probability Basis Overlay** (Medium Priority) — `pmo_basis_bps`, `pmo_poly_prob`, `pmo_boost`, `pmo_reason`.
  * **Narrative Gravity Divergence from Fundamental Valuation Overlay** (Medium Priority) — `ngd_gravity`, `ngd_fund_gap`, `ngd_boost`, `ngd_reason`.
  * **Streamlit Fragment Refresh Health & Staleness Attribution Overlay** (Long-Term) — `sfr_age_s`, `sfr_fragment_ok`, `sfr_boost`, `sfr_reason`.

---

## [2.61.0] - 2026-10-13

### Added
* **AIS Maritime Traffic & Port Congestion Overlay** (`sie/ais_maritime.py`).
  Preferred columns: `ais_congestion`, `ais_wait_hrs`, `ais_boost`, `ais_reason`.
  Soft +1 when key-port congestion eases and vessel waiting times fall into a confirming narrative; caution on rising AIS congestion or extended wait hours while narrative heat remains elevated.
  Wired through analyzer (`include_ais_maritime`), CLI (`--no-ais-maritime`), config (`ais_maritime:`), Streamlit preferred columns.
  Deterministic synthetic proxy; live AIS feed reserved.

### Changed
* Version bump to **2.61.0** across package, CLI, dashboard and docs.
* Removed completed AIS Maritime item from FUTURE-IMPROVEMENTS.md High Priority.

---
