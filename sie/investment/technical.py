"""Dependency-free technical indicators."""
from __future__ import annotations
import math
from typing import Any

def sma(values: list[float], period: int) -> float | None:
    return sum(values[-period:]) / period if len(values) >= period else None

def rsi(values: list[float], period: int = 14) -> float | None:
    if len(values) <= period: return None
    changes = [values[i] - values[i - 1] for i in range(1, len(values))]
    gains = [max(x, 0.0) for x in changes]
    losses = [max(-x, 0.0) for x in changes]
    avg_gain, avg_loss = sum(gains[:period]) / period, sum(losses[:period]) / period
    for i in range(period, len(changes)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    if avg_loss == 0: return 100.0 if avg_gain else 50.0
    return 100.0 - 100.0 / (1.0 + avg_gain / avg_loss)

def ema_series(values: list[float], period: int) -> list[float]:
    if not values: return []
    alpha, result = 2.0 / (period + 1.0), [values[0]]
    for value in values[1:]: result.append(alpha * value + (1.0 - alpha) * result[-1])
    return result

def analyze_history(history: list[dict[str, Any]]) -> dict[str, Any]:
    closes = [float(row["close"]) for row in history if row.get("close") is not None]
    if not closes: return {"status": "unavailable", "reason": "No daily close history"}
    price, mean20 = closes[-1], sma(closes, 20)
    ma50, ma200, rsi14 = sma(closes, 50), sma(closes, 200), rsi(closes)
    ema12, ema26 = ema_series(closes, 12), ema_series(closes, 26)
    macd_line = [a - b for a, b in zip(ema12, ema26)]
    signal_line = ema_series(macd_line, 9)
    std = math.sqrt(sum((x - mean20) ** 2 for x in closes[-20:]) / 20) if len(closes) >= 20 and mean20 is not None else None
    high, low = max(closes[-252:]), min(closes[-252:])
    trend = "bullish" if ma50 is not None and ma200 is not None and price > ma50 > ma200 else ("bearish" if ma50 is not None and ma200 is not None and price < ma50 < ma200 else "mixed")
    return {"status": "ok", "price": price, "sma20": mean20, "sma50": ma50, "sma200": ma200,
            "rsi14": rsi14, "macd": macd_line[-1], "macd_signal": signal_line[-1],
            "bollinger_upper": mean20 + 2 * std if mean20 is not None and std is not None else None,
            "bollinger_lower": mean20 - 2 * std if mean20 is not None and std is not None else None,
            "high_52w": high, "low_52w": low,
            "drawdown_from_52w_high_pct": (price / high - 1) * 100 if high else None, "trend": trend}
