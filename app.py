import streamlit as st
import pandas as pd
import time
from sie.analyzer import analyze_watchlist, run_report
from sie.config import load_config
from sie.backtest import backtest_watchlist

st.set_page_config(page_title="Stock Intelligence Engine", layout="wide")
st.title("Stock Intelligence Engine v2.10.0 — Institutional 13F + Prediction Markets + Insider Clusters + Narrative Velocity")

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
    st.info(
        f"🔄 Auto-refreshing every {refresh_interval} seconds. Live prices, signals, "
        "X narratives, velocity forecasts, **Insider Form 4 clusters**, **Polymarket odds** & **Institutional 13F changes**."
    )
    placeholder = st.empty()
    while True:
        with placeholder.container():
            report = analyze_watchlist(
                cfg, include_news=True, include_social=True,
                include_insider=True, include_pm=True, include_institutional=True
            )
            df = pd.DataFrame(report["rows"])
            display_cols = [c for c in df.columns if c not in ("headlines", "transactions", "odds", "inst_top_holders")]
            st.dataframe(df[display_cols], use_container_width=True)

            st.subheader("Signals · Buzz · X Narratives · Forecasts · Insider Clusters · Prediction Markets · 13F Ownership")
            for row in report["rows"]:
                narr = (
                    f"Narr: {row.get('dominant_narrative','N/A')} "
                    f"{'🚨CRISIS' if row.get('crisis_flag') else ''} "
                    f"Vel:{row.get('sentiment_velocity',0):.1f}"
                )
                forecast = (
                    f" | 🔮 Forecast→{row.get('predicted_phase','N/A')} "
                    f"(conf {row.get('forecast_confidence',0):.0%})"
                )
                insider = ""
                if row.get("insider_cluster_size", 0) > 0 or row.get("insider_side") not in (None, "none"):
                    side_emoji = "🟢" if row.get("insider_side") == "buy" else "🔴" if row.get("insider_side") == "sell" else "⚪"
                    insider = (
                        f" | {side_emoji} Insider {row.get('insider_side','—').upper()} "
                        f"cluster={row.get('insider_cluster_size',0)} "
                        f"net={row.get('insider_net_shares',0):,}"
                    )
                pm = ""
                if row.get("pm_best_probability") is not None:
                    pm = (
                        f" | 🎯 PM {row.get('pm_best_probability',0):.0%} "
                        f"(boost={row.get('pm_boost',0)}, src={row.get('pm_source','?')})"
                    )
                inst = ""
                if row.get("inst_side") not in (None, "none") or row.get("inst_holder_count", 0) > 0:
                    inst_emoji = "🏦🟢" if row.get("inst_side") == "increase" else "🏦🔴" if row.get("inst_side") == "decrease" else "🏦"
                    inst = (
                        f" | {inst_emoji} 13F {row.get('inst_side','—').upper()} "
                        f"Δ={row.get('inst_pct_change',0):+.1f}% "
                        f"holders={row.get('inst_holder_count',0)}"
                    )
                news_info = ""
                if row.get("headlines"):
                    news_info = " | News sent: " + str([h.get("sentiment_label") for h in row["headlines"]])
                st.write(
                    f"{row.get('color','')} **{row['ticker']}**: {row.get('signal','')} | "
                    f"Buzz {row.get('buzz_score',0)} | {narr}{forecast}{insider}{pm}{inst}{news_info}"
                )
                if row.get("forecast_reason"):
                    st.caption(row["forecast_reason"])
                if row.get("insider_reason"):
                    st.caption(f"Insider: {row['insider_reason']} (src={row.get('insider_source','?')})")
                if row.get("pm_reason"):
                    st.caption(f"Prediction Market: {row['pm_reason']}")
                if row.get("inst_reason"):
                    st.caption(f"Institutional 13F: {row['inst_reason']} (src={row.get('inst_source','?')})")

            if st.button("Send Telegram Alert"):
                from sie.alerts import format_telegram_body, send_telegram_message
                tg_ok, msg = send_telegram_message(format_telegram_body(report), cfg)
                st.success(msg) if tg_ok else st.error(msg)

        time.sleep(refresh_interval)
        st.rerun()
else:
    report = analyze_watchlist(
        cfg, include_news=True, include_social=True,
        include_insider=True, include_pm=True, include_institutional=True
    )
    df = pd.DataFrame(report["rows"])
    st.dataframe(df.drop(columns=["headlines", "inst_top_holders"], errors="ignore"), use_container_width=True)
