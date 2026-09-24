"""Load configuration from config.yaml with defaults."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

DEFAULT_TICKERS: dict[str, dict[str, str]] = {
    "NVDA": {
        "name": "NVIDIA",
        "color": "\ud83d\udfe2",
        "note": "Strongest winner - inference boom",
        "narrative_fit": "strong",
    },
    "TSM": {
        "name": "TSMC",
        "color": "\ud83d\udfe2",
        "note": "Quiet chip enabler",
        "narrative_fit": "strong",
    },
    "CBRS": {
        "name": "Cerebras",
        "color": "\ud83d\udfe2",
        "note": "Pure specialized inference play (volatile)",
        "narrative_fit": "strong",
    },
    "CRDO": {
        "name": "Credo",
        "color": "\ud83d\udfe1",
        "note": "Viral AI connectivity play",
        "narrative_fit": "monitor",
    },
    "MU": {
        "name": "Micron",
        "color": "\ud83d\udfe1",
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
    "congressional": {
        "enabled": True,
        "lookback_days": 90,
        "min_trades": 2,
        "buy_boost_min": 2,
        "sell_penalty_min": 2,
        "min_trade_value": 15000,
    },
    "portfolio": {
        "enabled": True,
        "lookback_period": "1y",
        "min_periods": 30,
        "risk_free_rate": 0.04,
    },
    "dark_pool": {
        "enabled": True,
        "elevated_ratio": 1.8,
        "boost_ratio": 2.2,
        "penalty_ratio": 2.0,
        "min_confidence": 0.45,
    },
    "realtime": {
        "enabled": True,
    },
    "options_iv": {
        "enabled": True,
        "elevated_skew": 0.12,
        "boost_skew": 0.22,
        "penalty_skew": 0.28,
        "min_confidence": 0.40,
        "term_slope_threshold": 0.05,
    },
    "gex": {
        "enabled": True,
        "boost_abs_threshold": 0.55,
        "penalty_abs_threshold": 0.60,
        "pin_proximity_pct": 0.012,
        "min_confidence": 0.40,
        "prefer_live": True,
    },
    "social_intent": {
        "enabled": True,
        "high_intent_share": 0.42,
        "spam_share_penalty": 0.28,
        "high_intent_velocity_hot": 1.4,
        "min_confidence": 0.40,
    },
    "credit_spread": {
        "enabled": True,
        "tighten_bp": -8.0,
        "widen_bp": 12.0,
        "stress_spread_bp": 180.0,
        "narrative_hot": 1.4,
        "min_confidence": 0.40,
    },
    "earnings_call": {
        "enabled": True,
        "sentiment_hot": 0.28,
        "sentiment_cold": -0.18,
        "drift_up": 0.12,
        "drift_down": -0.12,
        "hedge_warn": 0.22,
        "narrative_hot": 1.4,
        "min_confidence": 0.40,
    },
    "news_authority": {
        "enabled": True,
        "high_auth_threshold": 0.68,
        "low_auth_threshold": 0.38,
        "unverified_warn": 0.45,
        "narrative_hot": 1.5,
        "min_confidence": 0.40,
    },
    "whisper_number": {
        "enabled": True,
        "beat_prob_hot": 0.68,
        "beat_prob_cold": 0.38,
        "cluster_hot": 0.55,
        "cluster_cold": -0.35,
        "narrative_hot": 1.4,
        "event_window_days": 21,
        "min_confidence": 0.40,
    },
    "etf_flow": {
        "enabled": True,
        "create_hot": 0.45,
        "redeem_hot": -0.40,
        "premium_hot_bps": 18.0,
        "discount_hot_bps": -22.0,
        "streak_hot": 3,
        "narrative_hot": 1.4,
        "min_confidence": 0.40,
    },
}


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    cfg = {**DEFAULT_CONFIG, "tickers": dict(DEFAULT_TICKERS)}
    config_path = Path(path or Path(__file__).resolve().parent.parent / "config.yaml")
    if not config_path.is_file():
        return cfg

    with config_path.open(encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    if not isinstance(raw, dict):
        return cfg

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
                    t, {"name": t, "color": "\ud83d\udfe1", "note": "", "narrative_fit": "monitor"}
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
    if congressional := raw.get("congressional"):
        cfg.setdefault("congressional", {}).update(congressional)
    if portfolio := raw.get("portfolio"):
        cfg.setdefault("portfolio", {}).update(portfolio)
    if dark_pool := raw.get("dark_pool"):
        cfg.setdefault("dark_pool", {}).update(dark_pool)
    if realtime := raw.get("realtime"):
        cfg.setdefault("realtime", {}).update(realtime)
    if options_iv := raw.get("options_iv"):
        cfg.setdefault("options_iv", {}).update(options_iv)
    if gex := raw.get("gex"):
        cfg.setdefault("gex", {}).update(gex)
    if social_intent := raw.get("social_intent"):
        cfg.setdefault("social_intent", {}).update(social_intent)
    if credit_spread := raw.get("credit_spread"):
        cfg.setdefault("credit_spread", {}).update(credit_spread)
    if earnings_call := raw.get("earnings_call"):
        cfg.setdefault("earnings_call", {}).update(earnings_call)
    if news_authority := raw.get("news_authority"):
        cfg.setdefault("news_authority", {}).update(news_authority)
    if whisper_number := raw.get("whisper_number"):
        cfg.setdefault("whisper_number", {}).update(whisper_number)
    if etf_flow := raw.get("etf_flow"):
        cfg.setdefault("etf_flow", {}).update(etf_flow)
    if backtest := raw.get("backtest"):
        cfg.setdefault("backtest", {}).update(backtest)
    if telegram := raw.get("telegram"):
        cfg.setdefault("telegram", {}).update(telegram)
    if sentiment := raw.get("sentiment"):
        cfg.setdefault("sentiment", {}).update(sentiment)
    return cfg
