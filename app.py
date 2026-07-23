import streamlit as st
import pandas as pd
import time
from sie.analyzer import analyze_watchlist, run_report
from sie.config import load_config
from sie.backtest import backtest_watchlist

st.set_page_config(page_title="Stock Intelligence Engine", layout="wide")
st.title("Stock Intelligence Engine v2.6.0 - Real-time Dashboard with Backtesting")

cfg = load_config()
dashboard_cfg = cfg.get("dashboard", {})
refresh_interval = dashboard_cfg.get("refresh_interval", 60)

if st.button("Run Backtest on Watchlist"):
    with st.spinner("Running historical backtest..."):
        bt = backtest_watchlist(cfg)
        st.subheader("📊 Backtest Results")
        for tkr, res in bt.items():
            st.write(f"**{tkr}**: Sharpe {res.get('sharpe_ratio')}, Return {res.get('total_return_pct')}%")

# Auto-refresh logic
if refresh_interval > 0:
    st.info(f"🔄 Auto-refreshing every {refresh_interval} seconds. Live prices, signals & X narratives.")
    placeholder = st.empty()
    while True:
        with placeholder.container():
            report = analyze_watchlist(cfg, include_news=True, include_social=True)
            df = pd.DataFrame(report["rows"])
            st.dataframe(df.drop(columns=["headlines"], errors="ignore"), use_container_width=True)

            st.subheader("Signals, Buzz & X Narratives")
            for row in report["rows"]:
                narr = f"Narr: {row.get('dominant_narrative','N/A')} {'🚨CRISIS' if row.get('crisis_flag') else ''} Vel:{row.get('sentiment_velocity',0):.1f}"
                news_info = ""
                if row.get("headlines"):
                    news_info = " | News sent: " + str([h.get('sentiment_label') for h in row["headlines"]])
                st.write(f"{row.get('color','')} **{row['ticker']}**: {row.get('signal','')} | Buzz {row.get('buzz_score',0)} | {narr}{news_info}")

            if st.button("Send Telegram Alert"):
                from sie.alerts import format_telegram_body, send_telegram_message
                tg_ok, msg = send_telegram_message(format_telegram_body(report), cfg)
                st.success(msg) if tg_ok else st.error(msg)

        time.sleep(refresh_interval)
        st.rerun()
else:
    report = analyze_watchlist(cfg, include_news=True, include_social=True)
    df = pd.DataFrame(report["rows"])
    st.dataframe(df.drop(columns=["headlines"], errors="ignore"), use_container_width=True)
