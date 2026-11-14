# Investment Intelligence Expansion

This release adds a deterministic quantitative analytics layer in
`sie.investment.advanced`. The functions are local calculations: they do not
execute trades, call paid APIs, or silently manufacture live market data.

## Implemented in this release

| Capability | Implementation | Data required |
|---|---|---|
| Portfolio risk | Annualized return/volatility, Sharpe, Sortino, Calmar, drawdown, historical VaR/CVaR | Aligned daily close series and optional weights |
| Correlation and concentration | Pairwise return correlation matrix and ranked pairs | Aligned close series |
| Portfolio optimization | Long-only max-Sharpe, minimum-volatility and risk-parity projected-gradient optimizers | Historical close series |
| Monte Carlo | Seeded geometric-Brownian-motion scenario distribution | User-supplied expected return and volatility |
| Backtesting | Buy-and-hold baseline plus periodic target-weight rebalancing with configurable fees/slippage | Date-aligned price series, target weights and explicit cost assumptions |
| Factor exposure | One-factor beta, correlation and alpha estimates | Asset and factor return series |
| Regime detector | Long-term trend and realized-volatility regime | Benchmark history (minimum 200 prices) |
| Dividend sustainability | EPS payout and free-cash-flow coverage diagnostics | Dividend, EPS, FCF and diluted shares |
| DCF sensitivity | Growth/discount-rate grid | FCF, shares, net cash and assumptions |
| Earnings surprise | Actual-vs-estimate delta and percentage | Actual and estimate from a timestamped source |
| Financial distress | Liquidity, cash/debt, interest coverage and Altman-style proxy | Reported financial statement inputs |
| Belgian tax scenarios | Configurable TOB, withholding and annual fund-tax estimates | EUR transaction/dividend values and verified rates |
| Fair-value consensus | Median, mean, range and implied upside | Independent valuation inputs |
| Stock screener and watchlist ranking | Explicit threshold filters and transparent raw-metric ranking | Caller-supplied, period-aligned stock metrics |
| Alerts | Drawdown, tail-risk, dividend, valuation and data-quality rules | Outputs from the analytics functions |
| Insider transactions | SEC Form 4 XML retrieval, transaction parsing and purchase/sale aggregation | Public SEC filings; configure contact-bearing `SEC_USER_AGENT` |
| Institutional holdings | SEC 13F-HR information-table retrieval and normalization | Public SEC filings; delayed long-equity disclosure |
| CFTC positioning | Legacy futures-only COT net positioning by contract | Public CFTC Socrata API; weekly reports |
| FRED macro series | Series observation retrieval with missing-value and vintage metadata | Free FRED API key; third-party series terms apply |
| Options risk | IV, open interest, volume and put/call volume summary | Caller-supplied option chain |
| Data provenance | Strict LIVE/CACHED/ESTIMATED/SYNTHETIC/UNAVAILABLE labels | Provider metadata |

## API examples

```python
from sie.investment.advanced import (
    portfolio_risk, optimize_portfolio, monte_carlo_projection,
    backtest_buy_and_hold, belgian_investment_taxes, dcf_sensitivity,
)

risk = portfolio_risk({"ASML": asml_closes, "MSFT": msft_closes})
weights = optimize_portfolio({"ASML": asml_closes, "MSFT": msft_closes},
                             objective="max_sharpe")
scenarios = monte_carlo_projection(10_000, .07, .20, years=10)
baseline = backtest_buy_and_hold(asml_closes, fee_bps=5, slippage_bps=5)
taxes = belgian_investment_taxes(5_000, instrument_type="stock",
                                  tob_rate=.0035, dividend_gross_eur=50)
sensitivity = dcf_sensitivity(1_000_000_000, 400_000_000)
```

## Follow-on integration map

These capabilities remain separate from the calculation layer until verified
provider adapters and UI contracts are added:

- **SEC insider intelligence:** the Form 4 fetcher now parses transaction
  codes, direct/indirect ownership, owner roles, amendments on request and
  10b5-1 flags. Still add robust amendment reconciliation, duplicate detection,
  cluster significance and issuer-wide insider ownership context. Never treat
  grants or option exercises as open-market purchases.
- **Earnings calendar and surprise history:** add a source adapter with
  estimate provider, timestamp, reporting currency and restatement metadata.
  The surprise calculator accepts supplied actual/estimate values only.
- **Sector rotation:** connect timestamped sector ETF total-return series and
  calculate relative momentum and breadth; no sector feed is inferred here.
- **Supply-chain intelligence:** join issuer-disclosed supplier/customer
  relationships to company identifiers and filing citations; keep confidence
  and disclosure date on every edge.
- **Institutional ownership / smart money:** SEC 13F-HR parsing is now
  available. Add manager/entity resolution, quarter-over-quarter position
  change history, filing amendment reconciliation and portfolio concentration;
  do not label delayed filings as real-time flow.
- **Options surface:** persist historical IV by tenor/strike before exposing
  IV rank, skew or dealer-gamma estimates. The present snapshot does not
  estimate dealer positioning.
- **UCITS ETF screener:** source KID/PRIIPs, TER, replication, domicile,
  distribution policy, fund size and benchmark with issuer URLs and update
  dates. Metadata supplied by a user is not independently verified.
- **Broker comparison and EUR reporting:** add broker fee schedules, FX
  spreads, custody fees, corporate-action handling and instrument eligibility.
- **Belgian tax engine:** maintain a versioned rate table with effective dates,
  TOB instrument classification, caps/exemptions, Reynders tax and dividend
  withholding. The present calculator requires explicit rates and is
  illustrative only.
- **Backtesting v2:** add point-in-time constituents, corporate actions,
  dividend reinvestment, FX, taxes, transaction logs, delistings, walk-forward
  validation and benchmark comparison before treating results as investable.
- **Dashboard:** surface portfolio risk, optimizer scenarios, correlation
  heatmap, watchlist/screener, valuation sensitivity, earnings calendar,
  tax/fee estimates and provenance status. UI wiring is a separate release.

## Data integrity rules

- `LIVE`, `CACHED`, `ESTIMATED`, `SYNTHETIC` and `UNAVAILABLE` are
  distinct states. Never promote a proxy or estimate to LIVE.
- Keep source, as-of timestamp, currency, unit, period and filing date with
  every observation.
- Do not combine assets in different currencies without an explicit FX series.
- Historical optimization, Monte Carlo and DCF outputs are scenario tools,
  not guaranteed returns or personalized recommendations.
- Belgian tax rates and classifications change. Verify effective rates with
  FPS Finance before acting.
- No order placement or broker write access is included.
