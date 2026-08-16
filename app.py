"""Stock Intelligence Engine — Streamlit Dashboard v2.18.0."""

import pandas as pd
import streamlit as st

from sie.analyzer import analyze_watchlist
from sie.config import load_config


st.set_page_config(page_title="Stock Intelligence Engine", layout="wide")
st.title(
    "Stock Intelligence Engine v2.18.0 — Same-Day SEC EDGAR + 0DTE Options Flow + "
    "Options IV Skew + Dark Pool / ATS Flow + Real-time Quotes + Congressional + "
    "Portfolio Correlation + Institutional 13F + Prediction Markets + Insider Clusters + "
    "Narrative Velocity"
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
        st.subheader("Same-Day SEC EDGAR Filings")
        st.dataframe(pd.DataFrame(rows)[["ticker"] + edgar_cols], use_container_width=True)
else:
    st.warning("No data returned. Check config and data sources.")

st.caption(
    "v2.18.0 — Same-Day SEC EDGAR Material Filing Detector fully integrated · 0DTE · Options IV · "
    "Autonomous maintainer cycle"
)
