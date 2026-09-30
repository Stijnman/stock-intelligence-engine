"""Job-Posting Skill-Mix & Posted-Compensation Inflation Overlay.

Scores the share of senior / scarce-skill postings and the year-over-year
delta in posted compensation as a labor-demand confirmation layer next to
the existing hiring-volume overlay.

Live Lightcast / Revelio / Indeed salary APIs are an explicit future hook.
Current source is always labeled synthetic_proxy when live data is
unavailable.

Preferred columns: hmix_senior_share, hmix_comp_delta, hmix_boost, hmix_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


TALENT_WAR_UNIVERSE = {
    "NVDA", "AVGO", "AMD", "TSM", "ASML", "AMZN", "MSFT", "GOOGL",
    "META", "AAPL", "TSLA", "PLTR", "SNOW", "CRWD", "PANW", "NOW",
    "DDOG", "NET", "SMCI", "ARM",
}


def _clip(v: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_hiring_skill_mix(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    hm_cfg = cfg.get("hiring_skill_mix", {})
    if not hm_cfg.get("enabled", True):
        return {
            "hmix_senior_share": 0.0,
            "hmix_comp_delta": 0.0,
            "hmix_scarce_share": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Hiring skill-mix overlay disabled",
            "source": "disabled",
        }

    senior_hot = float(hm_cfg.get("senior_hot", 0.38))
    senior_cold = float(hm_cfg.get("senior_cold", 0.14))
    comp_hot = float(hm_cfg.get("comp_hot", 0.08))
    comp_cold = float(hm_cfg.get("comp_cold", -0.04))
    vel_hot = float(hm_cfg.get("narrative_hot", 1.4))
    min_conf = float(hm_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 7711
    rng = random.Random(seed)
    row = row or {}

    if tkr in TALENT_WAR_UNIVERSE:
        senior_share = rng.uniform(0.18, 0.62)
        comp_delta = rng.uniform(-0.06, 0.22)
        scarce_share = rng.uniform(0.12, 0.48)
    else:
        senior_share = rng.uniform(0.08, 0.36)
        comp_delta = rng.uniform(-0.08, 0.10)
        scarce_share = rng.uniform(0.04, 0.22)

    vel = float(
        row.get("predicted_velocity")
        or row.get("auth_filtered_velocity")
        or row.get("sentiment_velocity")
        or rng.uniform(0.2, 3.8)
    )
    auth = float(row.get("auth_score") or 0.55)
    hire_mom = float(row.get("hiring_momentum") or row.get("hire_score") or 0.0)

    score = _clip(
        0.45 * (senior_share - 0.25)
        + 0.35 * comp_delta
        + 0.12 * (scarce_share - 0.15)
        + 0.08 * max(hire_mom, 0.0)
    )

    parts = [
        f"hmix senior_share={senior_share:.2f}",
        f"comp_delta={comp_delta:+.2f}",
        f"scarce_share={scarce_share:.2f}",
    ]
    boost = 0
    confidence = 0.42 + 0.16 * auth

    mix_confirm = (
        senior_share >= senior_hot
        and comp_delta >= comp_hot
        and vel >= vel_hot * 0.50
    )
    mix_warn = (
        senior_share <= senior_cold
        and comp_delta <= comp_cold
        and vel >= vel_hot * 0.60
    )

    if mix_confirm:
        boost = 1
        confidence = min(0.92, 0.48 + 0.26 * abs(score) + 0.14 * auth)
        parts.append(
            "senior/scarce skill mix + posted-comp inflation confirming demand — soft boost"
        )
    elif mix_warn:
        boost = -1
        confidence = min(0.90, 0.46 + 0.24 * abs(min(score, 0)) + 0.14 * max(vel / 4.0, 0))
        parts.append(
            "senior-share collapse + posted-comp deflation — hiring freeze caution"
        )
    else:
        parts.append("hiring skill-mix overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "hmix_senior_share": round(float(senior_share), 4),
        "hmix_comp_delta": round(float(comp_delta), 4),
        "hmix_scarce_share": round(float(scarce_share), 4),
        "hmix_score": round(float(score), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_hiring_skill_mix_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate job-posting skill-mix & posted-comp inflation into a row."""
    mom = detect_hiring_skill_mix(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "hmix_senior_share": mom["hmix_senior_share"],
            "hmix_comp_delta": mom["hmix_comp_delta"],
            "hmix_scarce_share": mom.get("hmix_scarce_share", 0.0),
            "hmix_score": mom.get("hmix_score", 0.0),
            "hmix_boost": mom["signal_boost"],
            "hmix_confidence": mom["confidence"],
            "hmix_reason": mom["reason"],
            "hmix_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | hiring-skill-mix {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | hiring-skill-mix {mom['reason']}"
    else:
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | hiring-skill-mix: {mom['reason']}"
    return row
