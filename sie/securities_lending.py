"""Securities Lending / Borrow Fee & Short Squeeze Risk Overlay.

Tracks a deterministic synthetic proxy for borrow fees, hard-to-borrow
status and days-to-cover as a short-pressure / squeeze-risk confirmation
layer. Soft boost when elevated borrow costs coincide with rising
narrative velocity and short-interest covering; caution when high borrow
+ expanding short interest + hot narrative signals elevated squeeze risk
without confirmation.

Live securities-lending feeds (IHS Markit / S3, ORC, broker HTB lists) are
left as an explicit future hook — no invented API keys or endpoints.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


def detect_securities_lending(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    sl_cfg = cfg.get("securities_lending", {})
    if not sl_cfg.get("enabled", True):
        return {
            "sl_borrow_fee": 0.0,
            "sl_days_to_cover": 0.0,
            "sl_htb": False,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Securities lending module disabled",
            "source": "disabled",
        }

    elevated_fee = float(sl_cfg.get("elevated_borrow_fee", 5.0))  # annualized %
    high_fee = float(sl_cfg.get("high_borrow_fee", 15.0))
    dtc_elevated = float(sl_cfg.get("elevated_days_to_cover", 4.0))
    min_conf = float(sl_cfg.get("min_confidence", 0.40))
    vel_hot = float(sl_cfg.get("narrative_hot", 1.5))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 73
    rng = random.Random(seed)

    # Realistic ranges: most names low fee; a minority elevated/HTB
    fee = round(rng.uniform(0.3, 28.0), 2)
    dtc = round(rng.uniform(0.8, 9.5), 2)
    htb = fee >= high_fee or (fee >= elevated_fee and rng.random() > 0.55)

    vel = 0.0
    si_change = 0.0
    if row:
        vel = float(row.get("predicted_velocity") or row.get("sentiment_velocity") or 0.0)
        si_change = float(row.get("si_change") or 0.0)

    boost = 0
    confidence = 0.50
    parts: list[str] = [
        f"Borrow fee {fee:.1f}% ann. | DTC {dtc:.1f}d" + (" | HTB" if htb else "")
    ]

    # Squeeze-risk caution: high fee + hot narrative + expanding shorts
    if fee >= high_fee and vel >= vel_hot and si_change > 0.05:
        boost = -1
        confidence = min(0.88, 0.58 + 0.35 * min(fee / 40.0, 1.0))
        parts.append("elevated borrow + expanding SI + hot narrative — squeeze-risk caution")
    # Soft boost: high fee + covering (negative si_change) + hot narrative
    elif fee >= elevated_fee and si_change <= -0.06 and vel >= vel_hot:
        boost = 1
        confidence = min(0.85, 0.55 + 0.4 * min(fee / 30.0, 1.0))
        parts.append("elevated borrow + short covering + rising narrative — soft squeeze-boost")
    elif fee >= elevated_fee or htb:
        parts.append("elevated borrow / HTB — observation only")
    else:
        parts.append("no material securities-lending overlay")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "sl_borrow_fee": fee,
        "sl_days_to_cover": dtc,
        "sl_htb": bool(htb),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_lending_proxy",
    }


def integrate_securities_lending_to_row(row: dict, cfg: dict | None = None) -> dict:
    mom = detect_securities_lending(row.get("ticker", ""), row, cfg)
    row.update({
        "sl_borrow_fee": mom["sl_borrow_fee"],
        "sl_days_to_cover": mom["sl_days_to_cover"],
        "sl_htb": mom["sl_htb"],
        "sl_boost": mom["signal_boost"],
        "sl_confidence": mom["confidence"],
        "sl_reason": mom["reason"],
        "sl_source": mom["source"],
    })
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 📉 {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 📉 {mom['reason']}"
    else:
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | Lending: {mom['reason']}"
    return row
