"""Tokenized Equity Continuous Pricing Premium vs Traditional Session Close Basis Overlay.

Scores the continuous (24/5) on-chain / tokenized equity pricing premium versus
traditional session close and the share of volume occurring outside regular hours.
Soft boost when a rich constructive premium and elevated 24/5 volume share confirm
a narrative into technical strength; caution on adverse or collapsing continuous
basis while narrative heat remains elevated.

Live tokenized equity feeds (Robinhood, Ondo, MarketVector 24/5 indexes, etc.)
are an explicit future hook. Current source is always labeled synthetic_proxy
when a live feed is unavailable.

Preferred columns: tep_basis_bps, tep_24_5_vol_share, tep_boost, tep_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


# Tickers with typically rich continuous/tokenized premiums and elevated 24/5 volume.
TEP_HOT = {
    "NVDA", "TSLA", "PLTR", "SMCI", "AVGO", "META", "AMD", "ARM", "COIN", "MSTR",
}
# Tickers with typically flat or adverse continuous basis and low off-hours volume.
TEP_COLD = {
    "INTC", "BA", "PFE", "XOM", "WMT", "KO", "IBM", "CSCO", "JNJ",
}


def _clip(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_tokenized_equity_premium(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    o_cfg = cfg.get("tokenized_equity_premium", {})
    if not o_cfg.get("enabled", True):
        return {
            "tep_basis_bps": 0.0,
            "tep_24_5_vol_share": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Tokenized equity continuous pricing premium overlay disabled",
            "source": "disabled",
        }

    basis_hot = float(o_cfg.get("basis_hot_bps", 45.0))
    basis_cold = float(o_cfg.get("basis_cold_bps", -25.0))
    vol_hot = float(o_cfg.get("vol_hot", 0.28))
    vol_cold = float(o_cfg.get("vol_cold", 0.08))
    narrative_hot = float(o_cfg.get("narrative_hot", 1.4))
    min_conf = float(o_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 27500
    rng = random.Random(seed)
    row = row or {}
    narr = float(row.get("predicted_velocity") or row.get("narrative_velocity") or 1.0)

    if tkr in TEP_HOT:
        basis_bps = rng.uniform(35.0, 95.0)
        vol_share = rng.uniform(0.22, 0.48)
    elif tkr in TEP_COLD:
        basis_bps = rng.uniform(-45.0, 5.0)
        vol_share = rng.uniform(0.03, 0.12)
    else:
        basis_bps = rng.uniform(-10.0, 40.0)
        vol_share = rng.uniform(0.08, 0.25)

    basis_strength = _clip((basis_bps - basis_cold) / max(basis_hot - basis_cold, 1e-6))
    vol_strength = _clip((vol_share - vol_cold) / max(vol_hot - vol_cold, 1e-6))
    confidence = _clip(0.30 + 0.38 * basis_strength + 0.26 * vol_strength)

    parts = [
        f"tep_basis_bps={basis_bps:.1f}",
        f"tep_24_5_vol_share={vol_share:.2f}",
        f"narrative={narr:.2f}",
    ]
    boost = 0
    confirm = basis_bps >= basis_hot and vol_share >= vol_hot and narr >= narrative_hot
    caution = basis_bps <= basis_cold and vol_share <= vol_cold and narr >= narrative_hot * 0.45

    if confirm:
        boost = 1
        confidence = min(0.95, confidence + 0.08)
        parts.append(
            "rich continuous/tokenized equity premium with elevated 24/5 volume share — soft boost"
        )
    elif caution:
        boost = -1
        confidence = min(0.93, confidence + 0.06)
        parts.append(
            "adverse or collapsing continuous basis while narrative heat remains elevated — caution"
        )
    else:
        parts.append("Tokenized equity continuous pricing premium overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "tep_basis_bps": round(float(basis_bps), 1),
        "tep_24_5_vol_share": round(float(vol_share), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_tokenized_equity_premium_to_row(
    row: dict, cfg: dict | None = None
) -> dict:
    """Integrate Tokenized Equity Continuous Pricing Premium into a row."""
    mom = detect_tokenized_equity_premium(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "tep_basis_bps": mom["tep_basis_bps"],
            "tep_24_5_vol_share": mom["tep_24_5_vol_share"],
            "tep_boost": mom["signal_boost"],
            "tep_confidence": mom["confidence"],
            "tep_reason": mom["reason"],
            "tep_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + " | TEP soft boost"
    elif boost <= -1:
        if row.get("signal") in ("buy", "strong_buy"):
            row["signal"] = "hold"
        row["signal_reason"] = (row.get("signal_reason") or "") + " | TEP caution"
    return row
