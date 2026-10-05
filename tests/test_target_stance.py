"""Target-specific financial stance overlay unit checks."""
from sie.target_stance import detect_target_stance, integrate_target_stance_to_row


def test_detect_preferred_columns():
    out = detect_target_stance("AAPL", {"predicted_velocity": 2.2})
    assert out["tsn_stance"] in ("constructive", "hedged", "cautious", "unknown")
    assert 0.0 <= out["tsn_specificity"] <= 1.0
    assert 0.0 <= out["tsn_qa_gap"] <= 1.0
    assert out["signal_boost"] in (-1, 0, 1)
    assert out["source"] == "synthetic_proxy"


def test_disabled():
    out = detect_target_stance("AMC", cfg={"target_stance": {"enabled": False}})
    assert out["source"] == "disabled"
    assert out["signal_boost"] == 0
    assert out["tsn_specificity"] == 0.0
    assert out["tsn_stance"] == "unknown"


def test_integrate_columns():
    row = integrate_target_stance_to_row({"ticker": "NVDA", "signal": "buy", "signal_reason": "base"})
    for col in ("tsn_stance", "tsn_specificity", "tsn_qa_gap", "tsn_boost", "tsn_reason"):
        assert col in row


def test_vague_heat_caution():
    cfg = {
        "target_stance": {
            "enabled": True,
            "specificity_hot": 0.95,
            "specificity_cold": 0.70,
            "qa_gap_hot": 0.20,
            "qa_gap_cold": 0.02,
            "narrative_hot": 1.0,
            "min_confidence": 0.20,
        }
    }
    out = detect_target_stance("AMC", {"predicted_velocity": 2.4}, cfg)
    assert out["signal_boost"] == -1
    assert "caution" in out["reason"]


def test_specific_confirm_boost():
    cfg = {
        "target_stance": {
            "enabled": True,
            "specificity_hot": 0.40,
            "specificity_cold": 0.05,
            "qa_gap_hot": 0.95,
            "qa_gap_cold": 0.90,
            "narrative_hot": 1.0,
            "min_confidence": 0.20,
        }
    }
    out = detect_target_stance("MSFT", {"predicted_velocity": 2.4}, cfg)
    assert out["signal_boost"] == 1
    assert "soft boost" in out["reason"]
