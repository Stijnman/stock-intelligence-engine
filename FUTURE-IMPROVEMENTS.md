# Roadmap

See [COMPETITION.md](COMPETITION.md) for full competitive analysis.

## High Priority

- [x] **X/Twitter Narrative Intelligence Integration** (v2.4.0): Real-time sentiment velocity, dominant narratives, key voices, and crisis flags using specialized logic in social.py. Enhances social.py, alerts, CLI, Streamlit dashboard. 2026-07-17

- [x] **Multi-source Narrative Velocity Forecasting** (v2.7.0): Time-series forecasting (simple exponential smoothing on rolling windows) of combined X sentiment velocity + news FinBERT/VADER scores to predict short-term narrative phase shifts (hype → dip) 1–3 days ahead. Integrated as forward-looking signal boost/penalty in analyzer, CLI, and Streamlit dashboard. 2026-07-25 https://github.com/Stijnman/stock-intelligence-engine/commit/3f0697667e4cac32032b207bad324a51414e231b

## Medium Priority

- [x] **Real-time Streamlit Dashboard** (v2.5.0): Auto-refresh with st.rerun, configurable interval, live price/signal/narrative updates. Integrated into app.py with progress indicators. 2026-07-20

- [ ] **Portfolio Correlation Heatmap & Risk Overlay**: Compute pairwise returns correlations and portfolio-level metrics (max drawdown, volatility, Sharpe of equal-weight basket) inside backtest + dashboard. Display interactive Plotly heatmap and risk summary for the full watchlist.

- [ ] **Streamlit Partial Reruns + Advanced Caching (2026 patterns)**: Refactor dashboard to use `@st.fragment` for independent live-price and narrative sections, `st.cache_data` with TTL for yfinance/X calls, and avoid full-page `st.rerun()` loops where possible. Improves responsiveness and reduces API rate-limit pressure.

## Completed

- [x] **Backtesting Framework** (v2.6.0): Historical signal performance evaluation with Sharpe ratio and returns metrics. Integrated into CLI (`--backtest`), Streamlit dashboard (button), and analyzer. 2026-07-23 https://github.com/Stijnman/stock-intelligence-engine/commit/ead6af1db28485a90c302f5169dfbaf118101320

- [x] **Narrative Phase Labels (Hype / Dip / Recovery)** (v2.6.1): Already implemented via dominant_narrative extraction in social.py (hype/dip/recovery/crisis keywords + Counter). Exposed in dashboard and row data. Cleaned from open items.

- [x] **pytest for RSI/MA math** (v2.6.1): Basic unit tests present in tests/test_technical.py covering RSI range and strong_buy signal logic. Sufficient for current scope.

- [x] **VADER news sentiment coverage** (v2.6.1): Fully covered as automatic fallback inside news.py compute_finbert_sentiment when FinBERT unavailable or fails. Marked redundant and closed.

## Long-Term / Nice-to-Have

- [ ] **Agentic Multi-Agent Research**: LLM-orchestrated deep dives into earnings transcripts and options flow.
- [ ] **Options Flow and Insider Data**: New data sources for enhanced signals.
- [ ] **Reddit Sentiment Aggregation**: Integrate WallStreetBets and r/stocks sentiment via Pushshift or official API for crowd narrative validation.
- [ ] **Earnings Transcript LLM Analysis**: Parse recent calls for management tone, guidance sentiment using local LLMs or APIs.
- [ ] **Cloud Deployment Enhancements**: Optimized Docker for Streamlit Cloud / AWS / GCP with secrets management.
- [ ] **SEC EDGAR 8-K / Material Filing NLP Alerts**: Poll or webhook SEC filings for watchlist tickers; run FinBERT (or stronger) tone analysis on 8-K items and surface material events + sentiment delta in dashboard and Telegram.
- [ ] **Unusual Options Activity + Dark Pool Print Signals**: Ingest high-conviction flow (large premium, sweeps, dark-pool prints) from free tiers (Finnhub, Polygon, or public scrapers) and flag when unusual activity aligns with narrative/technical signals.

Last updated: July 25, 2026
