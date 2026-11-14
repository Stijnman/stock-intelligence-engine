"""Stock Intelligence Engine — unified Streamlit dashboard."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from sie.analyzer import run_report
from sie.config import load_config

__version__ = "2.76.0"

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

st.divider()
st.header("Quantitative Portfolio Lab")
st.caption("Historical analytics and scenario tools. Indicative data only; no trading or portfolio write access.")
quant_tickers = st.multiselect(
    "Assets for quantitative analysis",
    options=configured_tickers or ["ASML", "MSFT", "NVDA", "VWCE", "SPY"],
    default=(selected or configured_tickers or ["ASML", "MSFT", "NVDA", "SPY"])[:5],
    key="quant_tickers",
)
backtest_col1, backtest_col2, backtest_col3 = st.columns(3)
with backtest_col1:
    quant_fee_bps = st.number_input("Backtest fee (bps / side)", min_value=0.0, value=5.0, step=1.0, key="quant_fee_bps")
with backtest_col2:
    quant_slippage_bps = st.number_input("Backtest slippage (bps / side)", min_value=0.0, value=5.0, step=1.0, key="quant_slippage_bps")
with backtest_col3:
    quant_rebalance_days = st.number_input("Rebalance interval (trading days)", min_value=1, max_value=252, value=21, step=1, key="quant_rebalance_days")
quant_run = st.button("Load price history and calculate portfolio analytics", key="quant_run")
if quant_run:
    if len(quant_tickers) < 2:
        st.error("Select at least two assets.")
    else:
        from sie.investment.providers import quote_and_history
        from sie.investment.advanced import (
            backtest_target_weights, correlation_matrix, monte_carlo_projection, optimize_portfolio,
            portfolio_risk,
        )
        with st.spinner("Loading historical price series..."):
            dated_histories = {}
            provider_errors = {}
            for symbol in quant_tickers:
                try:
                    payload = quote_and_history(symbol, range_="5y")
                    dated = {row["date"]: row["close"] for row in payload.get("history", [])
                             if row.get("date") and row.get("close") is not None}
                    if len(dated) >= 4:
                        dated_histories[symbol] = dated
                    else:
                        provider_errors[symbol] = "Insufficient price history."
                except Exception as exc:
                    provider_errors[symbol] = str(exc)
            common_dates = sorted(set.intersection(*(set(v) for v in dated_histories.values()))) if dated_histories else []
            histories = {symbol: [dated[day] for day in common_dates] for symbol, dated in dated_histories.items()}
            if len(common_dates) < 4 and histories:
                provider_errors["alignment"] = "Fewer than four common trading dates across selected assets."
                histories = {}
            quant_result = {"histories": histories, "common_dates": len(common_dates), "errors": provider_errors}
            if len(histories) >= 2:
                quant_result["risk"] = portfolio_risk(histories)
                quant_result["correlation"] = correlation_matrix(histories)
                quant_result["optimizer"] = optimize_portfolio(histories, objective="max_sharpe")
                quant_result["backtest"] = backtest_target_weights(
                    histories,
                    {symbol: 1.0 for symbol in histories},
                    fee_bps=quant_fee_bps,
                    slippage_bps=quant_slippage_bps,
                    rebalance_every=int(quant_rebalance_days),
                )
                risk = quant_result["risk"]
                if risk.get("status") == "ok":
                    quant_result["monte_carlo"] = monte_carlo_projection(
                        10000.0,
                        (risk.get("annual_return_pct") or 0.0) / 100,
                        (risk.get("annual_volatility_pct") or 0.0) / 100,
                        years=10,
                        simulations=3000,
                    )
            st.session_state["sie_quant_result"] = quant_result

quant_result = st.session_state.get("sie_quant_result")
if quant_result:
    if quant_result.get("errors"):
        st.warning("Some providers/assets were unavailable: " + "; ".join(
            f"{ticker}: {reason}" for ticker, reason in quant_result["errors"].items()
        ))
    if quant_result.get("risk", {}).get("status") == "ok":
        risk = quant_result["risk"]
        metrics = st.columns(4)
        metrics[0].metric("Annualized return", f"{risk['annual_return_pct']:.2f}%")
        metrics[1].metric("Annualized volatility", f"{risk['annual_volatility_pct']:.2f}%")
        metrics[2].metric("Sharpe ratio", f"{risk['sharpe']:.2f}" if risk.get("sharpe") is not None else "N/A")
        metrics[3].metric("Maximum drawdown", f"{risk['max_drawdown_pct']:.2f}%")
        risk_tabs = st.tabs(["Risk", "Optimizer", "Correlation", "Monte Carlo", "Backtest"])
        with risk_tabs[0]:
            st.json(risk)
        with risk_tabs[1]:
            optimizer = quant_result.get("optimizer", {})
            if optimizer.get("status") == "ok":
                st.dataframe(pd.DataFrame(
                    [{"Asset": ticker, "Suggested historical weight %": weight * 100}
                     for ticker, weight in optimizer["weights"].items()]
                ), use_container_width=True, hide_index=True)
                st.caption("Long-only historical optimizer; weights are mathematical scenarios, not investment instructions.")
            else:
                st.warning(optimizer.get("reason", "Optimizer unavailable."))
        with risk_tabs[2]:
            correlation = quant_result.get("correlation", {})
            if correlation.get("status") == "ok":
                st.dataframe(pd.DataFrame(correlation["matrix"]).T, use_container_width=True)
                st.dataframe(pd.DataFrame(correlation["highest_correlations"]), use_container_width=True, hide_index=True)
        with risk_tabs[3]:
            simulation = quant_result.get("monte_carlo", {})
            if simulation.get("status") == "ok":
                st.metric("Median 10-year scenario", f"€{simulation['median']:,.0f}")
                st.write({
                    "5th percentile": simulation["p05"],
                    "25th percentile": simulation["p25"],
                    "75th percentile": simulation["p75"],
                    "95th percentile": simulation["p95"],
                    "Probability of ending below starting value": simulation["probability_loss_pct"],
                })
                st.caption(simulation["method"])
        with risk_tabs[4]:
            backtest = quant_result.get("backtest", {})
            if backtest.get("status") == "ok":
                backtest_metrics = st.columns(4)
                backtest_metrics[0].metric("Backtest return", f"{backtest['total_return_pct']:.2f}%")
                backtest_metrics[1].metric("Final value (currency units)", f"{backtest['final_value']:,.2f}")
                backtest_metrics[2].metric("Maximum drawdown", f"{backtest['max_drawdown_pct']:.2f}%")
                backtest_metrics[3].metric("Rebalance events", str(backtest["rebalance_events"]))
                st.json(backtest)
                st.caption(backtest["warning"])
            else:
                st.warning(backtest.get("reason", "Backtest unavailable."))
    elif quant_result.get("errors"):
        st.error("Quantitative analysis could not be completed for at least two selected assets.")

with st.expander("Belgian ETF tax engine — official rates and FSMA evidence", expanded=False):
    from sie.investment.belgian_tax import calculate_tob, calculate_net_dividend_yield
    from sie.investment.data.fsma_uci import fetch_fsma_uci_registry

    st.caption("TOB is determined by legal form, share-class type and FSMA/EEA registration. UCITS status alone does not determine TOB.")
    fsma_query = st.text_input("FSMA fund or compartment name / ISIN", key="be_fsma_query")
    if st.button("Check official FSMA register", key="be_fsma_check"):
        try:
            st.session_state["be_fsma_result"] = fetch_fsma_uci_registry(
                isin=fsma_query.strip() if len(fsma_query.strip()) == 12 else None,
                name=fsma_query.strip() if len(fsma_query.strip()) != 12 else None,
            )
            st.session_state["be_fsma_error"] = None
        except Exception as exc:
            st.session_state["be_fsma_error"] = str(exc)
    if st.session_state.get("be_fsma_error"):
        st.error(st.session_state["be_fsma_error"])
    fsma_result = st.session_state.get("be_fsma_result")
    if fsma_result:
        st.write({"Status": fsma_result.get("status"), "As of": fsma_result.get("as_of"),
                  "Matches": len(fsma_result.get("matches", [])), "Source": fsma_result.get("source_url")})
        if fsma_result.get("matches"):
            st.dataframe(pd.DataFrame(fsma_result["matches"]), use_container_width=True, hide_index=True)

    tob_col, dividend_col = st.columns(2)
    with tob_col:
        st.markdown("**Transaction tax (TOB)**")
        trade_value = st.number_input("Trade amount (€)", min_value=0.0, value=5000.0, step=500.0, key="be_tob_amount")
        legal_form = st.selectbox("Legal form", ["sicav", "fcp"], key="be_tob_form")
        share_class = st.selectbox("Share class", ["distribution", "capitalisation"], key="be_tob_class")
        registration = st.selectbox("Registration evidence", ["fsma", "eea", "unregistered", "unknown"], key="be_tob_registration")
        trade_side = st.selectbox("Transaction", ["buy", "sell"], key="be_tob_side")
        if st.button("Calculate TOB", key="be_tob_calc"):
            st.session_state["be_tob_result"] = calculate_tob(
                trade_value, legal_form=legal_form, distribution=share_class,
                registration=registration, side=trade_side,
            )
        if st.session_state.get("be_tob_result"):
            st.json(st.session_state["be_tob_result"])
    with dividend_col:
        st.markdown("**Net cash dividend yield**")
        dividend_form = st.selectbox("Distribution fund legal form", ["sicav", "fcp"], key="be_div_form")
        gross_per_share = st.number_input("Annual distribution per share (€)", min_value=0.0, value=2.0, step=0.1, key="be_div_per_share")
        market_price = st.number_input("ETF market price (€)", min_value=0.01, value=100.0, step=1.0, key="be_div_price")
        share_count = st.number_input("Number of shares", min_value=0.0, value=1.0, step=1.0, key="be_div_shares")
        breakdown = st.checkbox("FCP: valid income breakdown available", key="be_fcp_breakdown")
        foreign_rate = st.number_input("Investor-level foreign withholding (%)", min_value=0.0, max_value=100.0, value=0.0, step=1.0, key="be_foreign_wht")
        if st.button("Calculate net dividend yield", key="be_div_calc"):
            st.session_state["be_div_result"] = calculate_net_dividend_yield(
                annual_distribution_per_share=gross_per_share, market_price=market_price,
                legal_form=dividend_form, fcp_breakdown_available=breakdown,
                shares=share_count, investor_level_foreign_withholding_pct=foreign_rate,
            )
        if st.session_state.get("be_div_result"):
            st.json(st.session_state["be_div_result"])
    st.caption("Rates: Wikifin/FSMA and FPS Finance. Fund TER must be sourced from the latest issuer KID/factsheet. Foreign tax inside the fund is not deducted a second time here. The new financial-asset capital-gains tax, broker commissions and full FCP look-through tax are not calculated in this panel.")

with st.expander("Broker transaction cost estimate (excluding tax)"):
    from sie.investment.advanced import broker_cost_estimate
    broker_value = st.number_input("Trade amount (€)", min_value=0.0, value=5000.0, step=500.0, key="broker_value")
    commission = st.number_input("Commission (€)", min_value=0.0, value=2.0, step=0.5, key="broker_commission")
    fx_spread = st.number_input("FX spread (%)", min_value=0.0, value=0.0, step=0.05, key="broker_fx_spread")
    other_cost = st.number_input("Other costs (€)", min_value=0.0, value=0.0, step=0.5, key="broker_other_cost")
    if st.button("Calculate broker costs", key="broker_calc"):
        st.json(broker_cost_estimate(
            broker_value, commission_eur=commission,
            fx_spread_pct=fx_spread, other_fees_eur=other_cost,
        ))


with st.expander("CFTC Commitments of Traders — weekly positioning"):
    st.caption("Official CFTC futures-only positioning. Weekly Tuesday snapshot, normally published Friday; not live order flow.")
    cot_col1, cot_col2 = st.columns([2, 1])
    with cot_col1:
        cot_commodity = st.text_input("Commodity filter", value="GOLD", key="cot_commodity")
    with cot_col2:
        cot_limit = st.number_input("Rows", min_value=10, max_value=2000, value=200, step=50, key="cot_limit")
    if st.button("Fetch CFTC positioning", key="fetch_cftc"):
        try:
            from sie.investment.data.cftc import fetch_legacy_futures_only
            cot_rows = fetch_legacy_futures_only(
                commodity=cot_commodity.strip() or None, limit=int(cot_limit)
            )
            st.session_state["sie_cot_rows"] = cot_rows
            st.session_state["sie_cot_error"] = None
        except Exception as exc:
            st.session_state["sie_cot_error"] = str(exc)
    if st.session_state.get("sie_cot_error"):
        st.error(st.session_state["sie_cot_error"])
    cot_rows = st.session_state.get("sie_cot_rows", [])
    if cot_rows:
        cot_markets = sorted({row.get("market") for row in cot_rows if row.get("market")})
        cot_market = st.selectbox("Contract / market", cot_markets, key="cot_market")
        cot_history = sorted(
            [row for row in cot_rows if row.get("market") == cot_market],
            key=lambda row: row.get("report_date", "")
        )
        cot_latest = cot_history[-1]
        cot_metrics = st.columns(3)
        cot_metrics[0].metric("Latest report", cot_latest.get("report_date", "N/A"))
        cot_metrics[1].metric(
            "Non-commercial net",
            f"{cot_latest['noncommercial_net']:,.0f}" if cot_latest.get("noncommercial_net") is not None else "N/A"
        )
        cot_metrics[2].metric(
            "Net / open interest",
            f"{cot_latest['noncommercial_net_pct_open_interest']:.1f}%"
            if cot_latest.get("noncommercial_net_pct_open_interest") is not None else "N/A"
        )
        cot_chart = pd.DataFrame([
            {"Report date": row.get("report_date"), "Non-commercial net": row.get("noncommercial_net")}
            for row in cot_history if row.get("noncommercial_net") is not None
        ])
        if not cot_chart.empty:
            st.line_chart(cot_chart.set_index("Report date"))
        st.dataframe(pd.DataFrame(cot_history).tail(20), use_container_width=True, hide_index=True)
        st.caption("Source: CFTC Public Reporting Environment. Positioning can be stale, crowded or hedging-related; it is not a directional trading signal by itself.")
