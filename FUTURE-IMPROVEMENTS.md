# Future Improvements — Stock Intelligence Engine

**Last updated:** 2026-10-10
**Current version baseline:** v2.58.0

This file is the single source of truth for the open roadmap.
Items that are fully implemented and wired (analyzer + CLI + config + dashboard) are removed here and recorded in CHANGELOG.md + README Recent Edits.

---

## High Priority

- [ ] **Domain-Tuned Financial LLM vs General LLM Sentiment Gap Overlay**.
  Preferred columns: `flm_sent`, `flm_gen_gap`, `flm_boost`, `flm_reason`.
  Soft boost when a domain-tuned financial LLM sentiment diverges constructively from a general LLM baseline into a confirming narrative; caution on adverse divergence.

- [ ] **Listed Event-Contract Book Depth vs Offshore Prediction-Market Basis Overlay**.
  Preferred columns: `lec_basis_bps`, `lec_listed_depth`, `lec_boost`, `lec_reason`.
  Soft boost when listed event-contract book depth supports a rich basis versus offshore prediction markets into a confirming narrative; caution on thin listed depth with adverse basis.

---

## Medium Priority

- [ ] **Reddit-ICE Market Insights Conversation Velocity Overlay**.
  Preferred columns: `rdt_vel`, `rdt_theme_align`, `rdt_boost`, `rdt_reason`.

- [ ] **MCP Data-Feed Freshness & Attestation Overlay**.
  Preferred columns: `mcp_age_s`, `mcp_attested`, `mcp_boost`, `mcp_reason`.

---

## Completed (moved to CHANGELOG)

- [x] **Agentic Brokerage Account Flow & Penetration Overlay** (v2.58.0, 2026-10-10). Preferred columns: `agt_flow_share`, `agt_tool_intensity`, `agt_boost`, `agt_reason`.
