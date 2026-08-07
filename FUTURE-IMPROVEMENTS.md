# Roadmap

See [COMPETITION.md](COMPETITION.md) for full competitive analysis.

## High Priority

- [x] **X/Twitter Narrative Intelligence Integration** (v2.4.0): Real-time sentiment velocity, dominant narratives, key voices, and crisis flags using specialized logic in social.py. Enhances social.py, alerts, CLI, Streamlit dashboard. 2026-07-17

- [x] **Multi-source Narrative Velocity Forecasting** (v2.7.0): Time-series forecasting (simple exponential smoothing on rolling windows) of combined X sentiment velocity + news FinBERT/VADER scores to predict short-term narrative phase shifts (hype → dip) 1–3 days ahead. Integrated as forward-looking signal boost/penalty in analyzer, CLI, and Streamlit dashboard. 2026-07-25 https://github.com/Stijnman/stock-intelligence-engine/commit/3f0697667e4cac32032b207bad324a51414e231b

- [x] **Insider Form 4 Clustering & Confirmation Signals** (v2.8.0): Ingest recent Form 4 filings (via yfinance insider_transactions + synthetic proxy fallback) for watchlist tickers; detect clustered insider buying/selling within 7–14 days and apply confirmation boost/penalty to narrative + technical signals. Surface cluster size, net shares, side, confidence and impact in dashboard + Telegram alerts. Configurable via `insider:` section in config.yaml. 2026-07-29

- [x] **Prediction Market Odds Overlay (Polymarket)** (v2.9.0): Ingest real-money prediction-market probabilities for company- or sector-specific events via free/public Polymarket Gamma API (+ realistic synthetic fallback). Map event odds to watchlist tickers and apply soft confirmation or penalty on divergence from narrative + technical signal. Fully integrated into analyzer, CLI (`--no-pm`), Streamlit dashboard, config.yaml (`prediction_markets:`). 2026-07-30 https://github.com/Stijnman/stock-intelligence-engine/commit/0ea2039b07fc8d67c01f3e4ac8b89a3c62a1a74f

- [x] **Institutional 13F Ownership Change Detector** (v2.10.0): Ingest recent institutional holdings (yfinance institutional_holders + realistic synthetic QoQ proxy fallback) for watchlist tickers; detect significant ownership increases or decreases by large funds and apply soft confirmation/penalty as smart-money flow overlay alongside insider Form 4 clusters. Surface top holders delta, net shares change and confidence in dashboard and alerts. Configurable via `institutional:` section. 2026-07-31

- [x] **Real-time WebSocket Price & Quote Feeds** (v2.13.0): Low-latency price/quote updates via sie/realtime.py with stable synthetic tick generator (deterministic per-minute drift) as free default + clean extension points for Polygon/Massive/Finnhub WebSockets when keys present. Surfaces last price, bid/ask, change %, volume proxy, source and latency_ms. Integrated into CLI (`--no-realtime`), Streamlit dashboard, analyzer row enrichment. Reduces lag between narrative shifts and technical confirmation. 2026-08-05

- [x] **Dark Pool / ATS Off-Exchange Flow Overlay** (v2.14.0): Ingest free FINRA ATS transparency data (weekly) or stable synthetic daily proxies for watchlist tickers; detect elevated off-exchange volume relative to average daily volume as institutional accumulation or distribution signal; apply soft boost/penalty as additional smart-money layer alongside 13F, insider and congressional overlays. Surface relative volume ratio, inferred side, confidence and source in dashboard & alerts. Configurable via `dark_pool:` section. 2026-08-05

- [x] **Options Implied Volatility Skew & Term Structure Overlay** (v2.15.0): Pull free yfinance options chains for near-term expirations (or stable synthetic proxy); compute put/call IV skew and term-structure slope as fear/greed and event-risk proxies; apply soft boost/penalty when elevated skew diverges from narrative + technical signal. Surfaces skew ratio, term slope, ATM IV, confidence and source in dashboard & alerts. Configurable via `options_iv:` section. Fully integrated into analyzer, CLI, Streamlit. 2026-08-07

- [ ] **Truth Social / Official Political Narrative Overlay**: Ingest real-time posts from key official and political accounts (Truth Social public proxies or licensed API) for policy-sensitive tickers (energy, defense, media, DJT-related); detect narrative shifts from official statements and apply soft boost/penalty when they diverge from broader market or X narrative. Surface key posts, tone delta, confidence and source in dashboard & alerts. Configurable via `political_narrative:` section.

- [ ] **0DTE Options Flow & Unusual Activity Proxy**: Derive near-zero-days-to-expiration volume/OI spikes and simple unusual-activity flags from free yfinance (or CBOE public) options chains; flag elevated 0DTE premium and directional flow as short-horizon event-risk / dealer-hedging signals. Apply soft boost/penalty and surface 0DTE ratio, side bias, confidence in dashboard & alerts. Configurable via `options_0dte:` section.

- [ ] **Same-Day SEC EDGAR Material Filing Detector**: Lightweight poll of EDGAR daily index / full-text search for watchlist tickers; detect fresh 8-K, Form 4 clusters or material item filings the same trading day and run quick FinBERT tone on key excerpts. Surface filing type, materiality flag, tone delta and link in dashboard + alerts. Configurable via `edgar:` section.

## Medium Priority

- [x] **Real-time Streamlit Dashboard** (v2.5.0): Auto-refresh with st.rerun, configurable interval, live price/signal/narrative updates. Integrated into app.py with progress indicators. 2026-07-20

- [x] **Portfolio Correlation Heatmap & Risk Overlay** (v2.11.0): Compute pairwise returns correlations and portfolio-level metrics (max drawdown, volatility, Sharpe of equal-weight basket) inside backtest + dashboard. Display interactive Plotly heatmap and risk summary for the full watchlist. New module `sie/portfolio.py`, CLI `--portfolio`, config `portfolio:` section. 2026-08-01

- [x] **Congressional Trading Overlay** (v2.12.0): Ingest recent congressional stock transactions (synthetic proxy + future live disclosure hooks) for watchlist tickers; flag clustered or large buys/sells by members of Congress as an additional smart-money confirmation layer alongside insider Form 4 clusters. Fully integrated into analyzer, CLI (`--no-congress`), Streamlit dashboard, config.yaml (`congressional:`). 2026-08-02

- [ ] **Streamlit Partial Reruns + Advanced Caching (2026 patterns)**: Refactor dashboard to use `@st.fragment` for independent live-price and narrative sections, `st.cache_data` with TTL for yfinance/X calls, and avoid full-page `st.rerun()` loops where possible. Improves responsiveness and reduces API rate-limit pressure.

- [ ] **Cross-Platform Narrative Convergence Score**: Fuse X velocity, Reddit mention/sentiment (once available), news FinBERT, and prediction-market odds (Polymarket or equivalent free API) into a single 0–100 convergence score that quantifies how aligned alternative data sources are on the current narrative. High convergence increases signal confidence.

- [ ] **Analyst Estimate Revision Momentum Tracker**: Monitor daily/weekly changes in consensus EPS and revenue estimates (Yahoo Finance, Finnhub free tier, or similar) and flag accelerating upward/downward revisions as leading indicators ahead of earnings. Integrate as a soft boost/penalty layer.

- [ ] **Podcast & Alternative Media Sentiment Layer**: Ingest and score sentiment from financial podcasts and alternative media transcripts/summaries (Context Analytics-style Podcast Sentiment feeds or free public sources) using lightweight keyword + FinBERT/LLM pipelines. Surface as additional narrative confirmation signal in analyzer and dashboard.

- [ ] **Employee Outlook & Glassdoor Sentiment Signals**: Track aggregated employee business outlook scores and Glassdoor rating trends as forward-looking management confidence proxies (inspired by AltIndex alternative-data layers). Apply soft confirmation/penalty to narrative + technical signals for watchlist names when outlook diverges from market narrative.

- [ ] **Short Interest & Squeeze Risk Monitor**: Pull short-interest ratios, days-to-cover, and recent changes (via free Yahoo Finance / FINRA-style endpoints or public scrapers) and surface elevated short interest as a volatility/squeeze risk flag that can modulate position sizing advice or signal confidence in the dashboard and CLI.

- [ ] **News Materiality & Volatility Impact Scoring**: Beyond pure sentiment polarity, score each news item / filing for expected short-term price impact and materiality (inspired by StockTitan Rhea-AI impact engine). Flag high-impact headlines that historically precede outsized moves and weight them more heavily in the narrative + signal pipeline.

- [ ] **Consumer App Download & Engagement Momentum Signals**: For consumer-facing tickers, track daily/weekly app download ranks, active-user trends or engagement proxies (free public rank trackers or lightweight scrapers) as leading demand indicators. Apply soft boost when download momentum accelerates ahead of narrative confirmation.

- [ ] **AI Technical Pattern Confirmation Layer**: Lightweight rule-based + pattern detection (breakouts above resistance, support tests, flag/pennant formations) on recent price series; apply soft boost when detected technical pattern confirms the current or predicted narrative phase (hype/recovery), or penalty on conflict. Surfaces pattern type, confidence and alignment score in dashboard.

- [ ] **Cross-Asset Correlation Shock Detector**: Compute rolling correlations of each watchlist ticker vs SPY, QQQ and relevant sector ETF; flag sudden correlation spikes (contagion / risk-off) and apply caution penalty to pure narrative-driven signals during elevated co-movement regimes. Configurable lookback and threshold.

- [ ] **Multi-Factor Composite AI Score (0–100)**: Aggregate existing narrative velocity, technical, insider, 13F, congressional, prediction-market and realtime layers into a single transparent 0–100 composite score with component breakdown (inspired by 2026 Danelfin / Zen Ratings / Prospero multi-factor systems). Surface score + top contributing factors in dashboard and alerts for faster triage.

- [ ] **Earnings Surprise Magnitude & Post-Drift Context**: Track reported EPS/revenue vs consensus (yfinance or free endpoints) and quantify surprise size; attach short-horizon post-earnings drift context to refine signal timing and confidence in the days surrounding earnings.

- [ ] **Retail Whisper Number vs Consensus Divergence Tracker**: Aggregate informal EPS/revenue “whisper” estimates from Reddit (r/stocks, r/investing) and X FinTwit communities around earnings windows; flag material divergence from official analyst consensus as a leading retail-sentiment indicator. Surface whisper range, consensus delta, confidence and source in dashboard & alerts.

- [ ] **As-Reported Fundamentals Preference & Restatement Alert Layer**: Prefer as-reported financial line items over vendor-normalized numbers for agentic deep research; detect material presentation differences, restatements or caliber shifts (consolidated vs parent) that could alter narrative interpretation of growth, margins or leverage. Surfaces divergence flags and confidence for research briefs.

- [ ] **FINRA Short Volume Ratio & Squeeze Risk Overlay**: Ingest free FINRA daily short-volume series (or yfinance/short proxy) for watchlist tickers; compute short-volume % of total volume and flag elevated ratios as potential squeeze or distribution risk. Apply soft confidence modulation and surface ratio, days-to-cover proxy, side bias in dashboard & alerts. Configurable via `short_volume:` section.

- [ ] **Unified Multi-Platform Attention / Buzz Score**: Fuse Reddit mention velocity, X cashtag volume, news headline count and Polymarket volume into a single 0–100 attention/buzz score (Adanos-style multi-source). High buzz that aligns with narrative phase increases signal confidence; divergence flags caution. Surface component breakdown in dashboard.

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
- [ ] **Kalshi Prediction Market Cross-Check Overlay**: In parallel with Polymarket, pull CFTC-regulated Kalshi event odds (where public endpoints or free tiers allow) for the same company/sector events; surface cross-platform probability divergence as an additional confidence or caution flag.
- [ ] **Social Media Follower Growth Velocity Tracker**: Monitor week-over-week follower growth rates on X, Instagram, TikTok (or free rank proxies) for consumer and brand-sensitive tickers as a leading attention/demand signal, inspired by AltIndex social-follower layers.
- [ ] **Market-Outcome-Aligned Sentiment Refiner**: Lightweight adaptive weighting inspired by 2026 FinSMART research that adjusts the contribution of FinBERT / X sentiment scores based on subsequent short-horizon realized returns; improves signal quality over rolling windows without requiring a full reinforcement-learning pipeline.
- [ ] **Free-Tier Unusual Options Activity Proxy**: Derive unusual options activity flags from publicly available yfinance options chains (volume-to-open-interest spikes, skew changes, large near-term premium) as a zero-cost alternative to paid flow providers; integrate as soft confirmation layer when UOA aligns with narrative + technical signals.
- [ ] **Narrative Contagion Rate Tracker**: Quantify how quickly a dominant narrative (from X + news) spreads across related tickers / sector peers using simple co-mention and sentiment-correlation metrics; flag high-contagion regimes that historically amplify moves.
- [ ] **Prompt-Based Financial-Stability Sentiment Filter**: Lightweight prompt-engineered LLM classifier (inspired by 2026 ECB FinBERT/GPT comparisons) that isolates sentences containing explicit risk or stability assessments from news/filings and surfaces directional tone shifts that dictionary or pure FinBERT methods miss.

- [ ] **AI News Summary Engagement Multiplier**: Weight news items higher in the narrative + signal pipeline when they carry AI-generated summaries (inspired by 2026 HBS research showing stronger/faster market reactions and deeper comprehension). Improves timing and confidence on high-attention stories without requiring paid news APIs.

- [ ] **Gamma Exposure (GEX) Surface Proxy**: Approximate dealer gamma exposure from free near-term options chains (yfinance or CBOE public) using simplified open-interest × delta scaling; flag large positive/negative GEX regimes that historically dampen or amplify moves. Surface net GEX proxy, flip level estimate and confidence as an advanced volatility-regime overlay.

Last updated: August 7, 2026
