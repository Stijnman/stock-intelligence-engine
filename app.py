"""Stock Intelligence Engine — Streamlit Dashboard v2.24.0.

Streamlit Fragment Live Dashboard Refresh:
- Uses @st.fragment(run_every=...) for selective auto-refresh of the live signal
  table and status cards without full-script reruns.
- Honours config.yaml dashboard.refresh_interval (seconds; 0 disables auto).
- Manual "Force Full Refresh" still available for complete pipeline re-run.
- Fully wired Signal Confidence Calibration & Self-Critique.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pandas as pd
import streamlit as st

from sie.analyzer import analyze_watchlist
from sie.config import load_config

__version__ = "2.24.0"

st.set_page_config(
    page_title="Stock Intelligence Engine",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Sidebar controls
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Dashboard Controls")
    cfg = load_config()
    refresh_interval = int(cfg.get("dashboard", {}).get("refresh_interval", 60) or 0)
    st.caption(f"Auto-refresh interval: {refresh_interval}s (0 = off)")
    force_full = st.button("Force Full Refresh", type="primary", use_container_width=True)
    st.divider()
    st.markdown(
        f"**v{__version__}** — Fragment Live Refresh + Confidence Calibration + Honesty Detector + "
        "Thesis + Brief + Hiring + EDGAR + 0DTE + IV + Dark Pool + Realtime + "
        "Congressional + 13F + Polymarket + Insider + Narrative Velocity"
    )

# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------
st.title(
    f"Stock Intelligence Engine v{__version__} — "
    "Streamlit Fragment Live Dashboard Refresh + "
    "Signal Confidence Calibration + LLM Self-Critique + "
    "LLM Bull/Bear Thesis + Self-Explaining Signal Brief + "
    "Honesty / Contradiction Detector + Corporate Hiring + Same-Day SEC EDGAR + "
    "0DTE Options Flow + Options IV Skew + Dark Pool / ATS Flow + Real-time Quotes + "
    "Congressional + Portfolio Correlation + Institutional 13F + Prediction Markets + "
    "Insider Clusters + Narrative Velocity"
)

# ---------------------------------------------------------------------------
# Cached full analysis (expensive path)
# ---------------------------------------------------------------------------
@st.cache_data(ttl=300, show_spinner=False)
def _run_full_analysis(_cfg_hash: str, cfg: dict[str, Any]) -> dict[str, Any]:
    """Run the complete analysis pipeline. Cache keyed by a simple config fingerprint."""
    return analyze_watchlist(cfg)


def _cfg_fingerprint(cfg: dict[str, Any]) -> str:
    """Cheap stable fingerprint so cache invalidates when watchlist/theme changes."""
    tickers = sorted((cfg.get("tickers") or {}).keys())
    theme = (cfg.get("narrative") or {}).get("theme", "")
    return f"{theme}|{','.join(tickers)}"


# Force full refresh clears cache and re-runs
if force_full:
    st.cache_data.clear()
    st.rerun()

# ---------------------------------------------------------------------------
# Live status fragment (lightweight, runs every N seconds)
# ---------------------------------------------------------------------------
@st.fragment(run_every=refresh_interval if refresh_interval > 0 else None)
def live_status_fragment() -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Last Live Tick", now)
    with col2:
        st.metric("Auto-Refresh", f"{refresh_interval}s" if refresh_interval > 0 else "Off")
    with col3:
        st.metric("Engine Version", __version__)
    st.caption(
        "Live status fragment updates independently. Full signal table below uses "
        "cached analysis (TTL 5 min) and is refreshed by the same fragment timer "
        "or by the Force Full Refresh button."
    )


live_status_fragment()

# ---------------------------------------------------------------------------
# Main signal table fragment (also on the same timer)
# ---------------------------------------------------------------------------
@st.fragment(run_every=refresh_interval if refresh_interval > 0 else None)
def signal_table_fragment() -> None:
    with st.spinner("Loading / refreshing analysis…"):
        report = _run_full_analysis(_cfg_fingerprint(cfg), cfg)
    rows = report.get("rows", [])
    if not rows:
        st.warning("No analysis rows returned. Check config.yaml tickers and data sources.")
        return

    df = pd.DataFrame(rows)
    # Prefer a readable column order if present
    preferred = [
        "ticker", "name", "signal", "score", "rsi", "price", "change_pct",
        "confidence_score", "confidence_label", "honesty_risk", "honesty_label",
        "brief", "thesis_bull", "thesis_bear",
        "narrative_phase", "velocity", "reasons",
    ]
    ordered = [c for c in preferred if c in df.columns] + [
        c for c in df.columns if c not in preferred
    ]
    df = df[ordered]

    st.subheader("Live Signal Table")
    st.dataframe(
        df,
        use_container_width=True,
        height=min(600, 40 + 35 * len(df)),
        hide_index=True,
    )

    # Quick summary metrics
    if "signal" in df.columns:
        buys = (df["signal"].astype(str).str.contains("buy", case=False, na=False)).sum()
        holds = (df["signal"].astype(str).str.contains("hold", case=False, na=False)).sum()
        cautions = (df["signal"].astype(str).str.contains("caution|sell", case=False, na=False)).sum()
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Tickers", len(df))
        m2.metric("Buy / Strong Buy", int(buys))
        m3.metric("Hold", int(holds))
        m4.metric("Caution / Sell", int(cautions))


signal_table_fragment()

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.divider()
st.caption(
    f"v{__version__} — Streamlit Fragment Live Dashboard Refresh + Confidence Calibration fully wired · "
    "Honesty Signal Detector · Thesis · Brief · Hiring · EDGAR · 0DTE · Options IV · "
    "Dark Pool · Realtime · Congressional · 13F · Polymarket · Insider · Narrative Velocity. "
    "Educational research tool only — not financial advice."
)
