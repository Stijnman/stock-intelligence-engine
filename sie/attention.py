"""Wikipedia / Google Trends Attention Momentum Tracker.

Seeded pageview / search-interest momentum proxy keyed by ticker + company name.
Optional Wikimedia pageview API peek when reachable with stdlib only.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict
import json
import random
import urllib.parse
import urllib.request

from sie.config import load_config

WIKI_TITLES = {
    "NVDA": "Nvidia",
    "TSM": "TSMC",
    "CBRS": "Cerebras",
    "CRDO": "Credo_Technology",
    "MU": "Micron_Technology",
    "AMD": "Advanced_Micro_Devices",
    "AVGO": "Broadcom_Inc.",
    "ASML": "ASML_Holding",
}


def _wiki_pageviews(title: str) -> float | None:
    """Stdlib GET to Wikimedia pageviews. Returns WoW momentum or None."""
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=14)
    enc = urllib.parse.quote(title.replace(" ", "_"), safe="_")
    url = (
        "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
        f"en.wikipedia/all-access/user/{enc}/daily/"
        f"{start.strftime('%Y%m%d')}00/{end.strftime('%Y%m%d')}00"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "SIE/2.26 (educational)"})
    try:
        with urllib.request.urlopen(req, timeout=4) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        items = payload.get("items") or []
        views = [int(i.get("views", 0)) for i in items if i.get("views") is not None]
        if len(views) < 8:
            return None
        recent = sum(views[-7:]) / 7.0
        prior = sum(views[-14:-7]) / max(1, len(views[-14:-7]))
        if prior <= 0:
            return None
        return (recent / prior) - 1.0
    except Exception:
        return None


def detect_attention(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    at_cfg = cfg.get("attention", {})
    if not at_cfg.get("enabled", True):
        return {
            "attn_momentum": 0.0,
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Attention module disabled",
            "source": "disabled",
        }

    boost_th = float(at_cfg.get("boost_momentum", 0.25))
    penalty_th = float(at_cfg.get("penalty_momentum", -0.20))
    min_conf = float(at_cfg.get("min_confidence", 0.40))

    name = (row or {}).get("name") or ticker
    title = WIKI_TITLES.get(ticker.upper()) or str(name).replace(" ", "_")

    live = None
    if at_cfg.get("try_wikimedia", True):
        live = _wiki_pageviews(title)

    if live is not None:
        momentum = float(live)
        source = "public_wikimedia"
        conf_base = 0.62
    else:
        seed = sum(ord(c) for c in ticker.upper()) + datetime.now().timetuple().tm_yday + 53
        rng = random.Random(seed)
        momentum = round(rng.uniform(-0.35, 0.55), 3)
        source = "synthetic_proxy"
        conf_base = 0.48

    if momentum >= boost_th:
        boost = 1
        confidence = min(0.88, conf_base + 0.35 * min(momentum, 1.0))
        reason = f"Attention MOMENTUM +{momentum:.0%} ({title}) — retail search/pageview heat"
    elif momentum <= penalty_th:
        boost = -1
        confidence = min(0.82, conf_base + 0.25 * min(abs(momentum), 1.0))
        reason = f"Attention COOLING {momentum:.0%} ({title}) — fading retail interest"
    else:
        boost = 0
        confidence = conf_base
        reason = f"Attention stable {momentum:+.0%} ({title})"

    if confidence < min_conf and boost != 0:
        boost = 0
        reason += " (confidence below gate — signal suppressed)"

    return {
        "attn_momentum": round(float(momentum), 3),
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": reason,
        "source": source,
    }


def integrate_attention_to_row(row: dict, cfg: dict | None = None) -> dict:
    mom = detect_attention(row.get("ticker", ""), row, cfg)
    row.update({
        "attn_momentum": mom["attn_momentum"],
        "attn_boost": mom["signal_boost"],
        "attn_confidence": mom["confidence"],
        "attn_reason": mom["reason"],
        "attn_source": mom["source"],
    })
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 📈 {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 📈 {mom['reason']}"
    else:
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | Attention: {mom['reason']}"
    return row
