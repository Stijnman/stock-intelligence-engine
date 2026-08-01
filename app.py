import streamlit as st
import pandas as pd
import time
from sie.analyzer import analyze_watchlist, run_report
from sie.config import load_config
from sie.backtest import backtest_watchlist

st.set_page_config(page_title="Stock Intelligence Engine", layout="wide")
st.title("Stock Intelligence Engine v2.10.1 — Institutional 13F + Prediction Markets + Insider Clusters + Narrative Velocity")

config = load_config()
watchlist = config.get("watchlist", ["AAPL", "MSFT", "NVDA", "TSLA", "GOOGL"])

st.sidebar.header("Controls")
refresh = st.sidebar.slider("Auto-refresh (seconds)", 30, 300, 60)
do_backtest = st.sidebar.button("Run Backtest")
no_13f = st.sidebar.checkbox("Disable 13F overlay", False)
no_pm = st.sidebar.checkbox("Disable Prediction Markets", False)

placeholder = st.empty()

def render():
    with placeholder.container():
        st.subheader("Live Watchlist Signals")
        results = analyze_watchlist(watchlist, config, use_13f=not no_13f, use_pm=not no_pm)
        if results:
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True)
            for r in results:
                st.caption(f"{r.get('ticker')}: {r.get('signal')} | 13F: {r.get('institutional_side', 'n/a')} Δ{r.get('institutional_pct', 0):.1f}% | PM: {r.get('pm_prob', 'n/a')}")
        else:
            st.warning("No results")

if do_backtest:
    st.subheader("Backtest Results")
    bt = backtest_watchlist(watchlist, config)
    st.json(bt)

render()
time.sleep(0.1)
# Auto refresh loop simplified for stability
