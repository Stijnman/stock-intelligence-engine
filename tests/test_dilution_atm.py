"""ATM dilution overlay unit checks."""
from sie.dilution_atm import detect_dilution_atm, integrate_dilution_atm_to_row


def test_detect_preferred_columns():
    out = detect_dilution_atm("PLTR", {"predicted_velocity": 2.4})
    assert 0.0 <= out["dil_atm_velocity"] <= 1.0
    assert "dil_share_delta" in out
    assert out["signal_boost"] in (-1, 0, 1)


def test_disabled():
    out = detect_dilution_atm("PLTR", cfg={"dilution_atm": {"enabled": False}})
    assert out["source"] == "disabled"
    assert out["signal_boost"] == 0


def test_integrate_columns():
    row = integrate_dilution_atm_to_row({"ticker": "SMCI", "signal": "buy", "signal_reason": "base"})
    for col in ("dil_atm_velocity", "dil_share_delta", "dil_boost", "dil_reason"):
        assert col in row
