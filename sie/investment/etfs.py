"""ETF diagnostics from verified, user-supplied issuer metadata."""
from typing import Any

def analyze_etf(metadata: dict[str, Any]) -> dict[str, Any]:
    required = ("ticker", "ter_pct", "aum", "domicile", "ucits", "distribution")
    missing = [key for key in required if metadata.get(key) in (None, "")]
    return {"ticker": metadata.get("ticker"), "metadata": metadata, "missing_fields": missing,
            "data_completeness_pct": round((len(required) - len(missing)) / len(required) * 100, 1),
            "checks": {"ucits": metadata.get("ucits"), "distribution": metadata.get("distribution"),
                       "annual_cost_per_10000": float(metadata["ter_pct"]) / 100 * 10000 if metadata.get("ter_pct") is not None else None,
                       "aum": metadata.get("aum"), "domicile": metadata.get("domicile"),
                       "replication": metadata.get("replication"), "benchmark": metadata.get("benchmark"),
                       "holdings_count": metadata.get("holdings_count")},
            "warning": "Verify TER, AUM, domicile, UCITS and holdings against the latest issuer KID/factsheet. Missing data remains blank."}
