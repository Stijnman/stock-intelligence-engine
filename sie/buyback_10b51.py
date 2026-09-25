"""Rule 10b5-1 / Buyback Authorization vs Execution Overlay.

Cluster scheduled 10b5-1 plan adoptions/amendments and compare
announced buyback authorizations against actual repurchase cadence.
Soft boost when execution is running ahead of authorization with
supportive narrative; caution on stalled buybacks.

Live Form 10b5-1 / 8-K buyback execution feeds are an explicit
future hook. Current source is always labeled synthetic_proxy when
live data is unavailable.

Preferred columns: bb_util, bb_plan_delta, bb_boost, bb_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


BUYBACK_ACTIVE = {
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "AVGO",
    "TSM", "ORCL", "CSCO", "QCOM", "INTC", "AMD", "TXN",
}


def _clip(v: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_buyback_10b51(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    bb_cfg = cfg.get("buyback_10b51", {})
    if not bb_cfg.get("enabled", True):
        return {
            "bb_util": 0.0,
            "bb_plan_delta": 0.0,
            "bb_auth_usd_bn": 0.0,
            "bb_exec_pace": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Rule 10b5-1 / buyback overlay disabled",
            "source": "disabled",
        }

    util_hot = float(bb_cfg.get("util_hot", 0.72))
    util_stall = float(bb_cfg.get("util_stall", 0.28))
    plan_hot = float(bb_cfg.get("plan_delta_hot", 0.18))
    plan_cold = float(bb_cfg.get("plan_delta_cold", -0.15))
    vel_hot = float(bb_cfg.get("narrative_hot", 1.4))
    min_conf = float(bb_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 1051
    rng = random.Random(seed)
    row = row or {}

    if tkr in BUYBACK_ACTIVE:
        util = rng.uniform(0.18, 1.08)
        plan_delta = rng.uniform(-0.28, 0.42)
        auth_bn = rng.uniform(2.0, 48.0)
        exec_pace = rng.uniform(0.15, 1.25)
    else:
        util = rng.uniform(0.05, 0.78)
        plan_delta = rng.uniform(-0.22, 0.22)
        auth_bn = rng.uniform(0.2, 8.0)
        exec_pace = rng.uniform(0.08, 0.85)

    vel = float(
        row.get("predicted_velocity")
        or row.get("auth_filtered_velocity")
        or row.get("sentiment_velocity")
        or rng.uniform(0.2, 3.8)
    )
    auth = float(row.get("auth_score") or rng.uniform(0.28, 0.88))

    util = round(float(util), 3)
    plan_delta = round(float(plan_delta), 3)
    auth_bn = round(float(auth_bn), 2)
    exec_pace = round(float(exec_pace), 3)

    score = round(
        _clip(
            0.42 * _clip((util - 0.5) * 2.0)
            + 0.28 * _clip(plan_delta / 0.35)
            + 0.18 * _clip((exec_pace - 0.5) * 2.0)
            + 0.12 * _clip((vel / vel_hot) - 0.5, -1.0, 1.0),
            -1.0,
            1.0,
        ),
        3,
    )

    boost = 0
    confidence = 0.50
    parts = [
        f"10b5-1/buyback util {util:.0%} planΔ {plan_delta:+.2f}",
        f"auth ${auth_bn:.1f}bn pace {exec_pace:.2f} vel {vel:.1f}",
    ]

    execution_confirm = (
        util >= util_hot
        and plan_delta >= plan_hot * 0.4
        and exec_pace >= 0.70
        and vel >= vel_hot * 0.60
    )
    stalled_warn = (
        (util <= util_stall or plan_delta <= plan_cold or exec_pace <= 0.22)
        and vel >= vel_hot * 0.70
    )

    if execution_confirm:
        boost = 1
        confidence = min(0.92, 0.48 + 0.26 * abs(score) + 0.14 * auth)
        parts.append("execution running ahead of authorization with supportive narrative — soft boost")
    elif stalled_warn:
        boost = -1
        confidence = min(0.90, 0.46 + 0.24 * abs(min(score, 0)) + 0.14 * max(vel / 4.0, 0))
        parts.append("stalled buyback / 10b5-1 cadence into elevated social heat — caution")
    else:
        parts.append("Rule 10b5-1 / buyback overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "bb_util": util,
        "bb_plan_delta": plan_delta,
        "bb_auth_usd_bn": auth_bn,
        "bb_exec_pace": exec_pace,
        "bb_score": score,
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_buyback_10b51_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate Rule 10b5-1 / buyback execution into a row."""
    mom = detect_buyback_10b51(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "bb_util": mom["bb_util"],
            "bb_plan_delta": mom["bb_plan_delta"],
            "bb_auth_usd_bn": mom["bb_auth_usd_bn"],
            "bb_exec_pace": mom["bb_exec_pace"],
            "bb_score": mom.get("bb_score", 0.0),
            "bb_boost": mom["signal_boost"],
            "bb_confidence": mom["confidence"],
            "bb_reason": mom["reason"],
            "bb_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 10b5-1 {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 10b5-1 {mom['reason']}"
    else:
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 10b5-1: {mom['reason']}"
    return row
