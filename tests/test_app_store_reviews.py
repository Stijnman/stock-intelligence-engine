from sie.app_store_reviews import detect_app_store_reviews, integrate_app_store_reviews_to_row


def test_detect_app_store_reviews_keys():
    out = detect_app_store_reviews("NVDA", {"ticker": "NVDA", "signal": "hold", "signal_reason": "base"})
    assert "asr_sentiment" in out
    assert "asr_complaint_velocity" in out
    assert "signal_boost" in out
    assert "reason" in out
    assert out["source"] in {"synthetic_proxy", "disabled"}
    assert isinstance(out["asr_sentiment"], float)


def test_detect_disabled():
    out = detect_app_store_reviews("NVDA", cfg={"app_store_reviews": {"enabled": False}})
    assert out["signal_boost"] == 0
    assert out["source"] == "disabled"


def test_integrate_app_store_reviews_to_row():
    row = {"ticker": "AAPL", "signal": "hold", "signal_reason": "base"}
    out = integrate_app_store_reviews_to_row(row)
    assert "asr_boost" in out
    assert "asr_reason" in out
    assert "asr_sentiment" in out
    assert "app-store" in (out.get("signal_reason") or "")
