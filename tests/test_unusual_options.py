"""Unit tests for unusual options sweep vs block confirmation overlay."""
from sie.unusual_options import detect_unusual_options, integrate_unusual_options_to_row


def test_detect_returns_required_keys():
    out = detect_unusual_options("NVDA", {"ticker": "NVDA", "signal": "hold", "signal_reason": "base"})
    for key in (
        "uopt_sweep_score",
        "uopt_block_ratio",
        "uopt_call_put",
        "uopt_premium_usd_m",
        "signal_boost",
        "confidence",
        "reason",
        "source",
    ):
        assert key in out
    assert out["source"] in ("synthetic_proxy", "disabled")
    assert 0.0 <= out["uopt_sweep_score"] <= 1.0
    assert 0.0 <= out["uopt_block_ratio"] <= 1.0
    assert out["signal_boost"] in (-1, 0, 1)


def test_disabled_overlay():
    out = detect_unusual_options("NVDA", cfg={"unusual_options": {"enabled": False}})
    assert out["source"] == "disabled"
    assert out["signal_boost"] == 0


def test_integrate_adds_columns():
    row = {"ticker": "NVDA", "signal": "hold", "signal_reason": "base"}
    out = integrate_unusual_options_to_row(row)
    assert "uopt_sweep_score" in out
    assert "uopt_block_ratio" in out
    assert "uopt_boost" in out
    assert "uopt_reason" in out
    assert "UOPT" in out["signal_reason"]
