"""Stock Intelligence Engine — Streamlit Dashboard v2.42.0.

Rule 10b5-1 / Buyback Overlay + ETF AP Flow + KOL / Influencer Narrative Amplification +
Whisper Number / Pre-Earnings Alt-Data Beat Probability +
News-Source Authority Weighted Narrative +
Earnings Call Transcript Sentiment & Guidance Drift +
Corporate Credit Spread / CDS Momentum Overlay +
Social Trading Action Intent Classifier +
Authenticity-Filtered Social Narrative Velocity +
Dealer Gamma Exposure (GEX) & Pin-Risk Overlay.
"""
from __future__ import annotations

import streamlit as st
import pandas as pd
from sie.config import load_config
from sie.analyzer import run_report

__version__ = "2.42.0"

st.set_page_config(page_title="Stock Intelligence Engine", layout="wide")

with st.sidebar:
    st.header("Dashboard Controls")
    cfg = load_config()
    refresh_interval = int(cfg.get("dashboard", {}).get("refresh_interval", 60) or 0)
    st.caption(f"Auto-refresh interval: {refresh_interval}s (0 = off)")
    force_full = st.button("Force Full Refresh", type="primary", use_container_width=True)
    st.divider()
    st.markdown(
        f"**v{__version__}** — 10b5-1 / Buyback + KOL Amplification + Whisper Number + News-Source Authority + Earnings-Call Transcript + Credit Spread / CDS + Social Intent + GEX + Digital Footprint + Patent & IP Filing Momentum + Analyst Estimate Revision Velocity + Cross-Ticker Contagion + Borrow Fee / Squeeze Risk + Consumer Spend Nowcast + Authenticity Filter + "
        "Supply-Chain CapEx + Short Interest + Attention + Fragment Live Refresh + Regime + Confidence + "
        "Honesty + Thesis + Brief + Hiring + EDGAR + 0DTE + IV + Dark Pool + Realtime + Congressional + "
        "13F + Polymarket + Insider + Narrative Velocity"
    )

st.title(
    f"Stock Intelligence Engine v{__version__} — "
    "Rule 10b5-1 / Buyback Authorization vs Execution + KOL / Influencer Narrative Amplification + Whisper Number / Pre-Earnings Alt-Data Beat Probability + News-Source Authority Weighted Narrative + Earnings-Call Transcript Sentiment & Guidance Drift + Corporate Credit Spread / CDS + Social Trading Action Intent + GEX + Digital Footprint Momentum + Patent & IP Filing Momentum + Analyst Estimate Revision Velocity & Breadth + Cross-Ticker Narrative Contagion + Borrow Fee & Short Squeeze Risk + "
    "Consumer Spend Nowcasting + Authenticity-Filtered Narrative Velocity + Supply-Chain CapEx + FINRA Short + Attention Momentum + Regime Adaptive Weighting"
)

st.metric("Engine Version", __version__)

@st.fragment(run_every=refresh_interval if refresh_interval > 0 else None)
def signal_table_fragment():
    result = run_report(export=False, backtest=False)
    report = result.get("report") if isinstance(result, dict) else result
    rows = report.get("rows", []) if isinstance(report, dict) else []
    if not rows:
        st.warning("No data returned from analyzer.")
        return
    df = pd.DataFrame(rows)
    preferred = [
        "ticker", "name", "signal", "score", "rsi", "price", "change_pct",
        "confidence_score", "confidence_label", "market_regime", "regime_confidence",
        "er_velocity", "er_breadth", "er_direction", "er_boost", "er_reason",
        "pm_filing_velocity", "pm_citation_velocity", "pm_grant_ratio", "pm_direction", "pm_boost", "pm_reason",
        "ct_score", "ct_velocity_transfer", "ct_boost", "ct_peers", "ct_reason",
        "bf_fee_pct", "bf_dtc", "bf_htb", "bf_boost",
        "cs_momentum", "cs_score", "cs_boost",
        "cds_spread_bp", "cds_delta_bp", "cds_direction", "cds_boost", "cds_reason",
        "ect_sentiment", "ect_guidance_drift", "ect_hedge_density", "ect_direction", "ect_boost", "ect_reason",
        "nsa_authority", "nsa_weighted_vel", "nsa_tier1_share", "nsa_unverified_share", "nsa_boost", "nsa_reason",
        "wn_beat_prob", "wn_cluster_score", "wn_days_to_print", "wn_consensus_gap", "wn_boost", "wn_reason",
        "kol_score", "kol_cascade", "kol_amp_ratio", "kol_auth", "kol_boost", "kol_reason",
        "etf_flow_score", "etf_prem_disc", "etf_create_streak", "etf_theme", "etf_boost", "etf_reason",
        "bb_util", "bb_plan_delta", "bb_auth_usd_bn", "bb_exec_pace", "bb_boost", "bb_reason",
        "sti_intent", "sti_intent_share", "sti_high_intent_velocity", "sti_boost", "sti_reason",
        "auth_score", "auth_filtered_velocity", "auth_boost",
        "sc_capex_score", "sc_side", "sc_boost",
        "si_ratio", "si_boost",
        "attn_momentum", "attn_boost",
        "df_web_traffic_velocity", "df_app_download_velocity", "df_engagement_score", "df_direction", "df_boost", "df_reason",
        "gex_score", "pin_level", "gex_boost", "gex_reason", "gex_net", "gex_flip",
        "honesty_risk", "honesty_label",
        "brief", "thesis_bull", "thesis_bear",
    ]
    cols = [c for c in preferred if c in df.columns] + [c for c in df.columns if c not in preferred]
    st.dataframe(df[cols], use_container_width=True, height=600)

signal_table_fragment()

st.divider()
st.caption(
    f"v{__version__} — Rule 10b5-1 / Buyback Authorization vs Execution Overlay fully wired + KOL / Influencer Narrative Amplification fully wired + Whisper Number / Pre-Earnings Alt-Data Beat Probability Overlay fully wired + News-Source Authority / Reliability Weighted Narrative Overlay fully wired + Earnings Call Transcript Sentiment & Guidance Drift Overlay fully wired + Corporate Credit Spread / CDS Momentum Overlay fully wired + Social Trading Action Intent Classifier fully wired + Dealer GEX & Pin-Risk Overlay fully wired + Company Digital Footprint Momentum Overlay fully wired + Patent & Intellectual Property Filing Momentum Overlay + Analyst Estimate Revision Velocity & Breadth Overlay + Cross-Ticker Narrative Contagion Detector + Borrow Fee & Short Squeeze Risk + Consumer Spend Nowcasting + "
    "Authenticity-Filtered Narrative Velocity + Supply-Chain CapEx + FINRA Short + Attention Momentum "
    "· Regime · Confidence · Honesty · Thesis · Brief · Hiring · EDGAR · 0DTE · "
    "Options IV · Dark Pool · Realtime · Congressional · 13F · Polymarket · Insider · Narrative Velocity. "
    "Educational research tool only — not financial advice."
)
