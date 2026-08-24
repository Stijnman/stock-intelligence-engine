"""Stock Intelligence Engine — Streamlit Dashboard v2.20.4."""
import pandas as pd
import streamlit as st
from sie.analyzer import analyze_watchlist
from sie.config import load_config

st.set_page_config(page_title="Stock Intelligence Engine", layout="wide")
st.title(
    "Stock Intelligence Engine v2.20.4 — LLM Bull/Bear Thesis (fully wired) + "
    "Corporate Hiring & Headcount Momentum + Same-Day SEC EDGAR + 0DTE Options Flow + "
    "Options IV Skew + Dark Pool / ATS Flow + Real-time Quotes + Congressional + "
    "Portfolio Correlation + Institutional 13F + Prediction Markets + Insider Clusters + Narrative Velocity"
)

cfg = load_config()
if st.button("Refresh Analysis"):
    st.rerun()

with st.spinner("Running full analysis pipeline..."):
    report = analyze_watchlist(cfg)
rows = report.get("rows", [])
if rows:
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No analysis rows returned.")

st.caption(
    "v2.20.4 — LLM-Generated Bull/Bear Thesis Pair Generator fully wired end-to-end · Hiring · EDGAR · 0DTE · Options IV · "
    "Dark Pool · Realtime · Congressional · 13F · Polymarket · Insider · Narrative Velocity"
)
