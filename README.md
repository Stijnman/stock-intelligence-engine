# Stock Intelligence Engine

**Narrative-aware stock intelligence with technical confirmation**

![Banner](assets/banner.jpg)

Connect **market narratives** to **watchlist tickers**, then confirm with RSI, moving averages, and 52-week drawdown. Open-source Python — not a black-box signal feed.

> **Not financial advice.** Educational and research use only.

---

## What it does (v2.0.1)

| Layer | Feature |
|-------|---------|
| **Narrative** | Theme + per-ticker fit (`strong` / `monitor` / `caution`) from `config.yaml` |
| **Technical** | RSI(14), MA50, MA200, 52w drawdown via yfinance |
| **Signal** | `strong_buy` / `buy` / `hold` / `caution` with human-readable reasons |
| **News** | `--news` headlines per ticker (yfinance, no API key) |
| **Automation** | CSV export, email alerts, daemon `--refresh N` |
| **UI** | Streamlit dashboard |

See [COMPETITION.md](COMPETITION.md) for roadmap vs Quiver, Unusual Whales, Koyfin, etc.

---

## Recent Edits & Version History

- **2026-07-05 (v2.0.1)**: Autonomous research & evolution cycle. Full code audit confirmed **GitHub Actions CI** (`.github/workflows/ci.yml`) is fully implemented and working (multi-Python matrix, flake8, smoke tests + artifacts). Removed it from FUTURE-IMPROVEMENTS.md v2.1. Added detailed entry to CHANGELOG.md. Bumped version to **v2.0.1** in all files (stock_intelligence_engine.py, app.py, docs). Added 5 new high-value improvements from fresh July 2026 research (FinBERT sentiment scoring, X/Twitter v2 viral scanner, options flow detector, Streamlit 2026 UX overhaul with data_editor + themes, vectorbt/Monte Carlo narrative backtester). Categorized into existing priority sections. Roadmap now current and forward-looking.

---

## Quick start

### Local Python

```bash
git clone https://github.com/Stijnman/stock-intelligence-engine.git
cd stock-intelligence-engine
pip install -r requirements.txt

# Full report with news + CSV
python stock_intelligence_engine.py --news --export

# Dutch + email (configure .env first)
python stock_intelligence_engine.py --lang nl --email

# Daemon every 30 minutes
python stock_intelligence_engine.py --news --export --refresh 30

# Dashboard
streamlit run app.py
```

### Docker

```bash
cp .env.example .env   # optional, for --email
docker compose up --build
```

---

## CLI options

```
--lang en|nl       UI strings
--news             Include recent headlines
--export           Write exports/stock_intel_YYYYMMDD_HHMMSS.csv
--email            Send SMTP report (see .env.example)
--refresh N        Re-run every N minutes (daemon)
```

---

## Configuration

Edit `config.yaml`:

```yaml
narrative:
  theme: "AI Inference Boom"
technical:
  rsi_overbought: 70
  ma_fast: 50
  ma_slow: 200
tickers:
  NVDA:
    name: NVIDIA
    narrative_fit: strong
    note: "Inference leader"
```

---

## Signal logic (transparent)

A ticker scores higher when:

- Price > MA50 > MA200 (trend aligned)
- RSI not overbought (< 70 by default)
- `narrative_fit: strong` in config

Every signal includes a **reason string** — no black box.

---

## Project structure

```
stock-intelligence-engine/
├── stock_intelligence_engine.py   # CLI entry
├── app.py                         # Streamlit UI
├── config.yaml
├── sie/
│   ├── analyzer.py                # orchestration
│   ├── technical.py               # RSI, MA, signals
│   ├── news.py                    # headlines
│   ├── export.py                  # CSV
│   ├── alerts.py                  # email
│   └── config.py                  # YAML loader
├── COMPETITION.md                 # competitor analysis + roadmap
└── exports/                       # gitignored CSV output
```

---

## Disclaimer

This tool is for **education and research**. Past patterns do not guarantee future results. You are responsible for your own investment decisions.

---

*Stock Intelligence Engine v2.0.1*