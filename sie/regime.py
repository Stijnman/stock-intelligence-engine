"""Market Regime Adaptive Overlay Weighting.

Detects current market regime (VIX terciles + SPY trend strength + realized vol)
and dynamically re-weights narrative, technical, flow and fundamental overlays.
Reduces narrative weight in high-vol regimes and increases flow/technical weight
when trends are strong. Surfaces regime label, weights and soft adjustment reason.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional
import math

import pandas as pd
import yfinance as yf

from sie.config import load_config


def _safe_float(val: Any, default: float = 0.0) -> float:
    try:
        return float(val)
    except (TypeError, ValueError):
        return default


def detect_market_regime(cfg: dict | None = None) -> Dict[str, Any]:
    """
    Detect current market regime using VIX level, SPY trend and realized volatility.
    Returns regime label, adaptive weights for overlay groups, confidence and reason.
    Falls back to neutral weights on data failure.
    """
    cfg = cfg or load_config()
    regime_cfg = cfg.get("regime", {})
    if not regime_cfg.get("enabled", True):
        return {
            "regime": "disabled",
            "vix": None,
            "spy_trend": None,
            "realized_vol": None,
            "weights": {
                "narrative": 1.0,
                "technical": 1.0,
                "flow": 1.0,
                "fundamental": 1.0,
            },
            "signal_bias": 0,
            "confidence": 0.0,
            "reason": "Market regime module disabled",
            "source": "disabled",
        }

    # Defaults
    weights = {
        "narrative": 1.0,
        "technical": 1.0,
        "flow": 1.0,
        "fundamental": 1.0,
    }
    signal_bias = 0
    confidence = 0.35
    reason = "Neutral regime (fallback)"
    vix_val = None
    spy_trend = None
    realized_vol = None
    regime = "neutral"
    source = "yfinance"

    try:
        # VIX
        vix = yf.Ticker("^VIX")
        vix_hist = vix.history(period="5d")
        if not vix_hist.empty:
            vix_val = float(vix_hist["Close"].iloc[-1])

        # SPY for trend + realized vol
        spy = yf.Ticker("SPY")
        spy_hist = spy.history(period="60d")
        if len(spy_hist) >= 20:
            closes = spy_hist["Close"]
            # 20-day realized vol (annualized)
            rets = closes.pct_change().dropna()
            realized_vol = float(rets.tail(20).std() * math.sqrt(252) * 100)  # %
            # Simple trend: MA20 vs MA50 proxy via last vs 20d avg
            ma20 = float(closes.tail(20).mean())
            last = float(closes.iloc[-1])
            spy_trend = (last - ma20) / ma20 * 100  # % above/below MA20

        # Classify regime
        if vix_val is not None:
            if vix_val >= 28:
                regime = "high_vol_stress"
                # High vol: cut narrative hard, boost technical + flow
                weights = {"narrative": 0.45, "technical": 1.35, "flow": 1.40, "fundamental": 1.10}
                signal_bias = -1  # slight caution bias
                confidence = 0.78
                reason = f"High-vol stress regime (VIX={vix_val:.1f}). Narrative weight cut; technical/flow elevated."
            elif vix_val >= 20:
                regime = "elevated_vol"
                weights = {"narrative": 0.70, "technical": 1.20, "flow": 1.25, "fundamental": 1.05}
                signal_bias = 0
                confidence = 0.68
                reason = f"Elevated volatility (VIX={vix_val:.1f}). Moderate narrative de-weight; flow/technical preference."
            elif vix_val <= 14 and spy_trend is not None and spy_trend > 1.5:
                regime = "low_vol_bull"
                weights = {"narrative": 1.25, "technical": 0.95, "flow": 0.90, "fundamental": 1.15}
                signal_bias = 1
                confidence = 0.75
                reason = f"Low-vol bull regime (VIX={vix_val:.1f}, SPY trend +{spy_trend:.1f}%). Narrative + fundamental boosted."
            elif vix_val <= 16:
                regime = "low_vol_calm"
                weights = {"narrative": 1.15, "technical": 1.00, "flow": 0.95, "fundamental": 1.10}
                signal_bias = 0
                confidence = 0.70
                reason = f"Low-vol calm (VIX={vix_val:.1f}). Slight narrative preference."
            else:
                regime = "balanced"
                weights = {"narrative": 1.0, "technical": 1.05, "flow": 1.05, "fundamental": 1.0}
                signal_bias = 0
                confidence = 0.60
                reason = f"Balanced regime (VIX={vix_val:.1f}). Near-equal weights."
        else:
            # Fallback classification from realized vol + trend only
            if realized_vol is not None and realized_vol > 22:
                regime = "high_realized_vol"
                weights = {"narrative": 0.55, "technical": 1.30, "flow": 1.35, "fundamental": 1.05}
                signal_bias = -1
                confidence = 0.55
                reason = f"High realized vol ({realized_vol:.1f}%). Technical/flow preference."
            elif spy_trend is not None and spy_trend > 2.0:
                regime = "trending_bull"
                weights = {"narrative": 1.10, "technical": 1.15, "flow": 1.00, "fundamental": 1.05}
                signal_bias = 1
                confidence = 0.55
                reason = f"Trending bull (SPY +{spy_trend:.1f}% vs MA20). Mild technical preference."
            else:
                regime = "neutral"
                confidence = 0.40
                reason = "Neutral regime (insufficient VIX data)."

    except Exception as e:
        source = f"error:{type(e).__name__}"
        regime = "neutral_fallback"
        confidence = 0.25
        reason = f"Regime detection failed ({type(e).__name__}); using neutral weights."

    return {
        "regime": regime,
        "vix": round(vix_val, 2) if vix_val is not None else None,
        "spy_trend": round(spy_trend, 2) if spy_trend is not None else None,
        "realized_vol": round(realized_vol, 2) if realized_vol is not None else None,
        "weights": weights,
        "signal_bias": signal_bias,
        "confidence": round(confidence, 2),
        "reason": reason,
        "source": source,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def integrate_regime_to_row(row: dict[str, Any], cfg: dict | None = None) -> dict[str, Any]:
    """
    Attach market regime context and adaptive weights to a signal row.
    Applies soft signal bias only when confidence is high and current signal
    is borderline; always surfaces the regime reason for transparency.
    """
    cfg = cfg or load_config()
    regime_data = detect_market_regime(cfg)

    row["market_regime"] = regime_data["regime"]
    row["regime_vix"] = regime_data.get("vix")
    row["regime_spy_trend"] = regime_data.get("spy_trend")
    row["regime_realized_vol"] = regime_data.get("realized_vol")
    row["regime_weights"] = regime_data["weights"]
    row["regime_confidence"] = regime_data["confidence"]
    row["regime_reason"] = regime_data["reason"]
    row["regime_source"] = regime_data["source"]

    # Soft bias only on high confidence
    bias = regime_data.get("signal_bias", 0)
    conf = regime_data.get("confidence", 0.0)
    if conf >= 0.65 and bias != 0:
        current = row.get("signal", "hold")
        if bias > 0 and current in ("hold", "buy"):
            if current == "hold":
                row["signal"] = "buy"
            elif current == "buy":
                row["signal"] = "strong_buy"
            row["signal_reason"] = (row.get("signal_reason") or "") + f" | 📈 Regime bias ({regime_data['regime']})"
        elif bias < 0 and current in ("strong_buy", "buy"):
            if current == "strong_buy":
                row["signal"] = "buy"
            elif current == "buy":
                row["signal"] = "hold"
            row["signal_reason"] = (row.get("signal_reason") or "") + f" | 📉 Regime caution ({regime_data['regime']})"
        else:
            row["signal_reason"] = (row.get("signal_reason") or "") + f" | Regime: {regime_data['regime']}"
    else:
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | Regime: {regime_data['regime']}"

    return row
