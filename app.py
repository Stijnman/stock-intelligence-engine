"""Stock Intelligence Engine — Streamlit Dashboard v2.73.1.

Expert Network Call Novelty & Sentiment Velocity Overlay wired.
"""
from __future__ import annotations

import streamlit as st
import pandas as pd

from sie.config import load_config
from sie.analyzer import run_report

__version__ = "2.73.1"

st.set_page_config(page_title="Stock Intelligence Engine", layout="wide")
st.title(f"Stock Intelligence Engine v{__version__}")
st.metric("Engine Version", __version__)
st.markdown(
    "**Expert Network Call Novelty & Sentiment Velocity Overlay** "
    "(`enc_novelty`, `enc_sent_vel`, `enc_boost`, `enc_reason`) is now active. "
    "Signed Options Flow Toxicity and Unified Multi-Source Narrative Freshness also retained."
)

result = run_report(export=False, backtest=False)
if result and "rows" in result:
    df = pd.DataFrame(result["rows"])
    st.dataframe(df, use_container_width=True)
else:
    st.info("No rows returned. Check config.yaml and analyzer wiring.")
