# Simulation Notes (v2.0.0)

Run: `python stock_intelligence_engine.py --news --export`

## Observed behavior (2026-06-24)

| Ticker | Signal | Insight |
|--------|--------|---------|
| TSM | STRONG | Full trend alignment — best technical + narrative combo |
| NVDA | BUY | Strong narrative but below MA50 — "leader in pullback" |
| CBRS | HOLD | -27% drawdown, below MAs — narrative strong, timing weak |
| CRDO/MU | BUY | Trend OK, monitor narrative fit |

## Gaps exposed by simulation

1. **Headlines** — yfinance returns market-wide news; need ticker relevance filter
2. **NL mode** — signal *reasons* still English (technical strings)
3. **No benchmark** — can't tell if BUY beats SPY
4. **No position sizing** — CBRS volatile but same weight as TSM in output
5. **Single theme** — can't compare "AI inference" vs "energy" narratives

## Feature ideas from simulation (prioritized)

### Quick wins (v2.1)
- VADER sentiment on headlines → `sentiment_score` column in CSV
- Narrative phase: `Hype` (RSI>60 + near 52w high), `Dip` (drawdown <-15%), `Recovery`
- Translate `signal_reason` in NL mode
- Relative strength vs SPY (90-day % change delta)
- Headline relevance: filter titles containing ticker or company name

### Medium (v2.2)
- Position size hint: `full` / `half` / `watch` based on volatility + signal
- Multi-theme configs: `themes/inference.yaml`, `themes/defense.yaml`
- Telegram/Discord webhook alerts on signal changes
- Signal change detection: compare last CSV vs current run

### Strategic (v3)
- Narrative backtest: load historical theme dates, measure forward returns
- Viral discovery: keyword scan → suggest tickers for active theme
- Ollama summary: "Weekly narrative memo" from headlines + signals
- Grok skill: `stock-intelligence-engine` in grok-custom-skills

## Validation commands

```bash
python3 -m pytest tests/ -q
python3 scripts/check_repo.py
python3 stock_intelligence_engine.py --news --export
python3 stock_intelligence_engine.py --lang nl --news
```