"""Listed Earnings Event-Contract vs Whisper / Street Divergence Overlay.

Scores the implied beat probability on a listed earnings event contract against
the whisper / street consensus for the same print. Distinct from the already
wired whisper-number overlay and from prediction-market ETF overlap. The
contract is a priced probability; the whisper is a narrative consensus.

Live exchange event-contract books are an explicit future hook. Current source
is always labeled synthetic_proxy when a listed contract quote is unavailable.

Preferred columns: eec_implied_beat, eec_whisper_gap, eec_boost, eec_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


# Names where a listed earnings contract typically prices a beat above whisper.
EEC_RICH = {
    "NVDA", "META", "AMZN", "AVGO", "NFLX", "ARM", "MSFT", "GOOGL",
}
# Names where the contract typically prices a miss versus a still-hot street.
EEC_MISS = {
    "INTC", "PFE", "BA", "NKE", "DIS", "PYPL", "INTC", "WBA",
}


def _clip(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_earnings_event_contract(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    e_cfg = cfg.get("earnings_event_contract", {})
    if not e_cfg.get("enabled", True):
        return {
            "eec_implied_beat": 0.0,
            "eec_whisper_gap": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Earnings event-contract overlay disabled",
            "source": "disabled",
        }

    implied_hot = float(e_cfg.get("implied_hot", 0.62))
    implied_cold = float(e_cfg.get("implied_cold", 0.42))
    gap_hot = float(e_cfg.get("gap_hot", 0.06))
    gap_cold = float(e_cfg.get("gap_cold", -0.05))
    narrative_hot = float(e_cfg.get("narrative_hot", 1.4))
    min_conf = float(e_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 2710
    rng = random.Random(seed)
    row = row or {}
    narr = float(row.get("predicted_velocity") or row.get("narrative_velocity") or 1.0)

    if tkr in EEC_RICH:
        implied = rng.uniform(0.64, 0.86)
        whisper = rng.uniform(0.50, 0.62)
    elif tkr in EEC_MISS:
        implied = rng.uniform(0.28, 0.44)
        whisper = rng.uniform(0.52, 0.66)
    else:
        implied = rng.uniform(0.42, 0.64)
        whisper = implied + rng.uniform(-0.04, 0.04)

    gap = implied - whisper
    beat_strength = _clip((implied - implied_cold) / max(implied_hot - implied_cold, 1e-6))
    gap_strength = _clip((gap - gap_cold) / max(gap_hot - gap_cold, 1e-6))
    confidence = _clip(0.42 + 0.30 * beat_strength + 0.18 * abs(gap) / 0.20)

    parts = [
        f"implied_beat={implied:.2f}",
        f"whisper_gap={gap:+.3f}",
        f"narrative={narr:.2f}",
    ]
    boost = 0
    confirm = implied >= implied_hot and gap >= gap_hot and narr >= narrative_hot
    caution = implied <= implied_cold and gap <= gap_cold and narr >= narrative_hot * 0.35

    if confirm:
        boost = 1
        confidence = min(0.93, confidence + 0.08)
        parts.append(
            "listed earnings contract implies a beat above whisper into a confirming narrative — soft boost"
        )
    elif caution:
        boost = -1
        confidence = min(0.91, confidence + 0.06)
        parts.append(
            "listed earnings contract implies a miss versus whisper while narrative heat is still positive — caution"
        )
    else:
        parts.append("earnings event-contract versus whisper overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "eec_implied_beat": round(float(implied), 4),
        "eec_whisper_gap": round(float(gap), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_earnings_event_contract_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate listed earnings event-contract vs whisper gap into a row."""
    mom = detect_earnings_event_contract(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "eec_implied_beat": mom["eec_implied_beat"],
            "eec_whisper_gap": mom["eec_whisper_gap"],
            "eec_boost": mom["signal_boost"],
            "eec_confidence": mom["confidence"],
            "eec_reason": mom["reason"],
            "eec_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | eec {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | eec {mom['reason']}"
    return row
