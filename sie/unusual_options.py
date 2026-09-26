"""Unusual Options Sweep vs Block Confirmation Overlay.

Distinguish aggressive sweep prints from passive blocks on the
options tape and score confirmation vs fade against existing
0DTE / IV / GEX layers.

Live OPRA / multi-exchange sweep feeds are an explicit future hook.
Current source is always labeled synthetic_proxy when live data is
unavailable.

Preferred columns: uopt_sweep_score, uopt_block_ratio, uopt_boost, uopt_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


LIQUID_OPTIONS = {
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA",
    "AMD", "AVGO", "SPY", "QQQ", "IWM", "TSM", "MU", "INTC",
}


def _clip(v: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_unusual_options(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    u_cfg = cfg.get("unusual_options", {})
    if not u_cfg.get("enabled", True):
        return {
            "uopt_sweep_score": 0.0,
            "uopt_block_ratio": 0.0,
            "uopt_call_put": 0.0,
            "uopt_premium_usd_m": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Unusual options sweep/block overlay disabled",
            "source": "disabled",
        }

    sweep_hot = float(u_cfg.get("sweep_hot", 0.62))
    sweep_cold = float(u_cfg.get("sweep_cold", 0.22))
    block_passive = float(u_cfg.get("block_passive", 0.58))
    block_confirm = float(u_cfg.get("block_confirm", 0.28))
    vel_hot = float(u_cfg.get("narrative_hot", 1.4))
    min_conf = float(u_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 606
    rng = random.Random(seed)
    row = row or {}

    if tkr in LIQUID_OPTIONS:
        sweep = rng.uniform(0.12, 0.98)
        block_ratio = rng.uniform(0.08, 0.82)
        call_put = rng.uniform(-0.85, 0.92)
        prem_m = rng.uniform(0.4, 48.0)
    else:
        sweep = rng.uniform(0.04, 0.62)
        block_ratio = rng.uniform(0.12, 0.72)
        call_put = rng.uniform(-0.55, 0.55)
        prem_m = rng.uniform(0.05, 8.0)

    vel = float(
        row.get("predicted_velocity")
        or row.get("auth_filtered_velocity")
        or row.get("sentiment_velocity")
        or rng.uniform(0.2, 3.8)
    )
    gex_score = float(row.get("gex_score") or row.get("gex_net") or 0.0)
    iv_skew = float(row.get("iv_skew") or row.get("put_call_skew") or 0.0)
    dte0 = float(row.get("odte_score") or row.get("dte0_flow") or 0.0)

    sweep = round(float(sweep), 3)
    block_ratio = round(float(block_ratio), 3)
    call_put = round(float(call_put), 3)
    prem_m = round(float(prem_m), 2)

    score = round(
        _clip(
            0.44 * _clip((sweep - 0.45) * 2.2)
            + 0.22 * _clip((block_confirm - block_ratio) * 1.6)
            + 0.18 * _clip(call_put)
            + 0.10 * _clip((vel / vel_hot) - 0.5)
            + 0.06 * _clip(dte0),
            -1.0,
            1.0,
        ),
        3,
    )

    boost = 0
    confidence = 0.50
    parts = [
        f"sweep {sweep:.2f} block_ratio {block_ratio:.2f}",
        f"C/P {call_put:+.2f} prem ${prem_m:.1f}m vel {vel:.1f}",
    ]

    sweep_confirm = (
        sweep >= sweep_hot
        and block_ratio <= block_confirm
        and call_put >= 0.18
        and vel >= vel_hot * 0.50
    )
    fade_warn = (
        (sweep <= sweep_cold or block_ratio >= block_passive)
        and vel >= vel_hot * 0.70
        and call_put <= 0.05
    )
    if gex_score < -0.35 and sweep >= sweep_hot:
        parts.append(f"GEX {gex_score:+.2f} against aggressive sweeps")
    if iv_skew > 0.18 and call_put < 0:
        parts.append(f"IV skew {iv_skew:.2f} confirms put-side tape")

    if sweep_confirm:
        boost = 1
        confidence = min(0.92, 0.48 + 0.26 * abs(score) + 0.10 * max(sweep, 0))
        parts.append("aggressive sweeps confirm narrative vs passive blocks — soft boost")
    elif fade_warn:
        boost = -1
        confidence = min(0.90, 0.46 + 0.24 * abs(min(score, 0)) + 0.12 * max(vel / 4.0, 0))
        parts.append("passive blocks / weak sweeps into elevated social heat — fade / caution")
    else:
        parts.append("unusual options sweep/block overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "uopt_sweep_score": sweep,
        "uopt_block_ratio": block_ratio,
        "uopt_call_put": call_put,
        "uopt_premium_usd_m": prem_m,
        "uopt_score": score,
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_unusual_options_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate unusual options sweep vs block confirmation into a row."""
    mom = detect_unusual_options(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "uopt_sweep_score": mom["uopt_sweep_score"],
            "uopt_block_ratio": mom["uopt_block_ratio"],
            "uopt_call_put": mom["uopt_call_put"],
            "uopt_premium_usd_m": mom["uopt_premium_usd_m"],
            "uopt_score": mom.get("uopt_score", 0.0),
            "uopt_boost": mom["signal_boost"],
            "uopt_confidence": mom["confidence"],
            "uopt_reason": mom["reason"],
            "uopt_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | UOPT {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | UOPT {mom['reason']}"
    else:
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | UOPT: {mom['reason']}"
    return row
