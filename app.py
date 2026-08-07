"""Stock Intelligence Engine — Streamlit Dashboard v2.15.0"""
import streamlit as st
import pandas as pd
import time
from sie.analyzer import analyze_watchlist, run_report
from sie.config import load_config
from sie.portfolio import compute_portfolio_overlay
from sie.charts import plot_correlation_heatmap

st.set_page_config(page_title="Stock Intelligence Engine", layout="wide")
st.title("Stock Intelligence Engine v2.15.0 — Options IV Skew + Dark Pool / ATS Flow + Real-time Quotes + Congressional + Portfolio Correlation + Institutional 13F + Prediction Markets + Insider Clusters + Narrative Velocity")

cfg = load_config()

# Sidebar controls
st.sidebar.header("Controls")
auto_refresh = st.sidebar.checkbox("Auto-refresh", value=True)
interval = st.sidebar.slider("Refresh interval (s)", 30, 300, 60)

if st.sidebar.button("Run full report") or auto_refresh:
    with st.spinner("Analyzing..."):
        report = analyze_watchlist(cfg)
        rows = report.get("rows", [])
        if rows:
            df = pd.DataFrame(rows)
            # Prefer key signal + overlay columns when present
            display_cols = [c for c in [
                "ticker", "name", "signal", "price", "rsi", "drawdown_pct",
                "iv_skew_ratio", "iv_term_slope", "iv_atm", "iv_boost",
                "dark_pool_side", "dark_pool_ratio",
                "predicted_phase", "forecast_boost",
            ] if c in df.columns]
            st.dataframe(df[display_cols] if display_cols else df, use_container_width=True)
            for row in rows:
                if row.get("iv_reason"):
                    st.caption(f"{row.get('ticker')}: IV — {row.get('iv_reason')}")
        else:
            st.write(report)

if st.sidebar.button("Portfolio Correlation"):
    overlay = compute_portfolio_overlay(cfg)
    st.plotly_chart(plot_correlation_heatmap(overlay), use_container_width=True)

st.caption("v2.15.0 — Options IV Skew & Term Structure Overlay live · Autonomous evolution cycle active")
