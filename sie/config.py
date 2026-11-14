"""Load configuration from config.yaml with isolated defaults."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_CONFIG: dict[str, Any] = {
    "signed_options_flow_toxicity": {
        "enabled": True, "tox_hot": 0.28, "tox_cold": 0.72,
        "inf_hot": 0.68, "inf_cold": 0.32, "narrative_hot": 1.4,
        "min_confidence": 0.40,
    },
    "unified_multi_source_narrative_freshness": {
        "enabled": True, "fresh_hot_s": 180.0, "fresh_cold_s": 1200.0,
        "sources_hot": 0.75, "sources_cold": 0.35, "narrative_hot": 1.4,
        "min_confidence": 0.40,
    },
    "expert_network_call_novelty": {
        "enabled": True, "nov_hot": 0.68, "nov_cold": 0.32,
        "vel_hot": 0.55, "vel_cold": -0.35, "narrative_hot": 1.4,
        "min_confidence": 0.40,
    },
    "agentic_mcp_tool_call_latency": {
        "enabled": True, "lat_hot": 180.0, "lat_cold": 1200.0,
        "succ_hot": 0.82, "succ_cold": 0.45, "narrative_hot": 1.4,
        "min_confidence": 0.40,
    },
    "tokenized_equity_premium": {
        "enabled": True, "basis_hot_bps": 45.0, "basis_cold_bps": -25.0,
        "vol_hot": 0.28, "vol_cold": 0.08, "narrative_hot": 1.4,
        "min_confidence": 0.40,
    },
    "tickers": {"NVDA": {}, "TSLA": {}, "AAPL": {}, "MSFT": {}, "INTC": {}},
}


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    """Load YAML over a fresh deep copy of defaults.

    Relative config paths resolve from the repository root, not the caller's
    current working directory (important for Docker and Streamlit launches).
    """
    cfg = deepcopy(DEFAULT_CONFIG)
    config_path = Path(path) if path is not None else PROJECT_ROOT / "config.yaml"
    if not config_path.is_absolute():
        config_path = PROJECT_ROOT / config_path
    if not config_path.exists():
        return cfg
    with config_path.open(encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}
    if not isinstance(raw, dict):
        raise ValueError(f"Configuration must be a YAML mapping: {config_path}")
    for key, value in raw.items():
        if key == "tickers":
            if not isinstance(value, dict):
                raise ValueError("'tickers' must be a mapping of ticker to options")
            cfg[key] = value
        elif isinstance(value, dict) and isinstance(cfg.get(key), dict):
            cfg[key].update(value)
        else:
            cfg[key] = value
    return cfg
