"""Unit tests for ETF creation/redemption & AP flow overlay."""
from sie.etf_flow import detect_etf_flow, integrate_etf_flow_to_row


def test_detect_returns_required_keys():
    out = detect_etf_flow("NVDA", {"ticker": "NVDA", "signal": "hold", "signal_reason": "base"})
    for key in (
        "etf_flow_score",
        "etf_prem_disc",
        "etf_create_streak",
        "etf_theme",
        "signal_boost",
        "confidence",
        "reason",
        "source",
    ):
        assert key in out
    assert out["source"] in ("synthetic_proxy", "disabled")
    assert -1.0 <= out["etf_flow_score"] <= 1.0
    assert out["signal_boost"] in (-1, 0, 1)


def test_disabled_overlay():
    out = detect_etf_flow("NVDA", cfg={"etf_flow": {"enabled": False}})
    assert out["source"] == "disabled"
    assert out["signal_boost"] == 0


def test_integrate_adds_columns():
    row = {"ticker": "NVDA", "signal": "hold", "signal_reason": "base"}
    out = integrate_etf_flow_to_row(row)
    assert "etf_flow_score" in out
    assert "etf_boost" in out
    assert "etf_reason" in out
    assert "ETF:" in out["signal_reason"] or "📦" in out["signal_reason"]
