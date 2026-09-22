"""Unit tests for TRACE corporate-bond flow overlay."""
from sie.trace_flow import detect_trace_flow, integrate_trace_flow_to_row


def test_detect_returns_required_keys():
    out = detect_trace_flow("NVDA", {"ticker": "NVDA", "signal": "hold", "signal_reason": "base"})
    for key in (
        "trace_customer_flow",
        "trace_liq_score",
        "trace_dispersion",
        "signal_boost",
        "confidence",
        "reason",
        "source",
    ):
        assert key in out
    assert out["source"] in ("synthetic_proxy", "disabled")
    assert -1.0 <= out["trace_customer_flow"] <= 1.0
    assert 0.0 <= out["trace_liq_score"] <= 1.0
    assert out["signal_boost"] in (-1, 0, 1)


def test_disabled_overlay():
    out = detect_trace_flow("NVDA", cfg={"trace_flow": {"enabled": False}})
    assert out["source"] == "disabled"
    assert out["signal_boost"] == 0


def test_deterministic_within_session_day():
    row = {"ticker": "NVDA", "signal": "hold", "signal_reason": "base", "predicted_velocity": 1.6}
    first = detect_trace_flow("NVDA", row)
    second = detect_trace_flow("NVDA", row)
    assert first == second


def test_integrate_adds_columns():
    row = {"ticker": "NVDA", "signal": "hold", "signal_reason": "base"}
    out = integrate_trace_flow_to_row(row)
    assert "trace_customer_flow" in out
    assert "trace_liq_score" in out
    assert "trace_boost" in out
    assert "trace_reason" in out
    assert "TRACE:" in out["signal_reason"]
