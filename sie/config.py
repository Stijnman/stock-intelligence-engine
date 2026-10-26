"""Load configuration from config.yaml with defaults."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG: dict[str, Any] = {
    "signed_options_flow_toxicity": {
        "enabled": True,
        "tox_hot": 0.28,
        "tox_cold": 0.72,
        "inf_hot": 0.68,
        "inf_cold": 0.32,
        "narrative_hot": 1.4,
        "min_confidence": 0.40,
    },
    "unified_multi_source_narrative_freshness": {
        "enabled": True,
        "fresh_hot_s": 180.0,
        "fresh_cold_s": 1200.0,
        "sources_hot": 0.75,
        "sources_cold": 0.35,
        "narrative_hot": 1.4,
        "min_confidence": 0.40,
    },
    "expert_network_call_novelty": {
        "enabled": True,
        "nov_hot": 0.68,
        "nov_cold": 0.32,
        "vel_hot": 0.55,
        "vel_cold": -0.35,
        "narrative_hot": 1.4,
        "min_confidence": 0.40,
    },
    "tickers": {
        "NVDA": {},
        "TSLA": {},
        "AAPL": {},
        "MSFT": {},
        "INTC": {},
    },
}


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    cfg = {**DEFAULT_CONFIG}
    path = Path(path or "config.yaml")
    if path.exists():
        try:
            with path.open() as f:
                raw = yaml.safe_load(f) or {}
            for key in DEFAULT_CONFIG:
                if key in raw and isinstance(raw[key], dict):
                    cfg[key].update(raw[key])
            if "tickers" in raw:
                cfg["tickers"] = raw["tickers"]
        except Exception:
            pass
    return cfg
