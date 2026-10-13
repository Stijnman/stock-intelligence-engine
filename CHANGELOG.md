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

## [2.60.0] - 2026-10-12

### Added
* **Domain-Tuned Financial LLM vs General LLM Sentiment Gap Overlay** (`sie/fin_llm_gap.py`).
  Preferred columns: `flm_sent`, `flm_gen_gap`, `flm_boost`, `flm_reason`.
  Soft +1 when domain-tuned financial LLM sentiment is constructively more positive than a general LLM baseline into a confirming narrative; caution on adverse divergence while narrative heat remains elevated.
  Wired through analyzer (`include_fin_llm_gap`), CLI (`--no-fin-llm-gap`), config (`fin_llm_gap:`), Streamlit preferred columns.
  Deterministic synthetic proxy; live dual-LLM inference hook reserved.

### Changed
* Version bump to **2.60.0** across package, CLI, dashboard and docs.
* Removed completed Domain-Tuned FinLLM Gap item from FUTURE-IMPROVEMENTS.md High Priority.
* Restored full analyzer.py and CLI from prior production state after placeholder drift.

---

## [2.59.1] - 2026-10-12

### Changed
* Autonomous research & evolution cycle against main (v2.59.0).
* Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard). Nothing removed from the roadmap.
* Version strings synchronized to **2.59.1** across package, CLI, dashboard and docs.

### Added
* Roadmap only (not yet implemented):
  * **Always-On AI Agent Research Freshness & Workflow Completion Overlay** (High Priority) — `agt_fresh_s`, `agt_workflow_pct`, `agt_boost`, `agt_reason`.
  * **SEC Filing Structured Extraction Latency & Completeness Overlay** (High Priority) — `sec_latency_s`, `sec_completeness`, `sec_boost`, `sec_reason`.
  * **Cross-Platform Retail Sentiment Divergence (X + Reddit + StockTwits) Overlay** (Medium Priority) — `xrs_div`, `xrs_align`, `xrs_boost`, `xrs_reason`.
  * **Social Narrative Authenticity Scoring & Cluster Confidence Overlay** (Medium Priority) — `sna_auth`, `sna_cluster_conf`, `sna_boost`, `sna_reason`.
  * **WebSocket Streaming Latency Attribution vs Polling Overlay** (Long-Term) — `ws_latency_ms`, `poll_delta_ms`, `ws_boost`, `ws_reason`.

---

## [2.59.0] - 2026-10-11

### Added
* **Satellite Imagery / Geospatial Physical Activity Overlay** (`sie/satellite_imagery.py`).
  Preferred columns: `sat_fill`, `sat_delta`, `sat_boost`, `sat_reason`.
  Soft +1 when rising physical activity proxies (parking-lot fill rates, oil-tank levels, night-light intensity, vessel counts) confirm a narrative; caution on sharp activity drops while narrative heat remains elevated.
  Wired through analyzer (`include_satellite_imagery`), CLI (`--no-satellite-imagery`), config (`satellite_imagery:`), Streamlit preferred columns.
  Deterministic synthetic proxy; live satellite feed reserved.

### Changed
* Version bump to **2.59.0** across package, CLI, dashboard and docs.
* Removed completed Satellite Imagery item from FUTURE-IMPROVEMENTS.md High Priority.

---

## [2.58.1] - 2026-10-11

### Changed
* Autonomous research & evolution cycle against main (v2.58.0).
* Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard). Nothing removed from the roadmap.
* Version strings synchronized to **2.58.1** across package, CLI, dashboard and docs.

### Added
* Roadmap only (not yet implemented):
  * **Satellite Imagery / Geospatial Physical Activity Overlay** (High Priority) — `sat_fill`, `sat_delta`, `sat_boost`, `sat_reason`.
  * **AIS Maritime Traffic & Port Congestion Overlay** (High Priority) — `ais_congestion`, `ais_wait_hrs`, `ais_boost`, `ais_reason`.
  * **Real-Time X/Twitter Cashtag Firehose Velocity with Bot Filter Overlay** (Medium Priority) — `xtw_vel`, `xtw_auth`, `xtw_boost`, `xtw_reason`.
  * **Multi-Venue Options Flow Sweep Aggregation & Dark-Pool Cross-Confirmation Overlay** (Medium Priority) — `mvo_sweep`, `mvo_dark_conf`, `mvo_boost`, `mvo_reason`.
  * **European Consolidated Tape Liquidity Visibility Overlay** (Long-Term) — `ect_liq`, `ect_spread`, `ect_boost`, `ect_reason`.

---

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
