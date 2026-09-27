"""Employee Outlook / Glassdoor Business Sentiment Overlay.

Scores employer-review outlook, CEO approval, and complaint-vs-praise
mix as an operational-culture pulse orthogonal to hiring-volume and
digital-footprint layers.

Live Glassdoor / Indeed / Levels.fyi feeds are an explicit future hook.
Current source is always labeled synthetic_proxy when live data is
unavailable.

Preferred columns: eo_outlook, eo_ceo, eo_boost, eo_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


HIGH_REVIEW_UNIVERSE = {
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "AVGO",
    "TSM", "ORCL", "CSCO", "QCOM", "INTC", "AMD", "TXN",
    "NFLX", "CRM", "NOW", "SNOW", "PLTR",
}


def _clip(v: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_employee_outlook(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    eo_cfg = cfg.get("employee_outlook", {})
    if not eo_cfg.get("enabled", True):
        return {
            "eo_outlook": 0.0,
            "eo_ceo": 0.0,
            "eo_review_velocity": 0.0,
            "eo_complaint_share": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Employee outlook / Glassdoor overlay disabled",
            "source": "disabled",
        }

    outlook_hot = float(eo_cfg.get("outlook_hot", 0.62))
    outlook_cold = float(eo_cfg.get("outlook_cold", 0.32))
    ceo_hot = float(eo_cfg.get("ceo_hot", 0.68))
    ceo_cold = float(eo_cfg.get("ceo_cold", 0.38))
    vel_hot = float(eo_cfg.get("narrative_hot", 1.4))
    min_conf = float(eo_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 3141
    rng = random.Random(seed)
    row = row or {}

    if tkr in HIGH_REVIEW_UNIVERSE:
        outlook = rng.uniform(0.28, 0.92)
        ceo = rng.uniform(0.30, 0.94)
        review_vel = rng.uniform(0.15, 1.35)
        complaint = rng.uniform(0.08, 0.48)
    else:
        outlook = rng.uniform(0.18, 0.78)
        ceo = rng.uniform(0.20, 0.80)
        review_vel = rng.uniform(0.05, 0.85)
        complaint = rng.uniform(0.12, 0.62)

    vel = float(
        row.get("predicted_velocity")
        or row.get("auth_filtered_velocity")
        or row.get("sentiment_velocity")
        or rng.uniform(0.2, 3.8)
    )
    auth = float(row.get("auth_score") or rng.uniform(0.28, 0.88))

    outlook = round(float(outlook), 3)
    ceo = round(float(ceo), 3)
    review_vel = round(float(review_vel), 3)
    complaint = round(float(complaint), 3)

    score = round(
        _clip(
            0.40 * _clip((outlook - 0.5) * 2.0)
            + 0.28 * _clip((ceo - 0.5) * 2.0)
            + 0.18 * _clip((review_vel - 0.5) * 2.0)
            - 0.14 * _clip((complaint - 0.30) / 0.30),
            -1.0,
            1.0,
        ),
        3,
    )

    boost = 0
    confidence = 0.50
    parts = [
        f"employee outlook {outlook:.0%} CEO {ceo:.0%}",
        f"review vel {review_vel:.2f} complaint {complaint:.0%} social vel {vel:.1f}",
    ]

    culture_confirm = (
        outlook >= outlook_hot
        and ceo >= ceo_hot * 0.85
        and complaint <= 0.28
        and vel >= vel_hot * 0.55
    )
    culture_warn = (
        (outlook <= outlook_cold or ceo <= ceo_cold or complaint >= 0.42)
        and vel >= vel_hot * 0.70
    )

    if culture_confirm:
        boost = 1
        confidence = min(0.92, 0.48 + 0.26 * abs(score) + 0.14 * auth)
        parts.append("rising employee outlook / CEO approval confirming narrative — soft boost")
    elif culture_warn:
        boost = -1
        confidence = min(0.90, 0.46 + 0.24 * abs(min(score, 0)) + 0.14 * max(vel / 4.0, 0))
        parts.append("deteriorating Glassdoor outlook into elevated social heat — caution")
    else:
        parts.append("employee outlook / Glassdoor overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "eo_outlook": outlook,
        "eo_ceo": ceo,
        "eo_review_velocity": review_vel,
        "eo_complaint_share": complaint,
        "eo_score": score,
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_employee_outlook_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate employee outlook / Glassdoor sentiment into a row."""
    mom = detect_employee_outlook(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "eo_outlook": mom["eo_outlook"],
            "eo_ceo": mom["eo_ceo"],
            "eo_review_velocity": mom["eo_review_velocity"],
            "eo_complaint_share": mom["eo_complaint_share"],
            "eo_score": mom.get("eo_score", 0.0),
            "eo_boost": mom["signal_boost"],
            "eo_confidence": mom["confidence"],
            "eo_reason": mom["reason"],
            "eo_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | employee-outlook {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | employee-outlook {mom['reason']}"
    else:
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | employee-outlook: {mom['reason']}"
    return row
