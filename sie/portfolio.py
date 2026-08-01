"""Portfolio Correlation Heatmap & Risk Overlay.

Computes pairwise returns correlations for the watchlist and portfolio-level
metrics (equal-weight basket volatility, Sharpe, max drawdown). Used by the
backtest engine and Streamlit dashboard for interactive Plotly heatmap + risk
summary.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import yfinance as yf

from sie.config import load_config


def _safe_download(tickers: List[str], period: str = "1y") -> pd.DataFrame:
    """Download adjusted close prices for multiple tickers. Returns wide DF."""
    if not tickers:
        return pd.DataFrame()
    try:
        data = yf.download(
            tickers,
            period=period,
            auto_adjust=True,
            progress=False,
            threads=True,
        )
        if data.empty:
            return pd.DataFrame()
        # yfinance multi-ticker returns MultiIndex columns
        if isinstance(data.columns, pd.MultiIndex):
            closes = data["Close"]
        else:
            closes = data[["Close"]].rename(columns={"Close": tickers[0]})
        closes = closes.dropna(how="all")
        return closes
    except Exception:
        return pd.DataFrame()


def compute_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Daily percentage returns."""
    if prices.empty or prices.shape[1] == 0:
        return pd.DataFrame()
    return prices.pct_change().dropna(how="all")


def correlation_matrix(
    tickers: List[str],
    period: str = "1y",
    min_periods: int = 30,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns (corr_df, returns_df).
    corr_df is the pairwise Pearson correlation of daily returns.
    """
    prices = _safe_download(tickers, period=period)
    if prices.empty:
        return pd.DataFrame(), pd.DataFrame()
    rets = compute_returns(prices)
    if rets.empty or rets.shape[0] < min_periods:
        return pd.DataFrame(), rets
    # Align columns to requested tickers order when possible
    available = [t for t in tickers if t in rets.columns]
    rets = rets[available]
    corr = rets.corr(min_periods=min_periods)
    return corr, rets


def portfolio_risk_metrics(
    returns: pd.DataFrame,
    risk_free_rate: float = 0.04,
    annualization: int = 252,
) -> Dict[str, Any]:
    """
    Equal-weight portfolio metrics from a returns DataFrame (columns = tickers).
    """
    if returns.empty or returns.shape[1] == 0:
        return {
            "n_assets": 0,
            "vol_ann": None,
            "sharpe": None,
            "max_drawdown": None,
            "mean_corr": None,
            "period_days": 0,
            "error": "No returns data",
        }

    n = returns.shape[1]
    # Equal weight
    port_rets = returns.mean(axis=1)
    mean_daily = port_rets.mean()
    std_daily = port_rets.std()
    vol_ann = float(std_daily * np.sqrt(annualization)) if std_daily and not np.isnan(std_daily) else None
    excess = mean_daily - (risk_free_rate / annualization)
    sharpe = float(excess / std_daily * np.sqrt(annualization)) if std_daily and std_daily > 1e-12 else None

    # Max drawdown on cumulative equity curve
    equity = (1 + port_rets.fillna(0)).cumprod()
    peak = equity.cummax()
    dd = (equity - peak) / peak
    max_dd = float(dd.min()) if not dd.empty else None

    # Mean pairwise correlation (upper triangle)
    corr = returns.corr()
    if corr.shape[0] > 1:
        mask = np.triu(np.ones(corr.shape), k=1).astype(bool)
        mean_corr = float(corr.where(mask).stack().mean())
    else:
        mean_corr = 1.0

    return {
        "n_assets": n,
        "vol_ann": round(vol_ann, 4) if vol_ann is not None else None,
        "sharpe": round(sharpe, 3) if sharpe is not None else None,
        "max_drawdown": round(max_dd * 100, 2) if max_dd is not None else None,  # percent
        "mean_corr": round(mean_corr, 3) if mean_corr is not None else None,
        "period_days": int(returns.shape[0]),
        "error": None,
    }


def compute_portfolio_overlay(
    cfg: dict | None = None,
    period: str | None = None,
) -> Dict[str, Any]:
    """
    High-level entry point used by analyzer / dashboard / CLI.
    Returns correlation matrix (as dict), risk metrics, and metadata.
    """
    cfg = cfg or load_config()
    port_cfg = cfg.get("portfolio", {})
    if not port_cfg.get("enabled", True):
        return {
            "enabled": False,
            "correlation": {},
            "metrics": {},
            "tickers": [],
            "period": period or port_cfg.get("lookback_period", "1y"),
            "source": "disabled",
        }

    tickers = list(cfg.get("tickers", {}).keys())
    if not tickers:
        tickers = ["AAPL", "MSFT", "NVDA"]
    lookback = period or port_cfg.get("lookback_period", "1y")
    min_periods = int(port_cfg.get("min_periods", 30))
    rf = float(port_cfg.get("risk_free_rate", 0.04))

    corr_df, rets = correlation_matrix(tickers, period=lookback, min_periods=min_periods)
    metrics = portfolio_risk_metrics(rets, risk_free_rate=rf)

    # Convert corr to nested dict for JSON / Streamlit friendliness
    corr_dict: Dict[str, Dict[str, float]] = {}
    if not corr_df.empty:
        for i in corr_df.index:
            corr_dict[str(i)] = {
                str(j): round(float(corr_df.loc[i, j]), 3)
                if pd.notna(corr_df.loc[i, j])
                else None
                for j in corr_df.columns
            }

    return {
        "enabled": True,
        "correlation": corr_dict,
        "metrics": metrics,
        "tickers": list(corr_df.columns) if not corr_df.empty else tickers,
        "period": lookback,
        "source": "yfinance",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


def correlation_heatmap_figure(corr_dict: Dict[str, Dict[str, float]]) -> Any:
    """Build a Plotly heatmap figure from the correlation nested dict."""
    import plotly.graph_objects as go

    if not corr_dict:
        fig = go.Figure()
        fig.add_annotation(text="No correlation data", showarrow=False)
        fig.update_layout(template="plotly_dark", height=400)
        return fig

    tickers = list(corr_dict.keys())
    z = []
    for t in tickers:
        row = [corr_dict[t].get(u) for u in tickers]
        z.append(row)

    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=tickers,
            y=tickers,
            colorscale="RdBu_r",
            zmid=0,
            zmin=-1,
            zmax=1,
            text=[[f"{v:.2f}" if v is not None else "" for v in row] for row in z],
            texttemplate="%{text}",
            textfont={"size": 11},
            colorbar=dict(title="ρ"),
            hoverongaps=False,
        )
    )
    fig.update_layout(
        title="Watchlist Return Correlation Heatmap",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=480,
        margin=dict(t=50, b=40, l=60, r=40),
        xaxis=dict(side="bottom"),
        yaxis=dict(autorange="reversed"),
    )
    return fig
