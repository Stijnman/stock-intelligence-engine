"""TRACE Corporate-Bond Customer-Flow & Liquidity Shock Overlay.

Scores FINRA TRACE customer buy/sell imbalance and secondary-market
liquidity as a credit-tape layer, distinct from CDS spread and ETF flow.

Live TRACE prints are an explicit future hook. Current source is always
labeled synthetic_proxy when the tape is unavailable.

Preferred columns: trace_customer_flow, trace_liq_score, trace_boost, trace_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


# Names with active IG TRACE prints and deep customer two-way flow.
TRACE_LIQUID = {
    "AAPL", "MSFT", "AMZN", "GOOGL", "META", "NVDA", "JPM", "BAC",
    "XOM", "CVX", "T", "VZ", "WMT", "KO", "PEP", "UNH",
}
# Names where TRACE prints historically thin out into credit stress.
TRACE_STRESSED = {
    "AMC", "CVNA", "RIVN", "LCID", "WBD", "PARA", "BA", "F",
}


def _clip(v: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_trace_flow(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    tr_cfg = cfg.get("trace_flow", {})
    if not tr_cfg.get("enabled", True):
        return {
            "trace_customer_flow": 0.0,
            "trace_liq_score": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "TRACE customer-flow overlay disabled",
            "source": "disabled",
        }

    flow_hot = float(tr_cfg.get("flow_hot", 0.35))
    flow_cold = float(tr_cfg.get("flow_cold", -0.35))
    liq_hot = float(tr_cfg.get("liq_hot", 0.55))
    liq_cold = float(tr_cfg.get("liq_cold", 0.28))
    narrative_hot = float(tr_cfg.get("narrative_hot", 1.4))
    min_conf = float(tr_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 6606
    rng = random.Random(seed)
    row = row or {}

    if tkr in TRACE_STRESSED:
        customer_flow = rng.uniform(-0.82, -0.08)
        liq_score = rng.uniform(0.08, 0.42)
    elif tkr in TRACE_LIQUID:
        customer_flow = rng.uniform(-0.15, 0.72)
        liq_score = rng.uniform(0.48, 0.94)
    else:
        customer_flow = rng.uniform(-0.40, 0.40)
        liq_score = rng.uniform(0.22, 0.70)

    narr = float(
        row.get("predicted_velocity")
        or row.get("sentiment_velocity")
        or rng.uniform(0.3, 3.4)
    )
    score = _clip(0.58 * customer_flow + 0.42 * (liq_score - 0.45) / 0.45)

    parts = [
        f"cust_flow={customer_flow:+.2f}",
        f"liq={liq_score:.2f}",
    ]
    boost = 0
    confidence = 0.38 + 0.18 * liq_score

    bid = customer_flow >= flow_hot and liq_score >= liq_hot and narr >= narrative_hot * 0.45
    shock = customer_flow <= flow_cold and liq_score <= liq_cold

    if bid:
        boost = 1
        confidence = min(0.90, 0.46 + 0.22 * customer_flow + 0.14 * liq_score + 0.08 * min(narr / 4.0, 1.0))
        parts.append("TRACE customer bid into liquid prints — soft boost")
    elif shock:
        boost = -1
        confidence = min(0.92, 0.50 + 0.22 * abs(customer_flow) + 0.16 * (1.0 - liq_score))
        parts.append("TRACE customer selling into a liquidity shock — credit-tape caution")
    else:
        parts.append("TRACE customer-flow / liquidity overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "trace_customer_flow": round(float(customer_flow), 4),
        "trace_liq_score": round(float(liq_score), 4),
        "trace_score": round(float(score), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_trace_flow_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate TRACE customer-flow and liquidity into a row."""
    mom = detect_trace_flow(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "trace_customer_flow": mom["trace_customer_flow"],
            "trace_liq_score": mom["trace_liq_score"],
            "trace_score": mom.get("trace_score", 0.0),
            "trace_boost": mom["signal_boost"],
            "trace_confidence": mom["confidence"],
            "trace_reason": mom["reason"],
            "trace_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | trace {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | trace {mom['reason']}"
    return row
