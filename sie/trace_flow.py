"""TRACE Corporate-Bond Customer-Flow & Liquidity Shock Overlay.

Uses a deterministic offline proxy for issuer-level FINRA TRACE-style customer
flow and liquidity conditions. This is intentionally distinct from the existing
credit-spread/CDS overlay: it focuses on executed-flow direction and trading
quality rather than spread direction.

A soft +1 confirms constructive equity narrative when customer demand and
liquidity are healthy. A soft -1 cautions when customer selling and liquidity
stress diverge from hot equity narrative.

Live FINRA TRACE ingestion remains an explicit future hook. The current source
is always labeled synthetic_proxy unless disabled.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


TRACE_SENSITIVE = {
    "TSLA", "SMCI", "INTC", "AMD", "MU", "NVDA", "CRDO",
}


def detect_trace_flow(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    """Return a deterministic TRACE-style customer-flow/liquidity signal."""
    cfg = cfg or load_config()
    tf_cfg = cfg.get("trace_flow", {})
    if not tf_cfg.get("enabled", True):
        return {
            "trace_customer_flow": 0.0,
            "trace_liq_score": 0.0,
            "trace_dispersion": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "TRACE customer-flow / liquidity overlay disabled",
            "source": "disabled",
        }

    demand_hot = float(tf_cfg.get("customer_flow_hot", 0.35))
    selling_cold = float(tf_cfg.get("customer_flow_cold", -0.35))
    liq_good = float(tf_cfg.get("liquidity_good", 0.65))
    liq_stress = float(tf_cfg.get("liquidity_stress", 0.35))
    dispersion_warn = float(tf_cfg.get("dispersion_warn", 0.60))
    narrative_hot = float(tf_cfg.get("narrative_hot", 1.4))
    min_conf = float(tf_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 607
    rng = random.Random(seed)

    if tkr in TRACE_SENSITIVE:
        customer_flow = round(rng.uniform(-0.85, 0.90), 3)
        liquidity = round(rng.uniform(0.18, 0.92), 3)
        dispersion = round(rng.uniform(0.12, 0.90), 3)
    else:
        customer_flow = round(rng.uniform(-0.65, 0.72), 3)
        liquidity = round(rng.uniform(0.30, 0.94), 3)
        dispersion = round(rng.uniform(0.08, 0.72), 3)

    vel = 0.0
    credit_direction = "stable"
    if row:
        vel = float(
            row.get("predicted_velocity")
            or row.get("auth_filtered_velocity")
            or row.get("sentiment_velocity")
            or 0.0
        )
        credit_direction = str(row.get("cds_direction") or "stable")

    boost = 0
    confidence = 0.50
    parts = [
        f"TRACE flow {customer_flow:+.2f}",
        f"liquidity {liquidity:.2f}",
        f"dispersion {dispersion:.2f}",
        f"narrative vel {vel:.1f}",
    ]

    if (
        customer_flow >= demand_hot
        and liquidity >= liq_good
        and dispersion < dispersion_warn
        and vel >= narrative_hot
    ):
        boost = 1
        confidence = min(
            0.88,
            0.52
            + 0.18 * min(customer_flow, 1.0)
            + 0.12 * liquidity
            + (0.04 if credit_direction == "tightening" else 0.0),
        )
        parts.append("customer demand + healthy liquidity confirm constructive narrative")
    elif (
        customer_flow <= selling_cold
        and (liquidity <= liq_stress or dispersion >= dispersion_warn)
        and vel >= narrative_hot
    ):
        boost = -1
        confidence = min(
            0.88,
            0.52
            + 0.18 * min(abs(customer_flow), 1.0)
            + 0.12 * max(0.0, 1.0 - liquidity)
            + 0.08 * min(dispersion, 1.0),
        )
        parts.append("customer selling + liquidity stress diverge from hot equity narrative")
    elif customer_flow <= selling_cold and liquidity <= liq_stress:
        boost = -1
        confidence = min(0.82, 0.50 + 0.16 * min(abs(customer_flow), 1.0))
        parts.append("fixed-income demand/liquidity stress warrants caution")
    elif customer_flow >= demand_hot and liquidity >= liq_good:
        parts.append("constructive TRACE flow, but narrative confirmation is not hot enough")
    else:
        parts.append("TRACE flow/liquidity overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "trace_customer_flow": customer_flow,
        "trace_liq_score": liquidity,
        "trace_dispersion": dispersion,
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_trace_flow_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate TRACE customer flow and liquidity into an analysis row."""
    flow = detect_trace_flow(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "trace_customer_flow": flow["trace_customer_flow"],
            "trace_liq_score": flow["trace_liq_score"],
            "trace_dispersion": flow["trace_dispersion"],
            "trace_boost": flow["signal_boost"],
            "trace_confidence": flow["confidence"],
            "trace_reason": flow["reason"],
            "trace_source": flow["source"],
        }
    )

    boost = flow["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | TRACE: {flow['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | TRACE: {flow['reason']}"
    else:
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | TRACE: {flow['reason']}"
    return row
