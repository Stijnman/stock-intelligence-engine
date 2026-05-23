# Stock Intelligence Engine

**Narrative-aware stock intelligence for the modern investor.**

Real-time analysis of viral signals, news impact, historical patterns, and risk-adjusted buy signals.

![Stock Intelligence Engine Banner](assets/banner.jpg)

## What is Stock Intelligence Engine?

Stock Intelligence Engine is a professional-grade CLI tool that helps you understand **which stocks are positioned to profit or suffer** from the current market narrative.

It combines:
- Real-time viral discussion analysis (X/Twitter + financial news)
- Historical pattern recognition from past narrative shifts (DeepSeek, Mamba, post-IPO behavior, etc.)
- Multi-condition technical filters + risk-adjusted position sizing
- Clear buy/hold/lower priority signals with color coding

Perfect for investors who want to stay ahead of narrative-driven market moves instead of reacting after the fact.

## Key Features

### Core Intelligence
- **Thematic Color Coding** (🟢 Green = Strong thematic fit, 🟡 Yellow = Monitor, 🔴 Red = Higher risk)
- **Multi-condition Buy Signals** with MA50/MA200 + RSI filters
- **Risk-Adjusted Position Sizing** (smaller size for high-drawdown names like new IPOs)
- **52-week Drawdown tracking**
- **Narrative Phase Detection**

### Viral & News Intelligence
- Optional deep news impact analysis (`--news`)
- Maps current viral narratives to profit/suffer per ticker
- Automatically discovers relevant tickers from ongoing discussions

### Automation & Alerts
- Email alerts support
- Automatic refresh / daemon mode (`--refresh 300`)
- CSV export for tracking over time

### Usability
- Bilingual support (English + Dutch)
- Clean professional CLI output
- Full Docker support for easy deployment
- Strong legal disclaimers included

## Installation

### Quick Start with Docker (Recommended)

```bash
docker compose up
```

Or build and run manually:

```bash
docker build -t stock-intelligence-engine .
docker run -it stock-intelligence-engine
```

### Local Installation

```bash
git clone https://github.com/Stijnman/stock-intelligence-engine.git
cd stock-intelligence-engine
pip install -r requirements.txt
```

## Usage Examples

```bash
# Basic run
python stock_intelligence_engine.py

# Dutch language
python stock_intelligence_engine.py --lang nl

# With news impact analysis
python stock_intelligence_engine.py --news

# Full power + export + email
python stock_intelligence_engine.py --export --news --email

# Auto-refresh every 5 minutes
python stock_intelligence_engine.py --refresh 300
```

## Current Watchlist (Example)

The tool currently tracks a dynamic list focused on the efficient AI architecture + inference boom narrative, including NVDA, TSM, CBRS, CRDO, MU, and others.

## Important Legal Disclaimer

**This tool is for educational and informational purposes only.**

It is NOT financial advice. Past performance is not indicative of future results. Always do your own research and consult a licensed financial advisor before making any investment decisions.

The developers are not responsible for any financial losses incurred from the use of this tool.

## Contributing

Contributions are welcome! Please open an issue or pull request.

## License

MIT License

---

*Stock Intelligence Engine — See the narrative before it moves the market.*