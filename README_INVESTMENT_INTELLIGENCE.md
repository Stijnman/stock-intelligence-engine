# Investment Intelligence — free-first Hermes analyst

This extends the existing Stock Intelligence Engine. It adds modular, dependency-light research for stock fundamentals, scenario DCF, dividends, ETF metadata diagnostics, portfolio valuation and technical analysis.

## Architecture
- Hermes skill: skills/investment-intelligence/SKILL.md — research workflow and evidence rules.
- Market data: Yahoo Finance chart for daily history and dividend events (unofficial, can be delayed).
- US fundamentals: SEC CompanyFacts XBRL with local cache.
- Valuation: transparent bear/base/bull DCF with all assumptions returned.
- Dividends: trailing-12-month distributions and yield; payout only when EPS inputs exist.
- ETFs: issuer-metadata diagnostics; TER/holdings are never guessed.
- Portfolio: read-only CSV holdings valuation; currency buckets remain separate.
- Technicals: standard-library SMA, RSI, MACD and Bollinger calculations.

## Quick start
No extra packages are needed for the new investment modules (Python 3.10+ standard library only).

From this repository:
- python3 -m sie.investment_cli quote NVDA
- python3 -m sie.investment_cli analyze AAPL
- python3 -m sie.investment_cli compare AAPL,MSFT,NVDA
- python3 -m sie.investment_cli portfolio data/holdings.csv
- python3 -m sie.investment_cli etf data/etf_metadata.example.json
- python3 -m unittest discover -s tests -p 'test_investment_core.py' -v

Configure SEC identification:
- export SEC_USER_AGENT="StockIntelligenceEngine/0.1 contact: you@example.com"

## Install Hermes skill
Run: bash scripts/install_hermes_skill.sh
The installer creates a symlink under ~/.hermes/skills/investment-intelligence. No packages, API keys or broker permissions are installed.

## Data limits
- Yahoo chart is not an exchange-authoritative realtime feed and can be delayed or rate-limited.
- SEC CompanyFacts covers SEC reporting issuers; it does not provide complete statements for all Belgian/European companies.
- European fundamentals require official annual reports/ESEF or a verified provider.
- ETF TER, AUM, tracking difference, domicile, holdings and UCITS status must be verified from current issuer documents.
- Belgian TOB, withholding tax and fund taxation depend on instrument structure and current law; verify official rules before calculating net returns.

## Existing project vs new engine
The existing SIE dashboard, watchlist, news and technical alert features remain intact. New modules are additive and do not require paid data subscriptions.
