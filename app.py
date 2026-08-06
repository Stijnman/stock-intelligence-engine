"""Stock Intelligence Engine — Streamlit Dashboard v2.14.1"""
import streamlit as st
import pandas as pd
import time
from sie.analyzer import analyze_watchlist, run_report
from sie.config import load_config
from sie.portfolio import compute_portfolio_overlay
from sie.charts import plot_correlation_heatmap

st.set_page_config(page_title="Stock Intelligence Engine", layout="wide")
st.title("Stock Intelligence Engine v2.14.1 — Dark Pool / ATS Flow + Real-time Quotes + Congressional + Portfolio Correlation + Institutional 13F + Prediction Markets + Insider Clusters + Narrative Velocity")

cfg = load_config()

# Sidebar controls
st.sidebar.header("Controls")
auto_refresh = st.sidebar.checkbox("Auto-refresh", value=True)
interval = st.sidebar.slider("Refresh interval (s)", 30, 300, 60)

if st.sidebar.button("Run full report") or auto_refresh:
    with st.spinner("Analyzing..."):
        df = analyze_watchlist(cfg)
        st.dataframe(df)
        # Additional overlays rendered in full app

if st.sidebar.button("Portfolio Correlation"):
    overlay = compute_portfolio_overlay(cfg)
    st.plotly_chart(plot_correlation_heatmap(overlay))

st.caption("v2.14.1 — Autonomous evolution cycle active")
