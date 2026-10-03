"""TRACE customer-flow overlay unit checks."""
from sie.trace_flow import detect_trace_flow, integrate_trace_flow_to_row


def test_detect_preferred_columns():
    out = detect_trace_flow("JPM", {"predicted_velocity": 2.1})
    assert -1.0 <= out["trace_customer_flow"] <= 1.0
    assert 0.0 <= out["trace_liq_score"] <= 1.0
    assert out["signal_boost"] in (-1, 0, 1)
    assert out["source"] == "synthetic_proxy"


def test_disabled():
    out = detect_trace_flow("JPM", cfg={"trace_flow": {"enabled": False}})
    assert out["source"] == "disabled"
    assert out["signal_boost"] == 0


def test_integrate_columns():
    row = integrate_trace_flow_to_row({"ticker": "CVNA", "signal": "buy", "signal_reason": "base"})
    for col in ("trace_customer_flow", "trace_liq_score", "trace_boost", "trace_reason"):
        assert col in row


def test_shock_caution_on_stressed_name():
    cfg = {
        "trace_flow": {
            "enabled": True,
            "flow_hot": 0.35,
            "flow_cold": -0.05,
            "liq_hot": 0.55,
            "liq_cold": 0.90,
            "narrative_hot": 1.4,
            "min_confidence": 0.20,
        }
    }
    out = detect_trace_flow("CVNA", {"predicted_velocity": 0.4}, cfg)
    assert out["signal_boost"] == -1
    assert "liquidity shock" in out["reason"]
