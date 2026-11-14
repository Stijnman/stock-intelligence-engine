## v2.79.0 (2026-11-14)

- Added persistent SQLite history for issuer-confirmed KID/factsheet snapshots and issuer-labelled TER/OCF observations (local cache by default; configurable with `SIE_ETF_HISTORY_DB`).
- Added SHA-256 fingerprinting of downloaded PDF bytes and automatic KID/factsheet content-change events, including cost deltas where comparable values exist.
- Added cross-issuer ETF TER/OCF comparison, ranking and annual euro cost per €10,000; PRIIPs management/administrative cost proxies, transaction costs and RIY are excluded from TER ranking.
- Added Streamlit history/change views and CLI commands `etf-cost-history` and `etf-cost-compare`.

## v2.78.0 (2026-11-14)

- Completed ISIN-first Amundi document discovery using the issuer's public product and document APIs; selects the latest public English PRIIPs KID and monthly factsheet.
- Completed iShares document discovery: public search index locates the issuer product page, the exact ISIN is confirmed in that page, and the current PRIIPs KID URL is derived from the issuer KIID filename/share-class slug and ISIN, with a product-title fallback; issuer factsheet link is collected alongside it.
- All downloaded PDFs must be hosted on the issuer's official domain and contain the requested ISIN before cost evidence is accepted. Search index is used only for product-page discovery, never as a source of fee values.
- Returns both KID and factsheet metadata/evidence; top-level costs prioritize the PRIIPs KID. Factsheet/KID date extraction now respects the document's publication/as-of date instead of fund inception dates.
- Added mocked adapter tests and live end-to-end checks for Amundi and iShares; no manual PDF URL required.

## v2.77.0 (2026-11-14)

- Added issuer-first ETF KID/factsheet cost extraction for Vanguard, iShares/BlackRock, Amundi and Xtrackers/DWS.
- Extracts ongoing charges/TER-labelled values, portfolio transaction costs, entry/exit costs, performance fees, reduction-in-yield and tracking-difference where explicitly disclosed.
- Preserves source URL, ISIN confirmation, document date, extracted evidence snippets, method and text SHA-256; ambiguous or missing values remain unverified.
- Added `etf-costs` CLI and PDF text extraction through the system `pdftotext` utility (Poppler); no paid API or Python PDF dependency.

## v2.76.0 (2026-11-14)

- Implemented Belgian ETF/UCITS and investor tax engine using the official FSMA foreign UCI workbook, Wikifin TOB classifications and FPS Finance withholding guidance.
- Added TOB rates/caps by legal form, registration and share-class type; SICAV/FCP-aware cash distribution withholding; issuer-KID TER provenance and cost projections; FSMA register verification and Streamlit/CLI integration.
- Explicitly surfaced missing FSMA share-class ISIN data and exclusions for 2026 capital-gains tax and full fund-level look-through tax.

## v2.75.0 (2026-10-28)

- Fully implemented **Tokenized Equity Continuous Pricing Premium vs Traditional Session Close Basis Overlay** (`sie/tokenized_equity_premium.py`).
  Columns: `tep_basis_bps`, `tep_24_5_vol_share`, `tep_boost`, `tep_reason`.
  Soft boost when on-chain/tokenized equity continuous pricing (Robinhood, Ondo, MarketVector 24/5 indexes, etc.) shows a rich constructive premium and elevated 24/5 volume share into a confirming narrative; caution on adverse or collapsing continuous basis while narrative heat remains elevated.
  Wired through analyzer, CLI (`--no-tokenized-equity-premium`), config, and Streamlit dashboard.
  Deterministic synthetic proxy (live tokenized equity feed reserved).
  Removed from FUTURE-IMPROVEMENTS.md High Priority.
  Asset: [tokenized_equity_premium_v2.75.0.svg](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/tokenized_equity_premium_v2.75.0.svg).

## v2.74.1 (2026-10-28)

- Autonomous research & evolution cycle against main (v2.74.0). Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard). Nothing removed from the roadmap. Added four new high-value overlays to FUTURE-IMPROVEMENTS.md (two High Priority: Agentic Prediction-Market Trade Execution Latency & Fill Quality Overlay, Crowdsourced Earnings Estimate Revision Cascade Velocity Overlay; two Medium Priority: Finance Podcast & Long-Form Audio Transcript Sentiment Velocity Overlay, On-Chain Tokenized Equity Smart-Money Wallet Clustering Overlay). Version strings synchronized to 2.74.1.

## v2.74.0 (2026-10-27)

- Fully implemented **Agentic MCP Tool-Call Chain Latency & Success Rate Overlay** (`sie/agentic_mcp_tool_call_latency.py`).
  Columns: `mcp_latency_ms`, `mcp_success_rate`, `mcp_boost`, `mcp_reason`.
  Soft boost when agentic research workflows show low tool-call latency and high success/completion rate against financial MCP servers (Distilla, Equibles, Alpha Vantage MCP, etc.) into a confirming narrative; caution on elevated latency, tool failures, or incomplete chains while narrative heat remains elevated.
  Wired through analyzer, CLI (`--no-agentic-mcp-tool-call-latency`), config, and Streamlit dashboard.
  Deterministic synthetic proxy (live MCP telemetry reserved).
  Removed from FUTURE-IMPROVEMENTS.md High Priority.
  Asset: [agentic_mcp_tool_call_latency_v2.74.0.svg](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/agentic_mcp_tool_call_latency_v2.74.0.svg).

## v2.73.1 (2026-10-27)

- Autonomous research & evolution cycle against main (v2.73.0). Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard). Nothing removed from the roadmap. Added four new high-value overlays to FUTURE-IMPROVEMENTS.md (one High Priority: AI Multi-Model Council Forecast vs Prediction Market Probability Basis Overlay; two Medium Priority: Equibles MCP Full-Text Filing & Transcript Extraction Completeness & Latency Overlay, Graded AI Verdict Hit-Rate Cascade on Prediction Markets Overlay; one Long-Term: Sports Prediction Market Official Data Partnership Spillover Narrative Contagion Overlay). Version strings synchronized to 2.73.1.

## v2.73.0 (2026-10-26)

- Fully implemented **Expert Network Call Novelty & Sentiment Velocity Overlay** (`sie/expert_network_call_novelty.py`).
  Columns: `enc_novelty`, `enc_sent_vel`, `enc_boost`, `enc_reason`.
  Soft boost when high-novelty expert-network (Tegus/GLG-style) call transcripts exhibit constructive sentiment velocity confirming a narrative into technical strength; caution on low-novelty or adverse expert sentiment while narrative heat remains elevated.
  Wired through analyzer, CLI (`--no-expert-network-call-novelty`), config, and Streamlit dashboard.
  Deterministic synthetic proxy (live expert-network feed reserved).
  Removed from FUTURE-IMPROVEMENTS.md High Priority.
  Asset: [expert_network_call_novelty_v2.73.0.svg](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/expert_network_call_novelty_v2.73.0.svg).

## v2.72.1 (2026-10-26)

- Autonomous research & evolution cycle against main (v2.72.0). Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard). Nothing removed from the roadmap. Added four new high-value overlays to FUTURE-IMPROVEMENTS.md (two High Priority: Hiring Velocity & Employee Outlook Sentiment Overlay, Short Interest & Fails-to-Deliver Squeeze Pressure Overlay; two Medium Priority: App Download & Consumer Engagement Velocity Overlay, Prediction-Market Agent Signal Cascade Velocity Overlay). Version strings synchronized to 2.72.1.

## v2.72.0 (2026-10-25)

- Fully implemented **Signed Options Flow Toxicity & Informed Trading Probability Overlay** (`sie/signed_options_flow_toxicity.py`).
  Columns: `oft_toxicity`, `oft_informed_prob`, `oft_boost`, `oft_reason`.
  Soft boost when signed OPRA flow (customer buys/sells) shows low toxicity and constructive informed-trading probability into a confirming narrative; caution on elevated toxicity or adverse informed flow while narrative heat stays elevated.
  Wired through analyzer, CLI (`--no-signed-options-flow-toxicity`), config, and Streamlit dashboard.
  Deterministic synthetic proxy (live signed options-flow feed reserved).
  Removed from FUTURE-IMPROVEMENTS.md High Priority.
  Asset: [signed_options_flow_toxicity_v2.72.0.svg](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/signed_options_flow_toxicity_v2.72.0.svg).

## v2.71.1 (2026-10-25)

- Autonomous research & evolution cycle against main (v2.71.0). Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard). Nothing removed from the roadmap. Added four new high-value overlays to FUTURE-IMPROVEMENTS.md (two High Priority: Truth Social Influential Political Account Narrative Velocity Overlay, Adanos Unified Social + Prediction-Market Buzz Velocity Overlay; two Medium Priority: Multi-LLM Ensemble Financial Headline Sentiment Divergence Overlay, Streamlit st.fragment Live Market Pulse Auto-Refresh Overlay). Version strings synchronized to 2.71.1.

## v2.71.0 (2026-10-24)

- Fully implemented **Unified Real-Time Multi-Source Narrative Freshness Overlay** (`sie/unified_multi_source_narrative_freshness.py`).
  Columns: `ums_fresh_s`, `ums_sources_ok`, `ums_boost`, `ums_reason`.
  Soft boost when unified multi-source (news, X cashtags, SEC filings, Form 4, congressional disclosures) remains fresh and constructively aligned into a confirming narrative; caution on stale sources or adverse clustering while narrative heat stays elevated.
  Wired through analyzer, CLI (`--no-unified-multi-source-narrative-freshness`), config, and Streamlit dashboard.
  Deterministic synthetic proxy (live multi-source aggregator reserved).
  Removed from FUTURE-IMPROVEMENTS.md High Priority.
  Asset: [unified_multi_source_narrative_freshness_v2.71.0.svg](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/unified_multi_source_narrative_freshness_v2.71.0.svg).

## v2.70.1 (2026-10-24)

- Autonomous research & evolution cycle against main (v2.70.0). Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard). Nothing removed from the roadmap. Added five new high-value overlays to FUTURE-IMPROVEMENTS.md (three High Priority: Dark Pool / Off-Exchange Institutional Block Print Intensity & Informed Flow Overlay, Real-Time Earnings Call Transcript Sentiment Velocity vs Pre-Call Narrative Overlay, Gamma Exposure (GEX) Regime & Dealer Hedging Pressure Overlay; two Medium Priority: Congressional Trade Disclosure Clustering & Timing Alpha Overlay, Web Traffic & App Engagement Velocity as Leading Demand Proxy Overlay). Version strings synchronized to 2.70.1.

## v2.70.0 (2026-10-23)

- Fully implemented **Agent-Generated Research Memo Cascade Velocity Overlay** (`sie/agent_generated_memo_cascade.py`).
  Columns: `agc_vel`, `agc_memo_share`, `agc_boost`, `agc_reason`.
  Soft boost when high-velocity cascade of agent-generated research memos (AlphaSense SuperAnalyst-style always-on workflows) confirms a narrative into technical strength; caution when cascade collapses or turns adversarial while human narrative heat remains elevated.
  Wired through analyzer, CLI (`--no-agent-generated-memo-cascade`), config, and Streamlit dashboard.
  Deterministic synthetic proxy (live agent-memo monitor reserved).
  Removed from FUTURE-IMPROVEMENTS.md High Priority.
  Asset: [agent_generated_memo_cascade_v2.70.0.svg](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/agent_generated_memo_cascade_v2.70.0.svg).

## Unreleased — Advanced Investment Analytics

- Added dependency-light quantitative analytics for portfolio risk, optimization, Monte Carlo scenarios, a friction-aware buy-and-hold baseline, factor beta, correlation and market-regime heuristics.
- Added dividend sustainability, DCF sensitivity, earnings-surprise, financial-distress, fair-value consensus and rule-based alert calculations.
- Added configurable Belgian tax scenarios, broker-cost estimates, explicit-FX EUR portfolio reporting and sector momentum ranking.
- Added normalizers for supplied earnings calendars, UCITS ETF metadata, SEC-style insider transactions, institutional holdings, options chains and disclosed supply-chain relationships.
- Added strict provenance states and documented which features still require live provider adapters and dashboard wiring. No trade execution or paid API dependency was introduced.
- Added deterministic unit coverage for the new analytics layer.
- Added periodic target-weight backtesting, explicit-metric stock screening and transparent watchlist ranking.


- Added public CFTC Legacy Futures Only COT adapter with weekly non-commercial/commercial net positioning summaries.
- Added optional FRED observations adapter requiring a user-owned free API key, plus CLI commands and terms/non-endorsement notice.

- Added SEC EDGAR Form 4 transaction parsing and 13F-HR information-table extraction using public filings, with mandatory contact-bearing User-Agent and delayed-disclosure caveats.
- Added CLI commands for Form 4 insider scans and 13F manager holdings; live-source provenance is preserved in insider sentiment summaries.

- Added U.S. Treasury Fiscal Data Debt to the Penny adapter (no key), CLI access and graceful integration into the macro snapshot.

- Added date-aligned multi-asset historical risk and backtest workflows, exposed through CLI commands. Removed hard-coded Sharpe/return placeholders from the legacy backtest wrapper.
- Added an official SEC 8-K Item 2.02 reported-earnings history command; dates are verified filings, not estimated future events or consensus surprises.

- Added Belgian ETF tax engine: live cached FSMA foreign-UCIs/UCITS register parser, legal-form/share-class TOB calculator with caps, SICAV/FCP-aware net cash-distribution yield, issuer-KID TER cost projections and a cautious Reynders tax screen.
- Added CLI commands `fsma-uci`, `be-tob`, `be-net-dividend`; integrated FSMA verification into `etf` and added a Streamlit Belgian ETF tax panel.
- Versioned tax assumptions and documented exclusions, including the 2026 capital-gains tax and fund-specific look-through tax.
