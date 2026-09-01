"""Securities Lending / Borrow Fee & Short Squeeze Risk Overlay.

Deterministic synthetic proxy for securities-lending borrow fees, hard-to-borrow
flags and days-to-cover changes. Elevated borrow costs coinciding with rising
narrative velocity and short-interest covering produce a soft squeeze-risk boost;
persistently high fees against cold narrative act as a caution / distribution flag.

Live feeds (IBorrowDesk, S3 Partners, FINRA securities-lending summaries, broker
hard-to-borrow lists) are left as an explicit future hook — no invented API keys
or endpoints. Current source is always labeled synthetic_proxy.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config

# Tickers that historically show higher short-squeeze sensitivity in synthetic ranges.
SQUEEZE_SENSITIVE = {
    "MU", "CRDO", "AMD", "GME", "AMC", "TSLA", "NVDA", "SMCI",
}


def detect_borrow_fee(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    bf_cfg = cfg.get("borrow_fee", {})
    if not bf_cfg.get("enabled", True):
        return {
            "bf_fee_pct": 0.0,
            "bf_dtc": 0.0,
            "bf_htb": False,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Borrow-fee / securities-lending module disabled",
            "source": "disabled",
        }

    elevated_fee = float(bf_cfg.get("elevated_fee_pct", 8.0))
    squeeze_fee = float(bf_cfg.get("squeeze_fee_pct", 25.0))
    covering_dtc = float(bf_cfg.get("covering_dtc_change", -1.5))
    expanding_dtc = float(bf_cfg.get("expanding_dtc_change", 1.8))
    min_conf = float(bf_cfg.get("min_confidence", 0.40))
    vel_hot = float(bf_cfg.get("narrative_hot", 1.5))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 53
    rng = random.Random(seed)

    if tkr in SQUEEZE_SENSITIVE:
        fee_pct = round(rng.uniform(1.5, 85.0), 2)
        dtc = round(rng.uniform(0.4, 12.0), 2)
    else:
        fee_pct = round(rng.uniform(0.3, 18.0), 2)
        dtc = round(rng.uniform(0.2, 6.5), 2)

    dtc_change = round(rng.uniform(-3.2, 3.8), 2)
    htb = fee_pct >= elevated_fee or dtc >= 4.0

    vel = 0.0
    si_change = 0.0
    if row:
        vel = float(row.get("predicted_velocity") or row.get("sentiment_velocity") or 0.0)
        si_change = float(row.get("si_change") or 0.0)

    boost = 0
    confidence = 0.48
    parts: list[str] = [f"Borrow fee {fee_pct:.1f}% (DTC {dtc:.1f}, Δ{dtc_change:+.1f})"]

    # High fee + hot narrative + covering short interest → squeeze risk soft boost
    if fee_pct >= squeeze_fee and vel >= vel_hot and (dtc_change <= covering_dtc or si_change <= -0.05):
        boost = 1
        confidence = min(0.88, 0.55 + 0.012 * min(fee_pct, 60))
        parts.append("elevated borrow + covering + rising narrative — squeeze-risk soft boost")
    elif fee_pct >= elevated_fee and vel >= vel_hot and dtc_change <= covering_dtc:
        boost = 1
        confidence = min(0.82, 0.52 + 0.01 * min(fee_pct, 40))
        parts.append("elevated borrow fee + covering pressure — soft squeeze confirmation")
    elif fee_pct >= squeeze_fee and vel < 0.6 and dtc_change >= expanding_dtc:
        boost = -1
        confidence = min(0.80, 0.50 + 0.008 * min(fee_pct, 50))
        parts.append("very high borrow + expanding DTC vs cold narrative — distribution / caution")
    elif htb and fee_pct >= elevated_fee:
        parts.append("hard-to-borrow / elevated fee — observation only")
    else:
        parts.append("no material securities-lending overlay")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "bf_fee_pct": fee_pct,
        "bf_dtc": dtc,
        "bf_htb": bool(htb),
        "bf_dtc_change": dtc_change,
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_borrow_fee_to_row(row: dict, cfg: dict | None = None) -> dict:
    mom = detect_borrow_fee(row.get("ticker", ""), row, cfg)
    row.update({
        "bf_fee_pct": mom["bf_fee_pct"],
        "bf_dtc": mom["bf_dtc"],
        "bf_htb": mom["bf_htb"],
        "bf_dtc_change": mom.get("bf_dtc_change", 0.0),
        "bf_boost": mom["signal_boost"],
        "bf_confidence": mom["confidence"],
        "bf_reason": mom["reason"],
        "bf_source": mom["source"],
    })
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 🔥 {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 🔥 {mom['reason']}"
    else:
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | Borrow: {mom['reason']}"
    return row
