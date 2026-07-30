# Roadmap

See [COMPETITION.md](COMPETITION.md) for full competitive analysis.

## High Priority

- [x] **X/Twitter Narrative Intelligence Integration** (v2.4.0): Real-time sentiment velocity, dominant narratives, key voices, and crisis flags using specialized logic in social.py. Enhances social.py, alerts, CLI, Streamlit dashboard. 2026-07-17

- [x] **Multi-source Narrative Velocity Forecasting** (v2.7.0): Time-series forecasting (simple exponential smoothing on rolling windows) of combined X sentiment velocity + news FinBERT/VADER scores to predict short-term narrative phase shifts (hype → dip) 1–3 days ahead. Integrated as forward-looking signal boost/penalty in analyzer, CLI, and Streamlit dashboard. 2026-07-25 https://github.com/Stijnman/stock-intelligence-engine/commit/3f0697667e4cac32032b207bad324a51414e231b

- [x] **Insider Form 4 Clustering & Confirmation Signals** (v2.8.0): Ingest recent Form 4 filings (via yfinance insider_transactions + synthetic proxy fallback) for watchlist tickers; detect clustered insider buying/selling within 7–14 days and apply confirmation boost/penalty to narrative + technical signals. Surface cluster size, net shares, side, confidence and impact in dashboard + Telegram alerts. Configurable via `insider:` section in config.yaml. 2026-07-29

- [ ] **Real-time WebSocket Price & Quote Feeds**: Replace or augment yfinance polling with low-latency WebSocket sources (Polygon, Massive, or free-tier alternatives) for true real-time price/quote updates in the dashboard and signal engine. Reduces lag between narrative shifts and technical confirmation; supports sub-second dashboard refresh without aggressive polling.

- [ ] **Prediction Market Odds Overlay (Polymarket)**: Ingest real-money prediction-market probabilities for company- or sector-specific events (earnings outcomes, product launches, regulatory decisions) via free/public Polymarket Gamma or PredScope-style APIs. Map event odds to watchlist tickers and apply soft confirmation or penalty when market-implied probability diverges from current narrative + technical signal.

## Medium Priority

- [x] **Real-time Streamlit Dashboard** (v2.5.0): Auto-refresh with st.rerun, configurable interval, live price/signal/narrative updates. Integrated into app.py with progress indicators. 2026-07-20

- [ ] **Portfolio Correlation Heatmap & Risk Overlay**: Compute pairwise returns correlations and portfolio-level metrics (max drawdown, volatility, Sharpe of equal-weight basket) inside backtest + dashboard. Display interactive Plotly heatmap and risk summary for the full watchlist.

- [ ] **Streamlit Partial Reruns + Advanced Caching (2026 patterns)**: Refactor dashboard to use `@st.fragment` for independent live-price and narrative sections, `st.cache_data` with TTL for yfinance/X calls, and avoid full-page `st.rerun()` loops where possible. Improves responsiveness and reduces API rate-limit pressure.

- [ ] **Cross-Platform Narrative Convergence Score**: Fuse X velocity, Reddit mention/sentiment (once available), news FinBERT, and prediction-market odds (Polymarket or equivalent free API) into a single 0–100 convergence score that quantifies how aligned alternative data sources are on the current narrative. High convergence increases signal confidence.

- [ ] **Analyst Estimate Revision Momentum Tracker**: Monitor daily/weekly changes in consensus EPS and revenue estimates (Yahoo Finance, Finnhub free tier, or similar) and flag accelerating upward/downward revisions as leading indicators ahead of earnings. Integrate as a soft boost/penalty layer.

- [ ] **Podcast & Alternative Media Sentiment Layer**: Ingest and score sentiment from financial podcasts and alternative media transcripts/summaries (Context Analytics-style Podcast Sentiment feeds or free public sources) using lightweight keyword + FinBERT/LLM pipelines. Surface as additional narrative confirmation signal in analyzer and dashboard.

- [ ] **Employee Outlook & Glassdoor Sentiment Signals**: Track aggregated employee business outlook scores and Glassdoor rating trends as forward-looking management confidence proxies (inspired by AltIndex alternative-data layers). Apply soft confirmation/penalty to narrative + technical signals for watchlist names when outlook diverges from market narrative.

- [ ] **Short Interest & Squeeze Risk Monitor**: Pull short-interest ratios, days-to-cover, and recent changes (via free Yahoo Finance / FINRA-style endpoints or public scrapers) and surface elevated short interest as a volatility/squeeze risk flag that can modulate position sizing advice or signal confidence in the dashboard and CLI.

- [ ] **Congressional Trading Overlay**: Ingest recent congressional stock transactions (Quiver-style free data, official disclosures, or public APIs) for watchlist tickers; flag clustered or large buys/sells by members of Congress as an additional smart-money confirmation layer alongside insider Form 4 clusters.

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
- [ ] **Grok / xAI Agent Deep-Research Hook**: Optional integration that calls Grok (or compatible LLM via API) for on-demand multi-document research briefs (transcripts + filings + social) triggered from the Streamlit dashboard or CLI, with response caching to control cost and rate limits.
- [ ] **Alternative Data Proxies (Hiring & Web Traffic)**: Lightweight free-tier or public signals for open job postings growth and company website traffic trends as forward-looking demand proxies, inspired by AltIndex-style alternative data layers.
- [ ] **HMM / Regime Detection Filter**: Implement a lightweight Hidden Markov Model (or simpler volatility/returns regime classifier) on recent price series to detect bull / bear / sideways regimes and gate or re-weight narrative and technical signals accordingly, reducing false positives in hostile regimes.
- [ ] **MCP-Native Agent Data Hooks**: Expose SIE signals via Model Context Protocol (MCP) and/or consume MCP servers (Alpha Vantage MCP, StockContext, etc.) so external AI agents can query live narrative/technical scores and SIE can pull verified fundamentals, insiders, and filings more reliably in agentic workflows.
- [ ] **Earnings Whisper vs Actual Surprise Integration**: Track pre-earnings “whisper” numbers (where freely available) against consensus and actual reported EPS/revenue; compute surprise magnitude and post-earnings drift context to refine signal timing around earnings windows.
- [ ] **Multi-LLM Ensemble Narrative Extractor**: Optional ensemble that runs the same social/news/transcript snippets through two or more lightweight local or API LLMs (e.g. Grok + DeepSeek-style or Ollama models) and averages or majority-votes the extracted narrative labels and sentiment to reduce single-model bias.

Last updated: July 30, 2026
