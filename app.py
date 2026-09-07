"""Stock Intelligence Engine — Streamlit Dashboard v2.29.4.

Streamlit Fragment Live Dashboard Refresh + Regime + Confidence +
Supply-Chain CapEx + Short Interest + Attention Momentum +
Authenticity-Filtered Social Narrative Velocity +
Aggregated Consumer Transaction / Credit-Card Panel Spend Nowcasting +
Securities Lending / Borrow Fee & Short Squeeze Risk Overlay.
"""
from __future__ import annotations

import streamlit as st
import pandas as pd
from sie.config import load_config
from sie.analyzer import run_report

__version__ = "2.29.4"

st.set_page_config(page_title="Stock Intelligence Engine", layout="wide")

with st.sidebar:
    st.header("Dashboard Controls")
    cfg = load_config()
    refresh_interval = int(cfg.get("dashboard", {}).get("refresh_interval", 60) or 0)
    st.caption(f"Auto-refresh interval: {refresh_interval}s (0 = off)")
    force_full = st.button("Force Full Refresh", type="primary", use_container_width=True)
    st.divider()
    st.markdown(
        f"**v{__version__}** — Borrow Fee / Squeeze Risk + Consumer Spend Nowcast + Authenticity Filter + "
        "Supply-Chain CapEx + Short Interest + Attention + Fragment Live Refresh + Regime + Confidence + "
        "Honesty + Thesis + Brief + Hiring + EDGAR + 0DTE + IV + Dark Pool + Realtime + Congressional + "
        "13F + Polymarket + Insider + Narrative Velocity"
    )

st.title(
    f"Stock Intelligence Engine v{__version__} — "
    "Borrow Fee & Short Squeeze Risk + Consumer Spend Nowcasting + Authenticity-Filtered Narrative Velocity + "
    "Supply-Chain CapEx + FINRA Short + Attention Momentum + Regime Adaptive Weighting"
)

st.metric("Engine Version", __version__)

@st.fragment(run_every=refresh_interval if refresh_interval > 0 else None)
def signal_table_fragment():
    rows = run_report(export=False, backtest=False)
    if not rows:
        st.warning("No data returned from analyzer.")
        return
    df = pd.DataFrame(rows)
    preferred = [
        "ticker", "name", "signal", "score", "rsi", "price", "change_pct",
        "confidence_score", "confidence_label", "market_regime", "regime_confidence",
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
    f"v{__version__} — Borrow Fee & Short Squeeze Risk + Consumer Spend Nowcasting + "
    "Authenticity-Filtered Narrative Velocity + Supply-Chain CapEx + FINRA Short + Attention Momentum "
    "fully wired · Regime · Confidence · Honesty · Thesis · Brief · Hiring · EDGAR · 0DTE · "
    "Options IV · Dark Pool · Realtime · Congressional · 13F · Polymarket · Insider · Narrative Velocity. "
    "Educational research tool only — not financial advice."
)
