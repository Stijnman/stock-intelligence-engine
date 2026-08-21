"""Stock Intelligence Engine — Streamlit Dashboard v2.20.1."""

import pandas as pd
import streamlit as st

from sie.analyzer import analyze_watchlist
from sie.config import load_config


st.set_page_config(page_title="Stock Intelligence Engine", layout="wide")
st.title(
    "Stock Intelligence Engine v2.20.1 — LLM Bull/Bear Thesis + "
    "Corporate Hiring & Headcount Momentum + Same-Day SEC EDGAR + 0DTE Options Flow + "
    "Options IV Skew + Dark Pool / ATS Flow + Real-time Quotes + Congressional + "
    "Portfolio Correlation + Institutional 13F + Prediction Markets + Insider Clusters + Narrative Velocity"
)

cfg = load_config()

if st.button("Refresh Analysis"):
    st.rerun()

with st.spinner("Analyzing watchlist..."):
    report = analyze_watchlist(cfg)

rows = report.get("rows", []) if report else []
if rows:
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
    # Surface key EDGAR columns if present
    edgar_cols = [c for c in ["edgar_primary_form", "edgar_tone", "edgar_materiality", "edgar_reason"] if c in pd.DataFrame(rows).columns]
    if edgar_cols:
        st.subheader("SEC EDGAR Material Filings")
        st.dataframe(pd.DataFrame(rows)[["ticker"] + edgar_cols], use_container_width=True)
    hiring_cols = [c for c in ["hiring_growth_pct", "hiring_signal", "hiring_confidence", "hiring_reason"] if c in pd.DataFrame(rows).columns]
    if hiring_cols:
        st.subheader("Corporate Hiring & Headcount Momentum")
        st.dataframe(pd.DataFrame(rows)[["ticker"] + hiring_cols], use_container_width=True)
    thesis_cols = [c for c in ["thesis_bull", "thesis_bear", "thesis_confidence", "thesis_reason"] if c in pd.DataFrame(rows).columns]
    if thesis_cols:
        st.subheader("LLM-Generated Bull / Bear Thesis Pairs")
        st.dataframe(pd.DataFrame(rows)[["ticker"] + thesis_cols], use_container_width=True)
else:
    st.warning("No analysis rows returned.")

st.caption(
    "v2.20.1 — LLM-Generated Bull/Bear Thesis Pair Generator fully integrated · Hiring · EDGAR · 0DTE · Options IV · "
    "Dark Pool · Realtime · Congressional · 13F · Polymarket · Insider · Narrative Velocity"
)
