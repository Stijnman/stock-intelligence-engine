# Future Improvements — Stock Intelligence Engine

**Last updated:** 2026-09-19  
**Current version baseline:** v2.36.0

This file is the single source of truth for the open roadmap.  
Items that are fully implemented and wired (analyzer + CLI + config + dashboard) are removed here and recorded in CHANGELOG.md + README Recent Edits.

---

## High Priority

- [ ] **Earnings Call Transcript Real-Time Sentiment & Guidance Drift Detector**. Ingest same-day or near-real-time earnings-call / conference transcripts (or high-fidelity synthetic proxies), extract guidance language shifts, management tone, and key-metric sentiment. Soft boost when guidance tone + narrative velocity align upward; caution on guidance soft-pedaling or hedging language that diverges from social heat. Preferred columns: `ect_sentiment`, `ect_guidance_drift`, `ect_boost`, `ect_reason`.

- [ ] **News-Source Authority / Reliability Weighted Narrative Score**. Weight news and social velocity by source authority (tier-1 outlets, verified accounts, historical accuracy proxies) instead of treating all mentions equally. Soft boost on high-authority confirmed narrative; caution on low-authority / unverified spikes. Extends authenticity + honesty layers.

- [ ] **Whisper Number / Pre-Earnings Alt-Data Beat Probability Overlay**. Fuse existing nowcasting layers (consumer spend, digital footprint, hiring, attention, supply-chain) into a probabilistic whisper beat/miss estimate ahead of earnings. Soft boost when multi-signal alt-data cluster implies high beat probability + supportive narrative; caution on deteriorating cluster even when street consensus is stable. Preferred columns: `wn_beat_prob`, `wn_cluster_score`, `wn_boost`, `wn_reason`.

- [ ] **Key Opinion Leader (KOL) / Influencer Narrative Amplification Detector**. Identify high-follower / high-engagement authentic accounts driving narrative velocity on X/Reddit/YouTube and score amplification cascades. Soft boost on organic KOL-driven velocity confirmation; caution on coordinated or low-authenticity amplification spikes. Extends authenticity + contagion layers.

- [ ] **ETF Creation / Redemption & Authorized-Participant Flow Overlay**. Track net creation/redemption and premium/discount vs NAV for thematically relevant ETFs as a mechanical demand pulse into underlying names. Soft boost on multi-session creation streaks confirming narrative; caution on redemption streaks or persistent discount while social heat is elevated. Preferred columns: `etf_flow_score`, `etf_prem_disc`, `etf_boost`, `etf_reason`. Synthetic proxy acceptable offline.

- [ ] **Rule 10b5-1 / Buyback Authorization vs Execution Overlay**. Cluster scheduled 10b5-1 plan adoptions/amendments and compare announced buyback authorizations against actual repurchase cadence. Soft boost when execution is running ahead of authorization with supportive narrative; caution on stalled buybacks. Preferred columns: `bb_util`, `bb_plan_delta`, `bb_boost`, `bb_reason`.

- [ ] **Unusual Options Sweep vs Block Confirmation Overlay**. Distinguish aggressive sweep prints from passive blocks on the options tape and score confirmation vs fade against existing 0DTE / IV / GEX layers. Soft boost when multi-strike sweeps align with narrative velocity and positive GEX; caution on large blocks into strength that look like distribution. Preferred columns: `uopt_sweep_score`, `uopt_block_ratio`, `uopt_boost`, `uopt_reason`. Synthetic proxy acceptable offline.

- [ ] **Employee Outlook / Glassdoor Business Sentiment Overlay**. Track employee business-outlook and CEO-approval deltas as an inside-the-firm leading indicator distinct from raw hiring-count momentum. Soft boost when outlook rises with hiring and digital-footprint velocity; caution on collapsing outlook while street estimates are still rising. Preferred columns: `eo_outlook`, `eo_ceo`, `eo_boost`, `eo_reason`.

---

## Medium Priority

See prior roadmap items (ESG narrative, multi-agent thesis debate, long-form velocity, retail vs institutional options flow, expert-network aspects, MCP tool server, GPU/HBM lead-times, 10-K risk-factor delta, FOMC surprise, supplier-customer surprise graph).

- [ ] **Earnings Calendar Distance-Decay & Event-Risk Overlay**. Score days-to-next-print and historically implied event vol so overlays can auto-dampen or concentrate into the event window. Soft boost when pre-event alt-data cluster is aligned and IV is not already fully priced; caution when event is imminent and honesty / contradiction flags are elevated. Preferred columns: `ecd_days`, `ecd_event_vol`, `ecd_boost`, `ecd_reason`.

---

## Long-Term / Nice-to-Have

See prior roadmap items (event-driven webhooks, AIS/freight, data-center power, satellite night-lights, SAR activity, on-chain liquidity pulse).

- [ ] **SEC Comment Letter / Regulatory Docket Velocity Overlay**. Track incoming SEC comment letters, FDA/DoJ/FTC docket pulses, and reply cadence as a slow-burn legal-risk narrative. Soft caution on accelerating comment velocity or unanswered letters; modest boost when dockets close cleanly alongside supportive narrative. Preferred columns: `reg_docket_velocity`, `reg_unanswered`, `reg_boost`, `reg_reason`.

---

## Completed this cycle

- [x] **Corporate Credit Spread / CDS Momentum Overlay** — shipped in v2.36.0 (2026-09-19). Module `sie/credit_spread.py`, CLI `--no-credit-spread`, config `credit_spread:`, dashboard columns `cds_*`.

## Notes

- All new overlays must follow the established pattern: pure function in `sie/`, soft ±1 boost, config block, CLI disable flag, preferred columns in Streamlit, and a deterministic synthetic proxy when live data is unavailable.
- Educational research tool only — not financial advice.

*End of roadmap.*
