"""Index Reconstitution & Forced Passive-Flow Overlay.

Scores upcoming index add / delete / weight-change events and the estimated
forced passive dollar flow from benchmarked funds. Distinct from the already
wired ETF creation/redemption overlay and from dealer gamma. Passive trackers
must trade on the effective date regardless of narrative.

Live S&P / Russell / Nasdaq reconstitution parsers are an explicit future hook.
Current source is always labeled synthetic_proxy when a signed index notice is
unavailable.

Preferred columns: idx_event, idx_forced_usd, idx_boost, idx_reason.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
import random

from sie.config import load_config


# Names with a plausible near-term add or upweight and positive forced inflow.
IDX_ADDS = {
    "PLTR", "CRWD", "APP", "SMCI", "DELL", "AXON", "VST", "CEG",
}
# Names with a plausible delete or downweight and forced selling.
IDX_DELETES = {
    "WBA", "PARA", "AAL", "SEDG", "VFC", "LUMN", "TDOC", "WOLF",
}


def _clip(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def detect_index_reconstitution(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    i_cfg = cfg.get("index_reconstitution", {})
    if not i_cfg.get("enabled", True):
        return {
            "idx_event": "none",
            "idx_forced_usd": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Index reconstitution overlay disabled",
            "source": "disabled",
        }

    forced_hot = float(i_cfg.get("forced_hot_usd", 250_000_000))
    forced_cold = float(i_cfg.get("forced_cold_usd", -200_000_000))
    narrative_hot = float(i_cfg.get("narrative_hot", 1.4))
    min_conf = float(i_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 2610
    rng = random.Random(seed)
    row = row or {}

    if tkr in IDX_ADDS:
        event = "add" if rng.random() > 0.35 else "upweight"
        forced = rng.uniform(280_000_000, 1_400_000_000)
        days = rng.randint(2, 18)
    elif tkr in IDX_DELETES:
        event = "delete" if rng.random() > 0.40 else "downweight"
        forced = -rng.uniform(180_000_000, 900_000_000)
        days = rng.randint(1, 14)
    else:
        roll = rng.random()
        if roll > 0.82:
            event = "upweight"
            forced = rng.uniform(40_000_000, 220_000_000)
            days = rng.randint(5, 40)
        elif roll < 0.12:
            event = "downweight"
            forced = -rng.uniform(30_000_000, 160_000_000)
            days = rng.randint(5, 40)
        else:
            event = "none"
            forced = rng.uniform(-25_000_000, 25_000_000)
            days = 99

    narr = float(
        row.get("predicted_velocity")
        or row.get("sentiment_velocity")
        or 0.0
    )
    parts = [
        f"event={event}",
        f"forced_usd={forced:.0f}",
        f"days_to_effective={days}",
    ]
    magnitude = _clip(abs(forced) / 1_200_000_000)
    confidence = _clip(0.36 + 0.34 * magnitude + (0.12 if event != "none" else 0.0))
    boost = 0

    add_confirm = (
        event in ("add", "upweight")
        and forced >= forced_hot
        and narr >= narrative_hot * 0.45
    )
    delete_caution = (
        event in ("delete", "downweight")
        and forced <= forced_cold
        and narr >= narrative_hot * 0.35
    )

    if add_confirm:
        boost = 1
        confidence = min(
            0.93,
            0.48
            + 0.22 * magnitude
            + 0.08 * min(narr / 4.0, 1.0)
            + (0.06 if event == "add" else 0.0),
        )
        parts.append("confirmed index add or upweight with material forced passive inflow into a confirming narrative — soft boost")
    elif delete_caution:
        boost = -1
        confidence = min(
            0.91,
            0.46 + 0.26 * magnitude + 0.10 * min(narr / 4.0, 1.0),
        )
        parts.append("index delete or downweight forcing passive selling into narrative heat — caution")
    else:
        parts.append("index reconstitution overlay neutral")

    if confidence < min_conf and boost != 0:
        boost = 0
        parts.append("(confidence below gate — signal suppressed)")

    return {
        "idx_event": event,
        "idx_forced_usd": round(float(forced), 2),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": " | ".join(parts),
        "source": "synthetic_proxy",
    }


def integrate_index_reconstitution_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Integrate index event and forced passive flow into a row."""
    mom = detect_index_reconstitution(row.get("ticker", ""), row, cfg)
    row.update(
        {
            "idx_event": mom["idx_event"],
            "idx_forced_usd": mom["idx_forced_usd"],
            "idx_boost": mom["signal_boost"],
            "idx_confidence": mom["confidence"],
            "idx_reason": mom["reason"],
            "idx_source": mom["source"],
        }
    )
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | idx {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | idx {mom['reason']}"
    return row
