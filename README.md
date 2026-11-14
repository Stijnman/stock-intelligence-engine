# Stock Intelligence Engine

A narrative-first equity research and investment analysis toolkit. It combines market narratives, configurable alternative-data overlays, technical confirmation and fundamental analysis, then explains which inputs influenced each signal.

The project runs as a Python CLI and a Streamlit dashboard. It also includes a free-first investment data package for public macroeconomic and regulatory datasets.

> **Research tool, not financial advice.** Outputs are estimates and research aids, not instructions to buy or sell. Verify source data, timestamps, assumptions and licensing before relying on a result.

## Features

- **Narrative intelligence:** news and optional X/Twitter search, sentiment, mention velocity and narrative classification.
- **Overlay engine:** independently configurable signal adjustments with human-readable reasons.
- **Investment analysis:** market data, technical indicators, valuation/DCF scenarios, dividend analysis, ETF and portfolio utilities.
- **Public-data adapters:** ECB, Eurostat, NBB.Stat, World Bank Indicators and SEC company facts.
- **Outputs:** CLI reports, JSON, CSV exports and an interactive Streamlit dashboard.
- **Docker:** batch export and dashboard services via Docker Compose.

## Important: understand data provenance

Not every overlay is backed by a live external feed. A number of advanced overlays currently use deterministic synthetic inputs to validate their schemas and scoring logic. These include tokenized-equity pricing, agentic MCP latency, expert-network novelty, signed options flow, multi-source freshness, generated research memos, prediction-market basis, YouTube sentiment, RAG earnings guidance, multi-agent debate, AIS maritime, satellite imagery and related experimental signals.

Treat synthetic overlays as **pipeline demonstrations, not market evidence**. Check each overlay's implementation, configuration and [FUTURE-IMPROVEMENTS.md](FUTURE-IMPROVEMENTS.md) before using it in research. A plausible-looking score does not mean a live data source was queried.

Yahoo Finance access through `yfinance` is unofficial and may change or be rate-limited. X/Twitter search requires a valid Bearer Token and API access that supports recent search; availability and limits depend on the X developer plan. No paid data provider is required for the public ECB, Eurostat, NBB and World Bank adapters.

## Quick start

Python 3.10 or newer is required.

```bash
git clone https://github.com/Stijnman/stock-intelligence-engine.git
cd stock-intelligence-engine

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

# Run the main research CLI
python stock_intelligence_engine.py --help
python stock_intelligence_engine.py --json

# Launch the dashboard
streamlit run app.py
```

The default watchlist and overlay settings are in `config.yaml`. Edit that file to change tickers and provider/overlay options. Keep credentials out of tracked files: use local-only configuration or environment variables only where the relevant adapter explicitly supports them. Do not commit API tokens, passwords or personal data.

## Main CLI

The primary application CLI supports analysis, optional headlines, JSON output and CSV export. See the current argument list before running:

```bash
python stock_intelligence_engine.py --help

# JSON report
python stock_intelligence_engine.py --json

# Include news and export report files
python stock_intelligence_engine.py --news --export

# Run without the investment-analysis section
python stock_intelligence_engine.py --no-investment --export
```

Individual overlays can be disabled for a run with their corresponding `--no-<overlay-name>` option. Overlay settings can also be changed in `config.yaml` or through the dashboard.

## Free public-data CLI

The investment research CLI is available as `sie-invest` (module form: `python -m sie.investment_cli`).

```bash
# Show available commands
python -m sie.investment_cli --help

# ECB daily EUR reference rates against USD
python -m sie.investment_cli ecb-fx USD --start 2025-01-01

# Combined ECB, Eurostat and World Bank macro context
python -m sie.investment_cli macro --country BE --currency USD

# Belgian HICP dataset from Eurostat
python -m sie.investment_cli eurostat prc_hicp_midx \
  --filter geo=BE --filter coicop=CP00 --filter unit=I15

# World Bank GDP growth indicator
python -m sie.investment_cli worldbank BE NY.GDP.MKTP.KD.ZG --start 2000 --end 2025

# List available NBB.Stat presets
python -m sie.investment_cli nbb-preset

# Fetch an NBB preset
python -m sie.investment_cli nbb-preset mfi-interest-rates --start-period 2020-01

# Analyze a ticker with macro context
python -m sie.investment_cli analyze AAPL --macro --macro-country BE --macro-currency USD
```

### Data-source coverage

| Source | Data | Access / caveats |
|---|---|---|
| European Central Bank (ECB) | EUR reference exchange rates and macro series | Public data portal; no API key required |
| Eurostat | European economic and price statistics, including HICP | Public API; dataset and dimension codes matter |
| National Bank of Belgium (NBB.Stat) | Belgian monetary and financial statistics | Public SDMX/CSV endpoints and verified presets; check dataset reuse terms |
| World Bank | Country-level development and macro indicators | Public Indicators API v2; annual observations may be published with a delay |
| SEC EDGAR | Company facts and filing-derived fundamentals | Public endpoints; provide a descriptive User-Agent and respect SEC fair-access guidance |
| Yahoo Finance via `yfinance` | Quotes and historical market data | Unofficial interface; no availability or stability guarantee |
| X API v2 | Recent public posts for narrative analysis | Optional Bearer Token; API access, quotas and recent-search availability depend on the account plan |

Public data does not automatically mean unrestricted commercial reuse. Check the source's current terms, attribution requirements and dataset-specific licence before redistribution or commercial use. SEC access must follow the SEC's current fair-access policy.

### Cache

Public-data adapter responses are cached under `~/.cache/stock-intelligence` by default. Set `SIE_CACHE_DIR` to use another cache directory. Check the observation period as well as the retrieval timestamp; macroeconomic datasets are often revised or published with a lag.

## Dashboard and Docker

Start the dashboard locally:

```bash
streamlit run app.py
```

Or run the dashboard in Docker:

```bash
docker compose up --build dashboard
```

Open `http://localhost:8501`.

Run the batch export service:

```bash
docker compose run --build --rm stock-intel
```

The batch service runs the configured news/export command and writes generated CSV files to the host's `exports/` directory. The dashboard and batch service mount `config.yaml` read-only.

## Configuration

- `config.yaml`: watchlist, overlay switches and thresholds.
- `.env.example`: optional email-alert configuration template.
- `exports/`: generated reports (created by the application when needed).

For X narrative analysis, configure the `twitter` section with `enabled`, `bearer_token`, `lookback_hours` and `search_limit`. The token is a secret: keep your local configuration private and never commit a real token. Without a token, the current social module returns mock narrative data; those results must not be mistaken for live X observations.

## Development and checks

```bash
python -m compileall -q sie
python -m pytest -q
git diff --check
```

The GitHub Actions workflows run the test suite, CI checks, CodeQL and security scans. The container workflow builds the Docker image and runs Trivy against CRITICAL and HIGH vulnerabilities (unfixed findings are excluded by the workflow configuration). A successful application test run is not a substitute for a successful container scan.

## Project documentation

- [CHANGELOG.md](CHANGELOG.md) — release and implementation history.
- [FUTURE-IMPROVEMENTS.md](FUTURE-IMPROVEMENTS.md) — planned work and unwired data sources.
- [config.yaml](config.yaml) — default watchlist and overlay configuration.

## Version

The application version is maintained in the project source and release history. See [CHANGELOG.md](CHANGELOG.md) for the latest recorded changes.

## Advanced quantitative analytics

The dependency-light calculation layer is available through `sie.investment` and documented in [INVESTMENT-EXPANSION.md](INVESTMENT-EXPANSION.md). It includes portfolio risk (Sharpe, Sortino, drawdown, historical VaR/CVaR), long-only portfolio optimization, seeded Monte Carlo scenarios, friction-aware buy-and-hold and periodic-rebalance backtests, factor beta, correlation, market-regime heuristics, dividend coverage, DCF sensitivity, earnings surprises, financial-distress flags, configurable Belgian tax scenarios, broker-cost estimates, EUR reporting with explicit FX, sector momentum, supplied earnings-calendar normalization, UCITS ETF metadata checks, insider/13F record normalization, options-chain summaries, supply-chain disclosure edges, fair-value aggregation, stock screening, watchlist ranking and rule-based alerts.

These analytics do not imply live feed coverage. Insider/13F, earnings-calendar, options, ETF metadata and supply-chain functions normalize caller-supplied records; connect and verify provider adapters before describing them as live. Belgian tax calculations require explicit rates and are illustrative. See the expansion guide for API examples, limitations and the remaining provider/dashboard integration work.


## Additional free macro and positioning feeds

- **CFTC Commitments of Traders:** public Socrata API, no token normally required. The adapter defaults to Legacy Futures Only to avoid mixing futures with the separate futures-and-options combined report. COT positions are weekly (Tuesday snapshot, normally released Friday), not live order flow. Example: `python -m sie.investment_cli cftc-cot --commodity GOLD --limit 100`.
- **FRED:** optional series adapter for macroeconomic time series. It requires your own free API key; set `FRED_API_KEY` locally. Example: `FRED_API_KEY=... python -m sie.investment_cli fred DFF --start 2020-01-01`. FRED series may have third-party licensing conditions and must retain the required non-endorsement notice and terms link. See [FRED API key documentation](https://fred.stlouisfed.org/docs/api/api_key.html) and [FRED terms](https://fred.stlouisfed.org/legal/terms/).

The CFTC adapter's source and report semantics are documented at the [official CFTC COT reporting environment](https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm). These feeds supplement, rather than replace, company-specific filings and market price sources.

- **SEC Form 4 insider transactions:** `python -m sie.investment_cli sec-insiders MSFT --filings 10`. Parses non-derivative and derivative transactions, P/S codes, owner role, filing/report dates and 10b5-1 flags. Set `SEC_USER_AGENT="Your App contact: you@example.com"` before requesting SEC filings; SEC asks automated clients to identify themselves and provide a contact.
- **SEC 13F holdings:** `python -m sie.investment_cli sec-13f BRK-B`. Retrieves information-table holdings for a manager that files 13F. Reported values are USD thousands and filings are delayed; 13F is not a complete portfolio and does not disclose short positions.
