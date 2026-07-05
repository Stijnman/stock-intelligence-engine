# Roadmap

See [COMPETITION.md](COMPETITION.md) for full competitive analysis.

## v2.1 (next sprint) - High Priority

- [ ] VADER news sentiment score per ticker
- [ ] Narrative phase labels (Hype / Dip / Recovery)
- [ ] Telegram alert channel
- [ ] pytest for RSI/MA math
- [ ] **FinBERT / transformer-based sentiment scoring** for news headlines and narrative fit analysis. Config-driven model selection (VADER fallback or Hugging Face FinBERT). Adds numeric sentiment delta (-1.0 to +1.0) to boost or dampen signal confidence. GPU/CPU aware with graceful fallback.
- [ ] **X/Twitter API v2 real-time viral & sentiment scanner** for existing watchlist tickers and themes. Tracks mention volume, sentiment spikes, and computes "buzz_score". New column in signal table and dashboard. Uses official API or fallback scrapers with rate limiting.

## v2.2 - Medium Priority

- [ ] Multi-theme config (`themes/inference.yaml`)
- [ ] PDF/HTML weekly narrative report
- [ ] Relative strength vs SPY
- [ ] Smart yfinance cache
- [ ] **Unusual options activity detector & overlay**. Pulls options chain data (yfinance or free endpoints), flags unusual volume, IV spikes, sweeps, or large trades. Highlights in dashboard table with severity badges and links to details. Configurable thresholds.
- [ ] **Streamlit 2026 best practices upgrade**. Full use of session_state for persistent filters and user prefs, st.data_editor for live inline editing of config.yaml watchlist, enhanced Plotly interactive charts (subplots for price + signals + sentiment), auto-refresh toggle, theme switcher (dark/light), and better mobile/responsive layout.

## v3.0+ - Long-Term / Nice-to-Have

- [ ] Viral ticker discovery (X/Reddit keyword scan)
- [ ] SEC insider / congress trade overlay
- [ ] Narrative backtest module
- [ ] Local Ollama earnings summary
- [ ] Plugin architecture
- [ ] **Enhanced narrative-aware backtester** with vectorbt (or pandas-ta fallback), Monte Carlo simulations, walk-forward optimization, and full performance attribution broken down by narrative phase/theme. Outputs Sharpe, Sortino, Calmar, win rate, max drawdown, and edge metrics per strategy variant. Historical replay of signals vs actual price action.
- [ ] **One-click cloud deployment automation** for Streamlit Cloud, Render.com, Railway, or Hugging Face Spaces. Includes Dockerfile tweaks, secrets handling, and health checks. Scripts to deploy from CLI with minimal config.

Last updated: July 5, 2026