# Future Improvements — Stock Intelligence Engine

**Last updated:** 2026-09-16  
**Current version baseline:** v2.33.2

This file is the single source of truth for the open roadmap.  
Items that are fully implemented and wired (analyzer + CLI + config + dashboard) are removed here and recorded in CHANGELOG.md + README Recent Edits.

---

## High Priority

- [ ] **Dealer Gamma Exposure (GEX) & Pin-Risk Overlay**. Compute approximate dealer gamma exposure and pin-risk levels from options chain / OI data (or high-fidelity synthetic proxy when live chain unavailable). Soft boost when price approaches high-GEX pin levels under supportive narrative; caution on large negative GEX + elevated 0DTE flow. Config block `gex:`, CLI flag, preferred dashboard columns (`gex_score`, `pin_level`, `gex_boost`, `gex_reason`).

- [ ] **Social Trading Action Intent Classifier**. LLM / rule hybrid that classifies social posts (X / Reddit) into actionable intent categories (buy-the-dip, FOMO chase, bag-holding, short-squeeze call, etc.) rather than pure polarity. Filters velocity for high-intent authentic posts only. Soft boost on rising high-intent authentic velocity; caution on low-intent / spam-driven spikes. Extends authenticity layer.

- [ ] **Corporate Credit Spread / CDS Momentum Overlay**. Track relative credit-spread / CDS widening or tightening as a leading fundamental stress / relief signal. Soft boost on tightening spreads + rising narrative (confirmation); caution on rapid widening even when social heat is elevated. Synthetic or free-data proxy preferred for open-source footprint.

- [ ] **Earnings Call Transcript Real-Time Sentiment & Guidance Drift Detector**. Ingest same-day or near-real-time earnings-call / conference transcripts (or high-fidelity synthetic proxies), extract guidance language shifts, management tone, and key-metric sentiment. Soft boost when guidance tone + narrative velocity align upward; caution on guidance soft-pedaling or hedging language that diverges from social heat. Preferred columns: `ect_sentiment`, `ect_guidance_drift`, `ect_boost`, `ect_reason`.

- [ ] **News-Source Authority / Reliability Weighted Narrative Score**. Weight news and social velocity by source authority (tier-1 outlets, verified accounts, historical accuracy proxies) instead of treating all mentions equally. Soft boost on high-authority confirmed narrative; caution on low-authority / unverified spikes. Extends authenticity + honesty layers.

---

## Medium Priority

- [ ] **ESG / Sustainability Narrative LLM-Summary Sentiment Overlay**. Generate short LLM summaries of recent ESG / sustainability disclosures and score the narrative tone + materiality. Soft boost on improving high-materiality ESG narrative; caution on deteriorating or greenwashing-flagged language. Integrates with honesty detector.

- [ ] **Multi-Agent Thesis Debate & Consensus Layer**. Spawn lightweight bull / bear / skeptic agents that debate the current signal stack and produce a consensus confidence adjustment + residual risk list. Surfaces disagreement score on the dashboard. Builds on existing thesis + confidence modules.

- [ ] **Long-Form Content (YouTube / Podcast / Earnings-Call Transcript) Narrative Velocity**. Measure mention velocity and sentiment shift in long-form sources that typically lag short-form social. Soft boost when long-form velocity confirms short-form narrative; caution on divergence (hype without institutional follow-through).

- [ ] **Retail vs Institutional Options Flow Divergence Detector**. Compare retail-dominated flow (small size, 0DTE heavy) against larger / institutional-looking flow. Soft boost when institutional flow confirms the narrative direction; caution when retail is chasing while institutional is fading or hedging.

- [ ] **Expert Network / Conference Call Aspect Extraction Overlay**. Lightweight aspect-based sentiment (pricing power, demand, inventory, AI/CapEx intensity) extracted from expert-network style or public conference transcripts. Soft boost on consistent positive aspect clusters; caution on emerging negative aspect clusters that contradict broad narrative. Synthetic proxy acceptable offline.

- [ ] **MCP / Agent Tool Server Surface**. Expose core analyzer, overlay stack and report generation as a standards-compliant MCP (Model Context Protocol) tool server so external AI agents can call the engine as a first-class financial-intelligence tool. Keeps deterministic offline fallbacks.

---

## Long-Term / Nice-to-Have

- [ ] **Event-Driven Overlay Refresh & Webhook Ingestion**. Move selected overlays (Form 4, EDGAR 8-K, unusual options, major social spikes) to event / webhook driven updates instead of pure poll. Reduce latency for material events while keeping deterministic offline fallbacks.

- [ ] **Maritime AIS / Port Congestion & Freight Rate Leading Indicator Overlay**. Use public AIS / port dwell / freight-rate proxies as leading supply-chain and demand signals for industrials, energy, and consumer names. Soft boost / caution on congestion or rate spikes that corroborate or contradict the current narrative.

- [ ] **Data-Center Power / Energy Intensity Momentum for AI Names**. Track power-purchase, grid-interconnection and energy-intensity signals around major AI data-center operators as a leading CapEx / demand proxy. Complements existing supply-chain CapEx tracker.

- [ ] **Satellite / Geospatial Night-Lights & Activity Proxy Overlay**. Use publicly available night-lights, parking-lot, or mobility-derived activity indices as leading demand / foot-traffic proxies for consumer, retail and industrial names. Soft boost on accelerating activity confirming narrative; caution on deceleration. Synthetic proxy preferred for open-source reproducibility.

---

## Notes

- All new overlays must follow the established pattern: pure function in `sie/`, soft ±1 boost, config block, CLI disable flag, preferred columns in Streamlit, and a deterministic synthetic proxy when live data is unavailable.
- Prefer free / open data sources and local LLM inference to keep the project fully runnable offline.
- Educational research tool only — not financial advice.

*End of roadmap.*
