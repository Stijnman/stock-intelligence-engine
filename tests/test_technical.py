"""Tests for technical indicator helpers."""

import pandas as pd

from sie.technical import _rsi, compute_signal


def test_rsi_range():
    close = pd.Series([float(100 + i) for i in range(30)])
    value = _rsi(close, 14)
    assert value is not None
    assert 0 <= value <= 100


def test_strong_buy_signal():
    cfg = {"technical": {"rsi_overbought": 70, "rsi_oversold": 30}}
    signal, _ = compute_signal(110.0, 105.0, 100.0, 55.0, "strong", cfg)
    assert signal in ("strong_buy", "buy")