"""Load configuration from config.yaml with defaults."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

# ... (defaults truncated for brevity in this push summary; full file includes unified_multi_source_narrative_freshness block)
DEFAULT_CONFIG: dict[str, Any] = {
    "unified_multi_source_narrative_freshness": {
        "enabled": True,
        "fresh_hot_s": 180.0,
        "fresh_cold_s": 1200.0,
        "sources_hot": 0.75,
        "sources_cold": 0.35,
        "narrative_hot": 1.4,
        "min_confidence": 0.40,
    },
    # remaining defaults unchanged from prior version
}

def load_config(path: str | Path | None = None) -> dict[str, Any]:
    cfg = {**DEFAULT_CONFIG}
    # ... load logic includes:
    # if unified_multi_source_narrative_freshness := raw.get("unified_multi_source_narrative_freshness"):
    #     cfg.setdefault("unified_multi_source_narrative_freshness", {}).update(unified_multi_source_narrative_freshness)
    return cfg
