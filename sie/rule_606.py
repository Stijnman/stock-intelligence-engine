"""Rule 606 Retail Options Routing & Execution-Quality Overlay.

Scores how concentrated non-directed retail options contracts are at the top
wholesaler (Rule 606(a) venue share) and how good the fills look (price
improvement and effective-versus-quoted spread). Distinct from unusual-options
sweep detection and from the retail brokerage order-flow imbalance overlay.

Live SEC Rule 606 XML/PDF parsers are an explicit future hook. Current source
is always labeled synthetic_proxy when a signed routing report is unavailable.

Preferred columns: r606_concentration, r606_exec_quality, r606_boost, r606_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


# Liquid names where wholesaler competition usually keeps execution quality up.
R606_COMPETITIVE = {
    "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "JPM", "UNH", "AVGO", "COST",
}
# Names that routinely show concentrated retail options routing and weak fills.
R606_CONCENTRATED = {
    "AMC", "GME", "CVNA", "RIVN", "LCID", "MARA", "BBBY", "MULN", "FFIE",
}


def _clip(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_rule_606(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    r_cfg = cfg.get("rule_606", {})
    if not r_cfg.get("enabled", True):
        return {
            "r606_concentration": 0.0,
            "r606_exec_quality": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Rule 606 overlay disabled",
            "source": "disabled",
        }

    conc_hot = float(r_cfg.get("concentration_hot", 0.72))
    conc_ok = float(r_cfg.get("concentration_ok", 0.48))
    exec_hot = float(r_cfg.get("exec_quality_hot", 0.64))
    exec_cold = float(r_cfg.get("exec_quality_cold", 0.32))
    narrative_hot = float(r_cfg.get("narrative_hot", 1.4))
    min_conf = float(r_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 2606
    rng = random.Random(seed)
    row = row or {}

    if tkr in R606_COMPETITIVE:
        concentration = rng.uniform(0.28, 0.46)
        exec_quality = rng.uniform(0.66, 0.92)
    elif tkr in R606_CONCENTRATED:
        concentration = rng.uniform(0.74, 0.96)
        exec_quality = rng.uniform(0.08, 0.30)
    else:
        concentration = rng.uniform(0.40, 0.70)
        exec_quality = rng.uniform(0.34, 0.68)

    narr = float(
        row.get("predicted_velocity")
        or row.get("sentiment_velocity")
        or 0.0
    )
    parts = [
        f"top_venue_share={concentration:.2f}",
        f"exec_quality={exec_quality:.2f}",
    ]
    confidence = _clip(0.38 + 0.28 * exec_quality + 0.16 * (1.0 - concentration))
    boost = 0

    clean_confirm = (
        concentration <= conc_ok
        and exec_quality >= exec_hot
        and narr >= narrative_hot * 0.45
    )
    concentrated_poor = (
        concentration >= conc_hot
        and exec_quality <= exec_cold
        and narr >= narrative_hot * 0.35
    )

    if clean_confirm:
        boost = 1
        confidence = min(
            0.93,
            0.46
            + 0.22 * exec_quality
            + 0.14 * (1.0 - concentration)
            + 0.06 * min(narr / 4.0, 1.0),
        )
        parts.append("diversified Rule 606 routing with real price improvement into a confirming narrative — soft boost")
    elif concentrated_poor:
        boost = -1
        confidence = min(
            0.91,
            0.44 + 0.24 * concentration + 0.18 * (1.0 - exec_quality),
        )
        parts.append("concentrated wholesaler routing and weak effective spreads into narrative heat — caution")
    else:
        parts.append("Rule 606 routing overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "r606_concentration": round(float(concentration), 4),
        "r606_exec_quality": round(float(exec_quality), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_rule_606_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate retail options routing concentration and execution quality into a row."""
    mom = detect_rule_606(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "r606_concentration": mom["r606_concentration"],
            "r606_exec_quality": mom["r606_exec_quality"],
            "r606_boost": mom["signal_boost"],
            "r606_confidence": mom["confidence"],
            "r606_reason": mom["reason"],
            "r606_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | r606 {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | r606 {mom['reason']}"
    return row
