"""Streamlit dashboard for Stock Intelligence Engine."""

import streamlit as st

from sie.analyzer import analyze_watchlist, format_report
from sie.config import load_config
from sie.export import export_csv

st.set_page_config(page_title="Stock Intelligence Engine", layout="wide", page_icon="📈")

cfg = load_config()
lang = st.sidebar.selectbox("Language", ["en", "nl"])
include_news = st.sidebar.checkbox("Include headlines", value=True)
auto_export = st.sidebar.checkbox("Export CSV on analyze", value=False)

st.title("📈 Stock Intelligence Engine")
st.caption(f"Narrative theme: **{cfg['narrative']['theme']}**")

if st.button("Analyze watchlist", type="primary"):
    report = analyze_watchlist(cfg, include_news=include_news, lang=lang)
    st.code(format_report(report), language=None)

    rows = report["rows"]
    display = [
        {
            "Ticker": r["ticker"],
            "Name": r["name"],
            "Price": r.get("price"),
            "RSI": r.get("rsi"),
            "MA50": r.get("ma50"),
            "MA200": r.get("ma200"),
            "52w DD%": r.get("drawdown_pct"),
            "Signal": r.get("signal"),
            "Fit": r.get("narrative_fit"),
        }
        for r in rows
    ]
    st.dataframe(display, use_container_width=True)

    for r in rows:
        if r.get("headlines"):
            with st.expander(f"{r['ticker']} headlines"):
                for h in r["headlines"]:
                    st.write(f"• {h}")

    if auto_export:
        flat = [{k: v for k, v in r.items() if k != "headlines"} for r in rows]
        path = export_csv(flat, cfg.get("export", {}).get("directory", "exports"))
        st.success(f"Exported {path}")

st.info("Educational tool only — not financial advice.")