"""Stock Intelligence Engine — Streamlit Dashboard v2.13.0"""
import streamlit as st
import pandas as pd
import time
from sie.analyzer import analyze_watchlist, run_report
from sie.config import load_config
from sie.backtest import backtest_watchlist
from sie.portfolio import compute_portfolio_overlay, correlation_heatmap_figure

st.set_page_config(page_title="Stock Intelligence Engine", layout="wide")
st.title("Stock Intelligence Engine v2.13.0 — Real-time WebSocket Quotes + Congressional + Portfolio Correlation + Institutional 13F + Prediction Markets + Insider Clusters + Narrative Velocity")

config = load_config()
watchlist = list(config.get("tickers", {}).keys()) or ["AAPL", "MSFT", "NVDA", "TSLA", "GOOGL"]

st.sidebar.header("Controls")
refresh = st.sidebar.slider("Auto-refresh (seconds)", 30, 300, 60)
do_backtest = st.sidebar.button("Run Backtest")
show_portfolio = st.sidebar.checkbox("Show Portfolio Risk Overlay", True)
no_13f = st.sidebar.checkbox("Disable 13F overlay", False)
no_pm = st.sidebar.checkbox("Disable Prediction Markets", False)
no_insider = st.sidebar.checkbox("Disable Insider clusters", False)
no_congress = st.sidebar.checkbox("Disable Congressional overlay", False)
no_realtime = st.sidebar.checkbox("Disable Real-time Quotes", False)

placeholder = st.empty()

def render():
    with placeholder.container():
        st.subheader("Live Watchlist Signals")
        report = analyze_watchlist(
            config,
            include_insider=not no_insider,
            include_pm=not no_pm,
            include_institutional=not no_13f,
            include_congressional=not no_congress,
            include_realtime=not no_realtime,
        )
        results = report.get("rows", [])
        if results:
            df = pd.DataFrame(results)
            # Select key columns for cleaner display
            display_cols = [c for c in [
                "ticker", "signal", "price", "realtime_change_pct", "rsi", "drawdown_pct",
                "predicted_phase", "inst_side", "inst_pct_change",
                "cong_side", "cong_net_value",
                "pm_prob", "realtime_source", "signal_reason"
            ] if c in df.columns]
            st.dataframe(df[display_cols] if display_cols else df, use_container_width=True)
            for r in results:
                rt_note = ""
                if r.get("realtime_source") and r.get("realtime_source") != "disabled":
                    chg = r.get("realtime_change_pct")
                    lat = r.get("realtime_latency_ms")
                    rt_note = f" | RT {chg:+.2f}% ({r.get('realtime_source')}, {lat}ms)" if chg is not None else f" | RT src={r.get('realtime_source')}"
                st.caption(
                    f"{r.get('ticker')}: {r.get('signal')} | "
                    f"13F: {r.get('inst_side', 'n/a')} Δ{r.get('inst_pct_change', 0):.1f}% | "
                    f"Congress: {r.get('cong_side', 'n/a')} ${r.get('cong_net_value', 0):,} | "
                    f"PM: {r.get('pm_prob', 'n/a')} | "
                    f"Forecast: {r.get('predicted_phase', 'n/a')}"
                    f"{rt_note}"
                )
        else:
            st.warning("No results")

        if show_portfolio:
            st.subheader("Portfolio Correlation Heatmap & Risk Overlay")
            overlay = compute_portfolio_overlay(config)
            metrics = overlay.get("metrics", {})
            if metrics and not metrics.get("error"):
                cols = st.columns(4)
                cols[0].metric("Ann. Volatility", f"{metrics.get('vol_ann', 0)*100:.1f}%" if metrics.get("vol_ann") is not None else "n/a")
                cols[1].metric("Sharpe (eq-wt)", f"{metrics.get('sharpe', 0):.2f}" if metrics.get("sharpe") is not None else "n/a")
                cols[2].metric("Max Drawdown", f"{metrics.get('max_drawdown', 0):.1f}%" if metrics.get("max_drawdown") is not None else "n/a")
                cols[3].metric("Mean Corr", f"{metrics.get('mean_corr', 0):.2f}" if metrics.get("mean_corr") is not None else "n/a")
                fig = correlation_heatmap_figure(overlay.get("correlation", {}))
                st.plotly_chart(fig, use_container_width=True)
                st.caption(f"Lookback: {overlay.get('period')} · Assets: {metrics.get('n_assets')} · Days: {metrics.get('period_days')} · Source: {overlay.get('source')}")
            else:
                st.info("Portfolio overlay unavailable or disabled.")

if do_backtest:
    st.subheader("Backtest Results")
    bt = backtest_watchlist(config)
    st.json(bt)
    # Also surface portfolio metrics in backtest view
    overlay = compute_portfolio_overlay(config)
    st.write("**Equal-weight Portfolio Risk (same lookback)**")
    st.json(overlay.get("metrics", {}))

render()
time.sleep(0.1)
# Auto refresh loop simplified for stability
