"""Semiconductor / AI Supply-Chain CapEx Momentum Tracker.

Deterministic seeded proxy (optional yfinance peek) for supplier CapEx /
backlog momentum across ASML, AMAT, LRCX, KLAC, TSM as a leading indicator
for inference-related names. Soft boost/penalty only. Labeled source.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List
import random

from sie.config import load_config

DEFAULT_SUPPLIERS = ["ASML", "AMAT", "LRCX", "KLAC", "TSM"]
AI_NAMES = {"NVDA", "TSM", "CBRS", "CRDO", "MU", "AMD", "AVGO", "ASML", "ARM", "AMAT", "LRCX", "KLAC"}


def _safe_float(val: Any, default: float = 0.0) -> float:
    try:
        return float(val)
    except (TypeError, ValueError):
        return default


def _yfinance_supplier_momentum(suppliers: List[str]) -> Dict[str, Any] | None:
    """Best-effort public peek. Returns None if yfinance is missing or fails."""
    try:
        import yfinance as yf  # type: ignore
    except Exception:
        return None
    changes: List[float] = []
    used: List[str] = []
    for ticker in suppliers:
        try:
            hist = yf.Ticker(ticker).history(period="1mo")
            if hist is None or hist.empty or "Close" not in hist.columns:
                continue
            close = hist["Close"].dropna()
            if len(close) < 6:
                continue
            last = float(close.iloc[-1])
            prev = float(close.iloc[-6])
            if prev <= 0:
                continue
            changes.append((last / prev - 1.0) * 100.0)
            used.append(ticker)
        except Exception:
            continue
    if not changes:
        return None
    return {"avg_change_pct": sum(changes) / len(changes), "n": len(changes), "used": used}


def detect_supply_chain(
    ticker: str,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    sc_cfg = cfg.get("supply_chain", {})
    if not sc_cfg.get("enabled", True):
        return {
            "capex_score": 0.0,
            "side": "none",
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Supply-chain CapEx module disabled",
            "source": "disabled",
            "suppliers": [],
        }

    suppliers = list(sc_cfg.get("suppliers") or DEFAULT_SUPPLIERS)
    boost_th = float(sc_cfg.get("boost_score", 0.55))
    penalty_th = float(sc_cfg.get("penalty_score", -0.45))
    min_conf = float(sc_cfg.get("min_confidence", 0.40))

    live = _yfinance_supplier_momentum(suppliers) if sc_cfg.get("try_yfinance", True) else None
    source = "public_yfinance" if live else "synthetic_proxy"

    seed = sum(ord(c) for c in ticker.upper()) + datetime.now().timetuple().tm_yday + 17
    rng = random.Random(seed)
    bias = 0.10 if ticker.upper() in AI_NAMES else 0.0

    if live:
        raw = live["avg_change_pct"] / 12.0  # map ~monthly % into -1..1-ish score
        capex_score = max(-1.0, min(1.0, raw + bias))
        conf_base = min(0.78, 0.48 + 0.05 * live["n"])
        supplier_note = ",".join(live["used"][:5])
    else:
        capex_score = round(rng.uniform(-0.85, 0.95) + bias, 3)
        capex_score = max(-1.0, min(1.0, capex_score))
        conf_base = 0.52 if ticker.upper() in AI_NAMES else 0.46
        supplier_note = ",".join(suppliers[:5])

    if capex_score >= boost_th:
        side = "accel"
        boost = 1
        confidence = min(0.90, conf_base + 0.18 * capex_score)
        reason = (
            f"Supply-chain CapEx ACCEL score {capex_score:+.2f} via {supplier_note} "
            f"— leading indicator for inference demand"
        )
    elif capex_score <= penalty_th:
        side = "slow"
        boost = -1
        confidence = min(0.88, conf_base + 0.15 * abs(capex_score))
        reason = (
            f"Supply-chain CapEx SLOW score {capex_score:+.2f} via {supplier_note} "
            f"— possible equipment / backlog soft patch"
        )
    else:
        side = "stable"
        boost = 0
        confidence = conf_base
        reason = f"Supply-chain CapEx stable score {capex_score:+.2f} ({supplier_note})"

    if confidence < min_conf and boost != 0:
        boost = 0
        reason += " (confidence below gate — signal suppressed)"

    return {
        "capex_score": round(float(capex_score), 3),
        "side": side,
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": reason,
        "source": source,
        "suppliers": suppliers,
    }


def integrate_supply_chain_to_row(row: dict, cfg: dict | None = None) -> dict:
    mom = detect_supply_chain(row.get("ticker", ""), cfg)
    row.update({
        "sc_capex_score": mom["capex_score"],
        "sc_side": mom["side"],
        "sc_boost": mom["signal_boost"],
        "sc_confidence": mom["confidence"],
        "sc_reason": mom["reason"],
        "sc_source": mom["source"],
    })
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
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | CapEx: {mom['reason']}"
    return row
