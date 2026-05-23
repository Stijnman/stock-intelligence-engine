# Stock Intelligence Engine

**Professional Narrative-Aware Stock Intelligence**

![Banner](assets/banner.jpg)

**See the narrative before it moves the market.**

Real-time viral signals • News impact analysis • Historical context • Risk-adjusted buy signals

---

## What This Tool Actually Does

Stock Intelligence Engine helps you understand **which companies are positioned to win or lose** from the stories currently driving the market.

It doesn't just show prices. It connects:
- What people are talking about right now (viral X posts + financial news)
- How similar narratives played out historically
- Technical health of the stocks
- Clear, actionable signals with proper risk management

## Full Feature List

### 1. Narrative Intelligence
- Thematic color coding (🟢 Strong fit / 🟡 Monitor / 🔴 Higher caution)
- Per-ticker profit vs suffer analysis from current narrative
- Automatic discovery of relevant tickers from viral discussions
- Narrative phase detection (Hype → Dip → Recovery)

### 2. Technical + Risk Filters
- Multi-condition buy signals (price > MA50 + MA200 + RSI filter)
- 52-week drawdown tracking (critical for new IPOs like CBRS)
- Risk-adjusted position sizing suggestions
- RSI (14) to avoid buying euphoria

### 3. Automation & Alerts
- `--email` alerts with narrative context
- `--refresh N` automatic daemon mode
- CSV export for historical tracking

### 4. Usability
- `--lang nl` bilingual support
- Clean, professional CLI output
- Full Docker support (one command to run)
- Strong legal disclaimers built-in

## Installation & Usage

### Recommended: Docker (Easiest)

```bash
git clone https://github.com/Stijnman/stock-intelligence-engine.git
cd stock-intelligence-engine
cp .env.example .env   # Edit with your email credentials if using alerts
docker compose up
```

### Local Python

```bash
pip install -r requirements.txt
python stock_intelligence_engine.py --news --export
```

## Important Disclaimer

**This is NOT financial advice.**

This tool is for educational and research purposes only. All investment decisions are your own responsibility. Past narrative patterns do not guarantee future results. Always conduct your own due diligence.

## Visuals

Logo and banner generated for professional presentation. Add `assets/logo.jpg` and `assets/banner.jpg` to the repository for full visual appeal.

## Roadmap

Future versions will include more themes, web dashboard option, and deeper backtesting.

---

*Stock Intelligence Engine v1.0.0 — Narrative intelligence for serious investors.*