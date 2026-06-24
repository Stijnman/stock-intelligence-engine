"""Technical indicators from price history."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd
import yfinance as yf


@dataclass
class TechnicalSnapshot:
    price: float | None
    ma_fast: float | None
    ma_slow: float | None
    rsi: float | None
    high_52w: float | None
    low_52w: float | None
    drawdown_pct: float | None
    signal: str
    signal_reason: str
    error: str | None = None


def _rsi(series: pd.Series, period: int = 14) -> float | None:
    if len(series) < period + 1:
        return None
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    if avg_loss.iloc[-1] == 0:
        return 100.0 if avg_gain.iloc[-1] > 0 else 50.0
    rs = avg_gain / avg_loss
    value = 100 - (100 / (1 + rs))
    last = value.iloc[-1]
    return float(last) if pd.notna(last) else None


def compute_signal(
    price: float | None,
    ma_fast: float | None,
    ma_slow: float | None,
    rsi: float | None,
    narrative_fit: str,
    cfg: dict[str, Any],
) -> tuple[str, str]:
    tech = cfg.get("technical", {})
    overbought = tech.get("rsi_overbought", 70)

    if price is None or ma_fast is None or ma_slow is None:
        return "caution", "Insufficient price history"

    reasons: list[str] = []
    score = 0

    if price > ma_fast > ma_slow:
        score += 2
        reasons.append("price > MA50 > MA200")
    elif price > ma_slow:
        score += 1
        reasons.append("price above MA200 only")
    else:
        reasons.append("below key moving averages")

    if rsi is not None:
        if rsi >= overbought:
            score -= 1
            reasons.append(f"RSI elevated ({rsi:.1f})")
        elif rsi < tech.get("rsi_oversold", 30):
            score += 1
            reasons.append(f"RSI oversold ({rsi:.1f})")
        else:
            reasons.append(f"RSI neutral ({rsi:.1f})")

    if narrative_fit == "strong":
        score += 1
        reasons.append("strong narrative fit")
    elif narrative_fit == "caution":
        score -= 1
        reasons.append("weak narrative fit")

    if score >= 3:
        return "strong_buy", "; ".join(reasons)
    if score >= 2:
        return "buy", "; ".join(reasons)
    if score >= 1:
        return "hold", "; ".join(reasons)
    return "caution", "; ".join(reasons)


def analyze_ticker(ticker: str, meta: dict[str, str], cfg: dict[str, Any]) -> TechnicalSnapshot:
    tech = cfg.get("technical", {})
    period = "2y"
    try:
        hist = yf.Ticker(ticker).history(period=period, auto_adjust=True)
        if hist.empty or "Close" not in hist.columns:
            return TechnicalSnapshot(
                None, None, None, None, None, None, None, "caution", "No history", "empty history"
            )

        close = hist["Close"]
        price = float(close.iloc[-1])
        ma_fast = float(close.rolling(tech.get("ma_fast", 50)).mean().iloc[-1])
        ma_slow = float(close.rolling(tech.get("ma_slow", 200)).mean().iloc[-1])
        rsi = _rsi(close, tech.get("rsi_period", 14))

        window = close.tail(252)
        high_52w = float(window.max())
        low_52w = float(window.min())
        drawdown = ((price - high_52w) / high_52w * 100) if high_52w else None

        signal, reason = compute_signal(
            price, ma_fast, ma_slow, rsi, meta.get("narrative_fit", "monitor"), cfg
        )
        return TechnicalSnapshot(
            price=price,
            ma_fast=ma_fast,
            ma_slow=ma_slow,
            rsi=rsi,
            high_52w=high_52w,
            low_52w=low_52w,
            drawdown_pct=drawdown,
            signal=signal,
            signal_reason=reason,
        )
    except Exception as exc:  # noqa: BLE001 — report per-ticker failures
        return TechnicalSnapshot(
            None, None, None, None, None, None, None, "caution", str(exc), str(exc)
        )