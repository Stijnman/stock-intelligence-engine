"""Stock Intelligence Engine — Streamlit Dashboard v2.32.0.

Streamlit Fragment Live Dashboard Refresh + Regime + Confidence +
Supply-Chain CapEx + Short Interest + Attention Momentum +
Authenticity-Filtered Social Narrative Velocity +
Aggregated Consumer Transaction / Credit-Card Panel Spend Nowcasting +
Securities Lending / Borrow Fee & Short Squeeze Risk Overlay +
Cross-Ticker Narrative Contagion Detector +
Analyst Estimate Revision Velocity & Breadth Overlay +
Patent & Intellectual Property Filing Momentum Overlay.
"""
from __future__ import annotations

import streamlit as st
import pandas as pd
from sie.config import load_config
from sie.analyzer import run_report

__version__ = "2.32.0"

st.set_page_config(page_title="Stock Intelligence Engine", layout="wide")

with st.sidebar:
    st.header("Dashboard Controls")
    cfg = load_config()
    refresh_interval = int(cfg.get("dashboard", {}).get("refresh_interval", 60) or 0)
    st.caption(f"Auto-refresh interval: {refresh_interval}s (0 = off)")
    force_full = st.button("Force Full Refresh", type="primary", use_container_width=True)
    st.divider()
    st.markdown(
        f"**v{__version__}** — Patent & IP Filing Momentum + Analyst Estimate Revision Velocity + Cross-Ticker Contagion + Borrow Fee / Squeeze Risk + Consumer Spend Nowcast + Authenticity Filter + "
        "Supply-Chain CapEx + Short Interest + Attention + Fragment Live Refresh + Regime + Confidence + "
        "Honesty + Thesis + Brief + Hiring + EDGAR + 0DTE + IV + Dark Pool + Realtime + Congressional + "
        "13F + Polymarket + Insider + Narrative Velocity"
    )

st.title(
    f"Stock Intelligence Engine v{__version__} — "
    "Patent & IP Filing Momentum + Analyst Estimate Revision Velocity & Breadth + Cross-Ticker Narrative Contagion + Borrow Fee & Short Squeeze Risk + "
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
        "auth_score", "auth_filtered_velocity", "auth_boost",
        "sc_capex_score", "sc_side", "sc_boost",
        "si_ratio", "si_boost",
        "attn_momentum", "attn_boost",
        "honesty_risk", "honesty_label",
        "brief", "thesis_bull", "thesis_bear",
    ]
    cols = [c for c in preferred if c in df.columns] + [c for c in df.columns if c not in preferred]
    st.dataframe(df[cols], use_container_width=True, height=600)

signal_table_fragment()

st.divider()
st.caption(
    f"v{__version__} — Patent & Intellectual Property Filing Momentum Overlay fully wired + Analyst Estimate Revision Velocity & Breadth Overlay + Cross-Ticker Narrative Contagion Detector + Borrow Fee & Short Squeeze Risk + Consumer Spend Nowcasting + "
    "Authenticity-Filtered Narrative Velocity + Supply-Chain CapEx + FINRA Short + Attention Momentum "
    "· Regime · Confidence · Honesty · Thesis · Brief · Hiring · EDGAR · 0DTE · "
    "Options IV · Dark Pool · Realtime · Congressional · 13F · Polymarket · Insider · Narrative Velocity. "
    "Educational research tool only — not financial advice."
)
