"""Cross-Ticker Narrative Contagion Detector.

Measures rapid transfer of narrative velocity and sentiment between related
tickers (equity clusters such as AI/semiconductor, consumer, energy) so the
engine can surface contagion risk or confirmation before pure single-ticker
social metrics fully move.

Uses a deterministic synthetic cluster-contagion proxy (ticker + day seeded)
with known thematic adjacency. Live multi-ticker social graph / velocity
correlation is left as an explicit future hook — no invented endpoints.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List
import random

from sie.config import load_config

# Thematic clusters used for synthetic contagion adjacency.
AI_CLUSTER = {"NVDA", "TSM", "AMD", "AVGO", "MU", "CRDO", "SMCI", "ASML", "AMAT", "LRCX", "KLAC", "CBRS"}
CONSUMER_CLUSTER = {"AAPL", "AMZN", "TSLA", "SBUX", "NKE", "MCD", "COST", "WMT"}
ENERGY_CLUSTER = {"XOM", "CVX", "COP", "SLB", "HAL"}
MEME_CLUSTER = {"GME", "AMC", "BB", "NOK"}

CLUSTERS = [AI_CLUSTER, CONSUMER_CLUSTER, ENERGY_CLUSTER, MEME_CLUSTER]


def _cluster_for(ticker: str) -> set:
    t = (ticker or "").upper()
    for c in CLUSTERS:
        if t in c:
            return c
    return set()


def detect_contagion(
    ticker: str,
    row: dict | None = None,
    cfg: dict | None = None,
) -> Dict[str, Any]:
    cfg = cfg or load_config()
    ct_cfg = cfg.get("contagion", {})
    if not ct_cfg.get("enabled", True):
        return {
            "ct_score": 0.0,
            "ct_velocity_transfer": 0.0,
            "ct_peers": [],
            "signal_boost": 0,
            "confidence": 0.0,
            "reason": "Cross-ticker narrative contagion module disabled",
            "source": "disabled",
        }

    boost_th = float(ct_cfg.get("boost_transfer", 0.35))
    penalty_th = float(ct_cfg.get("penalty_transfer", -0.25))
    min_conf = float(ct_cfg.get("min_confidence", 0.40))

    tkr = (ticker or "").upper()
    seed = sum(ord(c) for c in tkr) + datetime.now().timetuple().tm_yday + 211
    rng = random.Random(seed)

    cluster = _cluster_for(tkr)
    peers: List[str] = sorted([p for p in cluster if p != tkr])[:4]

    # Synthetic transfer velocity: positive = inbound contagion from peers.
    if cluster:
        transfer = round(rng.uniform(-0.45, 0.65), 3)
        # Bias AI cluster slightly higher in current theme.
        if tkr in AI_CLUSTER:
            transfer = round(min(0.72, transfer + 0.08), 3)
    else:
        transfer = round(rng.uniform(-0.18, 0.22), 3)
        peers = []

    # Map to 0-1 score for downstream.
    score = max(0.0, min(1.0, 0.5 + transfer * 0.9))

    source = "synthetic_cluster_proxy"
    conf_base = 0.50 if peers else 0.38

    if transfer >= boost_th and peers:
        boost = 1
        confidence = min(0.87, conf_base + 0.35 * min(transfer, 0.7))
        reason = (
            f"Inbound narrative contagion +{transfer:.0%} from peers {", ".join(peers[:3])} — "
            "cluster confirmation soft boost"
        )
    elif transfer <= penalty_th and peers:
        boost = -1
        confidence = min(0.83, conf_base + 0.30 * min(abs(transfer), 0.5))
        reason = (
            f"Outbound / reverse contagion {transfer:.0%} vs peers {", ".join(peers[:3])} — "
            "cluster caution"
        )
    else:
        boost = 0
        confidence = conf_base
        if peers:
            reason = f"Contagion neutral {transfer:+.0%} vs cluster peers {", ".join(peers[:3])}"
        else:
            reason = f"No strong thematic cluster adjacency (transfer {transfer:+.0%})"

    if confidence < min_conf and boost != 0:
        boost = 0
        reason += " (confidence below gate — signal suppressed)"

    return {
        "ct_score": round(float(score), 3),
        "ct_velocity_transfer": transfer,
        "ct_peers": peers,
        "signal_boost": int(boost),
        "confidence": round(float(confidence), 2),
        "reason": reason,
        "source": source,
    }


def integrate_contagion_to_row(row: dict, cfg: dict | None = None) -> dict:
    mom = detect_contagion(row.get("ticker", ""), row, cfg)
    row.update({
        "ct_score": mom["ct_score"],
        "ct_velocity_transfer": mom["ct_velocity_transfer"],
        "ct_peers": mom["ct_peers"],
        "ct_boost": mom["signal_boost"],
        "ct_confidence": mom["confidence"],
        "ct_reason": mom["reason"],
        "ct_source": mom["source"],
    })
    boost = mom["signal_boost"]
    if boost >= 1:
        if row.get("signal") in ("buy", "hold"):
            row["signal"] = "strong_buy" if boost >= 1 else row["signal"]
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 🔗 {mom['reason']}"
    elif boost <= -1:
        if row.get("signal") in ("strong_buy", "buy"):
            row["signal"] = "hold"
        else:
            row["signal"] = "caution"
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | 🔗 {mom['reason']}"
    else:
        row["signal_reason"] = (row.get("signal_reason") or "") + f" | Contagion: {mom['reason']}"
    return row
