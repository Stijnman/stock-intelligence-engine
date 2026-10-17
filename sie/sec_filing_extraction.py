"""SEC Filing Structured Extraction Latency & Completeness Overlay.

Scores latency and completeness of structured extraction from 10-K/10-Q/8-K filings
for agent-facing consumption. Soft boost when latency is low and completeness high
into a confirming narrative; caution on delayed or incomplete parses while narrative
heat remains elevated.

Live filing-monitor feed is an explicit future hook. Current source is always labeled
synthetic_proxy when a live feed is unavailable.

Preferred columns: sec_latency_s, sec_completeness, sec_boost, sec_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


# Tickers with typically fast, complete structured SEC extraction (frequent filers, clean formats).
SEC_HOT = {
    "NVDA", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "AMD", "PLTR", "SMCI",
}
# Tickers with typically slower or less complete extraction (complex, multi-entity, or sparse).
SEC_COLD = {
    "INTC", "IBM", "PFE", "JNJ", "BA", "XOM", "CVX", "GE", "T", "VZ",
}


def _clip(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_sec_filing_extraction(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    s_cfg = cfg.get("sec_filing_extraction", {})
    if not s_cfg.get("enabled", True):
        return {
            "sec_latency_s": 0.0,
            "sec_completeness": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "SEC filing structured extraction overlay disabled",
            "source": "disabled",
        }

    latency_hot = float(s_cfg.get("latency_hot_s", 45.0))
    latency_cold = float(s_cfg.get("latency_cold_s", 420.0))
    completeness_hot = float(s_cfg.get("completeness_hot", 0.88))
    completeness_cold = float(s_cfg.get("completeness_cold", 0.45))
    narrative_hot = float(s_cfg.get("narrative_hot", 1.4))
    min_conf = float(s_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 8821
    rng = random.Random(seed)
    row = row or {}
    narr = float(row.get("predicted_velocity") or row.get("narrative_velocity") or 1.0)

    if tkr in SEC_HOT:
        latency_s = rng.uniform(12.0, 55.0)
        completeness = rng.uniform(0.82, 0.97)
    elif tkr in SEC_COLD:
        latency_s = rng.uniform(280.0, 720.0)
        completeness = rng.uniform(0.28, 0.52)
    else:
        latency_s = rng.uniform(60.0, 240.0)
        completeness = rng.uniform(0.48, 0.78)

    # Lower latency is better; invert for strength.
    latency_strength = _clip((latency_cold - latency_s) / max(latency_cold - latency_hot, 1e-6))
    completeness_strength = _clip((completeness - completeness_cold) / max(completeness_hot - completeness_cold, 1e-6))
    confidence = _clip(0.35 + 0.35 * latency_strength + 0.22 * completeness_strength)

    parts = [
        f"sec_latency_s={latency_s:.1f}",
        f"sec_completeness={completeness:.2f}",
        f"narrative={narr:.2f}",
    ]
    boost = 0
    confirm = latency_s <= latency_hot and completeness >= completeness_hot and narr >= narrative_hot
    caution = latency_s >= latency_cold and completeness <= completeness_cold and narr >= narrative_hot * 0.45

    if confirm:
        boost = 1
        confidence = min(0.95, confidence + 0.07)
        parts.append(
            "low latency + high completeness structured 10-K/10-Q/8-K extraction into confirming narrative — soft boost"
        )
    elif caution:
        boost = -1
        confidence = min(0.93, confidence + 0.06)
        parts.append(
            "delayed or incomplete agent-facing filing parses while narrative heat remains elevated — caution"
        )
    else:
        parts.append("SEC filing structured extraction overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "sec_latency_s": round(float(latency_s), 1),
        "sec_completeness": round(float(completeness), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_sec_filing_extraction_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate SEC Filing Structured Extraction Latency & Completeness into a row."""
    mom = detect_sec_filing_extraction(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "sec_latency_s": mom["sec_latency_s"],
            "sec_completeness": mom["sec_completeness"],
            "sec_boost": mom["signal_boost"],
            "sec_confidence": mom["confidence"],
            "sec_reason": mom["reason"],
            "sec_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | sec {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | sec {mom['reason']}"
    return row
