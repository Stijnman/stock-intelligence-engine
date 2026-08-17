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

- [x] **0DTE Options Flow & Unusual Activity Proxy** (v2.16.0 / confirmed v2.18.0): Derive near-zero-days-to-expiration volume/OI spikes and simple unusual-activity flags from free yfinance (or CBOE public) options chains; flag elevated 0DTE premium and directional flow as short-horizon event-risk / dealer-hedging signals. Apply soft boost/penalty and surface 0DTE ratio, side bias, confidence in dashboard & alerts. Configurable via `options_0dte:` section. Fully integrated 2026-08-16.

- [x] **Same-Day SEC EDGAR Material Filing Detector** (v2.18.0): Lightweight poll of EDGAR daily index / full-text search for watchlist tickers; detect fresh 8-K, Form 4 clusters or material item filings the same trading day and run quick FinBERT tone on key excerpts. Surface filing type, materiality flag, tone delta and link in dashboard + alerts. Configurable via `edgar:` section. Fully wired into analyzer, CLI, dashboard and config. 2026-08-16.

- [ ] **Corporate Hiring & Headcount Momentum Tracker**: Lightweight free-tier or public signals for open job postings growth / headcount momentum as forward-looking demand proxy (AltIndex-style). Apply soft confirmation when hiring accelerates ahead of narrative.

- [ ] **Narrative-Data Honesty / Contradiction Detector**: Cross-check dominant X/news narrative against recent filings, earnings language and price action for internal contradictions or “honesty signals” (inspired by 2026 NowNews / MarketPsych research). Flag high-contradiction regimes that historically precede reversals.

- [ ] **Authenticity-Filtered Narrative Velocity**: Score X and Reddit posts for authenticity / bot likelihood (inspired by 2026 Rolli IQ authenticity scoring) before including them in narrative velocity and phase forecasts; reduces noise from coordinated campaigns and spam while preserving genuine retail/institutional voice signals.

- [ ] **LLM ESG Summary Sentiment Overlay**: Generate or ingest LLM summaries of recent ESG / sustainability reports and extract FinBERT or prompt-based sentiment; research (2026) shows LLM-summary sentiment is more predictive of performance and valuation than full-text ESG sentiment. Soft confirmation layer for governance and social signals.

- [ ] **Retail-Institutional Sentiment Divergence Overlay**: Detect and score meaningful divergence between retail narrative velocity (X velocity + Reddit proxies) and smart-money overlays (13F changes, dark-pool ratios, congressional clusters, insider Form 4). Research and 2026 multi-source platforms show such divergences frequently precede mean-reversion or accelerated moves. Apply soft boost/penalty and surface divergence score, direction, and confidence in dashboard & alerts. Configurable via `divergence:` section.

- [ ] **Zero-Shot LLM Headline Materiality & Direction Classifier**: Beyond FinBERT polarity, apply lightweight zero-shot or prompt-based LLM classification (inspired by 2026 ECB / QLoRA financial NLP advances) to score each headline for expected short-horizon price impact magnitude and directional bias. Weight high-materiality items more heavily inside narrative velocity and event composites. Surface materiality score and reason.

- [ ] **Delayed News-Price Assimilation Lag Detector**: Detect and score the temporal lag between high-materiality news/narrative spikes and subsequent price response (inspired by NEXUS multi-modal news-exchange framework, 2026). Flag regimes of delayed assimilation or prolonged informational persistence for opportunistic signal timing and confidence adjustment. Surface lag_days, persistence score, and reason. Configurable via `assimilation:` section.

- [ ] **Social Trust / Narrative Credibility Index**: Composite credibility score combining source authenticity filters, cross-platform consistency, and MarketPsych-style trust signals. Re-weights narrative velocity and phase forecasts to down-rank low-trust or coordinated campaigns while amplifying high-credibility retail/institutional voices.

- [ ] **Narrative Momentum Acceleration Detector**: Compute the second derivative (acceleration) of multi-source narrative velocity to detect accelerating hype or panic phases earlier than velocity alone. Apply soft boost/penalty on strong positive/negative acceleration and surface acceleration score, direction, and confidence. Configurable via `momentum_accel:` section.

- [ ] **Unified Smart-Money Consensus Score**: Fuse insider Form 4 clusters, 13F ownership changes, congressional trades, dark-pool ratios, and options-flow proxies into a single 0–100 consensus score with agreement threshold. Raise overall signal confidence when multiple independent smart-money sources align; surface consensus level, contributing sources, and disagreement flags.

- [ ] **Earnings Call Transcript Sentiment & Guidance Shift Detector**: Ingest recent earnings call transcripts (public sources or free proxies) and apply FinBERT / lightweight LLM scoring to management tone, guidance language changes vs prior quarter, and Q&A sentiment. Flag positive/negative guidance shifts as high-materiality event overlays. Surface transcript tone delta, guidance direction, and confidence. Configurable via `earnings_transcript:` section. Inspired by 2026 SentiSense Earnings Analysis API and AlphaSense transcript sentiment indices.

- [ ] **Finance YouTube / Influencer Narrative Velocity Overlay**: Track mention volume, sentiment, and velocity from curated finance YouTube channels and influencers (inspired by 2026 SentiSense YouTube-as-first-class source). Apply soft confirmation when influencer consensus aligns with X/news narrative or diverges as leading indicator. Surface channel-weighted velocity and key thesis summaries.

- [ ] **Web Traffic & App Download Momentum Tracker**: Lightweight public or free-tier signals for company website traffic growth and consumer app download trends as forward-looking demand / engagement proxies (AltIndex-style). Soft boost when traffic/downloads accelerate ahead of price or narrative. Configurable via `web_traffic:` section.

## Medium Priority

- [x] **Real-time Streamlit Dashboard** (v2.5.0): Auto-refresh with st.rerun, configurable interval, live price/signal/narrative updates. Integrated into app.py with progress indicators. 2026-07-20

- [x] **Portfolio Correlation Heatmap & Risk Overlay** (v2.11.0): Compute pairwise returns correlations and portfolio-level metrics (max drawdown, volatility, Sharpe of equal-weight basket) inside backtest + dashboard. Display interactive Plotly heatmap and risk summary for the full watchlist. New module `sie/portfolio.py`, CLI `--portfolio`, config `portfolio:` section. 2026-08-01

- [ ] **Streamlit Partial Reruns + Advanced Caching (2026 patterns)**: Refactor dashboard to use `@st.fragment` for independent live-price and narrative sections, `st.cache_data` with TTL for yfinance/X calls, and avoid full-page `st.rerun()` loops where possible. Improves responsiveness and reduces API rate-limit pressure.

- [ ] **Employee Outlook / Glassdoor Sentiment Proxy**: Aggregate public employee review trends, business outlook scores, and CEO approval as soft cultural / operational health signals. Research shows employee sentiment often leads retail narrative. Soft confirmation or early warning layer.

- [ ] **Unusual Options Flow Percentile Ranking & Sweep Detector**: Extend 0DTE / options modules with market-wide percentile ranking of unusual activity, golden sweeps, and block trades (inspired by 2026 Unusual Whales / FlashAlpha / TickerDesk patterns). Surface relative unusualness score and directional bias for higher-conviction short-horizon signals.

(Remaining medium and long-term items unchanged — see full file history.)

## Completed

- [x] **Backtesting Framework** (v2.6.0): Historical signal performance evaluation with Sharpe ratio and returns metrics. Integrated into CLI (`--backtest`), Streamlit dashboard (button), and analyzer. 2026-07-23

- [x] **Narrative Phase Labels (Hype / Dip / Recovery)** (v2.6.1): Already implemented via dominant_narrative extraction in social.py. Exposed in dashboard and row data.

- [x] **pytest for RSI/MA math** (v2.6.1): Basic unit tests present in tests/test_technical.py.

- [x] **VADER news sentiment coverage** (v2.6.1): Fully covered as automatic fallback inside news.py.

Last updated: August 17, 2026 (v2.18.1 — Autonomous research cycle: 5 new 2026-sourced improvements added; version consistency fix)
