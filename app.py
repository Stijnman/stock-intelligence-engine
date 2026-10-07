"""Stock Intelligence Engine — Streamlit Dashboard v2.55.0.

Alternative-Data Provenance & AI-Synthetic Contamination Overlay +
Primary Credit Issuance / New-Issue Concession Overlay +
TRACE Corporate-Bond Customer-Flow Overlay +
Secondary Offering / ATM Dilution Velocity Overlay +
News Materiality / Predicted Next-Session Impact Score Overlay +
Cross-Venue Tokenized-Share Basis Overlay +
Job-Posting Skill-Mix & Posted-Compensation Inflation Overlay +
Retail Brokerage Order-Flow Imbalance Overlay +
App-Store Review Sentiment & Complaint Velocity Overlay +
Employee Outlook / Glassdoor + Unusual Options Sweep vs Block +
Rule 10b5-1 / Buyback Overlay + ETF AP Flow.
"""
from __future__ import annotations

import streamlit as st
import pandas as pd
from sie.config import load_config
from sie.analyzer import run_report

__version__ = "2.55.0"

st.set_page_config(page_title="Stock Intelligence Engine", layout="wide")

with st.sidebar:
    st.header("Dashboard Controls")
    cfg = load_config()
    refresh_interval = int(cfg.get("dashboard", {}).get("refresh_interval", 60) or 0)
    st.caption(f"Auto-refresh interval: {refresh_interval}s (0 = off)")
    force_full = st.button("Force Full Refresh", type="primary", use_container_width=True)
    st.divider()
    st.markdown(
        f"**v{__version__}** — Rule 606 Routing + Alt-Data Provenance + Target-Specific Stance + Primary Credit Issuance + TRACE Customer-Flow + ATM Dilution Velocity + News Materiality + Tokenized-Share Basis + Job-Posting Skill-Mix + Retail Order-Flow Imbalance + App-Store Review Sentiment & Complaint Velocity + Employee Outlook / Glassdoor + Unusual Options + 10b5-1 / Buyback + KOL + Whisper + News Authority + Earnings-Call + CDS + Social Intent + GEX + Digital Footprint"
    )

st.title(f"Stock Intelligence Engine v{__version__}")
st.metric("Engine Version", __version__)

@st.fragment(run_every=refresh_interval if refresh_interval > 0 else None)
def signal_table_fragment():
    result = run_report(export=False, backtest=False)
    report = result.get("report") if isinstance(result, dict) else result
    rows = report.get("rows", []) if isinstance(report, dict) else []
    if not rows:
        st.warning("No data returned from analyzer.")
        return
    df = pd.DataFrame(rows)
    preferred = [
        "ticker", "name", "signal", "score", "rsi", "price",
        "r606_concentration", "r606_exec_quality", "r606_boost", "r606_reason",
        "adp_provenance", "adp_crosscheck", "adp_boost", "adp_reason",
        "tsn_stance", "tsn_specificity", "tsn_qa_gap", "tsn_boost", "tsn_reason",
        "asr_sentiment", "asr_complaint_velocity", "asr_rating", "asr_boost", "asr_reason",
        "pci_concession_bp", "pci_supply_score", "pci_boost", "pci_reason",
        "trace_customer_flow", "trace_liq_score", "trace_boost", "trace_reason",
        "dil_atm_velocity", "dil_share_delta", "dil_boost", "dil_reason",
        "nimp_score", "nimp_vol_bucket", "nimp_boost", "nimp_reason",
        "tok_basis_bps", "tok_venue_liq", "tok_boost", "tok_reason",
        "hmix_senior_share", "hmix_comp_delta", "hmix_boost", "hmix_reason",
        "rflow_imbalance", "rflow_heat", "rflow_boost", "rflow_reason",
        "eo_outlook", "eo_ceo", "eo_boost", "eo_reason",
        "uopt_sweep_score", "uopt_boost", "uopt_reason",
        "confidence_score", "market_regime", "brief", "thesis_bull", "thesis_bear",
    ]
    cols = [c for c in preferred if c in df.columns] + [c for c in df.columns if c not in preferred]
    st.dataframe(df[cols], use_container_width=True, height=600)

signal_table_fragment()

st.divider()
st.caption(
    f"v{__version__} — Rule 606 Retail Options Routing & Execution-Quality Overlay fully wired. Educational research tool only — not financial advice."
)
