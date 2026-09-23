"""Unit tests for KOL / influencer amplification overlay."""
from sie.kol_amplification import detect_kol_amplification, integrate_kol_amplification_to_row


def test_detect_returns_required_keys():
    out = detect_kol_amplification("NVDA", {"ticker": "NVDA", "signal": "hold", "signal_reason": "base"})
    for key in (
        "kol_score",
        "kol_cascade",
        "kol_amp_ratio",
        "kol_auth",
        "signal_boost",
        "confidence",
        "reason",
        "source",
    ):
        assert key in out
    assert out["source"] in ("synthetic_proxy", "disabled")
    assert 0.0 <= out["kol_score"] <= 1.0
    assert out["signal_boost"] in (-1, 0, 1)


def test_disabled_overlay():
    out = detect_kol_amplification("NVDA", cfg={"kol_amplification": {"enabled": False}})
    assert out["source"] == "disabled"
    assert out["signal_boost"] == 0


def test_integrate_adds_columns():
    row = {"ticker": "NVDA", "signal": "hold", "signal_reason": "base"}
    out = integrate_kol_amplification_to_row(row)
    assert "kol_score" in out
    assert "kol_boost" in out
    assert "kol_reason" in out
    assert "KOL:" in out["signal_reason"] or "📣" in out["signal_reason"]
