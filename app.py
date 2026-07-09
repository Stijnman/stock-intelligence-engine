import streamlit as st
import pandas as pd
from sie.analyzer import analyze_watchlist
from sie.config import load_config

st.set_page_config(page_title="Stock Intelligence Engine", layout="wide")
st.title("Stock Intelligence Engine v2.1.0 - with X Viral Scanner")

cfg = load_config()
report = analyze_watchlist(cfg, include_news=True, include_social=True)

df = pd.DataFrame(report["rows"])
st.dataframe(df, use_container_width=True)

st.subheader("Signals & Buzz")
for row in report["rows"]:
    st.write(f"{row['color']} **{row['ticker']}**: Signal {row['signal']} | Buzz {row.get('buzz_score', 0)}")