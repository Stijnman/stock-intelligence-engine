# Roadmap

See [COMPETITION.md](COMPETITION.md) for full competitive analysis.

## High Priority

- [x] **X/Twitter Narrative Intelligence Integration** (v2.4.0): Real-time sentiment velocity, dominant narratives, key voices, and crisis flags using specialized logic in social.py. Enhances social.py, alerts, CLI, Streamlit dashboard. 2026-07-17

- [x] **Multi-source Narrative Velocity Forecasting** (v2.7.0): Time-series forecasting (simple exponential smoothing on rolling windows) of combined X sentiment velocity + news FinBERT/VADER scores to predict short-term narrative phase shifts (hype → dip) 1–3 days ahead. Integrated as forward-looking signal boost/penalty in analyzer, CLI, and Streamlit dashboard. 2026-07-25

- [x] **Insider Form 4 Clustering & Confirmation Signals** (v2.8.0): Ingest recent Form 4 filings (via yfinance insider_transactions + synthetic proxy fallback) for watchlist tickers; detect clustered insider buying/selling within 7–14 days and apply confirmation boost/penalty to narrative + technical signals. Surface cluster size, net shares, side, confidence and impact in dashboard + Telegram alerts. Configurable via `insider:` section in config.yaml. 2026-07-29

- [x] **Prediction Market Odds Overlay (Polymarket)** (v2.9.0): Ingest real-money prediction-market probabilities for company- or sector-specific events via free/public Polymarket Gamma API (+ realistic synthetic fallback). Map event odds to watchlist tickers and apply soft confirmation or penalty on divergence from narrative + technical signal. Fully integrated into analyzer, CLI (`--no-pm`), Streamlit dashboard, config.yaml (`prediction_markets:`). 2026-07-30

- [x] **Institutional 13F Ownership Change Detector** (v2.10.0): Ingest recent institutional holdings (yfinance institutional_holders + realistic synthetic QoQ proxy fallback) for watchlist tickers; detect significant ownership increases or decreases by large funds and apply soft confirmation/penalty as smart-money flow overlay alongside insider Form 4 clusters. Surface top holders delta, net shares change and confidence in dashboard and alerts. Configurable via `institutional:` section. 2026-07-31

- [x] **Congressional Trading Overlay** (v2.12.0): Ingest recent congressional stock transactions (synthetic proxy + future live disclosure hooks) for watchlist tickers; flag clustered or large buys/sells by members of Congress as an additional smart-money confirmation layer alongside insider Form 4 clusters. Fully integrated into analyzer, CLI (`--no-congress`), Streamlit dashboard, config.yaml (`congressional:`). 2026-08-02

- [x] **Real-time WebSocket Price & Quote Feeds** (v2.13.0): Low-latency price/quote updates via sie/realtime.py with stable synthetic fallback. Integrated into analyzer, dashboard, CLI. 2026-08-03

- [x] **Dark Pool / ATS Off-Exchange Flow Overlay** (v2.14.0): Detect elevated dark-pool / ATS volume ratios and prints as institutional flow signals. Module `sie/dark_pool.py`, soft boost/penalty, dashboard surfaces. 2026-08-05

- [x] **Options Implied Volatility Skew & Term Structure Overlay** (v2.15.0): Pulls free yfinance options chains (nearest 1–3 expirations) or synthetic proxy; computes put/call IV skew and term-structure slope; applies soft signal boost/penalty on elevated fear skew or inversion. Fully integrated. 2026-08-07

- [ ] **0DTE Options Flow & Unusual Activity Proxy**: Derive near-zero-days-to-expiration volume/OI spikes and simple unusual-activity flags from free yfinance (or CBOE public) options chains; flag elevated 0DTE premium and directional flow as short-horizon event-risk / dealer-hedging signals. Apply soft boost/penalty and surface 0DTE ratio, side bias, confidence in dashboard & alerts. Configurable via `options_0dte:` section.

- [ ] **Same-Day SEC EDGAR Material Filing Detector**: Lightweight poll of EDGAR daily index / full-text search for watchlist tickers; detect fresh 8-K, Form 4 clusters or material item filings the same trading day and run quick FinBERT tone on key excerpts. Surface filing type, materiality flag, tone delta and link in dashboard + alerts. Configurable via `edgar:` section.

- [ ] **Corporate Hiring & Headcount Momentum Tracker**: Lightweight free-tier or public signals for open job postings growth / headcount momentum as forward-looking demand proxy (AltIndex-style). Apply soft confirmation when hiring accelerates ahead of narrative.

- [ ] **Narrative-Data Honesty / Contradiction Detector**: Cross-check dominant X/news narrative against recent filings, earnings language and price action for internal contradictions or “honesty signals” (inspired by 2026 NowNews / MarketPsych research). Flag high-contradiction regimes that historically precede reversals.

- [ ] **Authenticity-Filtered Narrative Velocity**: Score X and Reddit posts for authenticity / bot likelihood (inspired by 2026 Rolli IQ authenticity scoring) before including them in narrative velocity and phase forecasts; reduces noise from coordinated campaigns and spam while preserving genuine retail/institutional voice signals.

- [ ] **LLM ESG Summary Sentiment Overlay**: Generate or ingest LLM summaries of recent ESG / sustainability reports and extract FinBERT or prompt-based sentiment; research (2026) shows LLM-summary sentiment is more predictive of performance and valuation than full-text ESG sentiment. Soft confirmation layer for governance and social signals.

- [ ] **Retail-Institutional Sentiment Divergence Overlay**: Detect and score meaningful divergence between retail narrative velocity (X velocity + Reddit proxies) and smart-money overlays (13F changes, dark-pool ratios, congressional clusters, insider Form 4). Research and 2026 multi-source platforms show such divergences frequently precede mean-reversion or accelerated moves. Apply soft boost/penalty and surface divergence score, direction, and confidence in dashboard & alerts. Configurable via `divergence:` section.

- [ ] **Zero-Shot LLM Headline Materiality & Direction Classifier**: Beyond FinBERT polarity, apply lightweight zero-shot or prompt-based LLM classification (inspired by 2026 ECB / QLoRA financial NLP advances) to score each headline for expected short-horizon price impact magnitude and directional bias. Weight high-materiality items more heavily inside narrative velocity and event composites. Surface materiality score and reason.

## Medium Priority

- [x] **Real-time Streamlit Dashboard** (v2.5.0): Auto-refresh with st.rerun, configurable interval, live price/signal/narrative updates. Integrated into app.py with progress indicators. 2026-07-20

- [x] **Portfolio Correlation Heatmap & Risk Overlay** (v2.11.0): Compute pairwise returns correlations and portfolio-level metrics (max drawdown, volatility, Sharpe of equal-weight basket) inside backtest + dashboard. Display interactive Plotly heatmap and risk summary for the full watchlist. New module `sie/portfolio.py`, CLI `--portfolio`, config `portfolio:` section. 2026-08-01

- [ ] **Streamlit Partial Reruns + Advanced Caching (2026 patterns)**: Refactor dashboard to use `@st.fragment` for independent live-price and narrative sections, `st.cache_data` with TTL for yfinance/X calls, and avoid full-page `st.rerun()` loops where possible. Improves responsiveness and reduces API rate-limit pressure.

- [ ] **Cross-Platform Narrative Convergence Score**: Fuse X velocity, Reddit mention/sentiment (once available), news FinBERT, and prediction-market odds (Polymarket or equivalent free API) into a single 0–100 convergence score that quantifies how aligned alternative data sources are on the current narrative. High convergence increases signal confidence.

- [ ] **Analyst Estimate Revision Momentum Tracker**: Monitor daily/weekly changes in consensus EPS and revenue estimates (Yahoo Finance, Finnhub free tier, or similar) and flag accelerating upward/downward revisions as leading indicators ahead of earnings. Integrate as a soft boost/penalty layer.

- [ ] **Podcast & Alternative Media Sentiment Layer**: Ingest and score sentiment from financial podcasts and alternative media transcripts/summaries using lightweight keyword + FinBERT/LLM pipelines. Surface as additional narrative confirmation signal.

- [ ] **Employee Outlook & Glassdoor Sentiment Signals**: Track aggregated employee business outlook scores and Glassdoor rating trends as forward-looking management confidence proxies. Apply soft confirmation/penalty when outlook diverges from market narrative.

- [ ] **Short Interest & Squeeze Risk Monitor**: Pull short-interest ratios, days-to-cover, and recent changes and surface elevated short interest as a volatility/squeeze risk flag.

- [ ] **News Materiality & Volatility Impact Scoring**: Beyond pure sentiment polarity, score each news item / filing for expected short-term price impact and materiality. Flag high-impact headlines and weight them more heavily.

- [ ] **Consumer App Download & Engagement Momentum Signals**: For consumer-facing tickers, track daily/weekly app download ranks or engagement proxies as leading demand indicators.

- [ ] **AI Technical Pattern Confirmation Layer**: Lightweight rule-based + pattern detection (breakouts, support tests, flag/pennant) on recent price series; soft boost when pattern confirms narrative phase.

- [ ] **Cross-Asset Correlation Shock Detector**: Detect sudden regime shifts in correlations between watchlist names and key assets (SPY, QQQ, sector ETFs, VIX) as early warning of liquidity or narrative contagion events.

- [ ] **FINRA Short Volume Ratio & Squeeze Risk Overlay**: Ingest free FINRA daily short-volume series (or yfinance/short proxy); compute short-volume % of total volume and flag elevated ratios. Configurable via `short_volume:` section.

- [ ] **Unified Multi-Platform Attention / Buzz Score**: Fuse Reddit mention velocity, X cashtag volume, news headline count and Polymarket volume into a single 0–100 attention/buzz score. High buzz aligning with narrative phase increases confidence.

- [ ] **Earnings Call Prepared Remarks vs Live Q&A Sentiment Delta**: Compare FinBERT/LLM tone of prepared management remarks versus live Q&A section of recent earnings calls; large negative deltas historically flag elevated risk of guidance disappointment.

- [ ] **Company Website Traffic & Engagement Momentum Proxy**: Free or public web-traffic / engagement trend proxies (SimilarWeb-style free tiers or public rank data) as demand leading indicator.

- [ ] **Event-Driven Surprise Composite**: Combine earnings surprise magnitude, same-day EDGAR materiality flags, and post-event social velocity into a single event-impact score that modulates short-horizon signal confidence and position-size hints.

- [ ] **Free CBOE Delayed Options UOA Enhancer**: Extend current options_iv and 0DTE proxies with official CBOE delayed chain files (public, no key) for higher-fidelity volume/OI spike detection and premium thresholds; improves unusual activity confidence without paid flow providers.

- [ ] **Options Sweep & Block Unusual Activity Proxy**: From free/delayed options chains (yfinance or CBOE public files), detect volume/OI and premium patterns consistent with sweeps or large block trades. Flag directional flow with size and confidence thresholds; soft confirmation layer that complements existing options_iv and 0DTE proxies. Surface sweep_score, side bias, and reason.

- [ ] **Streamlit Fragment + Persistent Session Watchlist Hardening**: Full production hardening of the dashboard using `@st.fragment`, robust `st.session_state` for watchlist persistence, alert history, and user preferences, plus TTL-aware caching. Eliminates residual full-page rerun pressure and improves multi-session / cloud deployment stability.

## Long-Term / Nice-to-Have

- [ ] **Agentic Multi-Agent Research**: LLM-orchestrated deep dives into earnings transcripts and options flow.

- [ ] **Options Flow and Insider Data**: New data sources for enhanced signals.

- [ ] **Reddit Sentiment Aggregation**: Integrate WallStreetBets and r/stocks sentiment via official API or free proxies for crowd narrative validation.

- [ ] **Earnings Transcript LLM Analysis**: Parse recent calls for management tone, guidance sentiment using local LLMs or APIs.

- [ ] **Cloud Deployment Enhancements**: Optimized Docker for Streamlit Cloud / AWS / GCP with secrets management.

- [ ] **SEC EDGAR 8-K / Material Filing NLP Alerts**: Poll or webhook SEC filings; run FinBERT tone on 8-K items.

- [ ] **Unusual Options Activity + Dark Pool Print Signals**: Ingest high-conviction flow from free tiers and flag alignment with narrative/technical signals.

- [ ] **Grok / xAI Agent Deep-Research Hook**: Optional integration that calls Grok for on-demand multi-document research briefs with response caching.

- [ ] **Alternative Data Proxies (Hiring & Web Traffic)**: Lightweight free-tier signals for open job postings growth and website traffic trends.

- [ ] **HMM / Regime Detection Filter**: Lightweight Hidden Markov Model or volatility/returns regime classifier to gate or re-weight signals by bull/bear/sideways regime.

- [ ] **MCP-Native Agent Data Hooks**: Expose SIE signals via Model Context Protocol (MCP) and/or consume MCP servers so external AI agents can query live scores and SIE can pull verified fundamentals more reliably.

- [ ] **Earnings Whisper vs Actual Surprise Integration**: Track pre-earnings whisper numbers against consensus and actuals; compute surprise magnitude and post-earnings drift context.

- [ ] **Kalshi Cross-Check Overlay**: Cross-reference Polymarket odds with CFTC-regulated Kalshi event odds; surface cross-platform probability divergence.

- [ ] **Social Media Follower Growth Velocity Tracker**: Monitor week-over-week follower growth rates on X, Instagram, TikTok (or free rank proxies) as leading attention/demand signal.

- [ ] **Market-Outcome-Aligned Sentiment Refiner**: Adaptive weighting of FinBERT / X sentiment scores based on subsequent short-horizon realized returns (FinSMART-style).

- [ ] **Free-Tier Unusual Options Activity Proxy**: Derive UOA flags from yfinance options chains (volume-to-OI spikes, skew changes, large near-term premium).

- [ ] **Narrative Contagion Rate Tracker**: Quantify how quickly a dominant narrative spreads across related tickers / sector peers using co-mention and sentiment-correlation metrics.

- [ ] **Prompt-Based Financial-Stability Sentiment Filter**: Prompt-engineered LLM classifier that isolates sentences containing explicit risk or stability assessments from news/filings.

- [ ] **AI News Summary Engagement Multiplier**: Weight news items higher when they carry AI-generated summaries (HBS 2026 research on stronger/faster market reactions).

- [ ] **Gamma Exposure (GEX) Surface Proxy**: Approximate dealer gamma exposure from free near-term options chains using simplified open-interest × delta scaling; flag large positive/negative GEX regimes.

- [ ] **Max Pain & Simplified Dealer Positioning Overlay**: Compute approximate max-pain strike from free options chains and simple dealer positioning heuristics; surface as volatility-regime and pin-risk context.

- [ ] **Vanna Exposure (VEX) Proxy**: Approximate dealer vanna exposure from free options data (alongside GEX) to capture sensitivity of delta to volatility changes; flag regimes where volatility shocks are likely to amplify or dampen directional moves.

- [ ] **Agentic Multi-Document Research Brief Generator**: On-demand, cacheable LLM synthesis that pulls recent filings, news headlines, options/flow context and narrative velocity into a short structured research note per ticker. Extends existing Grok/xAI hook ideas with deterministic prompt templates and local/offline fallback.

## Completed

- [x] **Backtesting Framework** (v2.6.0): Historical signal performance evaluation with Sharpe ratio and returns metrics. Integrated into CLI (`--backtest`), Streamlit dashboard (button), and analyzer. 2026-07-23

- [x] **Narrative Phase Labels (Hype / Dip / Recovery)** (v2.6.1): Already implemented via dominant_narrative extraction in social.py. Exposed in dashboard and row data.

- [x] **pytest for RSI/MA math** (v2.6.1): Basic unit tests present in tests/test_technical.py.

- [x] **VADER news sentiment coverage** (v2.6.1): Fully covered as automatic fallback inside news.py.

Last updated: August 11, 2026 (v2.15.3 autonomous research cycle)
