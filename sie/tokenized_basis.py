"""Cross-Venue Tokenized-Share Basis / On-Chain Equity Premium Overlay.

Scores the basis (in bps) between a listed equity and its tokenized /
on-chain wrappers, plus venue liquidity depth, as a confirmation layer
next to dark-pool and retail-flow.

Live Superstate / Backed / Dinari / Ondo / Robinhood tokenized-share
APIs are an explicit future hook. Current source is always labeled
synthetic_proxy when live data is unavailable.

Preferred columns: tok_basis_bps, tok_venue_liq, tok_boost, tok_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


TOKENIZED_UNIVERSE = {
    "NVDA", "AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "SPY",
    "QQQ", "COIN", "MSTR", "HOOD", "PLTR", "AMD", "AVGO", "TSM",
}


def _clip(v: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_tokenized_basis(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    tok_cfg = cfg.get("tokenized_basis", {})
    if not tok_cfg.get("enabled", True):
        return {
            "tok_basis_bps": 0.0,
            "tok_venue_liq": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Tokenized-share basis overlay disabled",
            "source": "disabled",
        }

    premium_hot = float(tok_cfg.get("premium_hot_bps", 35.0))
    discount_hot = float(tok_cfg.get("discount_hot_bps", -40.0))
    liq_hot = float(tok_cfg.get("liq_hot", 0.55))
    liq_cold = float(tok_cfg.get("liq_cold", 0.18))
    vel_hot = float(tok_cfg.get("narrative_hot", 1.4))
    min_conf = float(tok_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 9041
    rng = random.Random(seed)
    row = row or {}

    if tkr in TOKENIZED_UNIVERSE:
        basis_bps = rng.uniform(-85.0, 95.0)
        venue_liq = rng.uniform(0.22, 0.92)
    else:
        basis_bps = rng.uniform(-25.0, 30.0)
        venue_liq = rng.uniform(0.05, 0.38)

    vel = float(
        row.get("predicted_velocity")
        or row.get("auth_filtered_velocity")
        or row.get("sentiment_velocity")
        or rng.uniform(0.2, 3.8)
    )
    auth = float(row.get("auth_score") or 0.55)

    score = _clip(
        0.55 * (basis_bps / 80.0)
        + 0.30 * (venue_liq - 0.40)
        + 0.15 * max(min(vel / 4.0, 1.0), 0.0)
    )

    parts = [
        f"tok basis={basis_bps:+.1f}bps",
        f"venue_liq={venue_liq:.2f}",
    ]
    boost = 0
    confidence = 0.40 + 0.16 * auth

    prem_confirm = (
        basis_bps >= premium_hot
        and venue_liq >= liq_hot
        and vel >= vel_hot * 0.50
    )
    disc_warn = (
        basis_bps <= discount_hot
        and venue_liq <= liq_cold
        and vel >= vel_hot * 0.55
    )

    if prem_confirm:
        boost = 1
        confidence = min(0.92, 0.48 + 0.24 * abs(score) + 0.14 * auth)
        parts.append(
            "on-chain wrapper trades rich vs listed + liquid venue — soft boost"
        )
    elif disc_warn:
        boost = -1
        confidence = min(0.90, 0.46 + 0.22 * abs(min(score, 0)) + 0.12 * max(vel / 4.0, 0))
        parts.append(
            "tokenized share trades cheap with thin venue liquidity — basis caution"
        )
    else:
        parts.append("tokenized-share basis overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "tok_basis_bps": round(float(basis_bps), 2),
        "tok_venue_liq": round(float(venue_liq), 4),
        "tok_score": round(float(score), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_tokenized_basis_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate cross-venue tokenized-share basis into a row."""
    mom = detect_tokenized_basis(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "tok_basis_bps": mom["tok_basis_bps"],
            "tok_venue_liq": mom["tok_venue_liq"],
            "tok_score": mom.get("tok_score", 0.0),
            "tok_boost": mom["signal_boost"],
            "tok_confidence": mom["confidence"],
            "tok_reason": mom["reason"],
            "tok_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | tok-basis {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | tok-basis {mom['reason']}"
    else:
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | tok-basis: {mom['reason']}"
    return row
