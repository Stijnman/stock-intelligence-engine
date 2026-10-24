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

# Changelog

## v2.69.1 (2026-10-23)

- Autonomous research & evolution cycle against main (v2.69.0). Code audit: no open FUTURE-IMPROVEMENTS item is fully wired (analyzer + CLI + config + dashboard). Nothing removed from the roadmap. Added four new high-value overlays to FUTURE-IMPROVEMENTS.md High Priority (Reddit WallStreetBets & Financial Subreddit Mention Cascade Velocity, Prediction-Market Firm-Level KPI Probability vs Analyst Consensus Basis, Live Insider Trading Cluster Significance & Direct Ownership, Agentic Research Citation Density & Source Authenticity). Version strings synchronized to 2.69.1.

## v2.69.0 (2026-10-22)

- Fully implemented **Kalshi Regulated vs Polymarket Offshore Earnings Beat Probability Basis Overlay** (`sie/kalshi_polymarket_basis.py`).
  Columns: `kpm_basis_bps`, `kpm_kalshi_prob`, `kpm_boost`, `kpm_reason`.
  Soft boost when regulated Kalshi earnings-beat probability shows a rich constructive basis versus offshore Polymarket into a confirming narrative; caution on adverse or collapsing basis while narrative heat remains elevated.
  Wired through analyzer, CLI (`--no-kalshi-polymarket`), config, and Streamlit dashboard.
  Deterministic synthetic proxy (live Kalshi + Polymarket feed reserved).
  Removed from FUTURE-IMPROVEMENTS.md High Priority.
  Asset: [kalshi_polymarket_basis_v2.69.0.svg](https://raw.githubusercontent.com/Stijnman/stock-intelligence-engine/main/assets/kalshi_polymarket_basis_v2.69.0.svg).
