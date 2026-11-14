"""Stock Intelligence Engine — unified Streamlit dashboard."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from sie.analyzer import run_report
from sie.config import load_config

__version__ = "2.75.0"

st.set_page_config(page_title="Stock Intelligence Engine", layout="wide")
st.title(f"Stock Intelligence Engine v{__version__}")
st.caption("Narrative overlays are experimental synthetic proxies. Fundamental analysis uses external provider data.")

cfg = load_config()
configured_tickers = list((cfg.get("tickers") or {}).keys())
with st.sidebar:
    st.header("Research settings")
    selected = st.multiselect(
        "Watchlist",
        options=configured_tickers or ["NVDA", "TSLA", "AAPL", "MSFT", "INTC"],
        default=(configured_tickers or ["NVDA", "TSLA", "AAPL", "MSFT", "INTC"])[:5],
    )
    show_fundamentals = st.checkbox("Fetch live market + SEC fundamentals", value=True)
    show_news = st.checkbox("Fetch recent headlines", value=False)
    run_clicked = st.button("Run analysis", type="primary")

if "sie_report" not in st.session_state or run_clicked:
    if run_clicked and selected:
        cfg["tickers"] = {ticker: {} for ticker in selected}
    with st.spinner("Collecting available research data..."):
        st.session_state["sie_report"] = run_report(
            config=cfg,
            include_investment=show_fundamentals,
            include_news=show_news,
        )

report = st.session_state["sie_report"]
rows = report.get("rows", [])
if rows:
    st.subheader("Narrative overlay diagnostics")
    st.warning("Overlay values are synthetic test proxies, not live options flow, tokenized-market activity or expert-network telemetry.")
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

analyses = report.get("investment_analysis", {})
if analyses:
    st.subheader("Market and fundamental analysis")
    summary = []
    for ticker, analysis in analyses.items():
        market = analysis.get("market", {})
        fundamentals = analysis.get("fundamentals", {})
        latest = fundamentals.get("latest", {}) if isinstance(fundamentals, dict) else {}
        valuation = analysis.get("valuation", {})
        base = valuation.get("base", {}) if isinstance(valuation, dict) else {}
        summary.append({
            "Ticker": ticker,
            "Price": market.get("price"),
            "Currency": market.get("currency"),
            "As of": market.get("as_of"),
            "Revenue": latest.get("revenue"),
            "FCF": latest.get("free_cash_flow"),
            "DCF base/share": base.get("intrinsic_value_per_share"),
            "Margin of safety %": base.get("margin_of_safety_pct"),
            "Data quality": " | ".join(analysis.get("data_quality", [])),
        })
    st.dataframe(pd.DataFrame(summary), use_container_width=True, hide_index=True)
    for ticker, analysis in analyses.items():
        with st.expander(f"{ticker} — detailed research"):
            st.json(analysis)

news = report.get("news", {})
if news:
    st.subheader("Recent headlines")
    for ticker, items in news.items():
        st.markdown(f"**{ticker}**")
        if isinstance(items, list) and items:
            st.dataframe(pd.DataFrame(items), use_container_width=True, hide_index=True)
        else:
            st.caption("No headlines returned by the provider.")

st.caption(f"Generated: {report.get('generated_at', 'unknown')} · Enabled overlays: {', '.join(report.get('overlays', [])) or 'none'}")
