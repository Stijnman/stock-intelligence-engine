"""Load configuration from config.yaml with defaults."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

DEFAULT_TICKERS: dict[str, dict[str, str]] = {
    "NVDA": {
        "name": "NVIDIA",
        "color": "🟢",
        "note": "Strongest winner - inference boom",
        "narrative_fit": "strong",
    },
    "TSM": {
        "name": "TSMC",
        "color": "🟢",
        "note": "Quiet chip enabler",
        "narrative_fit": "strong",
    },
    "CBRS": {
        "name": "Cerebras",
        "color": "🟢",
        "note": "Pure specialized inference play (volatile)",
        "narrative_fit": "strong",
    },
    "CRDO": {
        "name": "Credo",
        "color": "🟡",
        "note": "Viral AI connectivity play",
        "narrative_fit": "monitor",
    },
    "MU": {
        "name": "Micron",
        "color": "🟡",
        "note": "HBM memory - inference critical",
        "narrative_fit": "monitor",
    },
}

DEFAULT_CONFIG: dict[str, Any] = {
    "narrative": {"theme": "AI Inference Boom"},
    "technical": {
        "rsi_period": 14,
        "rsi_overbought": 70,
        "rsi_oversold": 30,
        "ma_fast": 50,
        "ma_slow": 200,
    },
    "tickers": DEFAULT_TICKERS,
    "export": {"directory": "exports"},
    "alerts": {"email": False},
    "twitter": {
        "enabled": True,
        "bearer_token": "",
        "search_limit": 50,
        "lookback_hours": 24,
    },
    "dashboard": {
        "enabled": True,
        "port": 8501,
        "refresh_interval": 60,
    },
    "forecast": {
        "enabled": True,
        "smoothing_alpha": 0.35,
        "horizon_days": 2,
    },
    "insider": {
        "enabled": True,
        "lookback_days": 14,
        "min_cluster_size": 2,
        "buy_boost_min": 2,
        "sell_penalty_min": 2,
    },
    "prediction_markets": {
        "enabled": True,
        "min_volume": 1000,
        "boost_prob_threshold": 0.65,
        "penalty_prob_threshold": 0.35,
        "divergence_boost": 1,
    },
    "institutional": {
        "enabled": True,
        "min_holders": 3,
        "significant_pct_change": 0.5,
        "boost_pct_threshold": 1.0,
        "penalty_pct_threshold": -1.0,
    },
    "portfolio": {
        "enabled": True,
        "lookback_period": "1y",
        "min_periods": 30,
        "risk_free_rate": 0.04,
    },
}


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    cfg = {**DEFAULT_CONFIG, "tickers": dict(DEFAULT_TICKERS)}
    config_path = Path(path or Path(__file__).resolve().parent.parent / "config.yaml")
    if not config_path.is_file():
        return cfg

    with config_path.open(encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    if theme := raw.get("narrative", {}).get("theme"):
        cfg["narrative"]["theme"] = theme
    if tech := raw.get("technical"):
        cfg["technical"].update(tech)
    if tickers := raw.get("tickers"):
        if isinstance(tickers, dict):
            cfg["tickers"] = tickers
        elif isinstance(tickers, list):
            cfg["tickers"] = {
                t: DEFAULT_TICKERS.get(
                    t, {"name": t, "color": "🟡", "note": "", "narrative_fit": "monitor"}
                )
                for t in tickers
            }
    if alerts := raw.get("alerts"):
        cfg["alerts"].update(alerts)
    if twitter := raw.get("twitter"):
        cfg.setdefault("twitter", {}).update(twitter)
    if export := raw.get("export"):
        cfg["export"].update(export)
    if dashboard := raw.get("dashboard"):
        cfg.setdefault("dashboard", {}).update(dashboard)
    if forecast := raw.get("forecast"):
        cfg.setdefault("forecast", {}).update(forecast)
    if insider := raw.get("insider"):
        cfg.setdefault("insider", {}).update(insider)
    if prediction_markets := raw.get("prediction_markets"):
        cfg.setdefault("prediction_markets", {}).update(prediction_markets)
    if institutional := raw.get("institutional"):
        cfg.setdefault("institutional", {}).update(institutional)
    if portfolio := raw.get("portfolio"):
        cfg.setdefault("portfolio", {}).update(portfolio)
    if backtest := raw.get("backtest"):
        cfg.setdefault("backtest", {}).update(backtest)
    if telegram := raw.get("telegram"):
        cfg.setdefault("telegram", {}).update(telegram)
    if sentiment := raw.get("sentiment"):
        cfg.setdefault("sentiment", {}).update(sentiment)
    return cfg
