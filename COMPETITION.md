# Competitive Landscape & Feature Brainstorm

Research date: June 2026. Informs Stock Intelligence Engine roadmap.

## Competitor matrix

| Product | Strength | Gap we can exploit |
|---------|----------|-------------------|
| [Quiver Quantitative](https://www.quiverquant.com/) | Congress trades, lobbying, gov contracts, WSB trends | No narrative *theme* layer; expensive; US-centric |
| [Unusual Whales](https://unusualwhales.com/) | Options flow, dark pool, congressional trades, AI chat | Options-first; overwhelming UI; subscription |
| [Koyfin](https://www.koyfin.com/) | Fundamentals, transcripts, institutional charts | Heavy terminal; weak social/viral narrative |
| [LunarCrush](https://lunarcrush.com/) | Social sentiment, galaxy scores, trending topics | Crypto-heavy; not narrative→equity mapping |
| [StockGeist](https://www.stockgeist.ai/) | Real-time social sentiment per ticker | Black-box sentiment; no technical confirmation |
| [MediaWatcher](https://mediawatcher.ai/) | News sentiment before price moves | News-only; no watchlist narrative thesis |
| [Prospero.ai](https://www.prospero.ai/) | AI trade signals, portfolio tools | Proprietary signals; not self-hosted/open |

## Our differentiation (v2+)

1. **Narrative-first, technical-second** — theme → tickers → RSI/MA confirmation (most tools do sentiment OR charts, not both in one thesis)
2. **Open & local** — Python CLI, Docker, CSV export, no vendor lock-in
3. **Bilingual NL/EN** — underserved in US-only competitors
4. **Educational transparency** — show *why* each signal fired (reason string)

## Implemented in v2.0.0

- [x] RSI(14), MA50, MA200, 52-week drawdown
- [x] Rule-based signal (strong_buy / buy / hold / caution) + reasons
- [x] yfinance headlines (`--news`)
- [x] CSV export (`--export`)
- [x] Daemon refresh (`--refresh N`)
- [x] SMTP email (`--email` + `.env`)
- [x] `config.yaml` driven watchlist
- [x] Streamlit dashboard with signal table

## High-priority new features (beat competition)

| Feature | Inspired by | Effort | Impact |
|---------|-------------|--------|--------|
| **Narrative phase detector** | LunarCrush hype cycles | Medium | Hype → Dip → Recovery labels per theme |
| **Viral ticker discovery** | Unusual Whales trending | High | Scan X/Reddit keywords → suggest tickers for theme |
| **Earnings transcript summary** | Koyfin transcripts | Medium | yfinance + local Ollama summary per holding |
| **Congress / insider overlay** | Quiver | Medium | Free SEC API / quiver-style alt data |
| **Options unusual activity flag** | Unusual Whales | High | yfinance options volume spike detector |
| **News sentiment score** | StockGeist, MediaWatcher | Medium | VADER/LLM score on headlines (-1 to +1) |
| **Narrative backtest** | Unique | High | "When AI capex narrative heated in 2023, NVDA +X% in 90d" |
| **Telegram/Discord alerts** | Prospero, UW bots | Low | Extend `sie/alerts.py` |
| **PDF/HTML report** | Koyfin reports | Low | Weekly narrative memo export |
| **Multi-theme watchlists** | Unique | Medium | `config/themes/inference.yaml`, `energy.yaml` |

## Medium priority

- Smart cache layer (reduce yfinance rate limits)
- GitHub Actions CI + pytest for indicators
- Plugin architecture (`sie/plugins/`)
- Compare vs SPY relative strength
- Position sizing hint (Kelly-lite / max 2% risk)

## Long-term (moat builders)

- **Historical narrative database** — tag past market stories with winner/loser tickers
- **LLM narrative extractor** — paste FinTwit thread → structured theme + tickers
- **Groq/Ollama local agent** — natural language: "What's the inference trade?" 
- **Integration with `stock-intelligence` Grok skills** — `deep-search-enabler`, `insight-synthesizer`, `cron-scheduler`

## What NOT to copy

- Black-box "AI says buy" without reasoning (trust issue)
- Paywalled data we can't legally redistribute
- Options-heavy UI for a narrative equity tool
- Financial advice language (keep educational disclaimers)

## Suggested v2.1 sprint

1. News sentiment score on headlines (VADER, no API key)
2. Narrative phase label (rules from RSI + drawdown + headline count)
3. Telegram alert channel
4. pytest for RSI/MA calculations