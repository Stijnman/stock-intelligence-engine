"""Tests for Agentic Brokerage Account Flow & Penetration Overlay."""
from sie.agentic_flow import detect_agentic_flow, integrate_agentic_flow_to_row


def test_detect_returns_preferred_columns():
    out = detect_agentic_flow("NVDA")
    assert "agt_flow_share" in out
    assert "agt_tool_intensity" in out
    assert "signal_boost" in out
    assert "reason" in out
    assert out["source"] == "synthetic_proxy"
    assert 0.0 <= out["agt_flow_share"] <= 1.0
    assert 0.0 <= out["agt_tool_intensity"] <= 1.0


def test_integrate_updates_row():
    row = {"ticker": "NVDA", "signal": "buy", "signal_reason": "base"}
    updated = integrate_agentic_flow_to_row(row)
    assert "agt_boost" in updated
    assert "agt_reason" in updated
    assert "agt_boost" in updated  # reason only appended on non-zero boost


def test_disabled_returns_zero():
    out = detect_agentic_flow("NVDA", cfg={"agentic_flow": {"enabled": False}})
    assert out["source"] == "disabled"
    assert out["signal_boost"] == 0
