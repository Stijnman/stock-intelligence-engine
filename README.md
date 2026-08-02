# Stock Intelligence Engine

**Connect market narratives to your watchlist. Confirm with technicals. Explain every signal.**

**v2.12.0** — August 2026 · Congressional Trading Overlay + Portfolio Correlation Heatmap & Risk Overlay + Institutional 13F Ownership Change Detector + Prediction Market Odds Overlay (Polymarket) + Insider Form 4 Clustering + Multi-source Narrative Velocity Forecasting + Backtesting + Real-time Dashboard + X narratives

## Features
- Real-time signals with narrative intelligence
- **Congressional Trading Overlay** — Detects clustered or material congressional stock buys/sells (stable synthetic proxy) and applies soft confirmation/penalty as smart-money layer; surfaces trade count, net value, side and confidence in dashboard & alerts
- **Portfolio Correlation Heatmap & Risk Overlay** — Computes pairwise daily-return correlations and equal-weight portfolio metrics (annualized volatility, Sharpe, max drawdown, mean correlation); interactive Plotly heatmap in dashboard + CLI `--portfolio`
- **Institutional 13F Ownership Change Detector** — Detects significant institutional ownership increases/decreases (yfinance + synthetic QoQ proxy) and applies soft confirmation/penalty as smart-money flow overlay; surfaces top holders delta, net shares change and confidence in dashboard & alerts
- **Prediction Market Odds Overlay (Polymarket)** — Ingests free Gamma API odds for company/sector events, detects divergence from narrative+technical signal, and applies soft boost/penalty; surfaces probability, best question, confidence and source in dashboard & alerts
- **Insider Form 4 Clustering & Confirmation Signals** — Detects clustered insider buying/selling (yfinance + proxy) within a 14-day window and applies confirmation boost/penalty to signals; surfaces cluster size, net shares, side and confidence in dashboard & alerts
- **Multi-source Narrative Velocity Forecasting** - Predicts 1-3 day narrative phase shifts (hype/dip/recovery) from X velocity + news sentiment using exponential smoothing; applies boost/penalty to signals
- **Backtesting Framework** - Validate historical performance with Sharpe ratios
- Streamlit dashboard with live updates & auto-refresh
- X/Twitter dominant narrative, velocity & crisis flags
- FinBERT + VADER news sentiment
- Telegram alerts

## Recent Edits & Version History
- **v2.12.0 (2026-08-02)**: Implemented **Congressional Trading Overlay**. New module `sie/congressional.py` detects clustered congressional buys/sells via stable synthetic proxy (no paid API), applies soft signal boost/penalty, surfaces trade count / net value / side / confidence. Fully integrated into Streamlit dashboard (live Congress metrics + captions), CLI (`--no-congress`), config.yaml (`congressional:` section). Version bumped across all entry points and docs.
- **v2.11.0 (2026-08-01)**: Implemented **Portfolio Correlation Heatmap & Risk Overlay**. New module `sie/portfolio.py` downloads multi-ticker adjusted closes via yfinance, computes Pearson correlation of daily returns, equal-weight portfolio volatility / Sharpe / max drawdown / mean pairwise correlation. Fully integrated into Streamlit dashboard (interactive Plotly heatmap + metric cards), CLI (`--portfolio` flag and appended to `--backtest`), config.yaml (`portfolio:` section with lookback, min_periods, risk_free_rate). Version bumped across all entry points and docs.
- **v2.10.1 (2026-08-01)**: Autonomous research & evolution cycle. Full code audit confirmed Institutional 13F Ownership Change Detector fully implemented and live; no additional open FUTURE-IMPROVEMENTS items newly completed. Added 5 new high-value 2026 improvements (Congressional Stock Trade Monitor, Activist Ownership Change Detector, Multi-source Sentiment Momentum Oscillator, High-Impact Political / Truth Social Narrative Injector, Lightweight Channel-Check / Expert Sentiment Proxy). Docs & version sync.
- **v2.10.0 (2026-07-31)**: Implemented **Institutional 13F Ownership Change Detector**. New module `sie/institutional.py` fetches institutional holders via yfinance (with realistic synthetic QoQ proxy fallback), detects significant ownership increases/decreases by large funds, and applies soft signal boost/penalty. Fully integrated into analyzer, CLI (`--no-13f` flag), Streamlit dashboard (live 13F metrics + captions), config.yaml (`institutional:` section). Version bumped across all entry points and docs.
- **v2.9.1 (2026-07-31)**: Autonomous research & evolution cycle. Full code audit confirmed Prediction Market Odds Overlay (Polymarket) fully implemented and live; no additional open FUTURE-IMPROVEMENTS items newly completed. Added 5 high-value improvements from fresh research.
- **v2.9.0 (2026-07-30)**: Prediction Market Odds Overlay (Polymarket).
- **v2.8.0 (2026-07-29)**: Insider Form 4 Clustering & Confirmation Signals.
- **v2.7.0 (2026-07-25)**: Multi-source Narrative Velocity Forecasting.
- **v2.6.0 (2026-07-23)**: Backtesting Framework.

## Version highlights

| Version | Notes |
|---------|--------|
| 2.12.0 | Congressional Trading Overlay |
| 2.11.0 | Portfolio Correlation Heatmap & Risk Overlay |
| 2.10.1 | Roadmap refresh + 5 new 2026 research items |
| 2.10.0 | Institutional 13F Ownership Change Detector |
| 2.9.1 | Roadmap refresh + 5 new 2026 research items |
| 2.9.0 | Prediction Market Odds Overlay (Polymarket) |
| 2.8.0 | Insider Form 4 Clustering & Confirmation Signals |
| 2.7.0 | Multi-source Narrative Velocity Forecasting |
| 2.6.0 | Backtesting Framework added |
| 2.5.0 | Real-time Streamlit auto-refresh |
| 2.4.0 | X narrative intelligence |

**Usage:** `python stock_intelligence_engine.py --portfolio` or `--backtest`  
**Dashboard:** `streamlit run app.py`

## Congressional Overlay (v2.12.0)

```yaml
congressional:
  enabled: true
  lookback_days: 90
  min_trades: 2
  buy_boost_min: 2
  sell_penalty_min: 2
  min_trade_value: 15000
```

## Portfolio Overlay (v2.11.0)

```yaml
portfolio:
  enabled: true
  lookback_period: "1y"
  min_periods: 30
  risk_free_rate: 0.04
```
