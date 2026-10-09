"""Earnings event-contract vs whisper overlay."""
from sie.earnings_event_contract import (
    detect_earnings_event_contract,
    integrate_earnings_event_contract_to_row,
)


def test_rich_beats_miss_direction():
    rich = detect_earnings_event_contract("NVDA", {"predicted_velocity": 2.4})
    miss = detect_earnings_event_contract("INTC", {"predicted_velocity": 2.4})
    assert rich["eec_implied_beat"] > miss["eec_implied_beat"]
    assert rich["eec_whisper_gap"] > 0
    assert miss["eec_whisper_gap"] < 0
    assert rich["signal_boost"] >= 0
    assert miss["signal_boost"] <= 0


def test_disabled_gate():
    out = detect_earnings_event_contract(
        "NVDA",
        {"predicted_velocity": 3.0},
        {"earnings_event_contract": {"enabled": False}},
    )
    assert out["source"] == "disabled"
    assert out["signal_boost"] == 0
    assert out["eec_implied_beat"] == 0.0


def test_integrate_preferred_columns():
    row = {"ticker": "NVDA", "signal": "buy", "predicted_velocity": 2.6}
    out = integrate_earnings_event_contract_to_row(row)
    for col in ("eec_implied_beat", "eec_whisper_gap", "eec_boost", "eec_reason"):
        assert col in out
    assert out["eec_source"] == "synthetic_proxy"
