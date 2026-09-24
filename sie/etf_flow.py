"""ETF Creation / Redemption & Authorized-Participant Flow Overlay.

Track net creation/redemption and premium/discount vs NAV for
thematically relevant ETFs as a mechanical demand pulse into
underlying names. Soft boost on multi-session creation streaks
confirming narrative; caution on redemption streaks or persistent
discount while social heat is elevated.

Live AP / creation-unit / iNAV feeds are an explicit future hook.
Current source is always labeled synthetic_proxy when live data
is unavailable.

Preferred columns: etf_flow_score, etf_prem_disc, etf_boost, etf_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


THEME_SENSITIVE = {
    "NVDA", "TSM", "MU", "AMD", "INTC", "AAPL", "MSFT", "GOOGL", "AMZN", "META",
    "CBRS", "CRDO", "TSLA", "PLTR", "SMCI", "AVGO", "ASML",
}

THEME_ETFS = ("SMH", "SOXX", "BOTZ", "AIQ", "QQQ", "XLK")


def _clip(v: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_etf_flow(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    etf_cfg = cfg.get("etf_flow", {})
    if not etf_cfg.get("enabled", True):
        return {
            "etf_flow_score": 0.0,
            "etf_prem_disc": 0.0,
            "etf_create_streak": 0,
            "etf_theme": THEME_ETFS[0],
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "ETF creation/redemption overlay disabled",
            "source": "disabled",
        }

    create_hot = float(etf_cfg.get("create_hot", 0.45))
    redeem_hot = float(etf_cfg.get("redeem_hot", -0.40))
    prem_hot = float(etf_cfg.get("premium_hot_bps", 18.0))
    disc_hot = float(etf_cfg.get("discount_hot_bps", -22.0))
    streak_hot = int(etf_cfg.get("streak_hot", 3))
    vel_hot = float(etf_cfg.get("narrative_hot", 1.4))
    min_conf = float(etf_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 417
    rng = random.Random(seed)
    row = row or {}

    theme_etf = THEME_ETFS[seed % len(THEME_ETFS)]
    if tkr in THEME_SENSITIVE:
        net_create = rng.uniform(-0.35, 0.92)
        prem_bps = rng.uniform(-35.0, 42.0)
        streak = int(rng.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4, 5]))
    else:
        net_create = rng.uniform(-0.55, 0.55)
        prem_bps = rng.uniform(-28.0, 22.0)
        streak = int(rng.choice([-3, -2, -1, 0, 1, 2, 3]))

    vel = float(
        row.get("predicted_velocity")
        or row.get("auth_filtered_velocity")
        or row.get("sentiment_velocity")
        or rng.uniform(0.2, 3.8)
    )
    auth = float(row.get("auth_score") or rng.uniform(0.28, 0.88))

    flow_score = round(
        _clip(
            0.48 * net_create
            + 0.22 * _clip(prem_bps / 40.0)
            + 0.18 * _clip(streak / 5.0)
            + 0.12 * _clip((vel / vel_hot) - 0.5, -1.0, 1.0),
            -1.0,
            1.0,
        ),
        3,
    )
    prem_disc = round(prem_bps, 2)

    boost = 0
    confidence = 0.50
    parts = [
        f"ETF {theme_etf} flow {flow_score:+.2f} (prem/disc {prem_disc:+.1f} bps)",
        f"create streak {streak:+d}d vel {vel:.1f}",
    ]

    creation_confirm = (
        flow_score >= create_hot
        and streak >= streak_hot
        and prem_bps >= -5.0
        and vel >= vel_hot * 0.65
    )
    redemption_warn = (
        (flow_score <= redeem_hot or streak <= -streak_hot or prem_bps <= disc_hot)
        and vel >= vel_hot * 0.7
    )

    if creation_confirm:
        boost = 1
        confidence = min(0.92, 0.48 + 0.28 * abs(flow_score) + 0.12 * auth)
        parts.append("multi-session creation streak confirming narrative — soft boost")
    elif redemption_warn:
        boost = -1
        confidence = min(0.90, 0.46 + 0.24 * abs(min(flow_score, 0)) + 0.14 * max(vel / 4.0, 0))
        parts.append("redemption streak or persistent NAV discount into elevated social heat — caution")
    else:
        parts.append("ETF AP flow overlay neutral")

    if prem_bps >= prem_hot and boost == 0 and vel >= vel_hot * 0.8:
        parts.append("premium vs NAV elevated")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "etf_flow_score": flow_score,
        "etf_prem_disc": prem_disc,
        "etf_create_streak": streak,
        "etf_theme": theme_etf,
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_etf_flow_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate ETF creation/redemption flow into a row."""
    mom = detect_etf_flow(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "etf_flow_score": mom["etf_flow_score"],
            "etf_prem_disc": mom["etf_prem_disc"],
            "etf_create_streak": mom["etf_create_streak"],
            "etf_theme": mom["etf_theme"],
            "etf_boost": mom["signal_boost"],
            "etf_confidence": mom["confidence"],
            "etf_reason": mom["reason"],
            "etf_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 📦 {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 📦 {mom['reason']}"
    else:
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | ETF: {mom['reason']}"
    return row
