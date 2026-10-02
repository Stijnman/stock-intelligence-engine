from sie.news_materiality import detect_news_materiality, integrate_news_materiality_to_row


def test_detect_news_materiality_keys():
    out = detect_news_materiality("NVDA", {"ticker": "NVDA", "signal": "hold", "signal_reason": "base"})
    assert "nimp_score" in out
    assert out["nimp_vol_bucket"] in {"quiet", "elevated", "high", "extreme"}
    assert "signal_boost" in out
    assert "reason" in out
    assert out["source"] in {"synthetic_proxy", "disabled"}
    assert 0.0 <= out["nimp_score"] <= 1.0


def test_detect_disabled():
    out = detect_news_materiality("NVDA", cfg={"news_materiality": {"enabled": False}})
    assert out["signal_boost"] == 0
    assert out["source"] == "disabled"
    assert out["nimp_vol_bucket"] == "quiet"


def test_integrate_news_materiality_to_row():
    row = {"ticker": "NVDA", "signal": "hold", "signal_reason": "base", "predicted_velocity": 2.4, "auth_score": 0.7}
    out = integrate_news_materiality_to_row(row)
    assert "nimp_boost" in out
    assert "nimp_reason" in out
    assert "nimp_score" in out
    assert "nimp_vol_bucket" in out
    assert "nimp" in (out.get("signal_reason") or "")


def test_adverse_tape_can_caution():
    row = {
        "ticker": "TSLA",
        "signal": "buy",
        "signal_reason": "base",
        "avg_news_sentiment": -0.8,
        "predicted_velocity": 2.8,
        "auth_score": 0.72,
    }
    out = integrate_news_materiality_to_row(
        row,
        cfg={"news_materiality": {"enabled": True, "score_mid": 0.05, "adverse_hot": -0.05, "narrative_hot": 0.2, "min_confidence": 0.1}},
    )
    assert out["nimp_boost"] == -1
    assert out["signal"] in {"hold", "caution"}
