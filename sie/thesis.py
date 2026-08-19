"""LLM-Generated Bull/Bear Thesis Pair Generator.

On-demand generation of balanced bullish and bearish thesis paragraphs for each
watchlist ticker. Grounded in current narrative, technicals, overlay signals and
forecasts. Surfaces both sides with evidence citations for research transparency
and bias checking. Uses a lightweight structured-prompt style generator
(deterministic, no external LLM key required) that can be swapped for a real
LLM endpoint later. Configurable via `thesis:` section.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sie.config import load_config


def _safe_str(val: Any, default: str = "") -> str:
    if val is None:
        return default
    return str(val).strip()


def _safe_float(val: Any, default: float = 0.0) -> float:
    try:
        return float(val)
    except (TypeError, ValueError):
        return default


def generate_thesis_pair(
    ticker: str,
    row: dict[str, Any] | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    """
    Generate a balanced bull / bear thesis pair grounded in the current row data.

    Returns:
        bull_thesis, bear_thesis, evidence_citations, confidence, source, reason
    """
    cfg = cfg or load_config()
    thesis_cfg = cfg.get("thesis", {})
    if not thesis_cfg.get("enabled", True):
        return {
            "bull_thesis": "",
            "bear_thesis": "",
            "evidence_citations": [],
            "confidence": 0.0,
            "source": "disabled",
            "reason": "Thesis generator disabled in config",
        }

    row = row or {}
    name = _safe_str(row.get("name"), ticker)
    signal = _safe_str(row.get("signal"), "hold")
    reason = _safe_str(row.get("signal_reason"), "")
    theme = _safe_str(row.get("theme"), "AI Inference Boom")
    dominant = _safe_str(row.get("dominant_narrative"), "neutral")
    predicted_phase = _safe_str(row.get("predicted_phase"), "stable")
    rsi = _safe_float(row.get("rsi"), 50.0)
    drawdown = _safe_float(row.get("drawdown_pct"), 0.0)
    vel = _safe_float(row.get("sentiment_velocity"), 0.0)
    price = row.get("price")
    ma50 = row.get("ma50")
    ma200 = row.get("ma200")

    # Collect evidence snippets from available overlays
    evidence: List[str] = []
    bull_points: List[str] = []
    bear_points: List[str] = []

    # Narrative / forecast
    if dominant and dominant != "neutral":
        evidence.append(f"Dominant narrative: {dominant}")
        if any(k in dominant.lower() for k in ("hype", "bull", "positive", "acceleration", "boom")):
            bull_points.append(f"Narrative currently in '{dominant}' regime supporting continued attention.")
        else:
            bear_points.append(f"Narrative labelled '{dominant}' — potential fatigue or mean-reversion risk.")

    if predicted_phase:
        evidence.append(f"Forecast phase: {predicted_phase}")
        if predicted_phase in ("hype", "recovery", "acceleration"):
            bull_points.append(f"Multi-source forecast points to '{predicted_phase}' phase over next 1–3 days.")
        elif predicted_phase in ("dip", "cooling", "exhaustion"):
            bear_points.append(f"Forecast indicates possible '{predicted_phase}' phase — short-term caution.")

    if abs(vel) > 0.15:
        evidence.append(f"Sentiment velocity: {vel:+.2f}")
        if vel > 0.25:
            bull_points.append(f"Strong positive narrative velocity ({vel:+.2f}) indicating rising retail/institutional attention.")
        elif vel < -0.25:
            bear_points.append(f"Negative narrative velocity ({vel:+.2f}) suggesting fading interest or adverse flow.")

    # Technicals
    if rsi > 0:
        evidence.append(f"RSI: {rsi:.1f}")
        if rsi < 35:
            bull_points.append(f"RSI at {rsi:.1f} (oversold territory) — potential technical bounce setup.")
        elif rsi > 70:
            bear_points.append(f"RSI at {rsi:.1f} (overbought) — elevated risk of short-term mean reversion.")
        else:
            bull_points.append(f"RSI neutral-to-constructive at {rsi:.1f}.")

    if drawdown < -12:
        evidence.append(f"Drawdown from 52w high: {drawdown:.1f}%")
        bull_points.append(f"Trading {abs(drawdown):.1f}% below 52-week high — asymmetric upside if thesis holds.")
    elif drawdown > -3 and drawdown < 0:
        bear_points.append("Price near 52-week highs — limited margin of safety on new entries.")

    if price and ma50 and ma200:
        evidence.append(f"Price {price} vs MA50 {ma50} / MA200 {ma200}")
        if price > ma50 > ma200:
            bull_points.append("Price above both MA50 and MA200 — intermediate uptrend intact.")
        elif price < ma50 < ma200:
            bear_points.append("Price below both moving averages — intermediate downtrend pressure.")

    # Overlay signals (soft evidence)
    for key, label in [
        ("hire_reason", "Hiring momentum"),
        ("edgar_reason", "SEC EDGAR"),
        ("options_0dte_reason", "0DTE flow"),
        ("options_iv_reason", "IV skew"),
        ("dark_pool_reason", "Dark pool"),
        ("insider_reason", "Insider Form 4"),
        ("institutional_reason", "13F ownership"),
        ("congress_reason", "Congressional trades"),
        ("pm_reason", "Prediction markets"),
    ]:
        val = _safe_str(row.get(key))
        if val and "disabled" not in val.lower() and "stable" not in val.lower() and "none" not in val.lower():
            evidence.append(f"{label}: {val[:120]}")
            low = val.lower()
            if any(w in low for w in ("acceleration", "boost", "buy", "accumulation", "positive", "bullish", "growth")):
                bull_points.append(f"{label} provides supportive confirmation.")
            elif any(w in low for w in ("contraction", "penalty", "sell", "distribution", "negative", "bearish", "caution")):
                bear_points.append(f"{label} raises a caution flag.")

    # Headline sentiment
    headlines = row.get("headlines") or []
    if headlines:
        avg_sent = sum(_safe_float(h.get("sentiment_score")) for h in headlines) / max(1, len(headlines))
        evidence.append(f"Avg headline sentiment: {avg_sent:+.2f}")
        if avg_sent > 0.25:
            bull_points.append("Recent headlines carry positive FinBERT/VADER sentiment.")
        elif avg_sent < -0.25:
            bear_points.append("Recent headlines lean negative — narrative risk elevated.")

    # Ensure we always have at least one point each side
    if not bull_points:
        bull_points.append(
            f"{name} remains a core exposure to the '{theme}' theme with structural tailwinds in AI infrastructure."
        )
    if not bear_points:
        bear_points.append(
            "Valuation, competition, and macro rate sensitivity remain the primary risks; any narrative fatigue could trigger de-rating."
        )

    # Construct paragraphs (LLM-style but deterministic)
    bull_thesis = (
        f"**Bull case for {name} ({ticker}):** "
        + " ".join(bull_points[:4])
        + f" Overall signal context: {signal}. "
        + "If the current multi-source overlays continue to align, the path of least resistance remains higher within the broader theme."
    )

    bear_thesis = (
        f"**Bear case for {name} ({ticker}):** "
        + " ".join(bear_points[:4])
        + " "
        + "A break in narrative velocity, deterioration in smart-money overlays, or a broader risk-off move could quickly reverse recent gains. Position sizing and stop discipline remain essential."
    )

    confidence = 0.62
    if len(evidence) >= 5:
        confidence = min(0.88, 0.62 + 0.04 * (len(evidence) - 4))
    if signal in ("strong_buy", "buy") and len(bull_points) > len(bear_points):
        confidence = min(0.90, confidence + 0.05)
    elif signal in ("caution", "sell") and len(bear_points) > len(bull_points):
        confidence = min(0.90, confidence + 0.05)

    return {
        "bull_thesis": bull_thesis,
        "bear_thesis": bear_thesis,
        "evidence_citations": evidence[:12],
        "confidence": round(confidence, 2),
        "source": "structured_generator_v1",
        "reason": f"Generated balanced thesis pair from {len(evidence)} evidence items (narrative, technicals, overlays)",
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def integrate_thesis_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Attach bull/bear thesis pair to a signal row. Does not alter the core signal."""
    pair = generate_thesis_pair(row.get("ticker", ""), row, cfg)
    row.update({
        "thesis_bull": pair["bull_thesis"],
        "thesis_bear": pair["bear_thesis"],
        "thesis_evidence": pair["evidence_citations"],
        "thesis_confidence": pair["confidence"],
        "thesis_source": pair["source"],
        "thesis_reason": pair["reason"],
    })
    # Optionally surface a short note in signal_reason for CLI visibility
    if pair["bull_thesis"] and pair["source"] != "disabled":
        row["signal_reason"] = (row.get("signal_reason") or "") + " | 📝 Thesis pair generated"
    return row
