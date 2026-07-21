# Stock Intelligence Engine

**Connect market narratives to your watchlist. Confirm with technicals. Explain every signal.**

**v2.5.0** — July 2026 · Real-time Streamlit dashboard + X narrative intelligence

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/Stijnman/stock-intelligence-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/Stijnman/stock-intelligence-engine/actions/workflows/ci.yml)

## What it does

- Narrative-aware scoring for a configurable stock watchlist  
- Technical confirmation (trend, momentum, levels)  
- News impact + optional X/Twitter narrative velocity  
- Risk-adjusted buy / hold / caution style signals with explanations  
- Streamlit dashboard with auto-refresh  
- CSV/export helpers and email alert hooks  

## Quick start

```bash
git clone https://github.com/Stijnman/stock-intelligence-engine.git
cd stock-intelligence-engine
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add optional API keys
streamlit run app.py
```

CLI-style entry:

```bash
python stock_intelligence_engine.py
```

Docker:

```bash
docker compose up --build
```

## Configuration

| File / env | Purpose |
|------------|---------|
| `config.yaml` | Watchlist, refresh, feature flags |
| `.env` | API keys (news, X, SMTP, etc.) |
| `.streamlit/config.toml` | Theme / server |

See `.env.example` for variable names.

## Package layout

```
app.py                     # Streamlit dashboard
stock_intelligence_engine.py
sie/                       # library modules
  analyzer.py technical.py news.py social.py charts.py alerts.py export.py i18n.py
tests/
config.yaml
Dockerfile docker-compose.yml
```

## Version highlights

| Version | Notes |
|---------|--------|
| 2.5.0 | Real-time Streamlit auto-refresh |
| 2.4.0 | X narrative intelligence |
| earlier | Core engine, news, technicals, i18n |

## Disclaimer

**Not financial advice.** Markets are risky. This tool is for research and education. You are responsible for your own decisions.

## License

MIT © 2026 Stijnman
