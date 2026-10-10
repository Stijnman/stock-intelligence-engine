## [2.58.0] - 2026-10-10

### Added
* **Agentic Brokerage Account Flow & Penetration Overlay** (`sie/agentic_flow.py`).
  Preferred columns: `agt_flow_share`, `agt_tool_intensity`, `agt_boost`, `agt_reason`.
  Soft +1 when high agentic account flow share coincides with elevated tool intensity into a confirming narrative; caution when agentic accounts fade while narrative heat remains elevated.
  Wired through analyzer (`include_agentic_flow`), CLI (`--no-agentic-flow`), config (`agentic_flow:`), Streamlit preferred columns.
  Deterministic synthetic proxy; live brokerage agent-flow feed reserved.
* Dashboard chart: `assets/agentic_flow_v2.58.0.svg`.
* Unit tests: `tests/test_agentic_flow.py`.

### Changed
* Version bump to **2.58.0** across package, CLI, dashboard and docs.
* Removed the completed Agentic Brokerage Account Flow item from FUTURE-IMPROVEMENTS.md High Priority.

---

## [2.57.1] - 2026-10-10

### Changed
* Autonomous research & evolution cycle against main (v2.57.0).
* Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard) beyond the v2.57.0 earnings event-contract overlay. Nothing removed from the roadmap.
* Version strings synchronized to **2.57.1** across package, CLI, dashboard and docs.

### Added
* Roadmap only (not yet implemented):
  * **Agentic Brokerage Account Flow & Penetration Overlay** (High Priority) — `agt_flow_share`, `agt_tool_intensity`, `agt_boost`, `agt_reason`.
  * **Domain-Tuned Financial LLM vs General LLM Sentiment Gap Overlay** (High Priority) — `flm_sent`, `flm_gen_gap`, `flm_boost`, `flm_reason`.
  * **Listed Event-Contract Book Depth vs Offshore Prediction-Market Basis Overlay** (High Priority) — `lec_basis_bps`, `lec_listed_depth`, `lec_boost`, `lec_reason`.
  * **Reddit-ICE Market Insights Conversation Velocity Overlay** (Medium Priority) — `rdt_vel`, `rdt_theme_align`, `rdt_boost`, `rdt_reason`.
  * **MCP Data-Feed Freshness & Attestation Overlay** (Medium Priority) — `mcp_age_s`, `mcp_attested`, `mcp_boost`, `mcp_reason`.

---

# Prior changelog history preserved in git. See commits before this for v2.57.0 and earlier.
