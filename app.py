"""Stock Intelligence Engine — Streamlit Dashboard v2.15.3"""
import streamlit as st
import pandas as pd
import time
from sie.analyzer import analyze_watchlist, run_report
from sie.config import load_config
from sie.portfolio import compute_portfolio_overlay, correlation_matrix, portfolio_risk_metrics
from sie.charts import plot_correlation_heatmap
from sie.i18n import t

st.set_page_config(page_title="Stock Intelligence Engine", layout="wide")
st.title("Stock Intelligence Engine v2.15.3 — Options IV Skew + Dark Pool / ATS Flow + Real-time Quotes + Congressional + Portfolio Correlation + Institutional 13F + Prediction Markets + Insider Clusters + Narrative Velocity")

cfg = load_config()

if st.button("Refresh Analysis"):
    st.rerun()

with st.spinner("Analyzing watchlist..."):
    df = analyze_watchlist(cfg)

if df is not None and not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No data returned. Check config and data sources.")

st.caption("v2.15.3 — Options IV Skew & Term Structure Overlay live · Autonomous evolution cycle active")
