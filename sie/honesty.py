"""Narrative vs. Fundamentals Contradiction / Honesty Signal Detector.

Flags cases where multi-source narrative velocity or social sentiment diverges
sharply from hard overlays (13F flows, hiring, EDGAR tone, technical structure).
Surfaces an \"honesty risk\" score that can penalize pure-narrative signals.

v2.22.0
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from sie.config import load_config


def compute_honesty_risk(
    row: dict[str, Any],
    cfg: dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Compute honesty / contradiction risk between narrative layer and hard overlays.

    Narrative side (soft):
      - sentiment_velocity (higher = more narrative heat)
      - dominant_narrative (hype / recovery vs dip / crisis)
      - forecast_boost / predicted_phase
      - social sentiment if present

    Hard side (fundamentals / structure):
      - inst_boost (13F)
      - hire_boost (hiring / headcount)
      - edgar tone / materiality (if present)
      - technical signal direction
      - dark_pool / options soft signals when available

    Returns:
      honesty_risk: float 0.0–1.0 (higher = more contradiction / pure-narrative risk)
      honesty_score: float -1.0–1.0 (positive = narrative aligned with hard, negative = conflict)
      signal_boost: int -1 / 0 / +1 (soft penalty when high risk)
      reason: human-readable explanation
      contradictions: list of specific mismatch descriptions
      confidence: float
    """
    cfg = cfg or load_config()
    h_cfg = cfg.get("honesty", {})
    enabled = h_cfg.get("enabled", True)
    if not enabled:
        return {
            "honesty_risk": 0.0,
            "honesty_score": 0.0,
            "signal_boost": 0,
            "reason": "Honesty detector disabled",
            "contradictions": [],
            "confidence": 0.0,
            "source": "disabled",
        }

    # --- Narrative polarity (-1 bearish / conflict, 0 neutral, +1 bullish heat) ---
    vel = float(row.get("sentiment_velocity") or 0.0)
    dominant = str(row.get("dominant_narrative") or "neutral").lower()
    forecast_boost = float(row.get("forecast_boost") or 0)
    predicted_phase = str(row.get("predicted_phase") or "neutral").lower()
    social_sent = float(row.get("sentiment") or row.get("buzz_score") or 0.0)

    narr_score = 0.0
    if vel >= 3.0 or social_sent > 0.35:
        narr_score += 0.6
    elif vel >= 1.0 or social_sent > 0.15:
        narr_score += 0.3
    elif vel < 0.3 and social_sent < -0.1:
        narr_score -= 0.4

    if dominant in ("hype", "recovery"):
        narr_score += 0.4
    elif dominant in ("dip", "crisis"):
        narr_score -= 0.5

    if predicted_phase in ("hype", "recovery", "acceleration"):
        narr_score += 0.3
    elif predicted_phase in ("dip", "cooling", "crisis"):
        narr_score -= 0.3

    narr_score += max(-0.4, min(0.4, forecast_boost * 0.25))
    narr_score = max(-1.0, min(1.0, narr_score))

    # --- Hard / fundamental polarity ---
    hard_score = 0.0
    hard_count = 0
    contradictions: List[str] = []

    # Technical structure
    tech_sig = str(row.get("signal") or "hold").lower()
    if tech_sig in ("strong_buy", "buy"):
        hard_score += 0.5
        hard_count += 1
    elif tech_sig in ("caution", "sell", "strong_sell"):
        hard_score -= 0.5
        hard_count += 1
    else:
        hard_count += 0.5  # neutral still counts as observation

    # Institutional 13F
    inst_boost = int(row.get("inst_boost") or 0)
    if inst_boost != 0:
        hard_score += 0.6 * inst_boost
        hard_count += 1
        if narr_score > 0.4 and inst_boost < 0:
            contradictions.append("Narrative heat vs 13F distribution")
        elif narr_score < -0.3 and inst_boost > 0:
            contradictions.append("Narrative weakness vs 13F accumulation")

    # Hiring / headcount
    hire_boost = int(row.get("hire_boost") or 0)
    if hire_boost != 0:
        hard_score += 0.5 * hire_boost
        hard_count += 1
        if narr_score > 0.4 and hire_boost < 0:
            contradictions.append("Narrative heat vs hiring contraction")
        elif narr_score < -0.3 and hire_boost > 0:
            contradictions.append("Narrative weakness vs hiring acceleration")

    # EDGAR material filings (tone approximated via reason or explicit if present)
    edgar_boost = int(row.get("edgar_boost") or row.get("edgar_signal_boost") or 0)
    if edgar_boost != 0:
        hard_score += 0.55 * edgar_boost
        hard_count += 1
        if narr_score > 0.4 and edgar_boost < 0:
            contradictions.append("Narrative heat vs negative EDGAR materiality")
        elif narr_score < -0.3 and edgar_boost > 0:
            contradictions.append("Narrative weakness vs positive EDGAR filing")

    # Dark pool / options soft (optional weight)
    dp_boost = int(row.get("dp_boost") or row.get("dark_pool_boost") or 0)
    if dp_boost != 0:
        hard_score += 0.35 * dp_boost
        hard_count += 0.7

    opt_boost = int(row.get("opt_0dte_boost") or row.get("options_0dte_boost") or 0)
    if opt_boost != 0:
        hard_score += 0.3 * opt_boost
        hard_count += 0.6

    if hard_count > 0:
        hard_score = hard_score / max(1.0, hard_count * 0.6)
    hard_score = max(-1.0, min(1.0, hard_score))

    # --- Divergence / honesty risk ---
    divergence = abs(narr_score - hard_score)
    # Extra penalty when narrative is strongly positive while hard is neutral-to-negative
    pure_narrative_penalty = 0.0
    if narr_score > 0.45 and hard_score < 0.15:
        pure_narrative_penalty = 0.25 + 0.15 * (narr_score - hard_score)
    elif narr_score < -0.4 and hard_score > 0.2:
        pure_narrative_penalty = 0.2

    honesty_risk = min(1.0, divergence * 0.7 + pure_narrative_penalty)
    honesty_score = max(-1.0, min(1.0, 1.0 - 2.0 * honesty_risk))  # higher better (aligned)

    # Thresholds from config
    high_risk = float(h_cfg.get("high_risk_threshold", 0.55))
    mid_risk = float(h_cfg.get("mid_risk_threshold", 0.35))
    min_confidence = float(h_cfg.get("min_confidence", 0.40))

    signal_boost = 0
    if honesty_risk >= high_risk:
        signal_boost = -1
        reason = (
            f"Honesty risk {honesty_risk:.2f} (high) — narrative vs hard overlays diverge; "
            f"pure-narrative caution applied"
        )
    elif honesty_risk >= mid_risk:
        signal_boost = 0
        reason = f"Honesty risk {honesty_risk:.2f} (elevated) — mild narrative/hard tension"
    else:
        signal_boost = 0
        reason = f"Honesty risk {honesty_risk:.2f} (low) — narrative broadly consistent with hard signals"

    if contradictions:
        reason += " | " + "; ".join(contradictions[:3])

    confidence = min(0.95, 0.45 + 0.15 * hard_count + (0.2 if abs(narr_score) > 0.4 else 0.0))
    if confidence < min_confidence:
        signal_boost = 0  # gate weak signals

    return {
        "honesty_risk": round(honesty_risk, 3),
        "honesty_score": round(honesty_score, 3),
        "signal_boost": signal_boost,
        "reason": reason,
        "contradictions": contradictions,
        "confidence": round(confidence, 3),
        "narr_score": round(narr_score, 3),
        "hard_score": round(hard_score, 3),
        "source": "honesty_detector",
    }


def integrate_honesty_to_row(row: dict[str, Any], cfg: dict[str, Any] | None = None) -> dict:
    """Attach honesty / contradiction metrics and apply soft penalty when risk is high."""
    result = compute_honesty_risk(row, cfg)
    row.update({
        "honesty_risk": result["honesty_risk"],
        "honesty_score": result["honesty_score"],
        "honesty_boost": result["signal_boost"],
        "honesty_confidence": result["confidence"],
        "honesty_reason": result["reason"],
        "honesty_contradictions": result.get("contradictions", []),
        "honesty_narr_score": result.get("narr_score"),
        "honesty_hard_score": result.get("hard_score"),
    })

    boost = result["signal_boost"]
    if boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | ⚖️ {result['reason']}"
    else:
        if result["honesty_risk"] > 0.25:
            row["signal_reason"] = (row.get("signal_reason") or "") + f" | Honesty: {result['reason']}"

    return row
