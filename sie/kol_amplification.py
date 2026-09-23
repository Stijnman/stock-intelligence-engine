"""Key Opinion Leader (KOL) / Influencer Narrative Amplification Detector.

Identify high-follower / high-engagement authentic accounts driving
narrative velocity on X / Reddit / YouTube and score amplification
cascades. Soft boost on organic KOL-driven velocity confirmation;
caution on coordinated or low-authenticity amplification spikes.

Extends the authenticity + contagion layers.

Live follower-graph / engagement-graph feeds are an explicit future
hook. Current source is always labeled synthetic_proxy when live
data is unavailable.

Preferred columns: kol_score, kol_cascade, kol_amp_ratio, kol_auth,
kol_boost, kol_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


NARRATIVE_SENSITIVE = {
    "NVDA", "TSM", "MU", "AMD", "INTC", "AAPL", "MSFT", "GOOGL", "AMZN", "META",
    "CBRS", "CRDO", "TSLA", "PLTR", "SMCI",
}


def _clip(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_kol_amplification(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    kol_cfg = cfg.get("kol_amplification", {})
    if not kol_cfg.get("enabled", True):
        return {
            "kol_score": 0.0,
            "kol_cascade": 0.0,
            "kol_amp_ratio": 1.0,
            "kol_auth": 0.5,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "KOL amplification overlay disabled",
            "source": "disabled",
        }

    score_hot = float(kol_cfg.get("score_hot", 0.62))
    score_cold = float(kol_cfg.get("score_cold", 0.28))
    cascade_hot = float(kol_cfg.get("cascade_hot", 0.55))
    amp_hot = float(kol_cfg.get("amp_ratio_hot", 2.2))
    auth_floor = float(kol_cfg.get("auth_floor", 0.48))
    coord_warn = float(kol_cfg.get("coord_warn", 0.42))
    min_conf = float(kol_cfg.get("min_confidence", 0.40))
    vel_hot = float(kol_cfg.get("narrative_hot", 1.4))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 911
    rng = random.Random(seed)

    row = row or {}

    if tkr in NARRATIVE_SENSITIVE:
        base_reach = rng.uniform(0.35, 0.92)
        follower_log = rng.uniform(5.2, 7.1)
    else:
        base_reach = rng.uniform(0.12, 0.62)
        follower_log = rng.uniform(4.2, 6.4)

    auth = float(
        row.get("auth_score")
        or row.get("auth_filtered_velocity")
        and _clip(float(row.get("auth_score") or 0.55), 0.05, 0.98)
        or rng.uniform(0.28, 0.88)
    )
    auth = round(_clip(auth, 0.05, 0.98), 3)

    vel = float(
        row.get("predicted_velocity")
        or row.get("auth_filtered_velocity")
        or row.get("sentiment_velocity")
        or rng.uniform(0.2, 3.8)
    )
    sti_share = float(row.get("sti_intent_share") or rng.uniform(0.12, 0.62))
    contagion = float(row.get("ct_score") or row.get("ct_velocity_transfer") or rng.uniform(-0.2, 0.8))

    raw_heat = max(vel, 0.05)
    authentic_heat = max(raw_heat * auth, 0.02)
    amp_ratio = round(max(raw_heat / authentic_heat, 0.4), 3)

    coord = round(_clip((amp_ratio - 1.0) * 0.28 + (1.0 - auth) * 0.55 + max(contagion, 0) * 0.18), 3)

    cascade = round(
        _clip(
            0.34 * base_reach
            + 0.22 * _clip(follower_log / 7.2)
            + 0.18 * _clip(vel / 4.0)
            + 0.16 * sti_share
            + 0.10 * _clip(contagion, 0.0, 1.0)
        ),
        3,
    )

    kol_score = round(
        _clip(
            0.38 * cascade
            + 0.32 * auth
            + 0.18 * _clip(vel / vel_hot if vel_hot else vel / 1.4)
            - 0.28 * coord
        ),
        3,
    )

    boost = 0
    confidence = 0.50
    parts = [
        f"KOL score {kol_score:.2f} (cascade {cascade:.2f}, amp {amp_ratio:.2f}x)",
        f"auth {auth:.2f} coord {coord:.2f} vel {vel:.1f}",
    ]

    organic = (
        kol_score >= score_hot
        and cascade >= cascade_hot
        and auth >= auth_floor
        and coord < coord_warn
        and vel >= vel_hot * 0.7
    )
    coordinated_spike = (
        (kol_score <= score_cold or auth < auth_floor)
        and (amp_ratio >= amp_hot or coord >= coord_warn)
        and vel >= vel_hot * 0.6
    )

    if organic:
        boost = 1
        confidence = min(
            0.93,
            0.50 + 0.28 * kol_score + 0.18 * cascade + 0.16 * auth,
        )
        parts.append("organic KOL-driven velocity confirmation — soft boost")
    elif coordinated_spike:
        boost = -1
        confidence = min(
            0.90,
            0.48 + 0.24 * coord + 0.18 * (1.0 - auth) + 0.12 * min(amp_ratio / 4.0, 1.0),
        )
        parts.append("coordinated / low-authenticity amplification spike — caution")
    else:
        parts.append("KOL amplification overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "kol_score": kol_score,
        "kol_cascade": cascade,
        "kol_amp_ratio": amp_ratio,
        "kol_auth": auth,
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_kol_amplification_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate KOL / influencer amplification into a row."""
    mom = detect_kol_amplification(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "kol_score": mom["kol_score"],
            "kol_cascade": mom["kol_cascade"],
            "kol_amp_ratio": mom["kol_amp_ratio"],
            "kol_auth": mom["kol_auth"],
            "kol_boost": mom["signal_boost"],
            "kol_confidence": mom["confidence"],
            "kol_reason": mom["reason"],
            "kol_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 📣 {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 📣 {mom['reason']}"
    else:
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | KOL: {mom['reason']}"
    return row
