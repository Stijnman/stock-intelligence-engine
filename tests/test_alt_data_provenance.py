"""Alternative-data provenance overlay unit checks."""
from sie.alt_data_provenance import detect_alt_data_provenance, integrate_alt_data_provenance_to_row


def test_detect_preferred_columns():
    out = detect_alt_data_provenance("AAPL", {"predicted_velocity": 2.2})
    assert 0.0 <= out["adp_provenance"] <= 1.0
    assert 0.0 <= out["adp_crosscheck"] <= 1.0
    assert out["signal_boost"] in (-1, 0, 1)
    assert out["source"] == "synthetic_proxy"


def test_disabled():
    out = detect_alt_data_provenance("AMC", cfg={"alt_data_provenance": {"enabled": False}})
    assert out["source"] == "disabled"
    assert out["signal_boost"] == 0
    assert out["adp_provenance"] == 0.0
    assert out["adp_crosscheck"] == 0.0


def test_integrate_columns():
    row = integrate_alt_data_provenance_to_row({"ticker": "NVDA", "signal": "buy", "signal_reason": "base"})
    for col in ("adp_provenance", "adp_crosscheck", "adp_boost", "adp_reason"):
        assert col in row


def test_synthetic_heat_caution():
    cfg = {
        "alt_data_provenance": {
            "enabled": True,
            "provenance_hot": 0.95,
            "provenance_cold": 0.70,
            "crosscheck_hot": 0.95,
            "crosscheck_cold": 0.70,
            "narrative_hot": 1.0,
            "min_confidence": 0.20,
        }
    }
    out = detect_alt_data_provenance("AMC", {"predicted_velocity": 2.4}, cfg)
    assert out["signal_boost"] == -1
    assert "caution" in out["reason"]


def test_clean_confirm_boost():
    cfg = {
        "alt_data_provenance": {
            "enabled": True,
            "provenance_hot": 0.40,
            "provenance_cold": 0.05,
            "crosscheck_hot": 0.40,
            "crosscheck_cold": 0.05,
            "narrative_hot": 1.0,
            "min_confidence": 0.20,
        }
    }
    out = detect_alt_data_provenance("MSFT", {"predicted_velocity": 2.4}, cfg)
    assert out["signal_boost"] == 1
    assert "soft boost" in out["reason"]
