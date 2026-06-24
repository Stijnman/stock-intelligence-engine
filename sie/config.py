"""Load configuration from config.yaml with defaults."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

DEFAULT_TICKERS: dict[str, dict[str, str]] = {
    "NVDA": {
        "name": "NVIDIA",
        "color": "🟢",
        "note": "Strongest winner - inference boom",
        "narrative_fit": "strong",
    },
    "TSM": {
        "name": "TSMC",
        "color": "🟢",
        "note": "Quiet chip enabler",
        "narrative_fit": "strong",
    },
    "CBRS": {
        "name": "Cerebras",
        "color": "🟢",
        "note": "Pure specialized inference play (volatile)",
        "narrative_fit": "strong",
    },
    "CRDO": {
        "name": "Credo",
        "color": "🟡",
        "note": "Viral AI connectivity play",
        "narrative_fit": "monitor",
    },
    "MU": {
        "name": "Micron",
        "color": "🟡",
        "note": "HBM memory - inference critical",
        "narrative_fit": "monitor",
    },
}

DEFAULT_CONFIG: dict[str, Any] = {
    "narrative": {"theme": "AI Inference Boom"},
    "technical": {
        "rsi_period": 14,
        "rsi_overbought": 70,
        "rsi_oversold": 30,
        "ma_fast": 50,
        "ma_slow": 200,
    },
    "tickers": DEFAULT_TICKERS,
    "export": {"directory": "exports"},
    "alerts": {"email": False},
}


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    cfg = {**DEFAULT_CONFIG, "tickers": dict(DEFAULT_TICKERS)}
    config_path = Path(path or Path(__file__).resolve().parent.parent / "config.yaml")
    if not config_path.is_file():
        return cfg

    with config_path.open(encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    if theme := raw.get("narrative", {}).get("theme"):
        cfg["narrative"]["theme"] = theme
    if tech := raw.get("technical"):
        cfg["technical"].update(tech)
    if tickers := raw.get("tickers"):
        if isinstance(tickers, dict):
            cfg["tickers"] = tickers
        elif isinstance(tickers, list):
            cfg["tickers"] = {t: DEFAULT_TICKERS.get(t, {"name": t, "color": "🟡", "note": "", "narrative_fit": "monitor"}) for t in tickers}
    if alerts := raw.get("alerts"):
        cfg["alerts"].update(alerts)
    if export := raw.get("export"):
        cfg["export"].update(export)
    return cfg