# Roadmap

See [COMPETITION.md](COMPETITION.md) for full competitive analysis.

## v2.1 (next sprint) - High Priority

- [ ] VADER news sentiment score per ticker (redundant with FinBERT + fallback)
- [ ] Narrative phase labels (Hype / Dip / Recovery)
- [ ] Telegram alert channel
- [ ] pytest for RSI/MA math
- [x] **FinBERT / transformer-based sentiment scoring** for news headlines and narrative fit analysis (2026-07-12). Config-driven, VADER fallback. See CHANGELOG v2.2.0.
- [x] **X/Twitter API v2 real-time viral & sentiment scanner** ... (done v2.1.0)
- [ ] **Narrative contradiction detection engine**...
- [ ] **Retail social sentiment overlay**...

## v2.2 - Medium Priority

- [ ] **Options flow integration**: Real-time unusual options activity for conviction signals.
- [ ] **Insider trading monitoring**: Parse SEC Form 4 filings for buy/sell signals.
- [ ] **Reddit sentiment layer**: Aggregate WallStreetBets and stock sub sentiment.

## Long-Term / Nice-to-Have

- [ ] Multi-agent LLM reasoning for narrative contradictions.
- [ ] Advanced Streamlit dashboard with Plotly interactive charts and backtesting.

Last updated: July 14, 2026