# Stock Intelligence Engine

**Connect market narratives to your watchlist.  
Confirm with technicals.  
Explain every signal.**

**v2.18.0** — August 2026 · Same-Day SEC EDGAR Material Filing Detector + 0DTE Options Flow & Unusual Activity Proxy + Options IV Skew & Term Structure + Dark Pool / ATS Flow + Real-time Quotes + Congressional Trading + Portfolio Risk Overlay + Institutional 13F + Prediction Markets (Polymarket) + Insider Form 4 Clustering + Multi-source Narrative Velocity + Backtesting + Real-time Dashboard + X narratives

## Features

* Real-time signals with narrative intelligence
* **Same-Day SEC EDGAR Material Filing Detector** — Fresh 8-K / material filings with tone & materiality soft boost/penalty
* **0DTE Options Flow & Unusual Activity Proxy** — Near-expiry volume/OI spikes as short-horizon event / dealer-hedging signals
* **Options Implied Volatility Skew & Term Structure Overlay** — Free yfinance (or synthetic) options chains → put/call IV skew + term-structure slope
* **Dark Pool / ATS Off-Exchange Flow Overlay** — Elevated dark-pool volume ratios as institutional flow confirmation
* **Real-time WebSocket Price & Quote Feeds** — Low-latency quotes with stable fallback
* **Congressional Trading Overlay** — Clustered or large congressional buys/sells as smart-money layer
* **Portfolio Correlation Heatmap & Risk Overlay**
* **Institutional 13F Ownership Change Detector**
* **Prediction Market Odds Overlay (Polymarket)**
* **Insider Form 4 Clustering & Confirmation Signals**
* **Multi-source Narrative Velocity Forecasting**
* X/Twitter dominant narrative, velocity & crisis flags
* FinBERT + VADER news sentiment
* Telegram alerts (optional)
* Backtesting framework
* Streamlit real-time dashboard

## Quick Start

```bash
git clone https://github.com/Stijnman/stock-intelligence-engine.git
cd stock-intelligence-engine
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env        # optional: add X bearer token, Telegram, etc.
python stock_intelligence_engine.py
streamlit run app.py
```

## CLI Flags

```
--backtest          Run simple backtest
--portfolio         Portfolio correlation & risk metrics
--export            Export rows to CSV
--no-edgar          Disable Same-Day SEC EDGAR detector
--no-options-0dte   Disable 0DTE options flow
--no-options-iv     Disable IV skew overlay
--no-dark-pool      Disable dark-pool overlay
--no-realtime       Disable realtime quotes
--no-congress       Disable congressional overlay
--no-13f            Disable institutional 13F
--no-pm             Disable prediction markets
--no-insider        Disable insider Form 4
```

## Configuration

Edit `config.yaml` (or rely on defaults in `sie/config.py`). New sections:

```yaml
edgar:
  enabled: true
  lookback_hours: 36
  min_materiality: 0.55
  boost_on_positive: true
  penalty_on_negative: true
  min_confidence: 0.40

options_0dte:
  enabled: true
  min_volume_spike: 2.5
  min_oi_ratio: 1.8
  boost_threshold: 0.6
  penalty_threshold: 0.55
  min_confidence: 0.40
```

## Recent Edits & Version History

* **v2.18.0 (2026-08-16)**: Autonomous maintainer cycle. Fully integrated **Same-Day SEC EDGAR Material Filing Detector** into analyzer, CLI, dashboard and config. Confirmed 0DTE wiring and defaults. Restored README + CHANGELOG from placeholders. Marked both features complete in FUTURE-IMPROVEMENTS.md. Version bump across all entry points.
* **v2.17.0**: Intermediate preparation of EDGAR + 0DTE surfaces.
* **v2.16.x**: CI hardening, public API repair, docs.
* **v2.15.x – v2.4.0**: Progressive addition of options IV, dark pool, realtime, congressional, 13F, Polymarket, insider, narrative velocity, X intelligence, dashboard and backtesting.

See [CHANGELOG.md](CHANGELOG.md) and [FUTURE-IMPROVEMENTS.md](FUTURE-IMPROVEMENTS.md) for the full roadmap.

## Disclaimer

This is research / educational software only. Not financial advice. Past performance is not indicative of future results. Always do your own due diligence.

## License

MIT — see LICENSE.
