"""Rule 606 retail options routing overlay tests."""
from sie.rule_606 import detect_rule_606, integrate_rule_606_to_row


def test_competitive_name_has_better_fills_than_concentrated():
    clean = detect_rule_606("NVDA", {"predicted_velocity": 2.2})
    crowded = detect_rule_606("GME", {"predicted_velocity": 2.2})
    assert clean["source"] == "synthetic_proxy"
    assert clean["r606_exec_quality"] > crowded["r606_exec_quality"]
    assert clean["r606_concentration"] < crowded["r606_concentration"]
    assert clean["signal_boost"] == 1
    assert crowded["signal_boost"] == -1
    assert "r606_concentration" in clean and "r606_exec_quality" in clean


def test_disabled_overlay_is_neutral():
    out = detect_rule_606("NVDA", {"predicted_velocity": 3.0}, {"rule_606": {"enabled": False}})
    assert out["source"] == "disabled"
    assert out["signal_boost"] == 0


def test_integrate_writes_preferred_columns():
    row = {"ticker": "AAPL", "signal": "buy", "signal_reason": "base", "predicted_velocity": 2.0}
    out = integrate_rule_606_to_row(row)
    for col in ("r606_concentration", "r606_exec_quality", "r606_boost", "r606_reason"):
        assert col in out
    assert out["signal"] == "strong_buy"
    assert "r606" in out["signal_reason"]
