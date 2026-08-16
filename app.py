"""Stock Intelligence Engine — Streamlit Dashboard v2.17.0."""

import pandas as pd
import streamlit as st

from sie.analyzer import analyze_watchlist
from sie.config import load_config


st.set_page_config(page_title="Stock Intelligence Engine", layout="wide")
st.title(
    "Stock Intelligence Engine v2.17.0 — 0DTE Options Flow + Options IV Skew + "
    "Dark Pool / ATS Flow + Real-time Quotes + Congressional + Portfolio Correlation + "
    "Institutional 13F + Prediction Markets + Insider Clusters + Narrative Velocity + "
    "Same-Day SEC EDGAR"
)

cfg = load_config()

if st.button("Refresh Analysis"):
    st.rerun()

with st.spinner("Analyzing watchlist..."):
    report = analyze_watchlist(cfg)

rows = report.get("rows", []) if report else []
if rows:
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
else:
    st.warning("No data returned. Check config and data sources.")

st.caption(
    "v2.17.0 — Same-Day SEC EDGAR Material Filing Detector live · 0DTE · Options IV · "
    "Autonomous evolution cycle active"
)
