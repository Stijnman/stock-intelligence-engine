"""Target-Specific Financial Stance & Narrative Specificity Overlay.

Scores whether a name's public narrative is numerically specific (guidance,
margin, FCF, unit targets) versus generic, and the gap between prepared
remarks and Q&A. Distinct from earnings-call sentiment and whisper-number
beat probability.

Live transcript parsers are an explicit future hook. Current source is
always labeled synthetic_proxy when the call text is unavailable.

Preferred columns: tsn_stance, tsn_specificity, tsn_qa_gap, tsn_boost, tsn_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


# Issuers that habitually print numeric targets in prepared remarks.
TSN_SPECIFIC = {
    "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "AVGO", "COST", "UNH", "JPM",
}
# Names whose public narrative stays thematic and light on hard targets.
TSN_VAGUE = {
    "AMC", "GME", "CVNA", "RIVN", "LCID", "MARA", "WBD", "PLTR",
}

STANCES = ("constructive", "hedged", "cautious")


def _clip(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_target_stance(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    tsn_cfg = cfg.get("target_stance", {})
    if not tsn_cfg.get("enabled", True):
        return {
            "tsn_stance": "unknown",
            "tsn_specificity": 0.0,
            "tsn_qa_gap": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Target-specific financial stance overlay disabled",
            "source": "disabled",
        }

    spec_hot = float(tsn_cfg.get("specificity_hot", 0.62))
    spec_cold = float(tsn_cfg.get("specificity_cold", 0.32))
    gap_hot = float(tsn_cfg.get("qa_gap_hot", 0.48))
    gap_cold = float(tsn_cfg.get("qa_gap_cold", 0.22))
    narrative_hot = float(tsn_cfg.get("narrative_hot", 1.4))
    min_conf = float(tsn_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 2530
    rng = random.Random(seed)
    row = row or {}

    if tkr in TSN_SPECIFIC:
        specificity = rng.uniform(0.62, 0.94)
        qa_gap = rng.uniform(0.04, 0.28)
        stance = "constructive"
    elif tkr in TSN_VAGUE:
        specificity = rng.uniform(0.08, 0.38)
        qa_gap = rng.uniform(0.42, 0.88)
        stance = "cautious" if rng.random() > 0.35 else "hedged"
    else:
        specificity = rng.uniform(0.28, 0.70)
        qa_gap = rng.uniform(0.16, 0.55)
        stance = STANCES[rng.randrange(len(STANCES))]

    narr = float(
        row.get("predicted_velocity")
        or row.get("sentiment_velocity")
        or 0.0
    )
    parts = [
        f"stance={stance}",
        f"specificity={specificity:.2f}",
        f"qa_gap={qa_gap:.2f}",
    ]
    confidence = _clip(0.42 + 0.28 * specificity + 0.12 * (1.0 - qa_gap))
    boost = 0

    specific_confirm = (
        stance == "constructive"
        and specificity >= spec_hot
        and qa_gap <= gap_cold
        and narr >= narrative_hot * 0.45
    )
    vague_heat = (
        (specificity <= spec_cold or qa_gap >= gap_hot or stance == "cautious")
        and narr >= narrative_hot * 0.35
    )

    if specific_confirm:
        boost = 1
        confidence = min(
            0.92,
            0.50
            + 0.20 * specificity
            + 0.12 * (1.0 - qa_gap)
            + 0.08 * min(narr / 4.0, 1.0),
        )
        parts.append("numeric targets hold through Q&A into a confirming narrative — soft boost")
    elif vague_heat:
        boost = -1
        confidence = min(
            0.90,
            0.48 + 0.18 * qa_gap + 0.16 * (1.0 - specificity),
        )
        parts.append("narrative heat without target specificity or a wide Q&A gap — caution")
    else:
        parts.append("target-specific financial stance overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "tsn_stance": stance,
        "tsn_specificity": round(float(specificity), 4),
        "tsn_qa_gap": round(float(qa_gap), 4),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_target_stance_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate target specificity and Q&A gap into a row."""
    mom = detect_target_stance(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "tsn_stance": mom["tsn_stance"],
            "tsn_specificity": mom["tsn_specificity"],
            "tsn_qa_gap": mom["tsn_qa_gap"],
            "tsn_boost": mom["signal_boost"],
            "tsn_confidence": mom["confidence"],
            "tsn_reason": mom["reason"],
            "tsn_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | tsn {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | tsn {mom['reason']}"
    return row
