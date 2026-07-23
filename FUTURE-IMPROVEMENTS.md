# Roadmap

See [COMPETITION.md](COMPETITION.md) for full competitive analysis.

## v2.1 (next sprint) - High Priority

- [ ] VADER news sentiment score per ticker (redundant with FinBERT + fallback)
- [ ] Narrative phase labels (Hype / Dip / Recovery)
- [ ] pytest for RSI/MA math

## High Priority

- [x] **X/Twitter Narrative Intelligence Integration** (v2.4.0): Real-time sentiment velocity, dominant narratives, key voices, and crisis flags using specialized logic in social.py. Enhances social.py, alerts, CLI, Streamlit dashboard. 2026-07-17

## Medium Priority

- [x] **Real-time Streamlit Dashboard** (v2.5.0): Auto-refresh with st.rerun, configurable interval, live price/signal/narrative updates. Integrated into app.py with progress indicators. 2026-07-20

## Long-Term / Nice-to-Have

- [ ] **Agentic Multi-Agent Research**: LLM-orchestrated deep dives into earnings transcripts and options flow.
- [ ] **Options Flow and Insider Data**: New data sources for enhanced signals.
- [ ] **Reddit Sentiment Aggregation**: Integrate WallStreetBets and r/stocks sentiment via Pushshift or official API for crowd narrative validation.
- [ ] **Earnings Transcript LLM Analysis**: Parse recent calls for management tone, guidance sentiment using local LLMs or APIs.
- [ ] **Backtesting Framework**: Historical signal performance evaluation and Sharpe ratio metrics.
- [ ] **Cloud Deployment Enhancements**: Optimized Docker for Streamlit Cloud / AWS / GCP with secrets management.

Last updated: July 23, 2026