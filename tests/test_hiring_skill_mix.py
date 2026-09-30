from sie.hiring_skill_mix import detect_hiring_skill_mix, integrate_hiring_skill_mix_to_row


def test_detect_hiring_skill_mix_keys():
    out = detect_hiring_skill_mix("NVDA", {"ticker": "NVDA", "signal": "hold", "signal_reason": "base"})
    assert "hmix_senior_share" in out
    assert "hmix_comp_delta" in out
    assert "signal_boost" in out
    assert "reason" in out
    assert out["source"] in {"synthetic_proxy", "disabled"}
    assert isinstance(out["hmix_senior_share"], float)


def test_detect_disabled():
    out = detect_hiring_skill_mix("NVDA", cfg={"hiring_skill_mix": {"enabled": False}})
    assert out["signal_boost"] == 0
    assert out["source"] == "disabled"


def test_integrate_hiring_skill_mix_to_row():
    row = {"ticker": "NVDA", "signal": "hold", "signal_reason": "base"}
    out = integrate_hiring_skill_mix_to_row(row)
    assert "hmix_boost" in out
    assert "hmix_reason" in out
    assert "hmix_senior_share" in out
    assert "hiring-skill-mix" in (out.get("signal_reason") or "")
