import streamlit as st
import pandas as pd
from sie.analyzer import analyze_watchlist
from sie.config import load_config

st.set_page_config(page_title="Stock Intelligence Engine", layout="wide")
st.title("Stock Intelligence Engine v2.2.0 - FinBERT Sentiment")

cfg = load_config()
report = analyze_watchlist(cfg, include_news=True, include_social=True)

df = pd.DataFrame(report["rows"])
# Flatten headlines for display
if not df.empty and "headlines" in df.columns:
    df["news_sentiment"] = df["headlines"].apply(lambda hs: [h.get("sentiment_label", "") for h in hs] if isinstance(hs, list) else [])
st.dataframe(df.drop(columns=["headlines"], errors="ignore"), use_container_width=True)

st.subheader("Signals, Buzz & News Sentiment")
for row in report["rows"]:
    news_info = ""
    if row.get("headlines"):
        news_info = " | News: " + ", ".join([f"{h.get('sentiment_label', '')} ({h.get('sentiment_score',0):+.2f})" for h in row["headlines"]])
    st.write(f"{row['color']} **{row['ticker']}**: Signal {row['signal']} | Buzz {row.get('buzz_score', 0)}{news_info}")