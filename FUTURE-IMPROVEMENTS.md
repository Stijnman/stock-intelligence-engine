# Future Improvements — Stock Intelligence Engine

**Last updated:** 2026-09-18  
**Current version baseline:** v2.35.0

This file is the single source of truth for the open roadmap.  
Items that are fully implemented and wired (analyzer + CLI + config + dashboard) are removed here and recorded in CHANGELOG.md + README Recent Edits.

---

## High Priority

- [ ] **Corporate Credit Spread / CDS Momentum Overlay**. Track relative credit-spread / CDS widening or tightening as a leading fundamental stress / relief signal. Soft boost on tightening spreads + rising narrative (confirmation); caution on rapid widening even when social heat is elevated. Synthetic or free-data proxy preferred for open-source footprint.

- [ ] **Earnings Call Transcript Real-Time Sentiment & Guidance Drift Detector**. Ingest same-day or near-real-time earnings-call / conference transcripts (or high-fidelity synthetic proxies), extract guidance language shifts, management tone, and key-metric sentiment. Soft boost when guidance tone + narrative velocity align upward; caution on guidance soft-pedaling or hedging language that diverges from social heat. Preferred columns: `ect_sentiment`, `ect_guidance_drift`, `ect_boost`, `ect_reason`.

- [ ] **News-Source Authority / Reliability Weighted Narrative Score**. Weight news and social velocity by source authority (tier-1 outlets, verified accounts, historical accuracy proxies) instead of treating all mentions equally. Soft boost on high-authority confirmed narrative; caution on low-authority / unverified spikes. Extends authenticity + honesty layers.

- [ ] **Whisper Number / Pre-Earnings Alt-Data Beat Probability Overlay**. Fuse existing nowcasting layers (consumer spend, digital footprint, hiring, attention, supply-chain) into a probabilistic whisper beat/miss estimate ahead of earnings. Soft boost when multi-signal alt-data cluster implies high beat probability + supportive narrative; caution on deteriorating cluster even when street consensus is stable. Preferred columns: `wn_beat_prob`, `wn_cluster_score`, `wn_boost`, `wn_reason`.

- [ ] **Key Opinion Leader (KOL) / Influencer Narrative Amplification Detector**. Identify high-follower / high-engagement authentic accounts driving narrative velocity on X/Reddit/YouTube and score amplification cascades. Soft boost on organic KOL-driven velocity confirmation; caution on coordinated or low-authenticity amplification spikes. Extends authenticity + contagion layers.

- [ ] **ETF Creation / Redemption & Authorized-Participant Flow Overlay**. Track net creation/redemption and premium/discount vs NAV for thematically relevant ETFs as a mechanical demand pulse into underlying names. Soft boost on multi-session creation streaks confirming narrative; caution on redemption streaks or persistent discount while social heat is elevated. Preferred columns: `etf_flow_score`, `etf_prem_disc`, `etf_boost`, `etf_reason`. Synthetic proxy acceptable offline.

- [ ] **Rule 10b5-1 / Buyback Authorization vs Execution Overlay**. Cluster scheduled 10b5-1 plan adoptions/amendments and compare announced buyback authorizations against actual repurchase cadence. Soft boost when execution is running ahead of authorization with supportive narrative; caution on stalled buybacks. Preferred columns: `bb_util`, `bb_plan_delta`, `bb_boost`, `bb_reason`.

---

## Medium Priority

See prior roadmap items (ESG narrative, multi-agent thesis debate, long-form velocity, retail vs institutional options flow, expert-network aspects, MCP tool server, GPU/HBM lead-times, 10-K risk-factor delta, FOMC surprise, supplier-customer surprise graph).

---

## Long-Term / Nice-to-Have

See prior roadmap items (event-driven webhooks, AIS/freight, data-center power, satellite night-lights, SAR activity, on-chain liquidity pulse).

---

## Notes

- All new overlays must follow the established pattern: pure function in `sie/`, soft ±1 boost, config block, CLI disable flag, preferred columns in Streamlit, and a deterministic synthetic proxy when live data is unavailable.
- Educational research tool only — not financial advice.

*End of roadmap.*
