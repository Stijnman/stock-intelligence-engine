"""Primary credit issuance overlay unit checks."""
from sie.primary_credit import detect_primary_credit, integrate_primary_credit_to_row


def test_detect_preferred_columns():
    out = detect_primary_credit("AAPL", {"predicted_velocity": 2.2})
    assert out["pci_concession_bp"] >= 0.0
    assert 0.0 <= out["pci_supply_score"] <= 1.0
    assert out["signal_boost"] in (-1, 0, 1)
    assert out["source"] == "synthetic_proxy"


def test_disabled():
    out = detect_primary_credit("T", cfg={"primary_credit": {"enabled": False}})
    assert out["source"] == "disabled"
    assert out["signal_boost"] == 0
    assert out["pci_concession_bp"] == 0.0


def test_integrate_columns():
    row = integrate_primary_credit_to_row({"ticker": "VZ", "signal": "buy", "signal_reason": "base"})
    for col in ("pci_concession_bp", "pci_supply_score", "pci_boost", "pci_reason"):
        assert col in row


def test_supply_pressure_caution_on_heavy_issuer():
    cfg = {
        "primary_credit": {
            "enabled": True,
            "concession_tight_bp": 1.0,
            "concession_wide_bp": 8.0,
            "supply_hot": 0.40,
            "supply_cold": 0.02,
            "narrative_hot": 1.4,
            "min_confidence": 0.20,
        }
    }
    out = detect_primary_credit("CVNA", {"predicted_velocity": 0.4}, cfg)
    assert out["signal_boost"] == -1
    assert "supply-pressure" in out["reason"]


def test_scarce_calendar_boost_on_quiet_name():
    cfg = {
        "primary_credit": {
            "enabled": True,
            "concession_tight_bp": 20.0,
            "concession_wide_bp": 80.0,
            "supply_hot": 0.99,
            "supply_cold": 0.80,
            "narrative_hot": 1.0,
            "min_confidence": 0.20,
        }
    }
    out = detect_primary_credit("AAPL", {"predicted_velocity": 2.4}, cfg)
    assert out["signal_boost"] == 1
    assert "scarce primary supply" in out["reason"]
