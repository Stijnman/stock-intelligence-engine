"""Index reconstitution forced passive-flow overlay tests."""
from sie.index_reconstitution import (
    detect_index_reconstitution,
    integrate_index_reconstitution_to_row,
)


def test_add_name_has_positive_flow_versus_delete():
    added = detect_index_reconstitution("PLTR", {"predicted_velocity": 2.4})
    deleted = detect_index_reconstitution("WBA", {"predicted_velocity": 2.4})
    assert added["source"] == "synthetic_proxy"
    assert added["idx_event"] in ("add", "upweight")
    assert deleted["idx_event"] in ("delete", "downweight")
    assert added["idx_forced_usd"] > 0
    assert deleted["idx_forced_usd"] < 0
    assert added["signal_boost"] == 1
    assert deleted["signal_boost"] == -1


def test_disabled_overlay_is_neutral():
    out = detect_index_reconstitution(
        "PLTR",
        {"predicted_velocity": 3.0},
        {"index_reconstitution": {"enabled": False}},
    )
    assert out["source"] == "disabled"
    assert out["signal_boost"] == 0
    assert out["idx_event"] == "none"
    assert out["idx_forced_usd"] == 0.0


def test_integrate_writes_preferred_columns():
    row = {"ticker": "CRWD", "signal": "buy", "signal_reason": "base", "predicted_velocity": 2.1}
    out = integrate_index_reconstitution_to_row(row)
    for col in ("idx_event", "idx_forced_usd", "idx_boost", "idx_reason"):
        assert col in out
    assert out["signal"] == "strong_buy"
    assert "idx" in out["signal_reason"]
