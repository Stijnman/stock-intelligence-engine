"""Unit tests for whisper-number overlay."""
from sie.whisper_number import detect_whisper_number, integrate_whisper_number_to_row


def test_detect_returns_required_keys():
    out = detect_whisper_number("NVDA", {"ticker": "NVDA", "signal": "hold", "signal_reason": "base"})
    for key in (
        "wn_beat_prob",
        "wn_cluster_score",
        "wn_days_to_print",
        "wn_consensus_gap",
        "signal_boost",
        "confidence",
        "reason",
        "source",
    ):
        assert key in out
    assert out["source"] in ("synthetic_proxy", "disabled")
    assert 0.0 <= out["wn_beat_prob"] <= 1.0
    assert out["signal_boost"] in (-1, 0, 1)


def test_disabled_overlay():
    out = detect_whisper_number("NVDA", cfg={"whisper_number": {"enabled": False}})
    assert out["source"] == "disabled"
    assert out["signal_boost"] == 0


def test_integrate_adds_columns():
    row = {"ticker": "NVDA", "signal": "hold", "signal_reason": "base"}
    out = integrate_whisper_number_to_row(row)
    assert "wn_beat_prob" in out
    assert "wn_boost" in out
    assert "wn_reason" in out
    assert "WN:" in out["signal_reason"] or "🤐" in out["signal_reason"]
