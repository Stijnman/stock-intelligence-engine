"""Shared cache, HTTP and normalized observation primitives (stdlib only)."""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

CACHE_DIR = Path(os.getenv("SIE_CACHE_DIR", Path.home() / ".cache/stock-intelligence"))
CACHE_DIR.mkdir(parents=True, exist_ok=True)
USER_AGENT = os.getenv("SIE_USER_AGENT", "InvestmentIntelligenceEngine/0.2 (public-data research)")


@dataclass
class Observation:
    source: str
    dataset: str
    series: str
    period: str
    value: float
    unit: str | None = None
    currency: str | None = None
    currency_denom: str | None = None
    retrieved_at: str | None = None
    published_at: str | None = None
    status: str | None = None
    source_url: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _cache_path(key: str) -> Path:
    safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in key)
    return CACHE_DIR / f"public-{safe}.json"


def get_bytes(url: str, *, cache_key: str, ttl: int = 86400,
              accept: str = "application/json", headers: dict[str, str] | None = None) -> bytes:
    path = _cache_path(cache_key)
    if path.exists() and time.time() - path.stat().st_mtime < ttl:
        try:
            return bytes.fromhex(json.loads(path.read_text(encoding="utf-8"))["hex"])
        except (OSError, ValueError, KeyError, json.JSONDecodeError):
            pass
    request_headers = {"User-Agent": USER_AGENT, "Accept": accept}
    request_headers.update(headers or {})
    req = urllib.request.Request(url, headers=request_headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            body = response.read()
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"Public data request failed ({urllib.parse.urlparse(url).netloc}): {exc}") from exc
    path.write_text(json.dumps({"hex": body.hex()}), encoding="utf-8")
    return body


def get_json(url: str, *, cache_key: str, ttl: int = 86400) -> dict[str, Any]:
    body = get_bytes(url, cache_key=cache_key, ttl=ttl)
    try:
        return json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Invalid JSON response from {urllib.parse.urlparse(url).netloc}") from exc
