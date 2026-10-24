"""Stock Intelligence Engine \u2014 Streamlit Dashboard v2.71.0.

Unified Real-Time Multi-Source Narrative Freshness Overlay wired.
"""
from __future__ import annotations

import streamlit as st
import pandas as pd

from sie.config import load_config
from sie.analyzer import run_report

__version__ = "2.71.0"

st.set_page_config(page_title="Stock Intelligence Engine", layout="wide")
st.title(f"Stock Intelligence Engine v{__version__}")
st.metric("Engine Version", __version__)
st.markdown(
    "**Unified Real-Time Multi-Source Narrative Freshness Overlay** "
    "(`ums_fresh_s`, `ums_sources_ok`, `ums_boost`, `ums_reason`) is now active."
)

result = run_report(export=False, backtest=False)
if result and "rows" in result:
    df = pd.DataFrame(result["rows"])
    st.dataframe(df, use_container_width=True)
else:
    st.info("No rows returned. Check config.yaml and analyzer wiring.")
