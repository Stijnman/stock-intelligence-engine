# Stock Intelligence Engine

**Connect market narratives to your watchlist. Confirm with technicals. Explain every signal.**

**v2.8.1** — July 2026 · Insider Form 4 Clustering + Multi-source Narrative Velocity Forecasting + Backtesting + Real-time Dashboard + X narratives

## Features
- Real-time signals with narrative intelligence
- **Insider Form 4 Clustering & Confirmation Signals** — Detects clustered insider buying/selling (yfinance + proxy) within a 14-day window and applies confirmation boost/penalty to signals; surfaces cluster size, net shares, side and confidence in dashboard & alerts
- **Multi-source Narrative Velocity Forecasting** - Predicts 1-3 day narrative phase shifts (hype/dip/recovery) from X velocity + news sentiment using exponential smoothing; applies boost/penalty to signals
- **Backtesting Framework** - Validate historical performance with Sharpe ratios
- Streamlit dashboard with live updates & auto-refresh
- X/Twitter dominant narrative, velocity & crisis flags
- FinBERT + VADER news sentiment
- Telegram alerts

## Recent Edits & Version History
- **v2.8.1 (2026-07-30)**: Autonomous research & evolution cycle. Full code audit confirmed no open FUTURE-IMPROVEMENTS items were newly implemented. Added 5 high-value improvements from fresh July 30 2026 research (Prediction Market Odds Overlay (Polymarket), Short Interest & Squeeze Risk Monitor, Congressional Trading Overlay, Earnings Whisper vs Actual Surprise Integration, Multi-LLM Ensemble Narrative Extractor). Roadmap and docs synchronized. Version bump only — no core logic changes.
- **v2.8.0 (2026-07-29)**: Implemented **Insider Form 4 Clustering & Confirmation Signals**. New module `sie/insider.py` fetches recent insider transactions via yfinance (with realistic synthetic proxy fallback), detects buy/sell clusters within configurable lookback, and applies signal boost/penalty. Fully integrated into analyzer, CLI (`--no-insider` flag), Streamlit dashboard (live cluster metrics + captions), config.yaml (`insider:` section), and Telegram body path. Version bumped across all entry points and docs.
- **v2.7.2 (2026-07-29)**: Autonomous research & evolution cycle. Full code audit confirmed no open FUTURE-IMPROVEMENTS items were newly implemented. Added 5 high-value improvements from fresh July 29 2026 research (Real-time WebSocket Price & Quote Feeds, Podcast & Alternative Media Sentiment Layer, Employee Outlook & Glassdoor Sentiment Signals, HMM / Regime Detection Filter, MCP-Native Agent Data Hooks). Roadmap and docs synchronized. Version bump only — no core logic changes.
- **v2.7.1 (2026-07-28)**: Autonomous research & evolution cycle. Full code audit confirmed no open FUTURE-IMPROVEMENTS items were newly implemented. Added 5 high-value improvements from fresh July 2026 research (Insider Form 4 clustering, Cross-Platform Narrative Convergence Score, Analyst Estimate Revision Momentum, Grok/xAI Agent Deep-Research Hook, Alternative Data Proxies). Roadmap and docs synchronized. Version bump only — no core logic changes.
- **v2.7.0 (2026-07-25)**: Implemented Multi-source Narrative Velocity Forecasting. Simple exponential smoothing on combined X sentiment velocity + news FinBERT/VADER scores. Forward-looking phase prediction (hype/dip/recovery) with signal boost/penalty. Integrated in analyzer, CLI path, and Streamlit dashboard. Config options under `forecast:`. [Commit](https://github.com/Stijnman/stock-intelligence-engine/commit/3f0697667e4cac32032b207bad324a51414e231b)
- **v2.6.1 (2026-07-25)**: Autonomous research cycle — cleaned completed roadmap items (narrative phases already in social.py, pytest present, VADER fallback covered). Added 5 new high-value 2026 improvements (narrative velocity forecasting, portfolio risk heatmap, Streamlit fragments/caching, SEC 8-K NLP, unusual options/dark-pool). Docs & version sync.
- **v2.6.0 (2026-07-23)**: Implemented Backtesting Framework. CLI `--backtest`, dashboard button, integrated metrics. [Commit](https://github.com/Stijnman/stock-intelligence-engine/commit/ead6af1db28485a90c302f5169dfbaf118101320)

## Version highlights

| Version | Notes |
|---------|--------|
| 2.8.1 | Roadmap refresh + 5 new 2026 research items |
| 2.8.0 | Insider Form 4 Clustering & Confirmation Signals |
| 2.7.2 | Roadmap refresh + 5 new 2026 research items |
| 2.7.1 | Roadmap refresh + 5 new 2026 research items |
| 2.7.0 | Multi-source Narrative Velocity Forecasting |
| 2.6.1 | Roadmap cleanup + fresh 2026 research items |
| 2.6.0 | Backtesting Framework added |
| 2.5.2 | Fresh research-driven roadmap updates |
| 2.5.0 | Real-time Streamlit auto-refresh |
| 2.4.0 | X narrative intelligence |

**Usage:** `python stock_intelligence_engine.py --backtest`  
**Dashboard:** `streamlit run app.py`

## Insider Clustering (v2.8.0)

```yaml
insider:
  enabled: true
  lookback_days: 14
  min_cluster_size: 2
  buy_boost_min: 2
  sell_penalty_min: 2
```

When ≥2 Form-4-style buys (or sells) appear inside the lookback window the engine raises (or lowers) the signal and appends a clear reason string visible in both the CLI report and the live dashboard.
