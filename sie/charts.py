"""Plotly chart builders for the dashboard."""

from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf

SIGNAL_COLORS = {
    "strong_buy": "#00E676",
    "buy": "#18FFFF",
    "hold": "#FFD740",
    "caution": "#FF5252",
}

SIGNAL_SCORE = {"strong_buy": 4, "buy": 3, "hold": 2, "caution": 1}


def fetch_price_history(ticker: str, period: str = "1y") -> pd.DataFrame:
    hist = yf.Ticker(ticker).history(period=period, auto_adjust=True)
    if hist.empty:
        return pd.DataFrame()
    df = hist.reset_index()
    df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(None)
    close = df["Close"]
    df["MA50"] = close.rolling(50).mean()
    df["MA200"] = close.rolling(200).mean()
    return df


def signal_bar_chart(rows: list[dict[str, Any]]) -> go.Figure:
    labels = [r["ticker"] for r in rows]
    scores = [SIGNAL_SCORE.get(r.get("signal", "hold"), 2) for r in rows]
    colors = [SIGNAL_COLORS.get(r.get("signal", "hold"), "#FFD740") for r in rows]
    fig = go.Figure(
        go.Bar(
            x=labels,
            y=scores,
            marker=dict(color=colors, line=dict(width=0)),
            text=[r.get("signal", "").replace("_", " ").upper() for r in rows],
            textposition="outside",
        )
    )
    fig.update_layout(
        title="Signal strength by ticker",
        yaxis=dict(title="Score", range=[0, 4.5], tickvals=[1, 2, 3, 4], ticktext=["Caution", "Hold", "Buy", "Strong"]),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320,
        margin=dict(t=50, b=40),
    )
    return fig


def rsi_gauge(rsi: float | None, ticker: str) -> go.Figure:
    value = rsi if rsi is not None else 50
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": f"RSI — {ticker}", "font": {"size": 18}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#7C4DFF"},
                "steps": [
                    {"range": [0, 30], "color": "#1B5E20"},
                    {"range": [30, 70], "color": "#263238"},
                    {"range": [70, 100], "color": "#B71C1C"},
                ],
                "threshold": {
                    "line": {"color": "#FFD740", "width": 3},
                    "thickness": 0.8,
                    "value": 70,
                },
            },
        )
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        height=260,
        margin=dict(t=40, b=20, l=30, r=30),
    )
    return fig


def drawdown_chart(rows: list[dict[str, Any]]) -> go.Figure:
    df = pd.DataFrame(
        [{"ticker": r["ticker"], "drawdown": r.get("drawdown_pct") or 0} for r in rows]
    )
    fig = px.bar(
        df,
        x="ticker",
        y="drawdown",
        color="drawdown",
        color_continuous_scale=["#00E676", "#FFD740", "#FF5252"],
        labels={"drawdown": "52w drawdown %"},
    )
    fig.update_layout(
        title="Distance from 52-week high",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        coloraxis_showscale=False,
    )
    return fig


def price_ma_chart(ticker: str) -> go.Figure:
    df = fetch_price_history(ticker)
    fig = go.Figure()
    if df.empty:
        fig.add_annotation(text="No price data", showarrow=False, font=dict(size=16))
        fig.update_layout(template="plotly_dark", height=360)
        return fig

    fig.add_trace(
        go.Scatter(x=df["Date"], y=df["Close"], name="Price", line=dict(color="#18FFFF", width=2))
    )
    fig.add_trace(
        go.Scatter(x=df["Date"], y=df["MA50"], name="MA50", line=dict(color="#FFD740", width=1.5, dash="dot"))
    )
    fig.add_trace(
        go.Scatter(x=df["Date"], y=df["MA200"], name="MA200", line=dict(color="#FF5252", width=1.5, dash="dash"))
    )
    fig.update_layout(
        title=f"{ticker} — price & moving averages",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=360,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    return fig


def signal_donut(rows: list[dict[str, Any]]) -> go.Figure:
    counts: dict[str, int] = {}
    for r in rows:
        sig = r.get("signal", "hold")
        counts[sig] = counts.get(sig, 0) + 1
    fig = go.Figure(
        go.Pie(
            labels=[k.replace("_", " ").title() for k in counts],
            values=list(counts.values()),
            hole=0.55,
            marker=dict(colors=[SIGNAL_COLORS.get(k, "#888") for k in counts]),
            textinfo="label+percent",
        )
    )
    fig.update_layout(
        title="Portfolio signal mix",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        height=300,
        showlegend=False,
    )
    return fig