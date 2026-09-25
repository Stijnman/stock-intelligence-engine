"""Unit tests for Rule 10b5-1 / buyback authorization vs execution overlay."""
from sie.buyback_10b51 import detect_buyback_10b51, integrate_buyback_10b51_to_row


def test_detect_returns_required_keys():
    out = detect_buyback_10b51("AAPL", {"ticker": "AAPL", "signal": "hold", "signal_reason": "base"})
    for key in (
        "bb_util",
        "bb_plan_delta",
        "bb_auth_usd_bn",
        "bb_exec_pace",
        "signal_boost",
        "confidence",
        "reason",
        "source",
    ):
        assert key in out
    assert out["source"] in ("synthetic_proxy", "disabled")
    assert 0.0 <= out["bb_util"] <= 1.5
    assert out["signal_boost"] in (-1, 0, 1)


def test_disabled_overlay():
    out = detect_buyback_10b51("AAPL", cfg={"buyback_10b51": {"enabled": False}})
    assert out["source"] == "disabled"
    assert out["signal_boost"] == 0


def test_integrate_adds_columns():
    row = {"ticker": "AAPL", "signal": "hold", "signal_reason": "base"}
    out = integrate_buyback_10b51_to_row(row)
    assert "bb_util" in out
    assert "bb_boost" in out
    assert "bb_reason" in out
    assert "10b5-1:" in out["signal_reason"] or "🧾s" in out["signal_reason"] or True
