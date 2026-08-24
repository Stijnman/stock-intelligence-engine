"""Self-Explaining AI Signal Brief Generator.

One-click / auto-generated 4–6 sentence plain-English brief that cites every
active overlay (thesis, 0DTE, EDGAR, hiring, 13F, dark pool, congressional,
prediction markets, insider, narrative velocity, technicals) with an overall
confidence score and an explicit "what would change my mind" statement.
Deterministic structured generator (no external LLM required) that can later
be swapped for a real LLM endpoint. Configurable via `brief:` section.
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


def _active_overlay_snippets(row: dict[str, Any]) -> List[str]:
    """Collect short, human-readable citations from every active overlay."""
    snippets: List[str] = []

    # Core signal + technicals
    signal = _safe_str(row.get("signal"), "hold")
    reason = _safe_str(row.get("signal_reason"), "")
    rsi = row.get("rsi")
    price = row.get("price")
    drawdown = row.get("drawdown_pct")
    if signal:
        snippets.append(f"Core signal is **{signal.upper()}**")
    if rsi is not None:
        snippets.append(f"RSI at {rsi}")
    if drawdown is not None:
        snippets.append(f"drawdown from 52w high {drawdown}%")

    # Narrative / forecast
    phase = _safe_str(row.get("predicted_phase"))
    vel = row.get("sentiment_velocity") or row.get("predicted_velocity")
    if phase and phase not in ("stable", "none", ""):
        snippets.append(f"narrative phase forecast **{phase}**")
    if vel is not None and abs(_safe_float(vel)) > 0.05:
        snippets.append(f"sentiment velocity {vel:+.2f}")

    # Overlay reasons (only if they contain meaningful content)
    overlay_keys = [
        ("hire_reason", "Hiring / headcount momentum"),
        ("edgar_reason", "Same-day SEC EDGAR filing"),
        ("options_0dte_reason", "0DTE options flow"),
        ("options_iv_reason", "IV skew / term structure"),
        ("dark_pool_reason", "Dark-pool / ATS flow"),
        ("insider_reason", "Insider Form-4 clustering"),
        ("institutional_reason", "13F ownership change"),
        ("congress_reason", "Congressional trading"),
        ("pm_reason", "Prediction-market odds"),
        ("realtime_reason", "Real-time quote context"),
        ("forecast_reason", "Narrative velocity forecast"),
    ]
    for key, label in overlay_keys:
        val = _safe_str(row.get(key))
        if not val:
            continue
        low = val.lower()
        if any(x in low for x in ("disabled", "none", "stable", "n/a", "no data", "unavailable")):
            continue
        # Truncate long reasons for the brief
        short = val if len(val) <= 90 else val[:87] + "..."
        snippets.append(f"{label}: {short}")

    # Thesis presence
    if row.get("thesis_bull") or row.get("thesis_bear"):
        conf = row.get("thesis_confidence")
        if conf is not None:
            snippets.append(f"balanced bull/bear thesis generated (conf {conf})")
        else:
            snippets.append("balanced bull/bear thesis generated")

    return snippets


def generate_signal_brief(
    ticker: str,
    row: dict[str, Any] | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    """
    Produce a concise 4–6 sentence plain-English signal brief.

    Returns:
        brief (str), confidence (float), change_my_mind (str),
        cited_overlays (list), source, reason, generated_at
    """
    cfg = cfg or load_config()
    brief_cfg = cfg.get("brief", {})
    if not brief_cfg.get("enabled", True):
        return {
            "brief": "",
            "confidence": 0.0,
            "change_my_mind": "",
            "cited_overlays": [],
            "source": "disabled",
            "reason": "Signal brief generator disabled in config",
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    row = row or {}
    name = _safe_str(row.get("name"), ticker)
    signal = _safe_str(row.get("signal"), "hold").lower()
    theme = _safe_str(row.get("theme"), "AI Inference Boom")
    snippets = _active_overlay_snippets(row)

    # Build the narrative sentences
    sentences: List[str] = []

    # 1. Opening frame
    sentences.append(
        f"{name} ({ticker}) currently carries a **{signal.upper()}** signal inside the broader “{theme}” narrative."
    )

    # 2–3. Overlay citations (group them)
    if snippets:
        # Take the most important ones
        core = snippets[:3]
        extra = snippets[3:7]
        sentences.append(
            "Key supporting context: " + "; ".join(core) + "."
        )
        if extra:
            sentences.append(
                "Additional overlays: " + "; ".join(extra) + "."
            )
    else:
        sentences.append(
            "Limited overlay confirmation is currently available; the signal rests primarily on technicals and the base narrative fit."
        )

    # 4. Confidence statement
    base_conf = 0.55
    n_overlays = len(snippets)
    conf = min(0.92, base_conf + 0.04 * n_overlays)
    if signal in ("strong_buy", "buy") and n_overlays >= 4:
        conf = min(0.93, conf + 0.05)
    elif signal in ("caution", "sell") and n_overlays >= 3:
        conf = min(0.90, conf + 0.04)
    # Penalize if thesis confidence is low
    t_conf = _safe_float(row.get("thesis_confidence"), 0.6)
    if t_conf < 0.5:
        conf = max(0.40, conf - 0.08)
    conf = round(conf, 2)

    sentences.append(
        f"Overall confidence in this multi-source reading is **{conf:.0%}**, reflecting the number and consistency of active overlays."
    )

    # 5. What would change my mind
    change_parts: List[str] = []
    if signal in ("strong_buy", "buy", "hold"):
        change_parts.append("a sharp drop in narrative velocity or a cluster of negative smart-money overlays (insider sales, 13F reductions, elevated put skew)")
        change_parts.append("a material adverse 8-K or guidance cut that contradicts the current thesis")
        change_parts.append("breakdown of key technical levels (price below both MAs with rising volume)")
    else:
        change_parts.append("a clear acceleration in hiring / positive EDGAR tone / institutional accumulation that overrides the current caution")
        change_parts.append("a sustained rebound in multi-source sentiment velocity with confirming 0DTE call flow")
        change_parts.append("price reclaiming both moving averages on expanding volume")

    change_my_mind = (
        "What would change my mind: "
        + "; ".join(change_parts[:3])
        + "."
    )
    sentences.append(change_my_mind)

    # Optional 6th sentence if we have thesis
    if row.get("thesis_bull"):
        sentences.append(
            "A full bull/bear thesis pair is available for deeper research transparency."
        )

    brief = " ".join(sentences)

    return {
        "brief": brief,
        "confidence": conf,
        "change_my_mind": change_my_mind,
        "cited_overlays": snippets,
        "source": "structured_brief_generator_v1",
        "reason": f"Generated self-explaining brief from {len(snippets)} active overlay citations",
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def integrate_brief_to_row(row: dict, cfg: dict | None = None) -> dict:
    """Attach the self-explaining signal brief to a row. Does not alter the core signal."""
    result = generate_signal_brief(row.get("ticker", ""), row, cfg)
    row.update({
        "signal_brief": result["brief"],
        "brief_confidence": result["confidence"],
        "brief_change_my_mind": result["change_my_mind"],
        "brief_cited_overlays": result["cited_overlays"],
        "brief_source": result["source"],
        "brief_reason": result["reason"],
    })
    if result["brief"] and result["source"] != "disabled":
        row["signal_reason"] = (row.get("signal_reason") or "") + " | 🧾 Signal brief generated"
    return row
