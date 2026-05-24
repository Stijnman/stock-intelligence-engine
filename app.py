# Streamlit Dashboard for Stock Intelligence Engine
import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Stock Intelligence Engine", layout="wide")
st.title("Stock Intelligence Engine")
st.subheader("Narrative-Aware Stock Analysis")

# Sidebar
st.sidebar.header("Controls")
lang = st.sidebar.selectbox("Language", ["en", "nl"])
tickers = ["NVDA", "TSM", "CBRS", "CRDO", "MU"]

if st.button("Analyze Market Narrative"):
    st.write("### Current Narrative: AI Inference Boom")
    data = []
    for t in tickers:
        try:
            stock = yf.Ticker(t)
            info = stock.info
            price = info.get('regularMarketPrice', 'N/A')
            data.append({"Ticker": t, "Price": price, "Note": "Strong narrative fit"})
        except:
            pass
    df = pd.DataFrame(data)
    st.dataframe(df)

st.info("Production Dashboard with NL query support coming in future iterations.")