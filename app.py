import streamlit as st
import pandas as pd
import time
from sie.analyzer import analyze_watchlist
from sie.config import load_config

st.set_page_config(page_title="Stock Intelligence Engine", layout="wide")
st.title("Stock Intelligence Engine v2.5.0 - Real-time Dashboard")

cfg = load_config()
dashboard_cfg = cfg.get("dashboard", {})
refresh_interval = dashboard_cfg.get("refresh_interval", 60)

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
    # Fallback static
    report = analyze_watchlist(cfg, include_news=True, include_social=True)
    df = pd.DataFrame(report["rows"])
    st.dataframe(df.drop(columns=["headlines"], errors="ignore"), use_container_width=True)
    # ... similar display
