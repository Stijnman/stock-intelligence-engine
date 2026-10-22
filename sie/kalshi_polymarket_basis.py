"""Kalshi Regulated vs Polymarket Offshore Earnings Beat Probability Basis Overlay.

Scores the basis (in bps) between regulated Kalshi earnings-beat probability and
offshore Polymarket for the same event. Soft boost when regulated Kalshi shows a
rich constructive basis versus offshore into a confirming narrative; caution on
adverse or collapsing basis while narrative heat remains elevated.

Live Kalshi + Polymarket feed is an explicit future hook. Current source is always
labeled synthetic_proxy when a live feed is unavailable.

Preferred columns: kpm_basis_bps, kpm_kalshi_prob, kpm_boost, kpm_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


# Tickers with typically rich constructive Kalshi vs Polymarket basis.
KPM_HOT = {
    "NVDA", "TSLA", "META", "AMD", "AVGO", "PLTR", "SMCI", "CRWD", "ARM", "NET",
}
# Tickers with typically adverse or collapsing basis.
KPM_COLD = {
    "INTC", "BA", "PFE", "XOM", "WMT", "KO", "IBM", "CSCO", "F", "GM",
}


def _clip(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_kalshi_polymarket_basis(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    a_cfg = cfg.get("kalshi_polymarket_basis", {})
    if not a_cfg.get("enabled", True):
        return {
            "kpm_basis_bps": 0.0,
            "kpm_kalshi_prob": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Kalshi regulated vs Polymarket offshore earnings beat probability basis overlay disabled",
            "source": "disabled",
        }

    basis_hot_bps = float(a_cfg.get("basis_hot_bps", 40.0))
    basis_cold_bps = float(a_cfg.get("basis_cold_bps", -30.0))
    prob_hot = float(a_cfg.get("prob_hot", 0.62))
    prob_cold = float(a_cfg.get("prob_cold", 0.38))
    narrative_hot = float(a_cfg.get("narrative_hot", 1.4))
    min_conf = float(a_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 19456
    rng = random.Random(seed)
    row = row or {}
    narr = float(row.get("predicted_velocity") or row.get("narrative_velocity") or 1.0)

    if tkr in KPM_HOT:
        kalshi_prob = rng.uniform(0.58, 0.82)
        basis_bps = rng.uniform(25.0, 85.0)
    elif tkr in KPM_COLD:
        kalshi_prob = rng.uniform(0.22, 0.48)
        basis_bps = rng.uniform(-65.0, -15.0)
    else:
        kalshi_prob = rng.uniform(0.38, 0.62)
        basis_bps = rng.uniform(-20.0, 35.0)

    basis_strength = _clip((basis_bps - basis_cold_bps) / max(basis_hot_bps - basis_cold_bps, 1e-6))
    prob_strength = _clip((kalshi_prob - prob_cold) / max(prob_hot - prob_cold, 1e-6))
    confidence = _clip(0.34 + 0.36 * basis_strength + 0.26 * prob_strength)

    parts = [
        f"kpm_basis_bps={basis_bps:.1f}",
        f"kpm_kalshi_prob={kalshi_prob:.2f}",
        f"narrative={narr:.2f}",
    ]
    boost = 0
    confirm = basis_bps >= basis_hot_bps and kalshi_prob >= prob_hot and narr >= narrative_hot
    caution = basis_bps <= basis_cold_bps and narr >= narrative_hot * 0.45

    if confirm:
        boost = 1
        confidence = min(0.95, confidence + 0.08)
        parts.append(
            "rich constructive Kalshi regulated earnings-beat basis vs Polymarket into confirming narrative — soft boost"
        )
    elif caution:
        boost = -1
        confidence = min(0.93, confidence + 0.06)
        parts.append(
            "adverse or collapsing Kalshi vs Polymarket basis while narrative heat remains elevated — caution"
        )
    else:
        parts.append("Kalshi regulated vs Polymarket offshore earnings beat probability basis overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "kpm_basis_bps": round(float(basis_bps), 2),
        "kpm_kalshi_prob": round(float(kalshi_prob), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_kalshi_polymarket_basis_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate Kalshi Regulated vs Polymarket Offshore Earnings Beat Probability Basis into a row."""
    mom = detect_kalshi_polymarket_basis(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "kpm_basis_bps": mom["kpm_basis_bps"],
            "kpm_kalshi_prob": mom["kpm_kalshi_prob"],
            "kpm_boost": mom["signal_boost"],
            "kpm_confidence": mom["confidence"],
            "kpm_reason": mom["reason"],
            "kpm_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + " | KPM soft boost"
    elif boost <= -1:
        if row.get("signal") in ("buy", "strong_buy"):
            row["signal"] = "hold"
        row["signal_reason"] = (row.get("signal_reason") or "") + " | KPM caution"
    return row
