# Stock Intelligence Engine

**Narrative-aware stock intelligence with technical confirmation**

![Banner](assets/banner.jpg)

Connect **market narratives** to **watchlist tickers**, then confirm with RSI, moving averages, and 52-week drawdown. Open-source Python — not a black-box signal feed.

> **Not financial advice.** Educational and research use only.

---

## What it does (v2.0.0)

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

*Stock Intelligence Engine v2.0.0*

## Free public-data adapters (investment intelligence)

The sie.investment.data package provides standard-library-only adapters for
public macroeconomic data. No paid API subscription is required.

```bash
# ECB daily USD reference rates against EUR
python3 -m sie.investment_cli ecb-fx USD --start 2025-01-01

# Combined ECB FX + Eurostat Belgian HICP macro snapshot
python3 -m sie.investment_cli macro --country BE --currency USD

# Eurostat Belgian HICP index (overall, 2015=100)
python3 -m sie.investment_cli eurostat prc_hicp_midx \
  --filter geo=BE --filter coicop=CP00 --filter unit=I15
```

ECB series identifiers use SDMX flow/key syntax. The example
EXR/D.USD.EUR.SP00.A represents the ECB daily USD-per-EUR reference rate.
Eurostat dataset filters are dimension codes; check dataset metadata before
using a different series. Results include source, dataset, series, period,
retrieval timestamp and source URL. Responses are cached under
~/.cache/stock-intelligence (override with SIE_CACHE_DIR).

SEC annual XBRL extraction distinguishes point-in-time balance-sheet facts
from duration-based income/cash-flow facts and excludes quarterly/YTD durations
from annual values. Configure SEC_USER_AGENT with a descriptive contact string
and respect SEC fair-access limits. Yahoo remains unofficial and optional.


### Additional free public macro sources

- **NBB.Stat**: SDMX CSV adapter. Copy the dataset-specific CSV API query URL from NBB.Stat's **API queries** panel and run `python3 -m sie.investment_cli nbb 'https://stat.nbb.be/...'`. The adapter normalizes time, value, unit and observation-status fields. NBB's standard reuse terms state non-commercial reuse with attribution unless a dataset says otherwise; verify dataset-specific terms before commercial use.
- **World Bank Indicators API v2**: free, no API key. Example: `python3 -m sie.investment_cli worldbank BE NY.GDP.MKTP.KD.ZG --start 2000 --end 2025`.
- `macro --country BE` now adds annual World Bank GDP growth, unemployment and current-account context alongside ECB FX and Eurostat HICP. Annual World Bank series can lag; use observation periods and freshness checks, not the retrieval date, when interpreting them.


### Verified NBB.Stat presets

Run `python3 -m sie.investment_cli nbb-preset` to list built-in presets. The initial verified preset is `mfi-interest-rates`, sourced from the official NBB.Stat Data Explorer's DF_MIR query: `python3 -m sie.investment_cli nbb-preset mfi-interest-rates --start-period 2020-01`. It preserves SDMX dimensions and observation status; do not compare rates across instrument/maturity codes without interpreting the NBB metadata. Monthly business-survey data are available in NBB.Stat, but a safe fixed query requires the selected indicator/region/sector/adjustment codes; use the generic `nbb` command with a copied API query until those codes are verified.
