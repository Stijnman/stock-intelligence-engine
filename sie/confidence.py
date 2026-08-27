"""Signal Confidence Calibration & LLM Self-Critique Layer.

Post-signal self-critique that scores consistency across overlays and flags
over-confident or conflicting signals before they reach the dashboard or alerts.
Deterministic structured calibrator (LLM-swappable later). Surfaces a calibrated
confidence score (0-1), consistency ratio, conflict list, and a short plain-English
self-critique that cites which overlays agree / disagree and what would change the mind.

v2.24.0
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from sie.config import load_config


def _safe_float(val: Any, default: float = 0.0) -> float:
    try:
        return float(val)
    except (TypeError, ValueError):
        return default


def _safe_str(val: Any, default: str = "") -> str:
    if val is None:
        return default
    return str(val).strip()


def _direction_from_signal(signal: str) -> int:
    """Map core signal to polarity: +1 bullish, 0 neutral, -1 bearish."""
    s = (signal or "hold").lower()
    if s in ("strong_buy", "buy"):
        return 1
    if s in ("caution", "strong_sell", "sell"):
        return -1
    return 0


def _overlay_votes(row: dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Collect discrete votes from active overlays.
    Each vote: {"name": str, "polarity": -1/0/+1, "weight": float, "note": str}
    """
    votes: List[Dict[str, Any]] = []

    # Core technical already in row["signal"]
    core_pol = _direction_from_signal(row.get("signal", "hold"))
    votes.append({
        "name": "technical",
        "polarity": core_pol,
        "weight": 1.2,
        "note": f"core={row.get('signal')}",
    })

    # Narrative / social velocity
    vel = _safe_float(row.get("sentiment_velocity") or row.get("predicted_velocity"))
    phase = _safe_str(row.get("predicted_phase") or row.get("dominant_narrative"), "neutral").lower()
    narr_pol = 0
    if vel >= 2.0 or phase in ("hype", "recovery", "acceleration"):
        narr_pol = 1
    elif vel <= -1.5 or phase in ("dip", "cooling", "crisis"):
        narr_pol = -1
    votes.append({
        "name": "narrative",
        "polarity": narr_pol,
        "weight": 1.0,
        "note": f"vel={vel:.1f} phase={phase}",
    })

    # Honesty risk (high risk → against pure narrative, often caution)
    h_risk = _safe_float(row.get("honesty_risk"))
    if h_risk >= 0.55:
        votes.append({"name": "honesty", "polarity": -1, "weight": 1.1, "note": f"high risk {h_risk:.2f}"})
    elif h_risk <= 0.25:
        votes.append({"name": "honesty", "polarity": 1, "weight": 0.6, "note": f"aligned {h_risk:.2f}"})
    else:
        votes.append({"name": "honesty", "polarity": 0, "weight": 0.4, "note": f"mid {h_risk:.2f}"})

    # Institutional 13F
    inst_boost = int(row.get("inst_boost") or row.get("institutional_boost") or 0)
    if inst_boost != 0:
        votes.append({
            "name": "13F",
            "polarity": 1 if inst_boost > 0 else -1,
            "weight": 1.0,
            "note": f"boost={inst_boost}",
        })

    # Hiring / headcount
    hire_boost = int(row.get("hire_boost") or row.get("hiring_boost") or 0)
    if hire_boost != 0:
        votes.append({
            "name": "hiring",
            "polarity": 1 if hire_boost > 0 else -1,
            "weight": 0.8,
            "note": f"boost={hire_boost}",
        })

    # Insider Form 4
    insider_boost = int(row.get("insider_boost") or 0)
    if insider_boost != 0:
        votes.append({
            "name": "insider",
            "polarity": 1 if insider_boost > 0 else -1,
            "weight": 0.9,
            "note": f"boost={insider_boost}",
        })

    # Congressional
    cong_boost = int(row.get("cong_boost") or row.get("congressional_boost") or 0)
    if cong_boost != 0:
        votes.append({
            "name": "congressional",
            "polarity": 1 if cong_boost > 0 else -1,
            "weight": 0.7,
            "note": f"boost={cong_boost}",
        })

    # Dark pool
    dp_boost = int(row.get("dark_pool_boost") or row.get("dp_boost") or 0)
    if dp_boost != 0:
        votes.append({
            "name": "dark_pool",
            "polarity": 1 if dp_boost > 0 else -1,
            "weight": 0.8,
            "note": f"boost={dp_boost}",
        })

    # Options IV / 0DTE
    iv_boost = int(row.get("options_iv_boost") or row.get("iv_boost") or 0)
    if iv_boost != 0:
        votes.append({
            "name": "options_iv",
            "polarity": 1 if iv_boost > 0 else -1,
            "weight": 0.7,
            "note": f"boost={iv_boost}",
        })
    odte_boost = int(row.get("options_0dte_boost") or row.get("odte_boost") or 0)
    if odte_boost != 0:
        votes.append({
            "name": "0dte",
            "polarity": 1 if odte_boost > 0 else -1,
            "weight": 0.6,
            "note": f"boost={odte_boost}",
        })

    # EDGAR
    edgar_boost = int(row.get("edgar_boost") or 0)
    if edgar_boost != 0:
        votes.append({
            "name": "edgar",
            "polarity": 1 if edgar_boost > 0 else -1,
            "weight": 0.9,
            "note": f"boost={edgar_boost}",
        })

    # Prediction markets
    pm_boost = int(row.get("pm_boost") or row.get("prediction_boost") or 0)
    if pm_boost != 0:
        votes.append({
            "name": "polymarket",
            "polarity": 1 if pm_boost > 0 else -1,
            "weight": 0.7,
            "note": f"boost={pm_boost}",
        })

    return votes


def compute_confidence(
    row: dict[str, Any],
    cfg: dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Calibrate overall signal confidence from overlay consistency.
    Returns confidence_score, consistency_ratio, conflicts, self_critique, label, etc.
    """
    cfg = cfg or load_config()
    c_cfg = cfg.get("confidence", {})
    enabled = c_cfg.get("enabled", True)
    if not enabled:
        return {
            "confidence_score": 0.5,
            "consistency_ratio": 0.5,
            "conflicts": [],
            "agree_count": 0,
            "total_votes": 0,
            "self_critique": "Confidence calibration disabled",
            "confidence_label": "n/a",
            "source": "disabled",
        }

    core_pol = _direction_from_signal(row.get("signal", "hold"))
    votes = _overlay_votes(row)

    if not votes:
        return {
            "confidence_score": 0.4,
            "consistency_ratio": 0.0,
            "conflicts": [],
            "agree_count": 0,
            "total_votes": 0,
            "self_critique": "No overlay votes available for calibration",
            "confidence_label": "low",
            "source": "confidence_calibrator",
        }

    # Weighted agreement with core signal polarity (neutral votes count as partial)
    weighted_agree = 0.0
    weighted_total = 0.0
    conflicts: List[str] = []
    agree_names: List[str] = []
    disagree_names: List[str] = []

    for v in votes:
        w = float(v.get("weight", 1.0))
        pol = int(v.get("polarity", 0))
        name = v.get("name", "unknown")
        note = v.get("note", "")
        weighted_total += w
        if core_pol == 0:
            # Neutral core: agreement if overlay also neutral or mild
            if pol == 0:
                weighted_agree += w
                agree_names.append(name)
            else:
                weighted_agree += 0.3 * w
                conflicts.append(f"{name} ({note}) pulls directional while core is neutral")
                disagree_names.append(name)
        else:
            if pol == core_pol:
                weighted_agree += w
                agree_names.append(name)
            elif pol == 0:
                weighted_agree += 0.4 * w  # neutral is soft support
                agree_names.append(f"{name}~")
            else:
                # conflict
                conflicts.append(f"{name} ({note}) opposes core {row.get('signal')}")
                disagree_names.append(name)

    consistency = weighted_agree / max(0.01, weighted_total)
    consistency = max(0.0, min(1.0, consistency))

    # Base confidence from consistency + number of active overlays
    n_votes = len(votes)
    coverage_bonus = min(0.25, 0.04 * n_votes)
    confidence = 0.25 + 0.55 * consistency + coverage_bonus

    # Penalize high honesty risk further
    h_risk = _safe_float(row.get("honesty_risk"))
    if h_risk >= 0.55:
        confidence *= 0.75
    elif h_risk >= 0.35:
        confidence *= 0.90

    # Cap and floor
    min_c = float(c_cfg.get("min_confidence", 0.15))
    max_c = float(c_cfg.get("max_confidence", 0.95))
    confidence = max(min_c, min(max_c, confidence))

    # Label
    high_th = float(c_cfg.get("high_threshold", 0.70))
    mid_th = float(c_cfg.get("mid_threshold", 0.45))
    if confidence >= high_th:
        label = "high"
    elif confidence >= mid_th:
        label = "medium"
    else:
        label = "low"

    # Self-critique text (deterministic "LLM" style)
    signal = _safe_str(row.get("signal"), "hold").upper()
    agree_str = ", ".join(agree_names[:6]) if agree_names else "none"
    disagree_str = ", ".join(disagree_names[:4]) if disagree_names else "none"
    critique_parts = [
        f"Calibrated confidence {confidence:.2f} ({label}). "
        f"Core signal {signal} has {len(agree_names)}/{n_votes} overlays aligned "
        f"(consistency {consistency:.0%})."
    ]
    if conflicts:
        critique_parts.append(
            f"Conflicts: {'; '.join(conflicts[:3])}."
        )
    # What would change my mind
    change_mind = []
    if core_pol > 0:
        change_mind.append("material negative EDGAR filing")
        change_mind.append("RSI > 75 with accelerating sell volume")
        if h_risk < 0.4:
            change_mind.append("sudden honesty risk spike >0.55")
    elif core_pol < 0:
        change_mind.append("cluster of Form-4 buys or 13F accumulation")
        change_mind.append("narrative velocity flip to recovery + positive hiring")
    else:
        change_mind.append("clear directional consensus from 13F + insider + narrative")
    critique_parts.append(
        f"What would change my mind: {'; '.join(change_mind[:3])}."
    )

    self_critique = " ".join(critique_parts)

    return {
        "confidence_score": round(confidence, 3),
        "consistency_ratio": round(consistency, 3),
        "conflicts": conflicts,
        "agree_count": len(agree_names),
        "total_votes": n_votes,
        "self_critique": self_critique,
        "confidence_label": label,
        "agree_overlays": agree_names,
        "disagree_overlays": disagree_names,
        "source": "confidence_calibrator",
    }


def integrate_confidence_to_row(row: dict[str, Any], cfg: dict[str, Any] | None = None) -> dict:
    """Attach calibrated confidence + self-critique to the row. Soft-gate extreme low confidence."""
    result = compute_confidence(row, cfg)
    row.update({
        "confidence_score": result["confidence_score"],
        "confidence_label": result["confidence_label"],
        "consistency_ratio": result["consistency_ratio"],
        "self_critique": result["self_critique"],
        "confidence_conflicts": result.get("conflicts", []),
        "confidence_agree_count": result.get("agree_count", 0),
        "confidence_total_votes": result.get("total_votes", 0),
    })

    # Soft caution when confidence is very low on a strong signal
    score = result["confidence_score"]
    label = result["confidence_label"]
    if score < 0.30 and row.get("signal") in ("strong_buy", "buy"):
        row["signal"] = "hold"
        row["signal_reason"] = (
            (row.get("signal_reason") or "")
            + f" | 🔍 Low confidence ({score:.2f}) — self-critique gated strong signal"
        )
    elif label == "low":
        row["signal_reason"] = (
            (row.get("signal_reason") or "")
            + f" | Confidence {label} ({score:.2f})"
        )
    else:
        # Always surface a short note
        row["signal_reason"] = (
            (row.get("signal_reason") or "")
            + f" | Conf {score:.2f} ({label})"
        )

    return row
